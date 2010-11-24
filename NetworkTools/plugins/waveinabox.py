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

import urllib, urllib2

import websocket

from ..models import plugin
from ..models.user import User
from ..models.digest import Digest

from NetworkTools import ConnectionFailure

__all__ = ['WaveInABoxConnection']

class WaveInABoxConnection(plugin.Plugin):
    _accept_dict = {'username':'',
                    'password':'',
                    'domain':'' ##'acmewave.com',
                    }
    
    def __init__(self, username, password, domain):
        self.username = username.split('@')[0]
        self.password = password
        self.domain = domain
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            url = 'http://%s:9898/auth/signin' % self.domain
            login_data = urllib.urlencode({'address':self.username,
                                           'password':self.password,
                                           }
                                          )
            self.response = opener.open(url, login_data)
        except IOError, e:
            print "An Error occured when connecting to %s:" % self.domain, e
            raise ConnectionFailure("Could not connect to %s:\n" % self.domain)
        else:
            self.session_data = self.extract_session_data(self.response)
            self._session_id = self.session_data['id']
            self._session_address = self.session_data['address']
            self._session_domain = self.session_data['domain']
        finally:
            pass
    def _query(self, query, startpage):
        pass
    def _me(self):
        return User(name = self.username,
                    address = self._session_address,
                    avatar = 'http://wave.google.com/wave/static/images/unknown.jpg',
                    )
    def _contacts(self):
        return [self._me()]
    @classmethod
    def _accepts(cls):
        return cls._accept_dict
    def extract_session_data(self, response):
        response = response.read()
        print response
        response = response.split("var __session =")
        print response
        response = response[1]
        print response
        response = response.split(r";")
        print response
        response = response[0]
        print response
        response = eval(response)
        print response
        ##response = eval(response.split("var __session =")[1].split(";")[0])        
        return response
        
        
