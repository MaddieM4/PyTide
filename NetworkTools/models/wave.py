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




import user
import blip
import identifier

class WaveId(identifier.Identifier):
    sep = "!w+"
    rep = "WaveID: "

class WaveletId(identifier.Identifier):
    sep = "!"
    rep = "WaveletID: "
    
class Wave(object):
	"""Models a Wave.

    This object should not be directly instantiated, instead, the server method
    should be used, which will return a new Wave object.
    """
    def __init__(self, domain, identifier, *args, **kwargs):
        """Creates a new wave with a new Wave.ID object, and a root Wavelet.

        The root Wavelet object will create a root blip for itself, so to have
        a full, new, editable Wave, just do:
        w = wave.server.db.models.wave.Wave()
        root_blip = w.get_root().root_blip
        then perform your modify operations.
        """
        self._id = WaveId(domain, identifier)
        self._wavelet_id_mapping = {}
        self._wavelet_id_mapping[str(self._root.id)] = self._root.id
        self._wavelets = {self._root.id: self._root}
        raise NotImplemented("The Wave class is unfinished")
    
    @property
    def identifier(self):
        """Returns the WaveId for this wave."""
        return self._id

    @property
    def id(self):
        """Returns the WaveId for this wave."""
        return self.identifier
        raise DeprecationWarning
    

class Wavelet(object):
    """Models a Wavelet.

    Users should know never to instantiate a Wavelet object themselves. It
    should always be instantiated by calling Wave.new_wavelet(domain, user) on
    a Wave object returned by the server module."""
    def __init__(self, wave, identifier, *args, **kwargs):
        self._id = WaveletId(wave.identifier.domain, identifier)

        #if not digest:
        #    digest = Digest()
        # NOTE: Digest has not been made a property, as it was not clear if it
        # should be able to be reasigned or not. Clarification?
        #self.digest = digest
        self._wave = wave
        #self._participants = user.Participants(creator)
        #self._root_blip = blip.Blip()
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
