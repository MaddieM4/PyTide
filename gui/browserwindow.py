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
