from __future__ import with_statement

import functools
import logging
import re
import time
import tornado.websocket
from tornado import ioloop
from tornado import iostream
import tornad_io
import errno
import socket
import tornad_io.socket_io
import tornad_io.websocket


class FlashSocketIOHandler(tornad_io.websocket.WebSocketIOHandler):

    protocol = 'flashsocket'

    def __init__(self, handler):
        logging.debug("Initializing FlashSocketIOHandler...")
        tornad_io.websocket.WebSocketIOHandler.__init__(self, handler)

class FlashPolicyServer(object):
    """Flash Policy server, listens on port 843 by default (otherwise useless)"""

    def __init__(self, port=843, policy_file='flashpolicy.xml'):
        self.policy_file = policy_file
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(0)
        sock.bind(('', self.port))
        sock.listen(128)
        self.io_loop = ioloop.IOLoop.instance()
        callback = functools.partial(self.connection_ready, sock)
        self.io_loop.add_handler(sock.fileno(), callback, self.io_loop.READ)

    def connection_ready(self, sock, fd, events):
        while True:
            try:
                connection, address = sock.accept()
            except socket.error, e:
                if e[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                    raise
                return
            connection.setblocking(0)
            self.stream = iostream.IOStream(connection, self.io_loop)
            self.stream.read_bytes(22, self._handle_request)

    def _handle_request(self, request):
        if request != '<policy-file-request/>':
            self.stream.close()
        else:
            with open(self.policy_file, 'rb') as fh:
                self.stream.write(fh.read() + '\0')


if __name__ == "__main__":
    flash_policy = tornad_io.websocket.flash.FlashPolicyServer()
