from gui import wavelist

class Registry:
	"""reg is the registry, which allows windows to communicate 
	with each other.

	The main app instantiates a single Registry instance, and 
	passes it on to every window it makes. When those windows 
	make windows, they pass it on. This works by reference 
	because it's an instance of a new-style class, which means 
	it's treated much like a C pointer. 

	Python is weird like that.""" 

	def __init__(self):
		'''A standard registry has a single network, and a
		list each of WaveLists, WaveViewers, and BlipWindows.'''
		self.Network = None
		self.WaveLists = []
		self.WaveViewers = []
		self.BlipWindows = []
		self.MasterList = {}
		self.idPos = 0

	def newId(self):
		self.idPos += 1
		return self.idPos-1

	def getNetwork(self):
		return self.Network

	def msgWaveLists(self, msg, ignore=None):
		'''Send an object to every registered WaveList. Triggers
		the regmsg_receive() function. 

		Optional argument "Ignore" can be used to prevent the 
		window sending the event from also receiving it.'''
		for wlid in self.WaveLists:
			wl = self.MasterList[wlid]
			if wl != ignore:
				wl.regmsg_receive(msg)

	def msgAll(self, msg, ignore=None):
		'''Call all the individual msgSomething functions with
		the given arguments.'''
		self.msgWaveLists(msg,ignore)

	def newWaveList(self):
		'''Create a new wavelist. This also sends a message
		to all other objects proclaiming the birth, so to
		speak. This message does not get an ignore capability.'''
		id = self.newId()
		self.MasterList[id] = wavelist.WaveList(self)
		self.WaveLists.append(id)
		msg = {'type':'newWaveList', \
			'id':id}
		self.msgAll(msg)

	def fromID(self, id):
		return self.MasterList[id]

	def getWaveListId(self, wl):
		for id in self.WaveLists:
			if self.fromID(id) == wl:
				return id
		return None

	def getWaveLists(self):
		return [self.fromID(id) for id in self.WaveLists]

	def getAllWindows(self):
		return self.getWaveLists()

	def unregister(self, obj):
		for i in self.MasterList:
			if self.MasterList[i] == obj:
				# i is the object's ID
				if i in self.WaveLists: self.WaveLists.remove(i)
				elif i in self.WaveViewers: self.WaveViewers.remove(i)
				elif i in self.BlipWindows: self.BlipWindows.remove(i)

				# remove from master list without deleting actual object
				self.MasterList.pop(i)
				return True
		return False
