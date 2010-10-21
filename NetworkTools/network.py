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

import NetworkTools
from persistance.config import Config

import threading
from models import threads, operation
import json

class Network(threads.LoopingThread):
	'''The Network object is a thread, and it communicates between the connection plugin
	(also a thread) and the rest of the program. It holds the "official" version of every
	wavelet in its own memory.
	
	It handles the application of operations, notifying the appropriate objects in reg
	when stuff happens, and the management of connection plugins. '''

	def __init__(self, reg):
		super(Network, self).__init__(name="PyTideNetwork")
		self.registry = reg
		self.connection = None
		self._status = "No connection"
		self.wavelets = []
		self.contacts = []
		# start loading configs now. Let access block later if necessary
		self.savedlogins = Config(namespace="savedlogins")
		self.savedlogins.setAutoTimer(3)
		self.loginWindow = self.registry.newLoginWindow(self.connect, self.savedlogins)
		self.start()

	def process(self):
		if self.is_connected():
			self.connection.getUpdates()
			self.connection.submit()

	def query(self, query, startpage=0):
		try:
			results = self.connection.query(query, startpage=startpage)
			self.registry.setIcon('active')
			return results
		except NetworkTools.ConnectionFailure:
			self.registry.setIcon('error')
			return None

	def connect(self, username, password):
		print "Network connecting to %s" % username
		domain = username.split('@')[1]
		if domain == "googlewave.com" or domain == "gmail.com":
			try:
				self.status("Connecting to Google Wave")
				import gwave
				self.connection = gwave.GoogleWaveConnection(username, password, self)
				self.status("Connected")
				self.loginWindow.hide()
				self.registry.newWaveList()
				self.saveLogin(username, password)
				return True
			except NetworkTools.ConnectionFailure, e:
				self.status("Connection Failed - Your internet may be down or your login data incorrect")
				return False
		else:
			self.status("Domain name not recognized")

	def openURL(self, address, destroyCallback=None):
		print "Network.openURL(%s)" % address
		return self.registry.newBrowserWindow(address,destroyCallback=destroyCallback)

	def status(self, status_str):
		self._status = status_str
		if self.loginWindow != None:
			self.loginWindow.setStatus(self._status)
		print "Network status: %s" % self._status

	def is_connected(self):
		if self.connection == None:
			return False
		else:
			return True

	def participantMeta(self,address):
		ascii = ord(address.lower()[0])
		if ascii >=97 and ascii <= 122:
			avatar = "img/profile/"+address.lower()[0]+".jpg"
		else:
			avatar = "img/profile_base.png"
		return {
			'nick':address,
			'address':address,
			'avatar':avatar
			}

	def saveLogin(self, uname, pword):
		self.savedlogins.set({uname:pword})

	def getContacts(self):
		'''Return a list of all your personal contacts.'''
		return self.connection.get_contacts()

	def subscribe(doclocation):
		d = self.connection.subscribe(doclocation)
		self.documents.append(d)
		self.opqueues.append(models.OperationQueue(d))
		return d

	def unsubscribe(doclocation):
		for q in self.opqueues:
			if q.wavelet.location == doclocation:
				q.addOp(ops.CLOSE())
				return True
		return False
