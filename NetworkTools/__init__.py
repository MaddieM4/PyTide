# base class that connection classes will subclass

# This is basically just a suggestion to get the network
# guys started. I really don't want to get involved in
# that part of the program any more than I have to.
# People who understand the wave model better than I do
# are the people who should be building this and its
# subclasses. - Philip

class Document:
	def __init__(self, meta):
		self.meta = meta
		self.structure = []

	def addBlip(self, blip, position):
		self.structure.insert(position,blip)

class Blip:
	def __init__(self, contents, meta):
		self.contents = contents
		self.meta = meta

class Plugin:
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def connect(self):
		print "Connected"

	def disconnect(self):
		print "Disconnected"

	def query(self, query, callback):
		print "Searching for waves that match '"+query+"'"
		wavelet_list = []
		callback(wavelet_list)

	def getStructure(self, wavelet_id, callback):
		print "Retrieving the structure of wavelet",wavelet_id
		wavelet_tree = {}
		callback(wavelet_tree)

	def getBlip(self, blip_id):
		print "Retrieving blip contents of",blip_id
		return Blip()
