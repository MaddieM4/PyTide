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
    def __init__(self, document, **kwargs):
        """Pass arguments and keyword arguments as necessary"""
        self._document = document
        self._kwargs = kwargs

    @property
    def document(self):
        """All instructions must pertain to a document, otherwise they require
        no transformation.
        """
        return self._document
    
    @property
    def kwargs(self):
        if hasattr(self, '_kwargs') and self._kwargs:
            return self._kwargs
        else:
            self._kwargs = {}
            for indice, key in enumerate(self.__dict__):
                if key is '_kwargs':
                    continue
                if key.startswith("__"):
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
    
    def apply(self):
        """Apply the instruction"""
        raise NotImplemented("apply() needs to be defined by a subclass")
    
    def unapply(self):
        """Reverse 'apply'.

        If this instruction affects 'x', then apply(x) followed by unapply(x)
        returns the original x.
        """
        raise NotImplemented("unapply() needs to be defined by a subclass")

        
class Retain(Instruction):
    """Move x places forward in the document"""
    name = "Retain"
    def __init__(self, document, count):
        self._document = document
        self._count = count

    @property
    def count(self):
        return self._count

    def apply(self, document):
        document.retain(self._count)


class TextOp(Instruction):
    name = "TextOp"
    def __init__(self, document, string):
        self._document = document
        self._text = string

    @property
    def text(self):
        return self._text

    @property
    def characters(self):
        return self._text

class InsertCharacters(TextOp):
    name = "InsertCharacters"
    def __init__(self, document, string):
        super(InsertCharacters, self).__init__(document, string)

    def apply(self, document):
        document.insert_characters(self.text)

class DeleteCharacters(TextOp):
    name = "DeleteCharacters"
    def __init__(self, document, string):
        super(DeleteCharacters, self).__init__(document, string)

class OpenElement(TextOp):
    name = "OpenElement"
    def __init__(self, document):
        self._document = document

class DeleteOpenElement(Instruction):
    name = "DeleteOpenElement"
    def __init__(self, document,):
        self._document = document

class CloseElement(Instruction):
    name = "CloseElement"
    def __init__(self, document):
        self._document = document

class DeleteCloseElement(Instruction):
    name = "DeleteCloseElement"
    def __init__(self, document):
        self._document = document

class AnnotationBoundary(Instruction):
    name = "AnnotationBoundary"
    def __init__(self, document, starts = None, endkeys = None):
        if starts is None:
            starts = []
        if endkeys is None:
            endkeys = []
            
        self._document = document
        self._startkeys = []
        self._startvalues = []
        for tup in starts:
            self._startkeys.append(tup[0])
            self._startvalues.append(tup[1])
        self._endkeys = endkeys
