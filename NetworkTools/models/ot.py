#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from multiprocessing import Process, Manager, freeze_support
#from gtk.gdk import threads_enter, threads_leave
from websocket import WebSocket
from handler import CallbackHandler
import transform

class ServerBuffer(Process):
    def __init__(self, url, onopen_callback):
        super(ServerBuffer, self).__init__()
        self.__op_queue_outgoing, op_queue_incoming = Pipe()
        onopen_callback = CallbackHandler(onopen_callback,
                                          self.send_operation)
        self.connection = WebSocket(url,
                                    onopen=onopen_callback,
                                    onmessage=self._onmessage_callback,)

    @property
    def op_queue(self):
        """As it is incredibly important that the Op Queue doesn't get
        replaced with anything else, the op_queue attribute has been stuck
        through Python name mangling."""
        return self.__op_queue_outgoing
    def send_operation(self, op):
        self.op_queue.put(op)
    def process_message(self, msg):
        pass
    # ------------------- OVERIDE THESE -------------------
    def something_to_be_overridden(self):
        pass


class Composer(Process):
    def __init__(self):
        super(Composer, self).__init__()

class Transformer(Process):
    def __init__(self):
        super(Transformer, self).__init__()

if __name__ == "__main__":
    freeze_support()



# ---------------------------- DESIGN INTENTIONS ------------------------------
#
# This module will contain the following:
#   * A 'server buffer', which will control the sending and recieving of
#       operations to and from the server.
#       The buffer will have it's own processes (2), so as the sending and
#       recieving  of operations will not make the rest of the app 'hang'.
#       The buffer will send and recieve operations to/from the transformer by
#       means of a Pipe.
#   * A 'composer' to combine operations.
#   * A 'transformer' to transform operations.
#   * A Manager class of some sort, to organise the whole shebang.
