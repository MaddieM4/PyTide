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

import gtk
import time

import iconstates

class StatusIcon(gtk.StatusIcon):
	def __init__(self, registry):
		gtk.StatusIcon.__init__(self)
		self.setIconState(iconstates.ICON_ERROR)
		self.registry = registry
		self.registry.icon = self
		self.connect('popup-menu', self.on_right_click)
		self.connect('activate', self.on_left_click)
		gtk.main()

	def popupMenu(self, event_button, event_time, itemList=None):
		# Create and show the popup menu
		menu = gtk.Menu()

		for item in itemList:
			if len(item)==3:
				menuItem = gtk.MenuItem(item[0])
				menu.append(menuItem)
				menuItem.connect_object("activate",item[1],item[2])
				menuItem.show()
			else:
				# seperator
				menuItem = gtk.MenuItem()
				menu.append(menuItem)
				menuItem.show()
		menu.show()
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time,self)

	def on_right_click(self,data,event_button,event_time):
		allwins = self.registry.getAllWindows()
		openlist = []
		optionlist = []
		for win in allwins:
			openlist.append((win.getTitle(),self.focusWin,win))
		if openlist != []:
			openlist.append(())
		if self.registry.Network.is_connected():
			optionlist += [
				('New Inbox window',self.newWaveList,None),
				(),
				('Deflate',self.deflate, None)]
		else:
			login = self.registry.Network.loginWindow
			openlist += [(login.getTitle(),self.focusWin,login),()]

		self.popupMenu(event_button, event_time, openlist+optionlist+[
			('Quit',self.quit, None)] )

	def on_left_click(self,icon):
		if self.registry.Network.is_connected():
			popuplist = [('This is a blip (1)',self.newWaveViewer,None)]
#[('No updates',self.blank,None)]
		else:
			popuplist = [("You're not logged in.",self.blank,None)]
		self.popupMenu(1, gtk.get_current_event_time(),popuplist)

	def focusWin(self, data=None):
		if data != None:
			data.focus()

	def quit(self, data=None):
		gtk.main_quit()

	def deflate(self, data=None):
		self.registry.killAllWindows()

	def newWaveList(self, data=None):
		self.registry.newWaveList()

	def newWaveViewer(self, data=None):
		self.registry.newWaveViewer()

	def setIconState(self, iconpath):
		self.set_from_file(iconpath)

	def blank(self, data=None):
		pass
