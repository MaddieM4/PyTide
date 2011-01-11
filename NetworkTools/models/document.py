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

class OpenElement(object):
    def __init__(self, name, **kwargs):
        self._name = name
        self._properties = kwargs
        for kw, value in kwargs.items():
            setattr(self, kw, value)

    def __len__(self):
        return 1
    
    def __repr__(self):
        properties = tuple([(k+'="'+v+'"')
                            for k,v in self._properties.items()])
        return '<%s %s>' % (self.name, ' '.join(properties))
    
    @property
    def name(self):
        return self._name

class CloseElement(object):
    def __init__(self, el):
        """1 arg: 'el' - the element you are closing"""
        self._el = el
        self._name = el.name
        
    def __len__(self):
        return 1
    
    def __repr__(self):
        return '</%s>' % self._name
    
    @property
    def name(self):
        return self._name

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
        self._rotate(self.rotation)
        self.rotation = 0

    def _rotate(self, value):
        """Proxy to original deque behavior."""
        deque.rotate(self, value)
        
    def rotate(self, value):
        """Rotate the queue by 0-value, and set the new rotation.
        Value should be an integer.
        """
        self.rotation += value
        self._rotate(-value)

    def insert(self, value):
        """Inserts a single element at the current position.

        'value' should be a single object  e.g. a gadget or line element.
        'annotations' should be a dictionary of annotation key:value pairs.
        Alternatively, a list of 2 item tuples (key,value) can be used.
        """
        self.append(value)
        self.annotations.append(annotations)
        if self.rotation != 0:
            self.rotation += 1

    def delete(self, item):
        """Delete 'item' from the current position.
        For multiple items, multiple calls to delete must be made.
        """
        if item in self and item is self[0]:
            self.popleft()
            if self.rotation != 0:
                self.rotation -= 1
        else:
            raise Exception("Item is not in front of current position.")

    def complete(self): #lol
        """Calls 'fix_rotation()' then returns itself."""
        self.fix_rotation()
        return self

    def annotate(self, start, end, name, value):
        return self.annotations.annotate(start,end,name,value)

    @property
    def text(self):
	return str(self.complete())

        return item
