import logging
import re
import urlparse
# Newer versions of SimpleJSON from what's in Py 2.6 etc 
# have builtin decimal support and are preferred IMHO
try:
    import simplejson as json
except:
    import json

import tornado.escape
import tornado.web
import tornado.httpserver

import tornad_io.websocket
import tornad_io.websocket.flash
import tornad_io.polling
import tornad_io.socket_io

import beaker.session

logging.getLogger().setLevel(logging.DEBUG)

# TODO - Monkey Patchable package object?
PROTOCOLS = {
    "xhr-polling": tornad_io.polling.XHRPollingSocketIOHandler,
    "xhr-multipart": tornad_io.polling.XHRMultiPartSocketIOHandler,
    "jsonp-polling": tornad_io.polling.JSONPPollingSocketIOHandler,
    "htmlfile": tornad_io.polling.HTMLFileSocketIOHandler,
    "websocket": tornad_io.websocket.WebSocketIOHandler,
    "flashsocket": tornad_io.websocket.flash.FlashSocketIOHandler,
}

class SocketIOHandler(tornado.web.RequestHandler):

    protocol_impl = None

    @property
    def protocol(self):
        return getattr(self.protocol_impl, "protocol", None)

    @property
    def session(self):
        return getattr(self.protocol_impl, "session", None)

    def __init__(self, application, request):
        tornado.web.RequestHandler.__init__(self, application, request)
        self.active = True
        self.stream = request.connection.stream
        self.application = application
        self.request = request

    def _execute(self, transforms, *args, **kwargs):
        self.conn_args = args
        self.conn_kwargs = kwargs
        logging.debug("Enabled Protocols: %s" % self.application.settings['enabled_protocols'])
        try:
            extra = kwargs['extra']
            proto_type = kwargs['protocol']
            proto_init = kwargs['protocol_init']
            session_id = kwargs['session_id']
            logging.debug("Initializing %s(%s) Session ID: %s... Extra Data: %s [PATH: %s XHR PATH: %s JSONP Index: %s]" % (proto_type, proto_init, session_id, extra, kwargs['resource'], kwargs.get('xhr_path', None), kwargs.get("jsonp_index", None)))
            protocol = PROTOCOLS.get(proto_type, None)
            if proto_type in self.application.settings['enabled_protocols']\
                         and protocol\
                         and issubclass(protocol, tornad_io.socket_io.SocketIOProtocol):
                self.protocol_impl = protocol(self)
                if kwargs['session_id']:
                    self.protocol_impl.debug("Session ID passed to invocation... (%s)" % kwargs['session_id'])
                    sess = beaker.session.Session(kwargs, id=kwargs['session_id'])
                    if sess.is_new:
                        raise Exception('Invalid Session ID.  Could not find existing client in sessions.')

                    if not sess.has_key('output_handle') and sess['output_handle']:
                        raise Exception('Invalid Session.  Could not find a valid output handle.')

                    self.protocol_impl.handshaked = True
                    self.protocol_impl.connected = True
                    self.protocol_impl.session = sess
                self.protocol_impl._execute(transforms, *extra, **kwargs)
            else:
                raise Exception("Handler for protocol '%s' is currently unavailable." % protocol)
        except ValueError as e:
            logging.warning("Malformed request received: %s" % e)
            self._abort(400)
            return

    def send(self, message):
        """Message to send data to the client.
        Encodes in Socket.IO protocol and
        ensures it doesn't send if session
        isn't fully open yet."""
        self.protocol_impl.send(message)

    def on_open(self, *args, **kwargs):
        """Invoked when a protocol socket is opened...
        Passes in the args & kwargs from the route
        as Tornado deals w/ regex groups, via _execute method.
        See the tornado docs and code for detail."""
        #logging.debug("[socketio protocol] Opened Socket: args - %s, kwargs - %s" % (args, kwargs))
        pass

    def on_message(self, message):
        """Handle incoming messages on the protocol socket
        This method *must* be overloaded
        TODO - Abstract Method imports via ABC
        """
        logging.warning("[socketio protocol] Message On Socket: message - %s" % (message))
        raise NotImplementedError, "You must define an on_message handler."

    def on_close(self):
        """Invoked when the protocol socket is closed."""
        #logging.debug("[socketio protocol] Closed Socket")
        pass


    def _abort(self, error_code=None):
        """ Kill the connection """
        self.active = False
        self.stream.close()
        self.protocol_impl._abort()
        if error_code:
            raise tornado.web.HTTPError(error_code)

    @classmethod
    def routes(cls, resource, extraRE=None, extraSep=None):
        # TODO - Support named groups
        #return (r"/%s/((xhr-polling|xhr-multipart|jsonp-polling|htmlfile)/)?/?/(\d*)/(%s)" % (resource, extraRE), cls)
        if extraRE:
            if extraRE[0] != '(?P<extra>':
                if extraRE[0] == '(':
                    extraRE = r'(?P<extra>%s)' % extraRE
                else:
                    extraRE = r"(?P<extra>%s)" % extraRE
            if extraSep:
                extraRE = extraSep + extraRE
        else:
            extraRE = "(?P<extra>)"

        protoRE = "(%s)" % "|".join(PROTOCOLS.keys())
        route = (r"/(?P<resource>%s)%s/(?P<protocol>%s)/?(?P<session_id>[0-9a-zA-Z]*)/?((?P<protocol_init>\d*?)|(?P<xhr_path>\w*?))/?(?P<jsonp_index>\d*?)" % (resource, extraRE, protoRE), cls)
        return route

class SocketIOServer(tornado.httpserver.HTTPServer):
    """HTTP Server which does some configuration and automatic setup
    of Socket.IO based on configuration.
    Starts the IOLoop and listening automatically
    in contrast to the Tornado default behavior.
    If FlashSocket is enabled, starts up the policy server also."""

    def __init__(self, application, no_keep_alive=False, io_loop=None,
                 xheaders=False, ssl_options=None, socket_io_port=8888, 
                 flash_policy_port=843, flash_policy_file='flashpolicy.xml', 
                 enabled_protocols=['websocket', 'flashsocket', 'xhr-multipart', 'xhr-polling', 'jsonp-polling', 'htmlfile']):
        """Initializes the server with the given request callback.

        If you use pre-forking/start() instead of the listen() method to
        start your server, you should not pass an IOLoop instance to this
        constructor. Each pre-forked child process will create its own
        IOLoop instance after the forking process.
        """
        logging.debug("Starting up SocketIOServer with settings: %s" % application.settings)

        enabled_protocols = application.settings.get('enabled_protocols', ['websocket', 'flashsocket', 'xhr-multipart', 'xhr-polling', 'jsonp-polling', 'htmlfile'])
        flash_policy_file = application.settings.get('flash_policy_file', 'flashpolicy.xml')
        flash_policy_port = application.settings.get('flash_policy_port', 843)
        socket_io_port = application.settings.get('socket_io_port', 8888)

        tornado.httpserver.HTTPServer.__init__(self, application, no_keep_alive, io_loop,
                                      xheaders, ssl_options)
        logging.info("Starting up SocketTornad.IO Server on Port '%s'" % socket_io_port)
        self.listen(socket_io_port)

        if 'flashsocket' in enabled_protocols:
            logging.info("Flash Sockets enabled, starting Flash Policy Server on Port '%s'" % flash_policy_port)
            flash_policy = tornad_io.websocket.flash.FlashPolicyServer(port=flash_policy_port, policy_file=flash_policy_file)

        io_loop = io_loop or tornado.ioloop.IOLoop.instance()
        logging.info("Entering IOLoop...")
        io_loop.start()


class EchoHandler(SocketIOHandler):
    def on_open(self, *args, **kwargs):
        logging.info("Socket.IO Client connected with protocol '%s' {session id: '%s'}" % (self.protocol, self.session.id))
        logging.info("Extra Data for Open: '%s'" % (kwargs.get('extra', None)))

    def on_message(self, message):
        logging.info("[echo] %s" % message)
        self.send("[echo] %s" % message)

    def on_close(self):
        logging.info("Closing Socket.IO Client for protocol '%s'" % (self.protocol))

echoRoute = EchoHandler.routes("echoTest", "(?P<sec_a>123)(?P<sec_b>.*)", extraSep='/')

application = tornado.web.Application([
    echoRoute
], enabled_protocols=['websocket', 'flashsocket', 'xhr-multipart', 'xhr-polling'],
   flash_policy_port=8043, flash_policy_file='/etc/lighttpd/flashpolicy.xml',
   socket_io_port=8888)

if __name__ == "__main__":
    socketio_server = SocketIOServer(application)

#if __name__ == "__main__":
#    flash_policy = tornad_io.websocket.flash.FlashPolicyServer()
#    http_server = tornado.httpserver.HTTPServer(application)
#    http_server.listen(8888)
#    tornado.ioloop.IOLoop.instance().start()

