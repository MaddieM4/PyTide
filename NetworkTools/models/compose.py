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

import instruction
import operation

def compose(a, b):
    """Composes two *adjacent* instructions into a single instruction.

    The instructions must be adjacent, and a must come before b, otherwise,
    the returned instruction(s) will not perform the same behavior that the
    original instructions did.

    If the instructions cannot be composed, then the two are both returned
    again. The following code is recommended, to ensure no bugs occur because
    of this:

    instructions = (a, b) # a and b are instructions
    composed = compose(*instructions)
    if composed == instructions:
        # code to handle what happens when they don't compose.
    else:
        # code to handle what happens when they do.

    """
    if a.name is 'AnnotationBoundary':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'DeleteCharacters':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'DeleteCloseElement':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'DeleteOpenElement':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'InsertCharacters':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            document = a.document
            string = a.string + b.string
            return instruction.InsertCharacters(document=document,
                                                string=string)
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'InsertCloseElement':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'InsertOpenElement':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            pass


    elif a.name is 'Retain':
        if b.name is 'AnnotationBoundary':
            pass
        elif b.name is 'DeleteCharacters':
            pass
        elif b.name is 'DeleteCloseElement':
            pass
        elif b.name is 'DeleteOpenElement':
            pass
        elif b.name is 'InsertCharacters':
            pass
        elif b.name is 'InsertCloseElement':
            pass
        elif b.name is 'InsertOpenElement':
            pass
        elif b.name is 'Retain':
            document = a.document
            count = a.count + b.count
            return instruction.Retain(document=document,
                                      count=count)



