#           Licensed to the Apache Software Foundation (ASF) under one
#           or more contributor license agreements.  See the NOTICE file
#           distributed with this work for additional information
#           regarding copyright ownership.  The ASF licenses this file
#           to you under the Apache License, Version 2.0 (the
#           "License"); you may not use this file except in compliance
#           with the License.  You may obtain a copy of the License at

#             http://www.apache.org/licenses/LICENSE-2.0

#           Unless required by applicable law or agreed to in writing,
#           software distributed under the License is distributed on an
#           "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#           KIND, either express or implied.  See the License for the
#           specific language governing permissions and limitations
#           under the License. 
import re

# TODO: Create some sort of class which sets this instead
WEB_SOCKET_SWF_LOCATION = '/socket.io/flashsocket/WebSocketMain.swf'

class Frame:
    FRAME_CHAR = '~'
    # Control Codes
    CLOSE_CODE = 0
    SESSION_ID_CODE = 1
    TIMEOUT_CODE = 2
    PING_CODE = 3
    PONG_CODE = 4
    DATA_CODE = 0xE
    FRAGMENT_CODE = 0xF
    # Core Message Types
    TEXT_MESSAGE_TYPE = 0
    JSON_MESSAGE_TYPE = 1
    def encode(data, ftype, mtype,):
        if mtype:
            return ''.join((self.FRAME_CHAR,
                            str(ftype),
                            str(mtype),
                            self.FRAME_CHAR,
                            str(len(data)),
                            self.FRAME_CHAR,
                            data,))
        else:
            return ''.join((self.FRAME_CHAR,
                            str(ftype),
                            self.FRAME_CHAR,
                            str(len(data)),
                            self.FRAME_CHAR,
                            data,))
    def decode(self, data):
        frames = []
        idx = 0
        start = 0
        end = 0
        ftype = 0
        mtype = 0
        size = 0

        # Parse the data and silently ignore any part that fails to parse
        # properly.
        hex_regex = re.compile('[0-9A-Fa-f]+')
        while (len(data) > idx) and (data[idx] == self.FRAME_CHAR):
            ftype = 0
            mtype = 0
            start = idx + 1
            end = data.index(self.FRAME_CHAR, start)
            if ((end == -1) or
                (start == end) or
                (not hex_regex.match(data[start:end]))
                ): # sad face because we have to use Regex
                break
            
            ftype = int(data[start:start + 1], 16)
            if (end - start) > 1:
                if ftype in (self.DATA_CODE, self.FRAGMENT_CODE):
                    mtype = int(data[start + 1:end], 16)
                else:
                    break

            start = end + 1
            end = data.index(self.FRAME_CHAR, start)
            if ((end == -1) or
                (start == end) or
                (not hex_regex.test(data[start:end]))
                ):
                break

            size = int(data[start:end], 16)
            start = end + 1
            end = start + size
            if len(data) < end:
                break
            frames.append(dict(ftype = ftype,
                               mtype = mtype,
                               data = data[start:end]))
            idx = end
        return frames


class Transport(object):
    def __init__(self, base, options):
        self.base = base
        self.options = dict(timeout = 15000)
        self.options.update(options)
        self.message_id = 0
        self.frame = Frame()
    def send(self, mtype, data):
        self.message_id += 1
        self.rawsend(self.frame.encode(self.frame.DATA_CODE, mtype, data))
    def rawsend(self, *args, **kwargs):
        raise NotImplemented("Missing send() implementation")
    def _destroy(self, *args, **kwargs):
        raise NotImplemented("Missing _destroy() implementation")
    def connect(self, *args, **kwargs):
        raise NotImplemented("Missing connect() implementation")
    def disconnect(self, *args, **kwargs):
        raise NotImplemented("Missing disconnect() implementation")
    def close(self):
        self.close_id = 'client'
        self.rawsend(self.frame.encode(self.frame.CLOSE_CODE,
                                       None,
                                       self.close_id))
    def _on_data(self, data):
        self._set_timeout()
        msgs = self.frame.decode(data)
        if msgs and len(msgs):
            for i in range(len(msgs)):
                this.on_message(msgs[i])
    def _set_timeout(self):
        # !! REFACTOR THIS INTO BETTER PYTHON !!
        if hasattr(self, '_timeout'):
            clear_timeout(self._timeout)
        self._timeout = set_timeout(self._on_timeout(), self.options['timeout'])
        #230
    def _on_timeout(self):
        self._timedout = True
        if hasattr(self, '_interval'):
            clear_interval(self._interval)
            self._interval = None
        self.disconnect()
