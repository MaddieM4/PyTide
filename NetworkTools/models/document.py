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
        return '</%s>' % self.name
    @property
    def name(self):
        return self.name
