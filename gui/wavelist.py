import webgui
import json

from gui import rel_to_abs

class WaveList(webgui.browserWindow):
	def __init__(self,registry):
		webgui.browserWindow.__init__(self,rel_to_abs("gui/html/wavelist.html"),registry, echo=False)
		self.setTitle('Search "in:inbox" 1-19 of 19')

	def process(self, data):
		if data != None:
			print data
		else:
			return None

	def regmsg_receive(self, data):
		print "smokebomb",data

	def query(self, query):
		results = self.registry.network.query(query)
		jres = json.loads(results)
		self.send("reloadList('"+jres+"')")

