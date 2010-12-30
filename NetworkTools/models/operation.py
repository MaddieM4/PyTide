#
# Copyright Notice:
#
# Copyright 2010    Nathanael Abbotts (nat.abbotts@gmail.com),
#                   Philip Horger,
# 
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
#

import datetime
from collections import deque
    
class Operation(object):
    """An operation is a sequence of instructions to be performed."""
    def __init__(self, parent, children = None, instructions=None,):
        if instructions is None:
            instructions = []
        self._parent = parent
        self._instructions = instructions
    
    @property
    def displacement(self):
        """The displacement of an operation is the number of transforms
        required to re-align with the server.
        It is calculated to be one more than the displacement of the parent.
        """
        return self.parent.displacement + 1

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new):
        self._parent = new
