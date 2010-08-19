import webgui
import json
import os

def rel_to_abs(relpath):
	return os.path.abspath(os.path.join(os.curdir,relpath))

class WaveList(webgui.browserWindow):
	def __init__(self,registry):
		webgui.browserWindow.__init__(self, rel_to_abs("wavelist.html"),registry)
		self.setTitle('Search "in:inbox" 1-19 of 19')

	def process(self, data):
		if data != None:
			print data
		else:
			return None

	def regmsg_receive(self, data):
		print "smokebomb",data
