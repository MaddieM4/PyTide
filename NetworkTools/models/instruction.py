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

class Instruction(object):
    """Should be subclassed.
    apply() should be defined, but init should not need to be overwritten.
    """
    def __init__(self, *args, **kwargs):
        """Pass arguments and keyword arguments as necessary"""
        self.args = args
        self.kwargs = kwargs
    def __repr__(self):
        return (str(self.__class__) +
                "(" +
                ', '.join(self.args) +
                ', '.join([': '.join((str(k), repr(v)))
                           for k,v in self.kwargs.items()])
                )
    
    def __str__(self):
        return repr(self)
    def apply():
        """Apply the instruction"""
        raise NotImplemented("apply() needs to be defined by a subclass")

class Retain(Instruction):
    """Move x places forward in the document"""
    def apply():
        pass
    
        
