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
	def __init__(self, timestamp = None):
		if not timestamp:
                        timestamp = datetime.datetime.now()

	def apply(document):
		pass
	    
class OperationQueue(deque):
    """A queue of Operation objects

    When instantiating, you can provide any number of Operation instances as
    operations."""
    def __init__(self, position = 0, *args): #(self, wavelet, *args, position)
        """Creates an Operation Queue.
        
        *args should all be Operation objects, which will be added to the queue
            in sequential order.
        """
        super(OperationQueue, self).__init__(args)
        self.position = position
        # Note that this operation queue does not have a wavelet attribute - 
        # that is because I believe that a wavelet should have an opqueue, 
        # not the reverse. This will be discussed elsewhere though.
    def append(self, position, operation, arg):
        op = Operation(position, operation, arg)
        super(self.__class__, self).append(op)
