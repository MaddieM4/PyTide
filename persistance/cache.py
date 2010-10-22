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

import os.path

import threading
import json
import datetime
import persistance

from gtk.gdk import threads_enter, threads_leave

class CacheItem:
	''' Container class for things you want to stick in a cache.

	Each CacheItem corresponds to a folder in the filesystem,
	which consists of a text file called "index" and other
	resources. So, for example, a contact would store all metadata
	(most of its total data) in "index" and cache the avatar to
	a resource image.

	Every item needs a function to serialize it to a dict and
	a function to unserialize it back. The dicts are saved as JSON
	data to "index".

	Unlike Configuration options, cache items are liable to change
	very, very frequently during normal operation. So like the
	config, it has the ultra-short-term delay (autosavetime, the
	delay between a change in the data and a save. A change during
	the delay resets the delay to autosavetime again). But it also
	has a minimum delay between save events (mintime). Mintime
	is optional (set to -1), config-style autosave is not.
	'''
	def __init__(self, foldername, autosavetime, mintime=5):
		''' Autosavetime and mintime are both in seconds.

		Foldername is the root folder plus the name of the item.
		Don't worry about creating subfolders ahead of time, as
		long as the root folder exists, CacheItem will handle
		the rest.
		'''
		self.dir = foldername
		persistance.validate_dir(self.dir)
		self.saveDelay = autosavetime
		self.lastSave = None
		self.mintime = mintime
		self.autosave = None
		self.resources = []
		self.index = {}
		self.lock = threading.Lock()

	def merge(self, data):
		self.lock.acquire()
		try:
			self._merge(data)
			self.startTimer()
		finally:
			self.lock.release()

	def _merge(self, data):
		''' Internal function, do not use '''
		if type(data).__name__ != "dict"
			raise TypeError("Expected dict, got %s instead" % type(data).__name__)
		else:
			for i in data: self.index[i] = data[i]

	def save(self):
		''' Does not support resources yet. '''
		# save to disk
		threads_enter()
		self.lock.acquire()
		try:
			self.lastSave = datetime.datetime.now()
			index = open(os.path.join(self.dir, 'index'), 'w')
			index.truncate()
			index.write(json.dumps(self.index))
		finally:
			index.close()
			self.lock.release()
			threads_leave()

	def startTimer(self):
		now = datetime.datetime.now()
		delay = 0
		if self.mintime >= 0 and self.lastSave != None:
			# use minimum time between saves
			soonest = self.lastSave + datetime.timedelta(seconds=self.mintime)
			if soonest < now:
				delay = 0
			else:
				delay = (soonest-now).total_seconds()
		self.autosave = threading.Timer(self.saveDelay+delay, self.save)

	def cleanup(self):
		''' Delete all resource files that are not referenced by the index '''
		pass

class Cache:
	''' Base class for all caching mechanisms. '''

	def __init__(self, subfolder = ""):
		self.dir = os.path.join(persistance.init_dir(), "/cache/", subfolder)
		self.items = {}

class DocumentCache(Cache):
	''' Cache for storing wave documents. '''

	def __init__(self):
		super(DocumentCache, self).__init__("documents")

class UserCache(Cache):
	''' Cache for participant profiles, such as (but not limited to) your contacts.'''

	def __init__(self):
		super(DocumentCache, self).__init__("documents")

class OutboundCache(Cache):
	''' A class for storing locally-generated operations until it's verified that
	the server has recieved them. In the event of a crash or internet outage,
	your data will be saved. In fact, you can even work with your waves offline,
	and your changes will simply be synced next time you get online.'''

	def __init__(self):
		super(DocumentCache, self).__init__("documents")
