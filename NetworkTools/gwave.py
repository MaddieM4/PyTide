import json
import models
import os
import urllib
import NetworkTools

from waveapi import waveservice

class GoogleWaveConnection(models.Plugin):
	def __init__(self, username, password, network):
		models.Plugin.__init__(self)
		self.network = network
		self.username = username
		self.password = password

		try:
			serverResponse = urllib.urlopen("http://pytidewave.appspot.com/account/remotelogin",
				urllib.urlencode({'username':username,'password':password}))
		except IOError, e:
			raise NetworkTools.ConnectionFailure("Could not communicate with PyTide Server",e[1])

		print serverResponse.read()
		self.accessKey = None
		self.service = waveservice.WaveService()
		self.start()

	def run(self):
		pass

	def query(self, query):
		return self.service.search(query)

	def new_wavelet(self):
		pass
