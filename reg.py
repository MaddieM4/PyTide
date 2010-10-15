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

from gui import wavelist, waveviewer, browserwindow, loginwindow, iconstates
from NetworkTools import network
from persistance.config import Config

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
		self.icon = None
		self.idPos = 0
		self.config = {}
		self.config['wavelist'] = Config(namespace="wavelist", onload=self.pushglobalconf_WaveList)
		for i in self.config:
			self.config[i].setAutoTimer(4)

	def newId(self):
		self.idPos += 1
		return self.idPos-1

	def getNetwork(self):
		return self.Network

	def newNetwork(self):
		self.Network = network.Network(self)

	def newLoginWindow(self, callback, loginConfig):
		return loginwindow.LoginWindow(callback, loginConfig)

	def msgWaveLists(self, msg, ignore=None):
		'''Send an object to every registered WaveList. Triggers
		the regmsg_receive() function. 

		Optional argument "Ignore" can be used to prevent the 
		window sending the event from also receiving it.'''
		for wlid in self.WaveLists:
			wl = self.MasterList[wlid]
			if wl != ignore:
				wl.regmsg_receive(msg)

	def msgWaveViewers(self, msg, ignore=None):
		for wlid in self.WaveViewers:
			wl = self.MasterList[wlid]
			if wl != ignore:
				wl.regmsg_receive(msg)

	def msgAll(self, msg, ignore=None):
		'''Call all the individual msgSomething functions with
		the given arguments.'''
		self.msgWaveLists(msg,ignore)
		self.msgWaveViewers(msg,ignore)

	def newWaveList(self):
		'''Create a new wavelist. This also sends a message
		to all other objects proclaiming the birth, so to
		speak. This message does not get an ignore capability.'''
		self.setIcon("active")
		id = self.newId()
		self.MasterList[id] = wavelist.WaveList(self)
		self.WaveLists.append(id)
		msg = {'type':'newWaveList', \
			'id':id}
		self.msgAll(msg)

	def newWaveViewer(self):
		self.setIcon("active")
		id = self.newId()
		self.MasterList[id] = waveviewer.WaveViewer(self)
		self.WaveViewers.append(id)
		msg = {'type':'newWaveViewer', 'id': id}
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

	def getWaveViewers(self):
		return [self.fromID(id) for id in self.WaveViewers]

	def getAllWindows(self):
		return self.getWaveLists()+self.getWaveViewers()

	def killAllWindows(self):
		self.msgAll({'type':'kill'})

	def unregister(self, obj):
		for i in self.MasterList:
			if self.MasterList[i] == obj:
				# i is the object's ID
				if i in self.WaveLists: self.WaveLists.remove(i)
				elif i in self.WaveViewers: self.WaveViewers.remove(i)
				elif i in self.BlipWindows: self.BlipWindows.remove(i)

				# remove from master list without deleting actual object
				self.MasterList.pop(i)
				if len(self.MasterList)==0: self.setIcon("inactive")
				return True
		return False

	def getWaveListConfig(self,key):
		print "getWLC",key
		try:
			g = self.config['wavelist'].get(key)
			if g == None: return self.getWaveListConfigDefault(key)
			else: return g
		except:
			# return default
			return self.getWaveListConfigDefault(key)

	def getWaveListConfigDefault(self,key):
		if key == "tbshorten": return "default"	
		else: return None

	def setWaveListConfig(self,key,value):
		self.config['wavelist'].set({key:value})
		self.msgWaveLists({'type':'setOption','name':key,'value':value})

	def pushglobalconf_WaveList(self, conf):
		print "pgcWL"
		for i in conf:
			print "\t",i
			self.msgWaveLists({'type':'setOption','name':i,'value':conf[i]})

	def setIcon(self,statestr):
		if (self.icon == None): return False
		if statestr == "error":
			self.icon.setIconState(iconstates.ICON_ERROR)
			return True
		elif statestr == "active":
			self.icon.setIconState(iconstates.ICON_ACTIVE)
			return True
		elif statestr == "inactive":
			self.icon.setIconState(iconstates.ICON_INACTIVE)
			return True
		elif statestr == "unread":
			self.icon.setIconState(iconstates.ICON_UNREAD)
			return True
		else:
			return False
