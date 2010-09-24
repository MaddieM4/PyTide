import webgui
import json

from gui import rel_to_abs

class WaveList(webgui.browserWindow):
	def __init__(self,registry):
		webgui.browserWindow.__init__(self,rel_to_abs("gui/html/wavelist.html"),registry, echo=False)
		self.options = {}
		self.getConfig('tbshorten')

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
				# pass on data to other windows and save to config
				self.setConfig(data['key'],data['value'])
			print data
		else:
			return None

	def regmsg_receive(self, data):
		''' Recieve message from registry. '''
		if 'type' in data:
			if data['type'] == 'setOption':
				self.send("pushOption('%s','%s')" % (data['name'],data['value']))
		print "Reg >> Wavelist: ",data

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

	def getConfig(self,key):
		self.options[key] = self.registry.getWaveListConfig(key)
		self.send('pushOption("%s","%s")' % (key,self.options[key]))

	def setConfig(self,key, value=None):
		if value != None:
			self.options[key]=value
		self.registry.setWaveListConfig(key, self.options[key])
