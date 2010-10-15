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

from collections import deque

#from UserDict import DictMixin

class Annotation(object):
    def __init__(self, start, end, name, value):
        self._name = name
        self._value = value
        self._start = start
        self._end = end
    def __repr__(self):
        return "Annotation((%s : %s) = \"%s\", \"%s\")" % (self._start,
                                                           self._end,
                                                           self._name,
                                                           self._value)
    @property
    def name(self):
        return self._name
    @property
    def value(self):
        return self._value
    @property
    def start(self):
        return self._start
    @property
    def end(self):
        return self._start
    @property
    def range(self):
        return (self._start, self._end)


class Annotations(object,): #UserDict.DictMixin):
    """ """
    def __init__(self):
        """Creates a set() to contain the annotations.

        A set is used so that identical annotations are removed automatically.
        It is hoped that this will be extendible to allow the set's comparison
        to also merge annotations.
        """
        self._data = set()
        
    def copy(self):
        return self._data.copy()
    
    def __getitem__(self, pos):
        """Return a list of tuples containing all the annotations at pos.

        For instance, if our annotation list was:
        [(2,4, 'font', 'arial'),
         (2,5, 'color', 'red'),
         (1,3, 'size', '2em'),]

        Then getitem() would return the following for each call:
        getitem(0)
            []
        getitem(1)
            [('size', '2em')]
        getitem(2)
            [('font', 'arial'), ('color', 'red'), ('size', '2em')]
        getitem(3)
            [('font', 'arial'), ('color', 'red'), ('size', '2em')]
        getitem(4)
            [('font', 'arial'), ('color', 'red')]
        getitem(5)
            [(2,5, 'color', 'red')]
        getitem(6)
            []
        """
        output = []
        for i in self._data:
            if i.start <= pos <= i.end:
                output.append(i)
        return output
    def __setitem__(self, pos, value):
        """Create an annotation at a single position.

        Value should be a tuple of the sort ('annotation/name', 'value').
        """
        if not isinstance(value, tuple):
            # raise exeption?
            return
        if len(value) != 2:
            # raise exeption?
            return
        self._data.append(Annotation(pos, pos, *value))
    # delitem is not supported, because there is no apparent use-case for
    # deleting all annotations from a single position.
    # If you have a use case, please file an issue at
    # github.com/natabbotts/PyTide

    def __contains__(self, value):
        if isinstance(value, Annotation): # If value is an annotation
            return value in self._data
        elif len(value) == 4: # If value can be turned into an annotation
            value = Annotation(*value)
            return value in self._data
        else:
            return False
    def __iter__(self):
        for ann in self._data:
            yield ann
    
    def __getslice__(self, start, end):
        x = []
        for i in range(start, end):
            x.append(self.__getitem__(i))
        return list(set(x))
    def append(self, x):
        self._data.add(x)
def _test():
    x = Annotations()
    for i,j in zip(range(1, 10), range(6, 15, -1)):   
        x.append(Annotation(i,j,"color%s" % i, "red"))
    return x



class BlipDocument(deque):
    """Models the document section of a blip, containing all text and elements.

    Methods:
        retain(value) - Impliments the RETAIN operation, via the rotate method.

            'value' should be a number.


        insert_characters(value, annotations) - Impliments the INSERT_CHARACTERS
            operation, which will insert a sequence of characters into the blip.

            'value' should be a string containing multiple characters, or a
                list or iterable with each item a single character.
            'annotations' should be a dictionary of annotation key:value pairs,
                to be applied to all inserted characters. Alternatively, a list
                of 2 item tuples "(key, value)" can be used.


        insert(value, annotations) - Inserts 'value' at the current position,
            with 'annotations' as the annotations.

            'value' an object, e.g. a gadget element, a line element, etc.
            'annotations' should be a dictionary of annotation key:value pairs.
                Alternatively, a list of 2 item tuples (key,value) can be used.

        delete(value) - Impliments the DELETE operation. Deletes 'value' No. of
            characters appearing after the current position.

            'value' should be a number.


        fix_rotation() - Returns the blip to it's original order, so that text
            and elements are in the right place.

        complete() - Calls 'fix_rotation()' then returns itself.

    """

    def __init__(self):
        """Sets up the BlipDocument object. Do not pass values. """
        super(BlipDocument, self).__init__()
        self.annotations = Annotations()
        self.rotation = 0

    def __str__(self):
        """Returns string form of the current rotation of itself."""
        return ''.join(self)

    def fix_rotation(self):
        """Corrects the rotation that was created by different operations,
        so that the blip is now in readable form, with the first element first.
        """
        self.rotate(self.rotation)
        self.annotations.rotate(self.rotation)
        self.rotation = 0

    def retain(self, value):
        """A retain operation. Value should be an integer."""
        self.rotation += value
        self.rotate(-value)
        self.annotations.rotate(-value)

    def insert_characters(self, value, annotations = None):
        """An insert operation, to add characters.

        'value' should be a string or a list/iterable containing a single
        character at each element.

        'annotations' should be a dictionary of annotation key:value pairs,
        to be applied to all inserted characters. Alternatively, a list of
        2 item tuples "(key, value)" can be used.
        """
        self.extend(value)
        if self.rotation != 0:
            self.rotation += len(value)
        self.annotations.extend(len(value), annotations)

    def insert(self, value, annotations = None):
        """Inserts a single element at the current position.

        'value' should be a single object  e.g. a gadget or line element.
        'annotations' should be a dictionary of annotation key:value pairs.
        Alternatively, a list of 2 item tuples (key,value) can be used.
        """
        self.append(value)
        self.annotations.append(annotations)
        if self.rotation != 0:
            self.rotation += 1

    def delete(self, value):
        """Delete 'value' items after the current position."""
        for i in range(value):
            self.popleft()
        self.annotations.popleft()

    def complete(self): #lol
        """Calls 'fix_rotation()' then returns itself."""
        self.fix_rotation()
        return self

class Contributors(list):
    """A list containing users. Users cannot be removed or rearranged."""
    def __delitem__(self, arg):
        pass
    def __delslice__(self, arg1, arg2):
        pass
    def __setitem__(self, arg1, arg2):
        pass
    def __setslice__(self, arg1, arg2, arg3):
        pass
    def pop(self, arg = None):
        pass
    def remove(self, arg):
        pass
    def sort(self, cmp = None, key = None, reverse = None):
        pass
    def reverse(self):
        pass

class Blip(object):
    def __init__(self, creator):
        self.creator = creator
        self.contributors = Contributors()
        self.contributors.append(creator)
        self.document = BlipDocument()

    #TODO: Provide annotate() method which will apply an annotation to a range.
