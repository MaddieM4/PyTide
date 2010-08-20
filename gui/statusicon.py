import gtk

class StatusIcon(gtk.StatusIcon):
	def __init__(self, registry):
		gtk.StatusIcon.__init__(self)
		self.set_from_file("gui/html/img/something.jpg")
		self.registry = registry
		self.connect('popup-menu', self.on_right_click)
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

		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time,self)

	def on_right_click(self,data,event_button,event_time):
		allwins = self.registry.getAllWindows()
		openlist = []
		for win in allwins:
			openlist.append((win.getTitle(),self.focusWin,win))
		if openlist != []:
			openlist.append(())
		self.popupMenu(event_button, event_time, openlist+[
			('New WaveList window',self.newWaveList,None),
			('Quit',self.quit, None)
			])

	def focusWin(self, data=None):
		if data != None:
			data.focus()

	def quit(self, data=None):
		gtk.main_quit()

	def newWaveList(self, data=None):
		self.registry.newWaveList()
