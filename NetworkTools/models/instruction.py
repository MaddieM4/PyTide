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
    def __init__(self):
        pass

class Retain(Instruction):
    def __init__(self, count):
	self._count = count

    @property
    def count(self):
        return self._count

class TextOp(Instruction):
    def __init__(self, str):
        self._text = str

    @property
    def text(self):
        return self._text

    @property
    def characters(self):
        return self._text

class InsertCharacters(TextOp):
    pass

class DeleteCharacters(TextOp):
    pass

class OpenElement(TextOp):
    pass

class DeleteOpenElement(Instruction):
    pass

class CloseElement(Instruction):
    pass

class DeleteCloseElement(Instruction):
    pass

class AnnotationBoundary(Instruction):
    def __init__(self, starts = [], endkeys = []):
        self._startkeys = []
        self._startvalues = []
        for tup in starts:
		self._startkeys.append(tup[0])
		self._startvalues.append(tup[1])
        self._endkeys = endkeys
