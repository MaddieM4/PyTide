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
