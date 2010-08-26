import threading

# I will fill in more stuff here as I understand the scope of the requirements

class Operation:
	pass

class Blip:
	pass

class Wavelet:
	def __init__(self, digest = None):
		self.digest = digest

class Document:
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
	def __init__(self, name="", nick="", address = None, picture = None):
		self.name = name
		self.nick = nick
		self.addr = address
		self.pict = picture

# This space left intentionally blank for subclassing
class Plugin(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self, name="PyTideNetworkPlugin")

	def run(self):
		'''Handles stuff internally.
 
		Do not modify external resources in run(), leave that to the
		other functions. You don't want to make the program unstable, do ya?'''
		pass

	def getWavelet(self, waveid):
		'''Start loading a wave document into the network.'''
		pass

	def getUpdates(self):
		'''Does not return anything, it calls functions in self.network'''
		pass

	def query(self, query):
		'''Returns a list of (title, id, participants, blip count, unread count, date) tuples'''
		pass

	def submit(self):
		'''Push all local operations to server.'''
		pass
