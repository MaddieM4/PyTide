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
"""
These models were originally designed from the perspective of a server. 
To make client models, remove any user-authentication (checking if a user is on 
a wave). 
Ensure that all models can be constructed as replicas of server-sent data,
instead of all being constructed as new models entirely. 
"""

import random
from string import ascii_lowercase, digits
import re


import user
import blip


class Wave(object):
	"""Models a Wave.

    This object should not be directly instantiated, instead, the server method
    should be used, which will return a new Wave object.
    """
    class ID(object):
        """Represents a WaveID

        domain = the domain that the wave belongs to
        reserved = an iterable containing full string-form wave ids that are
        already in use.

        Instances of this class should not be directly created."""
        sep = '!w+'
        def __init__(self, domain, reserved):
            """Instantiate a new wave id. An iterable of reserved wave ids must
            be provided."""
            self._domain = domain
            self._id = None
            while (not self._id) or (self._id in reserved):
                self._id = random.sample(ascii_lowercase + digits, 11)
        def __str__(self):
            return self.sep.join((self._domain, self._id))
        def __repr__(self):
            return "WaveID: " + self.__str__()
        @property
        def domain(self):
            return self._domain
        @property
        def id(self):
            return self._id
        @classmethod
        def construct(cls, domain, id):
        	self = cls(domain, ())
        	self._id = id

    def __init__(self, domain, creator):
        """Creates a new wave with a new Wave.ID object, and a root Wavelet.

        The root Wavelet object will create a root blip for itself, so to have
        a full, new, editable Wave, just do:
        w = wave.server.db.models.wave.Wave()
        root_blip = w.get_root().root_blip
        then perform your modify operations.
        """
        # Wave ID references
        self._id = self.ID(domain)
        self._idstr = str(self._id)
        # Convenience attributes to save referencing the root wavelet
        self._domain = domain
        self._creator = creator
        # Dictionary containing Wavelet.ID objects keyed on Wavelet ID strings.
        self._wavelet_id_mapping = {}
        # Fast reference to the root wavelet, as it will be the most fetched.
        self._root = Wavelet(domain = domain, creator = creator, wave = self,
                             waveinstantiated = False)
        self._wavelet_id_mapping[str(self._root.id)] = self._root.id
        self._wavelets = {self._root.id: self._root}

    @property
    def id(self):
        """Returns the ID objectinstance for this wave."""
        return self._id
    @property
    def idstr(self):
        """Returns the string form of this wave's id"""
        return self._idstr
    @property
    def domain(self):
        """Returns the string form domain of this wave"""
        return self._domain
    @property
    def creator(self):
        """Returns the user.User object responsible for creating this wave"""
        return self._creator
    @property
    def reserved(self):
        """A tuple containing the reserved wavelet id objects."""
        return tuple(self._wavelet_id_mapping.values())
    @property
    def reserved_str(self):
        """Tuple containing string-form reserved wavelet ids"""
        return tuple(self._wavelet_id_mapping.keys())
    def get_wavelet(self, id, user):
        """If user is a participant of the referenced wavelet, it is returned.

        If a wavelet doesn't exist, get_wavelet returns None. If the user is not
        a participant in the wavelet, get_wavelet again returns None. This makes
        it impossible for a user to know if there are wavelets in a wave that
        are private.

        This method should be invoked by a server, not by a client. Clients
        should use the server's method that references this."""
        #TODO: Update with server's method name once defined.
        if id in self._wavelets:
            wavelet = self._wavelets[id]
        elif id in self._wavelet_id_mapping:
            wavelet = self._wavelets[self._wavelet_id_mapping[id]]
        else:
            return None
        if wavelet.is_participant(user):
            return wavelet
        else:
            return None
    def get_view(self, user):
        """Returns a list of Wavelets that the user can view in this wave.

        The list order is based on the Wavelets' creation dates.
        """
        if self._root.is_participant(user):
            wavelets = set((self._root,))
        else:
            wavelets = set()
        for wavelet_id, wavelet in self._wavelets.items():
            if wavelet.is_participant(user):
                wavelets.add(wavelet)
        return wavelets
    def get_root(self, user):
        """If 'user' is on the root wavelet of this wave, return the wave.

        else, return None
        """
        if self._root.is_participant(user):
            return self._root
        else:
            return None
    @property
    def root_id(self):
    	return getattr(self.root_wavelet, 'id', None)
    @property
    def root_wavelet(self):
    	return getattr(self, '_root', None)
    def new_wavelet(self, domain, user):
        """Creates a new wavelet object & associate it with this wave."""
        wavelet = Wavelet(domain = domain, creator = user, wave = self)
        self._wavelet_id_mapping[str(wavelet.id)] = wavelet.id
        self._wavelets[wavelet.id] = wavelet

class Wavelet(object):
    """Models a Wavelet.

    Users should know never to instantiate a Wavelet object themselves. It
    should always be instantiated by calling Wave.new_wavelet(domain, user) on
    a Wave object returned by the server module."""
    class ID(object):
        """Represents a WaveletID

        domain = the domain that the wavelet belongs to
        reserved = an iterable containing full string-form wavelet ids that are
        already in use.

        Instances of this class should not be directly created."""
        sep = '!'
        def __init__(self, domain, reserved = ()):
            """Instantiates an ID object & randomly generates a unique id."""
            self._domain = domain
            self._id = None
            while (not self._id) or (self._id in reserved):
                self._id = random.sample(ascii_lowercase + digits, 11)
                # TODO: Decide if reserved() should make a call to Wavelet.Wave
                # Considering that the Wavelet object creating this won't have
                # access to this list through any other method.
        def __str__(self):
            """Returns string form full identifer.
            domain.com!wavelet_id
            """
            return self.sep.join((self._domain, self._id))
        def __repr__(self):
        	"""Returns representation of the ID object.
        	WaveletID: domain.com!wavelet_id
        	"""
        	return "WaveletID: " + self.__str__()
        @property
        def domain(self):
            """returns the domain string"""
            return self._domain
        @property
        def id(self):
            """returns the wavelet id string (not including the domain)"""
            return self._id
        @classmethod
        def construct(cls, domain, id):
        	self = cls(domain, ())
        	self._id = id
    def __init__(self, domain, creator, wave, digest = None,
                 waveinstantiated = True):
        if waveinstantiated:
            self._id = self.ID(domain, wave.reservedstr)
        else:
            self._id = self.ID(domain,)

        if not digest:
            digest = Digest()
        # NOTE: Digest has not been made a property, as it was not clear if it
        # should be able to be reasigned or not. Clarification?
        self.digest = digest

        self._wave = wave
        self._participants = user.Participants(creator)
        self._root_blip = blip.Blip()
        #!...
    @property
    def domain(self):
        """Return the string form domain (same as Wavelet.id.domain)"""
        return self._id.domain
    @property
    def id(self):
        """Return the Wavelet.ID object associated with this wavelet"""
        return self._id
    @property
    def wave(self):
        """Return the Wave object that this wavelet is linked to."""
        return self._wave
    @property
    def root_blip(self):
        """Return the Blib object assigned to the root position in the wave."""
        return self._root_blip
    def is_participant(self, user):
        """Checks if user is a participant of the wavelet."""
        if user in self._participants:
            return True
        else:
            return False
    
    # ------------------------ CODE INCOMPLETE ---------------------------------
