import webgui
import json

from gui import rel_to_abs

class WaveList(webgui.browserWindow):
	def __init__(self,registry):
		webgui.browserWindow.__init__(self,rel_to_abs("gui/html/wavelist.html"),registry, echo=False)
		#self.query('in:inbox')

	def process(self, data):
		if data != None:
			if data['type'] == 'query':
				self.query(data['value'])
			elif data['type'] == 'sendHTML':
				print data['html']
			print data
		else:
			return None

	def regmsg_receive(self, data):
		print "smokebomb",data

	@staticmethod
	def escape(str):
		return str.replace('"','\"')

	def query(self, query):
		self.setTitle('Search "%s"' % query)
		results = self.registry.Network.query(query)
		jres = {'query':self.escape(query),'digests':[]}
		for digest in results.digests:
			plist = digest.participants.serialize()
			participants = [self.registry.Network.participantMeta(x) for x in plist]
			jres['digests'].append({
				'title':self.escape(digest.title),
				'participants':participants,
				'unread':digest.unread_count,
				'total':digest.blip_count,
				'date':digest.last_modified,
				})
		self.send("reloadList(%s)" % json.dumps(jres))
