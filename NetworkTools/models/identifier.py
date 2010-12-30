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

class Identifier(object):
    """Represents an Identifier

    domain = the domain that the identifier belongs to
    identifier = the string form identifier, usually random

    This class is designed to be subclassed.
    Subclasses are advised to override "sep" and "rep" below.
    """
    sep = '/'
    rep = 'Identifier: '
    
    def __init__(self, domain, identifier=None):
        """Instantiate a new wave id. An iterable of reserved wave ids must
        be provided."""
        self._domain = domain
        self._id = identifier
        
    def __str__(self):
        return self.sep.join((self._domain, self._id))
    
    def __repr__(self):
        return rep + self.__str__()
    
    @property
    def domain(self):
        return self._domain
    
    @property
    def id(self):
        return self._id

    @property
    def identifier(self):
        return self._id
    
    def __hash__(self):
        return hash(tuple(self.domain, self.id))
    
    def __eq__(self, other):
        if ((not hasattr(other, 'id')) or
            (not hasattr(other, 'domain')):
            return False
        elif ((self.id == other.id) and
            (self.domain == other.domain)):
            return True
        else:
            return False
            
    def __ne__(self, other):
        return not (self == other)
            
    @classmethod
    def randomid(cls, domain):
        identifier = None
        while not identifier:
            identifier = random.sample(ascii_lowercase + digits, 11)
        return cls(domain = domain, identifier = identifier)

#-------------- Subclasses ----------------------------------------------------

class WaveId(Identifier):
    sep = "+w"
    rep = "Wave ID: "

class WaveletId(Identifier):
    sep = "!"
    rep = "Wavelet ID: "
