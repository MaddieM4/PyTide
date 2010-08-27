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

			access_data = json.loads(serverResponse.read())
			self.service = waveservice.WaveService()
			self.service.set_access_token(access_data['serial'])
			self.start()
		except IOError, e:
			raise NetworkTools.ConnectionFailure("Could not communicate with PyTide Server",e[1])

	def run(self):
		pass

	def query(self, query):
		return self.service.search(query)

	def new_wavelet(self):
		pass
