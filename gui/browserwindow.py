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

import webgui

class BrowserWindow(webgui.browserWindow):
	def __init__(self, address, registry, destroyCallback=None):
		print "BrowserWindow.__init__(%s)" % address
		webgui.browserWindow.__init__(self, address, registry,size=(500,400),minsize=(300,200), echo=True)
		print "webgui.browserWindow.__init__ called with (",self,",",address,", ",registry,")"
		self.destroyCallback = destroyCallback

	def process(self, data=None):
		if data != None:
			self.setTitle(data)

	def destroy(self, widget,event):
		if self.destroyCallback != None:
			self.destroyCallback()
		return False
