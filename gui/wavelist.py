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
		''' Recieve UI input data from window '''
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
		''' Recieve message from registry. '''
		print "smokebomb",data

	@staticmethod
	def escape(str):
		return str.replace('"','\"')

	def getTitleFromQuery(self, querytext):
		''' Pretty self-explanatory. Takes in a query, returns the appropriate window title for it.'''
		if querytext == "in:inbox":
			return "Inbox"
		elif querytext == "in:all":
			return "Archive"
		elif querytext == "::contacts":
			return "Contacts"
		else: return 'Search "%s"' % querytext

	def query(self, query):
		'''Send a query to the Network, get a list of results back, and pass it on to the window.'''
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
