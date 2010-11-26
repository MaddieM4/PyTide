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
import NetworkTools
import os
import urllib

from ..models import plugin, user, digest
from ..waveapi import waveservice


PYTIDE_LOGIN_URL = "http://pytidewave.appspot.com/account/remotelogin"

class modelConverter:
    @staticmethod
    def SearchResults(wsresults, page, maxpage):
        ''' Turns a Data API search results list to a 
        models.SearchResults object '''
        digests = []
        for i in wsresults.digests:
            digests.append(modelConverter.Digest(i))
        return digest.SearchResults(wsresults.query,
                                    page,
                                    digests,
                                    maxpage)

    @staticmethod
    def Digest(wsdigest):
        return digest.Digest(wsdigest.wave_id,
                             wsdigest.title,
                             wsdigest.participants,
                             wsdigest.unread_count,
                             wsdigest.blip_count,
                             wsdigest.last_modified)

    @staticmethod
    def User(profile):
        return user.User(name = profile['name'],
                         address = profile['address'],
                         avatar = profile['imageUrl'])

        

class GoogleWaveConnection(plugin.Plugin):
    _accept_dict = {'username':'',
                    'password':'',}
    @classmethod
    def _accepts(cls):
        return cls._accept_dict
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        encoded_login = urllib.urlencode(dict(username=username,
                                              password=password)
                                         )
        try:
            server_response = urllib.urlopen(PYTIDE_LOGIN_URL, encoded_login)            
        except IOError, e:
            raise NetworkTools.ConnectionFailure("Could not communicate with PyTide Server",
                                                 e[1])
        else:
            access_data = json.loads(server_response.read())
            self.service = waveservice.WaveService()
            self.service.set_access_token(access_data['serial'])
            self.start()

    def _query(self, query, startpage):
        try:
            results=self.service.search(query,
                                        index=startpage*20,
                                        num_results=21)
        except:
            raise NetworkTools.ConnectionFailure("Connection to Google Wave failed")
            return # Why do we need to return after a raise?
        if results.num_results < 21:
            maxpage = startpage
        else:
            maxpage = startpage+1 # more pages exist, we will just assume one more
        return modelConverter.SearchResults(results, startpage, maxpage)

    def _me(self):
        return modelConverter.User(self.service.fetch_my_profile()['participantProfile'])

    def _contacts(self):
        return [modelConverter.User(self.service.fetch_my_profile()['participantProfile'])]
