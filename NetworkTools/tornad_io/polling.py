import functools
import re
import time
import tornado.websocket
import tornado.web
import tornado.ioloop
import tornad_io
from tornad_io.socket_io import SocketIOProtocol
try:
    import simplejson as json
except:
    import json
from decimal import Decimal

class PollingSocketIOHandler(SocketIOProtocol):
    def __init__(self, handler):
        tornad_io.socket_io.SocketIOProtocol.__init__(self, handler)
        self.debug("Initializing PollingSocketIOHandler...")
        tornado.web.RequestHandler.__init__(self, self.handler.application, self.handler.request)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.async_callback(self.open)(*args, **kwargs)

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        pass


    @tornado.web.asynchronous
    def options(self, *args, **kwargs):
        """Called for Cross Origin Resource Sharing Preflight message... Returns access headers."""
        self.debug("OPTIONS (args: %s kwargs: %s headers: %s) " % (args, kwargs, self.request.headers))
        self.preflight()
        self.finish()

    @tornado.web.asynchronous
    def preflight(self):
        """Called for Cross Origin Resource Sharing Preflight message... Returns access headers."""
        if self.request.headers.has_key('Origin'):
            if self.verify_origin():
                self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])
                if self.request.headers.has_key('Cookie'):
                    self.set_header('Access-Control-Allow-Credentials', True)
                return True
            else:
                return False
        else:
            return True

class XHRMultiPartSocketIOHandler(PollingSocketIOHandler):

    protocol ='xhr-multipart'

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary="socketio"')
        self.set_header('Connection', 'keep-alive')
        self.write('--socketio\n')
        self.open(*args, **kwargs)

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/plain')
        self.preflight()
        data = self.get_argument('data')
        self.async_callback(self._on_message)(
                data.decode("utf-8", "replace"))
        self.write('ok')
        self.finish()


    @tornado.web.asynchronous
    def _write(self, message):
        self.reset_timeout()
        self.preflight()
        self.write("Content-Type: text/plain; charset=us-ascii\n\n")
        self.write(message + '\n')
        self.write('--socketio\n')
        self.flush()

class HTMLFileSocketIOHandler(PollingSocketIOHandler):
    """ TODO - Find a browser that supports this.  IE 7 and IE 8 didn't work right.
    It needs I believe 5 or 6"""

    protocol = 'htmlfile'

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/html')
        self.set_header('Connection', 'keep-alive')
        self.set_header('Transfer-Encoding', 'chunked')
        self.write('<html><body>%s' % (' ' * 244))
        self.open(*args, **kwargs)

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/plain')
        data = self.get_argument('data')
        self.async_callback(self._on_message)(
                data.decode("utf-8", "replace"))
        self.write('ok')
        self.finish()


    @tornado.web.asynchronous
    def _write(self, message):
        self.reset_timeout()
        self.write('<script>parent.s_(%s), document);</script>' % (json.dumps(message, use_decimal=True)))
        self.flush()

class XHRPollingSocketIOHandler(PollingSocketIOHandler):
    use_queuing = True

    protocol = 'xhr-polling'

    config = {
        'timeout': None, # No heartbeats in polling
        'duration': 20000,
        'closeTimeout': 8000,
        'origins': [('*', '*')], # Tuple of (host, port)... * acceptable
    }

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.output_handle = self # Stays handle as long as polling runs.
        ## IMPORTANT - Capture the output handle now as *THIS* is the polling method
        # TODO - Buffering of messages in case nothing is open? This *COULD* potentially race
        # Runs for the poll time and then writes '' and closes.
        def pollingTimeout():
            try:
                if not self._finished:
                    self._write('')
                    self.finish()
            except:
                pass # Ignore any errors, channel is probably just closed

        timeout = time.time() + self.config['duration'] / 1000.0
        self.io_loop.add_timeout(timeout, pollingTimeout)
        self.debug("Polling until %d (and then closing channel)" % timeout)
        self.open(*args, **kwargs)

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/plain')
        data = self.get_argument('data')
        if not self.preflight():
            raise tornado.web.HTTPError(401, "unauthorized")
        self.async_callback(self._on_message)(
                data.decode("utf-8", "replace"))
        self.write('ok')
        self.finish()

    @tornado.web.asynchronous
    def _write(self, message):
        self.reset_timeout() # TODO - Make this the *CLOSE* timeout not HBeat
        self.preflight()
        self.set_header("Content-Type", "text/plain; charset=UTF-8")
        self.set_header("Content-Length", len(message))
        self.write(message)
        self.finish()

class JSONPPollingSocketIOHandler(XHRPollingSocketIOHandler):

    protocol = 'jsonp-polling'

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self._index = kwargs.get('jsonp_index', None)
        XHRPollingSocketIOHandler.get(self, *args, **kwargs)

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self._index = kwargs.get('jsonp_index', None)
        XHRPollingSocketIOHandler.post(self, *args, **kwargs)

    # TODO - Enforce index id included.
    @tornado.web.asynchronous
    def _write(self, message):
        self.reset_timeout() # TODO - Make this the *CLOSE* timeout not HBeat
        # Note a difference here... it only enforces CORS *IF* they sent an origin header
        # whereas other protocols require CORS, this allows it to be optional
        if self.request.headers.has_key('Origin') and not self.preflight():
            message = "alert('Violation of Cross Domain Security restrictions.');"
        else:
            message = "io.JSONP[%s]._(%s);" % (self._index,
                                              json.dumps(message, use_decimal=True))
        self.debug("Sending response message: '%s'" % message)
        self.set_header("Content-Type", "text/javascript; charset=UTF-8")
        self.set_header("Content-Length", len(message))
        self.write(message)
        self.finish()


