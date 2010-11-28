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

import urllib
import urllib2
from cookielib import CookieJar

import websocket

from ..models import plugin
from ..models.user import User
from ..models.digest import Digest

from NetworkTools import ConnectionFailure

__all__ = ['WaveInABoxConnection']

# ----------------------- TEMP. MEASURE - AUTODISCOVERY SOON ------------------
DOMAINS_USING_PORTS = {'acmewave.com':':9898',
                       '86.14.183.107':'9898',
                       'nathanael':'9898'}
def get_port(domain):
    if domain in DOMAINS_USING_PORTS:
        return DOMAINS_USING_PORTS[domain]
    else:
        return str()
# -----------------------------------------------------------------------------
class WaveInABoxConnection(plugin.Plugin):
    _accept_dict = {'username':'',
                    'password':'',
                    'domain':'' ##'acmewave.com',
                    }
    
    def __init__(self, username, password, domain):
        self.username = username.split('@')[0]
        self.password = password
        self.domain = domain
        self.cookie_jar = CookieJar()
        try:
            # This 'opener' includes cookies as you'll need some sort of
            # ID from inside it.
            cp = urllib2.HTTPCookieProcessor(self.cookie_jar)
            opener = urllib2.build_opener(cp)
            # MESSY! Why do some wiab instances use :9898 and others not?
            url = 'http://%s%s/auth/signin' % (self.domain, get_port(domain))
            login_data = urllib.urlencode({'address':self.username,
                                           'password':self.password,
                                           }
                                          )
            self.response = opener.open(url, login_data)

        except IOError, e:
            print "An Error occured when connecting to %s:" % (self.domain)
            raise ConnectionFailure("Could not connect to %s:\n" % self.domain)
        else:
            print self.response_data
        finally:
            pass 
    def _query(self, query, startpage):
        print "QUERY!"
    def _me(self):
        print "ME!"
        return User(name = self.username,
                    address = self._session_address,
                    avatar = 'http://wave.google.com/wave/static/images/unknown.jpg',
                    )
    def _contacts(self):
        print "CONTACTS!"
        return list(self._me())
    @classmethod
    def _accepts(cls):
        return cls._accept_dict
    @property
    def response_data(self):
        if hasattr(self, '_response_data'):
            return self._response_data
        else:
            self._response_data = self.response.read()
            return self._response_data
    @property
    def session_data(self):
        if hasattr(self, '_session_data'):
            return self._session_data
        else:
            self._session_data = eval(str.split(str.split("var __session = ",
                                                          self.response_data)
                                                [1],
                                                ";"))
            assert isinstance(self._session_data, dict)
            return self._session_data
    @property
    def session_id(self):
        if hasattr(self, '_session_id'):
            return self._session_id
        else:
            self._session_id = self.session_data['id']
            return self._session_id
    @property
    def session_address(self):
        if hasattr(self, '_session_address'):
            return self._session_address
        else:
            self._session_address = self.session_data['address']
            return self._session_address
    @property
    def session_domain(self):
        if hasattr(self, '_session_domain'):
            return self._session_domain
        else:
            self._session_domain = self.session_data['domain']
            return self._session_domain
    @property
    def j_session_id(self):
        if hasattr(self, '_j_session_id'):
            return self._j_session_id
        else:
            for c_dict in self.cookie_jar._cookies.values():
                if '/' in d:
                    if 'JSESSIONID' in c_dict['/']:
                        self._j_session_id = c_dict['/']['JSESSIONID'].value
                        break
            return self._j_session_id
            
