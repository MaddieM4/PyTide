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

import json
import models.plugin
import models.user
import models.digest
import os
import urllib
import NetworkTools

from waveapi import waveservice

class modelConverter:
	@classmethod
	def SearchResults(self,wsresults, page, maxpage):
		''' Turns a Data API search results list to a 
		models.SearchResults object '''
		digests = []
		for i in wsresults.digests:
			digests.append(modelConverter.Digest(i))
		return models.digest.SearchResults(wsresults.query,
							page,
							digests,
							maxpage)

	@classmethod
	def Digest(self,wsdigest):
		return models.digest.Digest(wsdigest.wave_id,
					wsdigest.title,
					wsdigest.participants,
					wsdigest.unread_count,
					wsdigest.blip_count,
					wsdigest.last_modified)

	@classmethod
	def User(self,profile):
		return models.user.User(
			name=profile['name'], 
			address=profile['address'],
			avatar=profile['imageUrl'] 
		)
		

class GoogleWaveConnection(models.plugin.Plugin):
	def __init__(self, username, password):
		super(GoogleWaveConnection, self).__init__()
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

	def _query(self, query, startpage):
		try:
			results=self.service.search(query, index=startpage*20,num_results=21)
		except:
			raise NetworkTools.ConnectionFailure("Connection to Google Wave failed")
			return
		if results.num_results < 21:
			maxpage = startpage
		else:
			maxpage = startpage+1 # more pages exist, we will just assume one more
		return modelConverter.SearchResults(results, startpage, maxpage)

	def _me(self):
		return modelConverter.User(self.service.fetch_profile()['participantProfile'])

	def _contacts(self):
		return [modelConverter.User(self.service.fetch_profile()['participantProfile'])]
