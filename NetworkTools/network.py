import NetworkTools

import threading
import models

class Network(threading.Thread):
	'''The Network object is a thread, and it communicates between the connection plugin
	(also a thread) and the rest of the program. It holds the "official" version of every
	wavelet in its own memory.
	
	It handles the application of operations, notifying the appropriate objects in reg
	when stuff happens, and the management of connection plugins. '''

	def __init__(self, reg):
		threading.Thread.__init__(self, name="PyTideNetwork")
		self.registry = reg
		self.connection = None
		self._status = "No connection"
		self.wavelets = []
		self.contacts = []
		self.loginWindow = self.registry.newLoginWindow(self.rcv_logindata)
		self.start()

	def rcv_logindata(self, username, password):
		self.connect(username, password)

	def run(self):
		if self.is_connected():
			self.connection.getUpdates()
			self.connection.submit()

	def query(self, query):
		return self.connection.query(query)

	def connect(self, username, password):
		print "Network connecting to %s" % username
		domain = username.split('@')[1]
		if domain == "googlewave.com" or domain == "gmail.com":
			try:
				self.status("Connecting to Google Wave")
				import gwave
				self.connection = gwave.GoogleWaveConnection(username, password, self)
				self.status("Connected")
				self.username = username
				self.loginWindow.hide()
				self.registry.newWaveList()
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
