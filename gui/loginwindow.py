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
import json
from gui import rel_to_abs

class LoginWindow(webgui.browserWindow):
	def __init__(self, loginCallback, loginConfig):
		self.logins = loginConfig
		print self.logins
		webgui.browserWindow.__init__(self, 
			rel_to_abs('gui/html/loginwindow.html'), 
			None,size=(300,170),
			minsize=(300,150),
			echo=True)
		self.loginCallback = loginCallback
		self.setTitle("Log in to PyTide")

	def process(self, data):
		GA = self.logins.getAll()
		if data == None: return
		elif data['type'] == 'logindata':
			self.loginCallback(data['username'],data['password'])
		elif data['type'] == 'ready' and GA != {}:
			pairs = {'pairs':[(i,GA[i]) for i in GA]}
			self.send("setLogins('"+json.dumps(pairs)+"')")

	def setStatus(self, status):
		self.send("setStatus('%s');" % status.replace("'","\'"))

	def destroy(self, widget, event):
		print "Destroying the universe from the login window"
		quit()

	def hide(self):
		self.window.hide()
