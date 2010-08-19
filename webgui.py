import time
import Queue
import thread
import threading
import urllib
import json

import gtk
import gobject

try:
	import webkit
	weblib = "webkit"
except:
	try:
		import GtkMozEmbed
		weblib = "mozkit"
	except:
		weblib = None

if weblib == None:
	raise Exception("You don't have a supported browser kit. Try 'sudo apt-get install python-webkit' ")
	quit()

class WebkitMethods():

	@staticmethod
	def create_browser():
		return webkit.WebView()

	@staticmethod
	def inject_javascript(browser, script):
		browser.execute_script(script)

	@staticmethod
	def connect_title_changed(browser, callback):
		def callback_wrapper(widget, frame, title): callback(title)
		browser.connect('title-changed', callback_wrapper)

	@staticmethod
	def open_uri(browser, uri):
		browser.open(uri)

class MozkitMethods():

	@staticmethod
	def create_browser():
		return gtkmozembed.MozEmbed()

	@staticmethod
	def inject_javascript(browser, script):
		uri = 'javascript:%s' % urllib.quote(script +'\n;void(0)')
		browser.load_url(uri)

	@staticmethod
	def connect_title_changed(browser, callback):
		def callback_wrapper(*args): callback(browser.get_title())
		browser.connect('title', callback_wrapper)

	@staticmethod
	def open_uri(browser, uri):
		browser.load_url(uri)

if weblib == "webkit":
	implementation = WebkitMethods
else:
	implementation = MozkitMethods 

def async_gtk_message(func):
	def worker((function, args, kwargs)):
		apply(function, args, kwargs)
	
	def addworker(*args, **kwargs):
		gobject.idle_add(worker, (func, args, kwargs))

	return addworker

def sync_gtk_message(func):
	class NoResult: pass

	def worker((R, function, args, kwargs)):
		R.result = apply(function, args, kwargs)

	def addworker(*args, **kwargs):
		class R: result = NoResult
		gobject.idle_add(worker, (R, func, args, kwargs))
		while R.result is NoResult: time.sleep(0.01)
		return R.result

	return addworker

def start_gtk_thread():
	gtk.gdk.threads_init()
	threads.start_new_thread(gtk.main, ())

def kill_gtk_thread():
	async_gtk_message(gtk.main.quit)()

class browserWindow:

	def __init__(self, uri, registry, size=(300,600), echo=True):
		self.echo = echo
		self.registry = registry
		self.window = gtk.Window()
		self.browser = implementation.create_browser()

		box = gtk.VBox(homogeneous = False, spacing = 0)
		self.window.add(box)
		self.window.set_geometry_hints(min_width = 270, min_height=400)
		if self.echo:
			print "shrinkable: ", self.window.allow_shrink
			print "growable: ", self.window.allow_grow
		box.pack_start(self.browser, expand=True, fill=True, padding=0)

		self.window.set_default_size(size[0],size[1])
		self.window.show_all()

		#self.message_queue = Queue.Queue()

		def title_changed(title):
			if title != 'null':
				if self.echo: print "[T<<<",title
				self.process(json.loads(title))
			else: 
				if self.echo: print "recieved null"

		implementation.connect_title_changed(self.browser, title_changed)
		implementation.open_uri(self.browser, uri)

	def send(self, msg):
		if self.echo: print "[T>>>", msg
		async_gtk_message(implementation.inject_javascript)(self.browser, msg)

	def setTitle(self, newtitle):
		self.window.set_title(newtitle)

	def process(self, data):
		pass

	def regmsg_receive(self, data):
		pass
