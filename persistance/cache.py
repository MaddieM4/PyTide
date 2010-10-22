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

import threading
import json
import persistance

class Cache:
	''' Base class for all caching mechanisms. '''
	pass

class DocumentCache(Cache):
	''' Cache for storing wave documents. '''
	pass

class UserCache(Cache):
	''' Cache for participant profiles, such as (but not limited to) your contacts.'''
	pass

class OutboundCache(Cache):
	''' A class for storing locally-generated operations until it's verified that
	the server has recieved them. In the event of a crash or internet outage,
	your data will be saved. In fact, you can even work with your waves offline,
	and your changes will simply be synced next time you get online.'''
	pass
