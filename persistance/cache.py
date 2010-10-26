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
import urllib2

from gtk.gdk import threads_enter, threads_leave

class Resource:
	''' This class works by pointer-y magic. A resource has
	an actual URI (set in init), a cache URI, and a magic
	address. The magic address is initialized to the actual
	URI immediately, so that there is immediately a valid
	address. Once the file has been downloaded in the background,
	the magic address is set to the cache URI.

	If you're using this class in something, remember that
	the magic address is myres.location, just like a regular
	old property. Also remember that the address is liable to
	change at any time, but in light of concurrency, it's
	build so that it's not changed while you're trying to read
	it.
	'''

	def __init__(self, address, filename, 
				lifetime=datetime.timedelta(hours=1), 
				expires = None,
				cached = False):
		self.uri = address
		if cached:
			self.magic = address
		else:
			self.magic = uri
		self.filename = filename
		self.lifetime = lifetime
		self.lock = threading.Lock()
		if expires == None:
			self.load()
			self.expires = datetime.datetime.now()+lifetime
		else:
			self.expires = expires

	@property
	def location(self):
		self.lock.acquire()
		addr = self.magic
		self.lock.release()
		return addr

	def load(self):
		self.downloader = threading.Thread(self.download)
		self.downloader.start()

	def download(self):
		threads_enter()
		try:
			self.lock.acquire()
			self.magic = self.uri
			self.lock.release()

			infile = urllib2.urlopen(self.uri)
			outfile = open(self.filename,'wb')
			outfile.truncate()
			outfile.write(infile.read())
			self.expires = datetime.datetime.now()+lifetime

			self.lock.acquire()
			self.magic = self.filename
			self.lock.release()
		finally:
			threads_leave()

	def toJSON(self):
		return json.dumps({'uri':self.uri, 
			'cacheaddress':self.filename,
			'cached':self.magic==self.filename,
			'expires':str(self.expires)})

	@classmethod
	def fromJSON(jsonstring):
		props = json.loads(jsonstring)
		return Resource(props['uri'], props['cacheaddress'],
			expires = datetime.datetime(props['expires']),
			cached = )

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
	def __init__(self, foldername, autosavetime=2, mintime=15):
		''' Autosavetime and mintime are both in seconds.

		Foldername is the root folder plus the name of the item.
		Don't worry about creating subfolders ahead of time, as
		long as the root folder exists, CacheItem will handle
		the rest.
		'''
		self.dir = foldername
		print "CacheItem at ", self.dir
		persistance.validate_dir(self.dir)
		self.saveDelay = autosavetime
		self.lastSave = None
		self.mintime = mintime
		self.autosave = None
		self.resources = []
		self.index = {}
		self.lock = threading.Lock()
		try:
			self.load()
		except:
			self.save(threaded=False)

	def get(self):
		self.lock.acquire()
		data = self.index
		self.lock.release()
		return data

	def merge(self, data):
		self.lock.acquire()
		try:
			self._merge(data)
			self.startTimer()
		finally:
			self.lock.release()

	def _merge(self, data):
		''' Internal function, do not use '''
		if type(data).__name__ != "dict":
			raise TypeError("Expected dict, got %s instead" % type(data).__name__)
		else:
			for i in data: self.index[i] = data[i]

	def load(self):
		print "acquiring load lock"
		self.lock.acquire()
		try:
			with open(os.path.join(self.dir,'index')) as f:
				print "trying to process file"
				self.index = json.loads(f.read())['index']
				print "Loaded CacheItem:",self.index
		finally:
			print "releasing load lock"
			self.lock.release()

	def save(self, threaded = True):
		''' Does not support resources yet. '''
		# save to disk
		print "Trying to get into save"
		if threaded: threads_enter()
		print "threads_enter success"
		self.lock.acquire()
		print "lock acquired"
		try:
			print "Trying to save"
			self.lastSave = datetime.datetime.now()
			index = open(os.path.join(self.dir, 'index'), 'w')
			index.truncate()
			index.write(json.dumps({'index':self.index,'resources':{}}))
			print "saved"
		finally:
			index.close()
			self.lock.release()
			if threaded: threads_leave()

	def startTimer(self):
		now = datetime.datetime.now()
		delay = 0
		if self.mintime >= 0 and self.lastSave != None:
			# use minimum time between saves
			soonest = self.lastSave + datetime.timedelta(seconds=self.mintime)
			if soonest < now:
				delay = 0
			else:
				delay = (soonest-now).seconds
		print "Total save delay:", self.saveDelay+delay
		if self.autosave != None: self.autosave.cancel()
		self.autosave = threading.Timer(self.saveDelay+delay, self.save)
		self.autosave.start()

	def cleanup(self):
		''' Delete all resource files that are not referenced by the index '''
		pass

class Cache:
	''' Base class for all caching mechanisms. '''

	def __init__(self, subfolder = ""):
		self.dir = os.path.join(persistance.init_dir(), "cache/", subfolder)
		print "Cache at ",self.dir
		self.items = {}

	def merge(self, name, index = {}):
		''' Add data to the index of an item.'''
		self.get(name).merge(index)

	def load(self, name):
		''' Load data from the hard drive. '''
		self.items[name] = CacheItem(os.path.join(self.dir,name))

	def get(self, name):
		''' Return the item with that name, load if necessary. '''
		if not name in self.items:
			self.load(name)
		return self.items[name]

class DocumentCache(Cache):
	''' Cache for storing wave documents. '''

	def __init__(self):
		super(DocumentCache, self).__init__("documents")

class UserCache(Cache):
	''' Cache for participant profiles, such as (but not limited to) your contacts.'''

	def __init__(self):
		super(DocumentCache, self).__init__("documents")

class QueryCache(Cache):
	''' Uses a hash for the name since queries are liable to contain
	funky characters. Expire very quickly.'''

	def __init__(self):
		super(DocumentCache, self).__init__("queries")

class OutboundCache(Cache):
	''' A class for storing locally-generated operations until it's verified that
	the server has recieved them. In the event of a crash or internet outage,
	your data will be saved. In fact, you can even work with your waves offline,
	and your changes will simply be synced next time you get online.'''

	def __init__(self):
		super(DocumentCache, self).__init__("documents")
