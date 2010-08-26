#!/usr/bin/python2.4
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines classes that are needed to model a participant profile."""


class ParticipantProfile(object):
  """Models a set of search results.

  Search results are composed of a list of digests, query, and number of
  results.
  """

  def __init__(self, json):
    """Inits this profile object with JSON data.

    Args:
      json: JSON data dictionary from Wave server.
    """
    self._name = json.get('name')
    self._image_url = json.get('imageUrl')
    self._profile_url = json.get('profileUrl')

  @property
  def name(self):
    """Returns the name for this profile."""
    return self._name

  @property
  def image_url(self):
    """Returns the URL of the participant's avatar."""
    return self._image_url

  @property
  def profile_url(self):
    """Returns the URL of the participant's external profile page."""
    return self._profile_url

  def serialize(self):
    """Return a dict of the profile properties."""
    return {'name': self._name,
            'imageUrl': self._image_url,
            'profileUrl': self._profile_url
           }
