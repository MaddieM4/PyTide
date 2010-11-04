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

from multiprocessing import Process, Queue
from Queue import Empty, Full
from threading import Lock
from threads import LoopingThread

class Responder(LoopingThread):
	''' A class used by the Plugin core to process the outqueue '''
	def __init__(self, plugin):
		super(Responder,self).__init__()
		self.plugin = plugin

	def process(self):
		try:
			res = self.plugin.outqueue.get_nowait()
			self.plugin.popcallback(res)(res[1])
		except Empty:
			pass

class Plugin(Process):
	''' Contains a process that handles messages and pushes some back. '''
	def __init__(self):
		super(Plugin, self).__init__()
		self.daemon = True
		self.inqueue = Queue()
		self.outqueue = Queue()
		self.callbacks = {}
		self.maxcallback = 0
		self.cblock = Lock()
		self.responder = Responder(self)
		self.responder.start()

	def run(self):
		''' Repeatedly process items in queue '''
		while 1:
			try:
				self.process(self.inqueue.get(timeout=2))
			except Empty:
				pass

	def process(self, data):
		''' Process a piece of data. All data is in dict form.

		"contacts" is a request for the full list of the user's contacts.

		"me" is a request for the users own information.
		The callback takes a models.user.User
		'''
		print "Models.plugin processing",data
		if type(data).__name__ != 'dict':
			return False
		t = data['type']
		if t == 'query':
			print "using query action"
			self.outqueue.put((data['callback'],self._query(data['query'],data['page'])))
		elif t == 'contacts':
			self.popcallback(data)(self._contacts())
		elif t == 'me':
			self.popcallback(data)(self._me())

	def pushcallback(self, c):
		print "pushcallback"
		self.cblock.acquire()
		self.callbacks[self.maxcallback]=c
		self.maxcallback += 1
		self.cblock.release()
		print self.callbacks
		return self.maxcallback-1

	def popcallback(self, data):
		print "popcallback"
		self.cblock.acquire()
		print self.callbacks
		c = self.callbacks[data[0]]
		del self.callbacks[data[0]]
		self.cblock.release()
		return c

	def query(self, query, startpage, callback):
		''' Callback function takes a models.digest.SearchResults '''
		self.inqueue.put({'type':'query',
				'query':query,
				'page':startpage,
				'callback':self.pushcallback(callback)})
		print "after query:", self.callbacks

	def get_contacts(self, callback):
		''' Callback function takes a list of models.user.User '''
		self.inqueue.put({'type':'contacts',
				'callback':self.pushcallback(callback)})

	def get_me(self, callback):
		''' Callback function takes a models.user.User '''
		self.inqueue.put({'type':'me',
				'callback':self.pushcallback(callback)})

	def _query(self, query, startpage):
		''' Override me! Return a models.digest.SearchResults '''
		pass

	def _contacts(self):
		''' Override me! Return a list of models.user.User '''
		pass

	def _me(self):
		''' Override me! Return a models.user.User '''
		pass
