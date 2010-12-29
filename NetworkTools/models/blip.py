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

import document

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
        self.document = document.BlipDocument()

    #TODO: Provide annotate() method which will apply an annotation to a range.
