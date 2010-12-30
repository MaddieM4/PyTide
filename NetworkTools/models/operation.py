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

class Instruction(object):
    def __init__(self):
        pass
    
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
        
    
            
	    
##class OperationQueue(deque):
##    """A queue of Operation objects
##
##    When instantiating, you can provide any number of Operation instances as
##    operations."""
##    def __init__(self, position = 0, *args): #(self, wavelet, *args, position)
##        """Creates an Operation Queue.
##        
##        *args should all be Operation objects, which will be added to the queue
##            in sequential order.
##        """
##        super(OperationQueue, self).__init__(args)
##        self.position = position
##        # Note that this operation queue does not have a wavelet attribute - 
##        # that is because I believe that a wavelet should have an opqueue, 
##        # not the reverse. This will be discussed elsewhere though.
##    def append(self, position, operation, arg):
##        op = Operation(position, operation, arg)
##        super(self.__class__, self).append(op)
##
##
##
##
### Just a note to anyone modifying this - unless you've fully tested any code
### you put in the '- Transform against X -' sections, as it is really
### important that no slip-ups happen with them, as it will be likely to go
### unnoticed.
###                                  --THANKS!--
###
### Note this will not apply once the testing code is written to check these :)
##
##class Transform(object):
##    """Transforms/Zips two operation queues
##into one, to be applied by the
##    client.
##
##    Processes 2 operation queues, transforming them against each other, then
##    outputing two queues of transformed operations.
##
##    Note that all operations from the in queues should have already been
##    executed where they originated from, but nowhere else. 
##
##    Usage #1: When you have no out queues predefined.
##    trans1, trans2 = ot.Transform(in_queue_1, in_queue_2).transform()
##
##    Usage #2: When you have 2 out queues predefined.
##    ot.Transform(queue_server, queue_client, out_queue).transform()
##    """
##    def __init__(self, queue_server, queue_client, out_queue):
##        """Sets up instance variables"""
##        self.from_server = queue_server
##        self.from_client = queue_client
##        if out_queue:
##            self.out = out_queue
##        else:
##            self.out = OperationQueue()
##    def transform(self, num = -1):
##        if num < 0:
##            # Transform all code.
##            pass
##        else:
##            # Transform 'num' number of operations & no more.
##            pass
##        # TODO: Make sure op.copy() is used so that the original op remains
##        # unchanged, so that it can be transformed against another op too.
##    # ------------------- Transform against RETAIN ----------------------------
##    def retain_retain(self, op1, op2):
##        """Transforms a retain against (after) a retain
##
##        As a retain operation doesn't actually modify text, operations after it
##        do not require transformation."""
##        if op1.position == op2.position:
##            return op1, op2
##        elif op1.position < op2.position:
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##    def retain_insert(self, op1, op2):
##        """Transforms an insert against (after) a retain
##        
##        As a retain operation doesn't actually modify text, operations after it
##        do not require transformation."""
##        if op1.position == op2.position:
##            return op1, op2
##        elif op1.position < op2.position:
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##    def retain_delete(self, op1, op2):
##        """Transforms a delete against (after) a retain
##
##        As a retain operation doesn't actually modify text, operations after it
##        do not require transformation."""
##        if op1.position == op2.position:
##            return op1, op2
##        elif op1.position < op2.position:
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##    # ------------------- Transform against INSERT ----------------------------
##    def insert_retain(self, op1, op2):
##        """Transforms a retain against (after) an insert
##
##        If positions are identical, retain does not need transformed.
##        
##        If the retain is at a position after the insert, it's position must be
##        increased by len(op1.param).
##
##        If the retain occurs before the insert, retain does not need transformed
##        """
##        # TODO: !
##        if op1.position == op2.position:
##            return op1, op2
##        elif op1.position < op2.position:
##            op2.param += len(op1.param)
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##        # TODO: FIX ^^^THIS^^^ as we need to work out the *new* position by
##        # doing op2.position + op2.param
##    def insert_insert(self, op1, op2):
##        """Transforms an insert against (after) an insert
##
##        If the positions are identical, ????
##
##        If the 2nd insert occurs at a position after the first, it requires
##        transformation by increasing it's position by len(op1.param).
##
##        If the 2nd insert occurs at a position before the first, it does not
##        require transformation."""
##        if op1.position == op2.position:
##            #TODO: What should be done here? Do we allow them to both add
##            # text at the same point? What algorithm should be used?
##            return op1, op2
##        elif op1.position < op2.position:
##            op2.position += len(op1.param)
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##    def insert_delete(self, op1, op2):
##        """Transforms a delete against (after) an insert
##        
##        If the positions are identical, increase the delete position by
##        len(op1.param).
##
##        If the delete occurs after the insert, increase the delete position by
##        len(op1.param).
##
##        If the delete occurs before the insert, it does not require a
##        transformation.
##        """
##        if op1.position == op2.position:
##            op2.position += len(op1.param)
##            return op1, op2
##        elif op1.position < op2.position:
##            op2.position += len(op1.param)
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##    # ------------------- Transform against DELETE ----------------------------
##    def delete_retain(self, op1, op2):
##        """Transforms a retain against (after) a delete"""
##        # TODO: !
##        if op1.position == op2.position:
##            pass
##        elif op1.position < op2.position:
##            pass
##        elif op1.position > op2.positon:
##            pass
##        # TODO: WRITE ^^^THIS^^^ as we need to work out the *new* position by
##        # doing op2.position + op2.param
##    def delete_insert(self, op1, op2):
##        """Transforms an insert against (after) a delete
##
##        If the insert occurs at the same position as the delete, no transform
##        is required.
##
##        If the insert occurs after the delete, it needs to be transformed by
##        reducing it's position by op1.param.
##
##        If the insert occurs before the delete, no transform is required."""
##        if op1.position == op2.position:
##            return op1, op2
##        elif op1.position < op2.position:
##            op2.position -= op1.param
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
##    def delete_delete(self, op1, op2):
##        """Transforms a delete against (after) a delete
##        
##        If the operations occur at the same position:
##            And they are the same length or the 2nd is shorter, discard the 2nd
##            (reduce param to 0).
##            If the 2nd is longer, reduce op2.param to the difference in length.
##
##        If the 2nd operation occurs after the first, transform it according to
##        the following:
##            Reduce op2.position by the amount op1.param.
##            Ajust for overlap (if op1 deletes some of what op2 was going to)
##            correct this by reducing op2.param accordingly.
##        
##        If the 2nd operation occurs before the first, no transform in required.
##        """
##        if op1.position == op2.position:
##            op2.param -= op1.param
##            if op2.param < 0: op2.param = 0
##            return op1, op2
##        elif op1.position < op2.position:
##            if op1.position + op1.param > op2.position:
##                op2.param -= op1.position + op1.param - op2.position
##            op2.position -= op1.param
##            return op1, op2
##        elif op1.position > op2.positon:
##            return op1, op2
