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
    name = "Instruction"
    def __init__(self, *args, **kwargs):
        """Pass arguments and keyword arguments as necessary"""
        self._args = args
        self._kwargs = kwargs
        
    @property
    def args(self):
        if hasattr(self, '_args'):
            return self._args
        else:
            self._args = []
            return self._args

    @property
    def kwargs(self):
        if hasattr(self, '_kwargs'):
            return self._kwargs
        else:
            self._kwargs = {}
            for indice, key in enumerate(self.__dict__):
                if key in ('_args', '_kwargs'):
                    continue
                if key.startswith("_"):
                    self._kwargs[key[1:]] = self.__dict__[key]
                else:
                    self._kwargs[key] = self.__dict__[key]
            return self._kwargs
        
    def __repr__(self):
        return (str(self.name) +
                "(" +
                ', '.join(self.args) +
                ', '.join([': '.join((str(k), repr(v)))
                           for k,v in self.kwargs.items()]) +
                ")"
                )
    
    def __str__(self):
        return repr(self)
    def apply():
        """Apply the instruction"""
        raise NotImplemented("apply() needs to be defined by a subclass")

class Retain(Instruction):
    """Move x places forward in the document"""
    name = "Retain"
    def __init__(self, count):
        self._count = count

    @property
    def count(self):
        return self._count

    def apply():
        pass

class TextOp(Instruction):
    name = "TextOp"
    def __init__(self, str):
        self._text = str

    @property
    def text(self):
        return self._text

    @property
    def characters(self):
        return self._text

class InsertCharacters(TextOp):
    name = "InsertCharacters"
    pass

class DeleteCharacters(TextOp):
    name = "DeleteCharacters"
    pass

class OpenElement(TextOp):
    name = "OpenElement"
    pass

class DeleteOpenElement(Instruction):
    name = "DeleteOpenElement"
    pass

class CloseElement(Instruction):
    name = "CloseElement"
    pass

class DeleteCloseElement(Instruction):
    name = "DeleteCloseElement"
    pass

class AnnotationBoundary(Instruction):
    name = "AnnotationBoundary"
    def __init__(self, starts = [], endkeys = []):
        self._startkeys = []
        self._startvalues = []
        for tup in starts:
            self._startkeys.append(tup[0])
            self._startvalues.append(tup[1])
        self._endkeys = endkeys
