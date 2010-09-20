import webgui
import json

from gui import rel_to_abs

class WaveList(webgui.browserWindow):
	def __init__(self,registry):
		webgui.browserWindow.__init__(self,rel_to_abs("gui/html/wavelist.html"),registry, echo=False)
		self.options = {
			'tbshorten':'autoshorten'
		}

	def process(self, data):
		if data != None:
			if data['type'] == 'query':
				self.query(data['value'])
			elif data['type'] == 'sendHTML':
				print data['html']
			elif data['type'] == 'getOptions':
				# Send a dict of all set options
				self.send("pushOptions(%s)" % json.dumps(self.options))
			elif data['type'] == 'setOption':
				# Future: pass on data to other windows and save to config
				pass
			print data
		else:
			return None

	def regmsg_receive(self, data):
		print "smokebomb",data

	@staticmethod
	def escape(str):
		return str.replace('"','\"')

	def getTitleFromQuery(self, querytext):
		if querytext == "in:inbox":
			return "Inbox"
		elif querytext == "in:all":
			return "Archive"
		elif querytext == "::contacts":
			return "Contacts"
		else: return 'Search "%s"' % querytext

	def query(self, query):
		if query == "": 
			query="in:inbox"
		self.setTitle(self.getTitleFromQuery(query))
		results = self.registry.Network.query(query)
		if "::contacts" in query:
			contacts = [{'name':c.name or c.nick,'address':c.addr,'avatar':c.pict} for c in self.registry.Network.getContacts()]
			self.send("contactsList(%s)" % json.dumps(contacts))
			return
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
