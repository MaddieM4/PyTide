import logging
import re
import urlparse
import functools
# Newer versions of SimpleJSON from what's in Py 2.6 etc 
# have builtin decimal support and are preferred IMHO
try:
    import simplejson as json
except:
    import json
from decimal import Decimal
from Queue import Queue

import tornado.escape
import tornado.web
import tornado.httpserver

from tornado import ioloop

# Uses Beaker for session management which enables persistence, etc.
# 
# As to the best of my knowledge the standard Socket.IO implementation
# doesn't use cookies for session tracking we don't for now either.
# Session ID's for now go away with say a websocket dropping but are reused
# by XHR, etc
#
# TODO - Look into cookie usage

import beaker.session

FRAME = '~m~'


class SocketIOProtocol(tornado.web.RequestHandler):
    """ Base interface class for Socket.IO implementing
    adapters (specific protocols like XHRPolling, etc)

    TODO - Options handling for Timeouts, heartbeat etc

    Based on tornado.websocket.WebSocketHandler from the
    Tornado Distribution, written by Jacob Kristhammar"""


    io_loop = ioloop.IOLoop.instance()

    # Indicates if it is a single bidirectional socket
    # or a set of asynch messages. Controls output handling.
    # Websockets == False, Polling = True
    asynchronous = True
    # Use queuing system.
    # Certain protocols like XHRPolling & JSONPPolling
    # Don't leave a connection open - they "GET" a single message
    # And then connect again for another
    # There is a possible race if we assume they're there - 
    # Turning queuing on will queue messages on the session
    # and pop them on each poll.
    use_queuing = False
    connected = False
    handshaked = False
    session = None 
    protocol = None

    _write_queue = []
    # TODO - Pass config in at constructor and allow overrides of specific keys
    config = {
        'timeout': 12000,
        'duration': 20000,
        'closeTimeout': 8000,
        'origins': [('*', '*')], # Tuple of (host, port)... * acceptable
    }

    _heartbeats = 0
    _heartbeat_timeout = None

    handler = None

    def debug(self, message):
        logging.debug("[%s | %s | %s]  %s" %
                      (getattr(self.session, 'id', None), self.request.method, self.protocol,
                       message))

    def info(self, message):
        logging.info("[%s | %s | %s]  %s" %
                      (getattr(self.session, 'id', None), self.request.method, self.protocol,
                       message))

    def error(self, message, exception, **kwargs):
        logging.error("[%s | %s | %s]  %s" %
                      (getattr(self.session, 'id', None), self.request.method, self.protocol,
                     message), exception, **kwargs)

    def warning(self, message):
        logging.warning("[%s | %s | %s]  %s" %
                       (getattr(self.session, 'id', None), self.request.method, self.protocol,
                       message))


    def __init__(self, handler):
        self.handler = handler
        self.application = self.handler.application
        self.request = self.handler.request

    @property
    def message_queue(self):
        return self.session.get("message_queue", Queue())

    @property
    def output_handle(self):
        return self.session.get("output_handle", None)

    @output_handle.setter
    def output_handle(self, fh):
        self.debug("Setting new output handle (%s)" % fh)
        if not getattr(self.session, 'id', None):
            self.warning("No session setup yet. Ignoring FH Set.")
        else:
            self.session['output_handle'] = fh
            self.session.save()
            if self.use_queuing:
                self._pop_queue() # pop a message off ye' ol' stack


    def _pop_queue(self):
        """ Pops a single message off the queue if the FH is open
        and tries sending it."""
        if self.use_queuing:
            if not self.message_queue.empty():
                self.debug("Current queue size: %d" % self.message_queue.qsize())
                if not self.output_handle._finished:
                    try:
                        msg = self.message_queue.get(timeout=self.config['duration'])
                        self.output_handle.send(msg, skip_queue=True)
                    except Exception as e:
                        self.warning("Exception while popping queue (%s) - returning message (%s) to queue." % (e, msg))
                        if msg:
                            self.message_queue.put(msg)
            else:
                self.info("Message queue empty.  NOOP.")

        else:
            self.warning("Pop queue invoked in a non-queuing protocol.  NOOP.")


    def open(self, *args, **kwargs):
        """Internal method for setting up session
        invocation. Don't mess with me.
        Left with non-privated naming to stay compatible
        with existing Tornado implementation of Websockets.

        This method is similar to the Client._payload method
        from Socket.IO-Node
        """
        payload = []

        self.connected = True

        if not self.handshaked:
            self.session = beaker.session.Session(kwargs)
            self.session['message_queue'] = Queue()
            payload.append(self.session.id)
            self.handshaked = True

        self.output_handle = self
        self.session.save()

        payload.extend(self._write_queue)
        self._write_queue = []
        self.send(payload)

        if self.config['timeout']:
            self.reset_timeout()

        self.async_callback(self.handler.on_open)(*args, **kwargs)

    def reset_timeout(self):
        if self._heartbeat_timeout:
            self._heartbeat_timeout.stop() # shut off the old one...
        if self.config['timeout']:
            self._heartbeat_timeout = ioloop.PeriodicCallback(self._heartbeat, self.config['timeout'])
            self._heartbeat_timeout.start()

    def _heartbeat(self):
        # TODO - Check we *RECEIVE* heartbeats
        try:
            if not self._finished and self.stream._check_closed:
                self._heartbeats += 1
                self.send('~h~%d' % self._heartbeats)
            else:
                raise Exception, "Connection closed."
        except Exception as e:
            self._abort()

    def on_heartbeat(self, beat):
        if beat == self._heartbeats:
            #self.debug("[%s] Received a heartbeat... " % beat)
            self.reset_heartbeat_timeout()
        else:
            self.warning("Mismatch on heartbeat count.  Timeout may occur. Got %d but expected %d" % (beat, self._heartbeats)) # This logging method may race

    def reset_heartbeat_timeout(self):
        pass

    def verify_origin(self):
        """Header check, enforces CORS *IF* they sent an origin header"""
        origin = self.request.headers.get("Origin", None)
        if origin:
            self.debug("Verify Origin: %s" % origin)
            origins = self.config['origins']
            url = urlparse.urlparse(origin)
            host = url.hostname
            port = url.port
            return filter(lambda t: (t[0] == '*' or t[0].lower() == host.lower()) and (t[1] == '*' or  t[1] == int(port)), origins)
        else:
            return True

    def send(self, message, skip_queue=False):
        """Message to send data to the client.
        Encodes in Socket.IO protocol and
        ensures it doesn't send if session
        isn't fully open yet."""

        if self.asynchronous:
            out_fh = self.output_handle
        else:
            out_fh = self

        if isinstance(message, list):
            for m in message:
                out_fh.send(m)
        else:
            if not skip_queue and self.use_queuing:
                self.message_queue.put(message)
                # We always queue even if it's the only message we'll send.
                self._pop_queue()
            else:
                self.async_callback(out_fh._write)(
                                    self._encode(message))


    def _encode(self, message):
        """Encode message in Socket.IO Protocol.

        TODO - Custom Encoder support for simplejson?"""
        encoded = ''
        if isinstance(message, list):
            for m in message:
                encoded += self._encode(message)
        elif not isinstance(message, (unicode, str)) and isinstance(message, (object, dict)):
            """
            Strings are objects... messy test.
            """
            if message is not None:
                encoded += self._encode('~j~' + json.dumps(message, use_decimal=True))
        else:
            encoded += "%s%d%s%s" % (FRAME, len(message), FRAME, message)


        return encoded

    def _decode(self, message):
        """decode message from Socket.IO Protocol."""
        messages = []
        parts = message.split("~m~")[1:]
        for i in range(1, len(parts), 2):
            l = int(parts[i - 1])
            data = parts[i]
            if len(data) != l:
                # TODO - Fail on invalid length?
                self.warning("Possibly invalid message. Expected length '%d', got '%d'" % (l, len(data)))
            # Check the frame for an internal message
            in_frame = data[:3]
            if in_frame == '~h~':
                self.async_callback(self.on_heartbeat)(int(data[3:]))
                continue
            elif in_frame == '~j~':
                data = json.loads(data[3:], parse_float=Decimal)
            messages.append(data)

        return messages

    def _on_message(self, message):
        """ Internal handler for new incoming messages.
        After decoding, invokes on_message"""
        messages = self._decode(message)
        for msg in messages:
            self.async_callback(self.on_message)(msg)

    def _write(self, message):
        """Write method which all protocols must define to
        indicate how to push to their wire"""
        self.warning("[socketio protocol] Default call to _write. NOOP. [%s]" % message)
        pass


    def async_callback(self, callback, *args, **kwargs):
        """Wrap callbacks with this if they are used on asynchronous requests.

        Catches exceptions properly and closes this connection if an exception
        is uncaught.
        """
        if args or kwargs:
            callback = functools.partial(callback, *args, **kwargs)
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception, e:
                self.error("Uncaught exception in %s",
                              self.request.path, exc_info=True)
                self._abort()
        return wrapper

    def _abort(self):
        self.connected = False
        #self.stream.close()

    #def on_open(self, *args, **kwargs):
    #    """Invoked when a protocol socket is opened...
    #    Passes in the args & kwargs from the route
    #    as Tornado deals w/ regex groups, via _execute method.
    #    See the tornado docs and code for detail."""

    def on_message(self, message):
        """Handle incoming messages on the protocol socket
        This method *must* be overloaded
        TODO - Abstract Method imports via ABC
        """
        self.async_callback(self.handler.on_message)(message)

    def on_close(self):
        """Invoked when the protocol socket is closed."""
        self.debug("Shutting down heartbeat schedule; connection closed.")
        if self._heartbeat_timeout:
            self._heartbeat_timeout.stop()
        self.async_callback(self.handler.on_close)()

