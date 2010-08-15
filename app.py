import webgui
import os

def rel_to_abs(relpath):
	return os.path.abspath(os.path.join(os.curdir,relpath))

class WaveList(webgui.browserWindow):
	def __init__(self):
		webgui.browserWindow.__init__(self, rel_to_abs("wavelist.html"))
		self.setTitle('Search "in:inbox" 1-19 of 19')

ListWindow = WaveList()

z = raw_input("Press Enter (or any other key, really) to quit.")
