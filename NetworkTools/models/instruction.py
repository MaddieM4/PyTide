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
    def __init__(self, document, **kwargs):
        """Pass arguments and keyword arguments as necessary"""
        self._document = document
        self._kwargs = kwargs

    @property
    def document(self):
        """All instructions must pertain to a document."""
        return self._document
    
    @property
    def kwargs(self):
        """This method smells. Why did I write it?"""
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
                ', '.join([': '.join((str(k), repr(v)))
                           for k,v in self.kwargs.items()]) +
                ")"
                )
    
    def __str__(self):
        return repr(self)
    
    @property
    def name(self):
        return type(self).__name__

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
    """Move 'count' places forward in the document"""
    def __init__(self, document, count):
        self._document = document
        self._count = count

    @property
    def count(self):
        return self._count
    
    def apply(self):
        self.document.rotate(self._count)

    def unapply(self):
        self.document.rotate(0 - self._count) # "0 - x" is clearer than "-x"


class TextOp(Instruction):
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
    def __init__(self, document, string):
        super(InsertCharacters, self).__init__(document, string)

    def apply(self):
        for i in self.text:
            self.document.insert(self.text)

    def unapply(self):
        for i in self.text:
            self.document.delete(i)


class DeleteCharacters(TextOp):
    def __init__(self, document, string):
        super(DeleteCharacters, self).__init__(document, string)

    def apply(self):
        for i in self.text:
            self.document.delete(i)
            
    def unapply(self):
        for i in self.text:
            self.document.insert(i)
            

class OpenElementInstruction(Instruction):
    def __init__(self, document, element):
        self._document = document
        self._element = element

    def insert(self):
        self.document.insert(self._element)

    def delete(self):
        self.document.delete(self._element)        

class InsertOpenElement(OpenElementInstruction):
    apply = OpenElementInstruction.insert
    unapply = OpenElementInstruction.delete

class DeleteOpenElement(OpenElementInstruction):
    apply = OpenElementInstruction.delete
    unapply = OpenElementInstruction.insert

class CloseElementInstruction(Instruction):
    def __init__(self, document, element):
        self._document = document
        self._element = element

    def insert(self):
        self.document.insert(self._element)

    def delete(self):
        self.document.delete(self._element)
        
class InsertCloseElement(CloseElementInstruction):
    apply = CloseElementInstruction.insert
    unapply = CloseElementInstruction.delete

class DeleteCloseElement(CloseElementInstruction):
    apply = CloseElementInstruction.delete
    unapply = CloseElementInstruction.insert

class AnnotationBoundary(Instruction):
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
