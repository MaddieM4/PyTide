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

def transform(a, b):
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
            pass
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
            pass 
    
    
        
