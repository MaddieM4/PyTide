import threading
import json
from os.path import expanduser

from gtk.gdk import threads_enter, threads_leave

class NamespaceError(Exception):
	'''A pretty general error for issues with namespaces. It will probably
	be subclassed for specific errors later.'''
	def __init__(self,textdescription):
		self.description = str(textdescription)
	def __str__(self):
		return "NamespaceError: "+self.description

class Config:
	'''This is the class you should use to store and access data persistantly.

	Saving can be done manually, but doesn't have to. Autosaving is set 
	up like this:

		myconf.setAutoTimer(10)

	which sets a recurring timer to save 10 seconds after the last change
	to the data. This way quick multiple calls to set() don't have a huge
	overhead, but changes get autosaved quickly. An Autosave can be
	disabled again by using -1 as the argument to setAutoTimer.
	'''

	def __init__(self, data={}, namespace=None, onload=None, autosave=-1):
		'''Can be called without arguments, preloaded with options with the 
		data argument (which should be a dict), and/or give you a simple way
		to shortcut to the load function by providing a namespace (with 
		optional onload argument). Also includes an optional autosave argument
		which is analagous to the setAutoTimer() function.

		onload does nothing without a namespace argument, but is harmless. 
		The data argument takes precedence over filesystem loading. Config
		uses a threaded subclass for disk IO called ConfigRW, which assumes
		a gtk environment and therefore doesn't really test well if you aren't
		somewhere where you've already called gtk.gdk.threads_init() and 
		gtk.main(). This is also the reason for the callback system, which 
		will use instance or class context if the callback function belongs 
		to something specific like that, but it will run in the ConfigRW's
		thread. '''

		print "config.init"
		self.namespace = namespace
		self.lock = threading.Lock()
		self.autosave = None
		self.autosave_time = -1
		if namespace != None:
			self.load(namespace=namespace, action=onload)
		self.data={}
		self.set(data)

	def set(self, data):
		'''Set a value in storage. Does not save anything; for that, call save().'''
		print "acquiring lock for set"
		self.lock.acquire()
		print "setting ",data
		try:
			self._set(data)
			print "data set"
			if self.autosave_time >=0:
				print "setting autotimer"
				if self.autosave != None: self.autosave.cancel()
				self.autosave = threading.Timer(self.autosave_time, self.save)
				self.autosave.start()
				print "Autotimer: ", self.autosave
		finally:
			print "releasing lock for set"
			self.lock.release()

	def _set(self, data):
		'''Internal setter that bypasses thread locks. Do not use externally!'''
		for i in data:
			self.data[i] = data[i]

	def get(self, name):
		'''Access a stored value by its key.'''
		print "acquiring lock for get"
		self.lock.acquire()
		d = None
		try:
			d = self.data[name]
		finally:
			print "releasing lock for get"
			self.lock.release()
		return d

	def hasKey(self, key):
		'''Tests whether a key exists in a Config object.'''
		print "acquiring lock for hasKey"
		self.lock.acquire()
		d = key in self.data
		print "releasing lock for hasKey"
		self.lock.release()
		return d

	def getAll(self):
		'''Return all stored data in the form of a dict. Pretty simple right
		now since that's the way it's stored internally, but I'd rather not
		hard-code that and have people touching a Config instance in it's 
		private "self.data" places. Besides, it really screws with the mutexy
		stuff, which keeps our digital citizens safe during times of loading
		and saving.'''
		print "acquiring lock for getAll"
		self.lock.acquire()
		d = self.data
		print "releasing lock for getAll"
		self.lock.release()
		return d

	def load(self, namespace=None, action=None):
		'''Load from the config file. The config file is divided into namespaces,
		and you can only access one at a time, even though it's one file.

		The namespace argument is an override of self.namespace. If used, it will
		set self.namespace to the new value. If not, and self.namespace has never
		been set, a NamespaceError will be raised. The callback argument, "action",
		is completely optional, but useful because of the threaded nature of the
		ConfigRW backend.'''
		self.namespace = self.namespace or namespace
		if not self.namespace:
			raise NamespaceError("None Specified")
		if action != None:
			def whendone(self, data):
				self._set(data)
				action(self.data)
				print "releasing lock for load"
				self.lock.release()
		else:
			def whendone(self, data):
				self._set(data)
				print "releasing lock for load"
				self.lock.release()
		print "acquiring lock for load"
		self.lock.acquire()
		reader = ConfigRW(self.namespace,whendone,self)

	def save(self, namespace=None, context=None):
		'''Save config data to the disk. It's non-destructive, meaning
		that you can save an incomplete config and it will automagically
		merge with the existing config behind the scenes. However, it's
		also impossible to clear a namespace, resetting it to a default
		state (The system is designed to robustly assume a default value
		when no config data is present, which should result in the eventual
		repopulation of a complete conf file over time).

		Erasing to default is a planned feature that will be included in
		the Config class as the "bleach()" function. The functionality
		already exists in ConfigRW.'''
		ns = self.namespace or namespace
		print "saving",self.data, "to namespace", ns
		if ns == None:
			return False
		def whendone(self, data):
			for key in self.data:
				data[key] = self.data[key]
			self.lock.release()
			print "releasing lock for save"
			return data
		print "acquiring lock for save"
		self.lock.acquire()
		reader = ConfigRW(ns, whendone,self)

	def setAutoTimer(self,time):
		'''Sets the delay in seconds between the last set() call and an
		automatic call to save(). Will do nothing if Config object in 
		question doesn't have a namespace.'''
		self.autosave_time = time

class ConfigRW(threading.Thread):
	def __init__(self, namespace, action, context):
		threading.Thread.__init__(self)
		print "ConfigRW.init(",namespace,",",action,") ", threading.current_thread()
		self.namespace = namespace
		self.action = action
		self.context = context
		self.filename = expanduser("~/.pytide")
		self.start()

	def run(self):
		threads_enter()
		f = open(self.filename,'rw+')
		try:
			allconfig = json.loads(f.read())
		except:
			allconfig = {}
		if self.namespace in allconfig:
			results = self.action(self.context,allconfig[self.namespace])
		else:
			results = self.action(self.context,{})
		if results != None:
			f.seek(0)
			allconfig[self.namespace] = results
			f.write(json.dumps(allconfig))
			f.truncate()
		f.close()
		threads_leave()
