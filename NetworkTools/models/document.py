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
        self._name = el.name
    def __repr__(self):
        return '</%s>' % self._name
    @property
    def name(self):
        return self._name

# -------- Annotations

class Annotation(object):
    """A single Annotation.

    To instantiate, provide the following values:
        start - an integer representing the start position in the blip.
        end   - an integer representing the end position in the blip.
            If we consider the following four letter blip, a start and end of
            (1, 3) would cover the letters "ex".
            0 1 2 3 4
            |t|e|x|t|
        name  - a string identical to the annotation name. This usually takes
                the form of "type/specific". A common example is "style" as the
                type, and "fontFamily" as the specific, making up the name of
                "style/fontFamily". This is merely a convention, and is not
                required - "magic" is as valid as "style/fontFamily".
        value - a string identical to the annotation value (can be empty). This
                can be anything, but the simplest value usually used would be a
                boolean, "" representing False, "true" representing True.

    The Annotation object provides these instantiating values as properties,
    along side a few other useful properties to save time.
        start - the starting position (see above)
        end   - the ending position (see above)
        name  - the annotation name (see above)
        value - the annotation value (see above)
        range - a tuple containing the start and end of the annotation (in that
                order).
        annotation - a tuple containing the annotation name and value (in that
                order).

    In order for an Annotation to behave properly in a set, the following
    methods were defined:
        __hash__ - the hash of an annotation is equal to the hash of the name
                    and value of the annotation.

    Because Annotations are stored in a set, they are immutable. As such, the
    properties provided are read only properties. It is strongly advised that
    you do not modify the attributes of an Annotation ( _start, _end, _name,
    _value), as the Annotation will no longer behave correctly and will cause
    bugs.
    """
    # ----------------------------- Base Methods ------------------------------
    def __init__(self, start, end, name, value):
        self._start = start
        self._end = end
        self._name = name
        self._value = value
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "Annotation((%s : %s) = \"%s\", \"%s\")" % (self._start,
                                                           self._end,
                                                           self._name,
                                                           self._value)
    # ----------------------------- Properties --------------------------------
    @property
    def start(self):
        """An integer representing the Annotation's start position in a blip."""
        return self._start
    @property
    def end(self):
        """An integer representing the Annotation's end position in a blip."""
        return self._end
    @property
    def name(self):
        """The name of the Annotation."""
        return self._name
    @property
    def value(self):
        """The value of the Annotation."""
        return self._value
    @property
    def range(self):
        """A tuple containing the start and end positions of the Annotation."""
        return (self._start, self._end)
    @property
    def annotation(self):
        """A tuple containing the name and value of the Annotation."""
        return (self._name, self._value)
    # ----------------------------- Set behavior ------------------------------
    def __eq__(self, y):
        """Determine equality with another Annotation, based on initial values.

        Annotations are equal if their name, value, start and end are equal.
        """
        if isinstance(y, Annotation):
            return ((self.name, self.value, self.start, self.end) ==
                    (y.name, y.value, y.start, y.end))
        else:
            return False
        
    def __ne__(self, y):
        """Determine inequality with another Annotation.

        Ineqality for an annotation is determined by comparing the start, end,
        name and value of the two annotations. If any do not match, False is
        returned.
        """
        return not (self == y)
    
    def __hash__(self):
        """Return the hash of the Annotation.

        This hash is based on the initial values of the Annotation, just as
        eqality is.
        The intial values are the start, end, name and value of the Annotation.
        """
        return hash(tuple(self._name, self._value))


class Annotations(object):
    """A collection of Annotations.

    Annotation objects are stored inside of a set, and the Annotations class
    is simply a proxy to that set. There are 2 clear benefits of producing a
    set.
        1)  Identical Annotations are automatically removed.
            * Annotations are deemed identical if all their attributes are the
              same (start, end, name, value)
        2)  The Annotations are unordered. This is a benefit because any order
            would have to be constantly updated and changed for efficiency.

    There are 
        """
    def __init__(self):
        """Creates a set to contain the annotations."""
        self._data = set()


    def _resolve_pair(self, annotation_1, annotation_2):
        ''' Test two annotations for overlap, equality, and such '''
        if annotation_2.end < annotation_1.end:
            # If the annotations are in the wrong order, swap them.
            a1 = annotation_2
            annotation_2 = annotation_1
            annotation_1 = a1
            del a1

        if annotation_2.start < annotation_1.end: #If there is an overlap
            # test: end of 1 >= start of another. Simplest overlap.
            if annotation_1.end >= annotation_2.start:
                new_annotation = Annotation(start = annotation_1.start,
                                            end = annotation_2.end,
                                            name = annotation_1.name,
                                            value = annotation_1.value)
                self._data.symmetric_difference_update(set((annotation_1,
                                                            annotation_2,
                                                            new_annotation)))
                return new_annotation
            elif ((annotation_2.start <= annotation_1.start) and
                  (annotation_1.end <= annotation_2.end)):
                # If annotation 1 is completely contained by annotation 2:
                self._data.remove(annotation_1)
                return annotation_2
        # If the 2 annotations do not match any scenarios, raise an exception
        # If this exception is raised, report to me: nat.abbotts@gmail.com
        # and I will update the code to account for the new situation.
        # This is because I cannot see any other possibility.
        raise Exception("Cannot resolve")

    def resolve(self):
        """Resolve all stored annotations.

        If two annotations overlap, and hold the same name and value,
            they are replaced with a single annotation.
        """
        for annotation_1 in self._data:
            for annotation_2 in self._data:
                if annotation_1 == annotation_2:
                    continue
                elif ((annotation_2.start < annotation_1.end) or
                      (annotation_1.start < annotation_2.end)):
                    self._resolve_pair(annotation_1, annotation_2)



    def _add_annotation(self, annotation):
        for current_annotation in self._data:
            if ((current_annotation.start < annotation.end) or
                (annotation.start < current_annotation.end)):
                annotation = self._resolve_pair(annotation, current_annotation)
    def annotate(self, start, end, name, value):
        self._add_annotation(Annotation(start = start,
                                        end = end,
                                        name = name,
                                        value = value))
    # ------------------------ BoilerPlate Methods ----------------------------
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
    def __setslice__(self, start, end, annotation):
        # There is *technically* no need for the first if clause, but
        # isinstance() is faster than "__iter__" in dir(annotation),
        # and as a tuple is most likely what will be called, it was decided
        # that two clauses are used.
        if isinstance(annotation, tuple) and (len(annotation == 2)):
            self.annotate(start, end, *annotation)
            return
        elif (len(annotation) == 2) and ("__iter__" in dir(annotation)):
            self.annotate(start, end, *annotation)



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
        """Delete """
        for i in range(value):
            self.popleft()
        self.annotations.popleft()

    def complete(self): #lol
        """Calls 'fix_rotation()' then returns itself."""
        self.fix_rotation()
        return self

    def annotate(self, start, end, name, value):
        return self.annotations.annotate(start,end,name,value)

    @property
    def text(self):
	return str(self.complete())
