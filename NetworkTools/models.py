import threading
import time
from gtk.gdk import threads_enter, threads_leave

import logging
LOG_FILENAME="loopingthread.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# I will fill in more stuff here as I understand the scope of the requirements

class Operation:
	pass

class OperationQueue:
	'''A sequence of operations. Every wavelet has one.'''

class Blip:
	pass

class Wavelet:
	def __init__(self, digest = None):
		self.digest = digest

class Document:
	'''A simple class to store and easily pass around wave snapshots. It has no
	facilities to submit and recieve updates over the network, this is handled
	by the plugin.'''
	def __init__(self, id=None, jsonInput=None):
		# Create a new document
		self.wavelets = []
		self.properties = {}
		self.id = id or "unspecified"
		open('~/.pytide/document','w').write(jsonInput)

	def toJSON(self):
		pass

class Digest:
	def __init__(title, id, participants, blipsTotal, blipsUnread, date, folder=None,features=[]):
		self.title = title
		self.id = id
		self.participants = participants
		self.blipsTotal = blipsTotal
		self.blipsUnread = blipsUnread
		self.date = date
		self.folder = folder
		self.features = features

class User:
	'''Used for contacts and participants and such. '''
	def __init__(self, name="", nick="", address = None, avatar = None):
		self.name = name
		self.nick = nick
		self.addr = address
		self.pict = avatar

class LoopingThread(threading.Thread):
	'''This class allows you to make a thready object that calls
	its function on an infinite loop, automatically working with
	the gtk.gdk mutex. Please note that when you subclass this,
	as you are meant to do, you are going to overwrite the PROCESS
	function, not the RUN function.'''
	def __init__(self, name=None,speed=3):
		threading.Thread.__init__(self, name=name)
		self.setDaemon(True)
		self.speed=speed
		self.stopper = threading.Event()

	def run(self):
		while 1:
			threads_enter()
#			logging.debug("LoopingThread")
			self.process()
			threads_leave()
			time.sleep(self.speed)

	def process(self):
		pass

# This space left intentionally blank for subclassing
# Although a bit of example code is here to get you started
class Plugin(LoopingThread):
	def __init__(self):
		LoopingThread.__init__(self, name="PyTideNetworkPlugin")
		self.documents = []

	def process(self):
		'''Handles stuff internally.
 
		Do not modify external resources in process(), leave that to the
		other functions. You don't want to make the program unstable, do ya?'''
		pass

	def subscribe(self, waveid):
		'''Start loading a wave document into the network.'''
		d = Document(id=waveid)
		self.documents.append(d)
		# start loading in plugin thread, sync to documents when network calls getUpdates()
		return d

	def unsubscribe(self, waveid):
		for doc in self.documents:
			if doc.id == waveid: 
				del doc
				return True
		return False

	def getUpdates(self):
		'''Does not return anything, is called by network to sync internal data to Document objects'''
		pass

	def query(self, query):
		'''Returns a list of (title, id, participants, blip count, unread count, date) tuples'''
		pass

	def submit(self):
		'''Push all local operations to server.'''
		pass

	def documents(self):
		return self.documents
