import threading
import json
from os.path import expanduser

from gtk.gdk import threads_enter, threads_leave

class Config:
	def __init__(self, data={}, namespace=None, onload=None):
		self.namespace = namespace
		if namespace != None:
			self.load(namespace=namespace, action=onload)
		self.data={}
		self.set(data)

	def set(self, data):
		for i in data:
			self.data[i] = data[i]

	def get(self, name):
		return data[name]

	def load(self, namespace=None, action=None):
		self.namespace = self.namespace or namespace
		if action != None:
			def whendone(data):
				self.set(data)
				action(self.data)
		else:
			def whendone(data):
				self.set(data)
		reader = ConfigRW(self.namespace, whendone)

	def save(self, namespace=None):
		ns = self.namespace or namespace
		if ns == None:
			return False
		def whendone(data):
			for key in self.data:
				data[key] = self.data[key]
			return data
		reader = ConfigRW(namespace, whendone)

class ConfigRW(threading.Thread):
	def __init__(self, namespace, action):
		threading.Thread.__init__(self)
		self.namespace = namespace
		self.action = action
		self.filename = expanduser("~/.pytide")
		self.start()

	def run(self):
		threads_enter()
		try:
			f = open(self.filename,'rw+')
			allconfig = json.loads(f.read())
		except:
			open(self.filename,'w').close()
			f = open(self.filename,'w')
			allconfig = {self.namespace:{}}
		results = self.action(allconfig[self.namespace])
		if results != None:
			f.truncate(0)
			f.write(json.dumps(results))
		f.close()
		threads_leave()
