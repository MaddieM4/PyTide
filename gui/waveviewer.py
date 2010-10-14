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

class WaveViewer(webgui.browserWindow):
	def __init__(self, registry):
		webgui.browserWindow.__init__(self,
			rel_to_abs("gui/html/waveviewer.html"),
			registry, 
			size=(700,800),
			minsize=(300,300),
			echo=False)
		self.setTitle("WaveViewer (demo)")

	def process(self, data):
		if data != None:
			if data['type'] == 'sendHTML':
				print data['html']
			print data
		else:
			return None

	def regmsg_receive(self, data):
		print "smokebomb",data

	@staticmethod
	def escape(str):
		return str.replace('"','\"')
