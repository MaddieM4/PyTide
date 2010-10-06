# Copyright 2010 Nathanael Abbotts (nat.abbotts@gmail.com),
#                Philip Horger (campadrenalin@gmail.com),
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import threading
import time
import datetime
from gtk.gdk import threads_enter, threads_leave
from collections import deque

import logging
LOG_FILENAME="loopingthread.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# I will fill in more stuff here as I understand the scope of the requirements

class Operation:
	def __init__(self, timestamp=datetime.datetime.now()):
		pass

	def apply(document):
		pass		


class Operation_Queue(deque):
    """A queue of Operation objects

    When instantiating, you can provide any number of Operation instances as
    operations."""
    def __init__(self, *args, position = 0,): #(self, wavelet, *args, position)
        """Creates an Operation Queue.
        
        *args should all be Operation objects, which will be added to the queue
            in sequential order.
        """
        super(Operation_Queue, self).__init__(args)
        self.position = position
        # Note that this operation queue does not have a wavelet attribute - 
        # that is because I believe that a wavelet should have an opqueue, 
        # not the reverse. This will be discussed elsewhere though.
    def append(self, position, operation, arg):
        op = Operation(position, operation, arg)
        super(Operation_Queue, self).append(op)
    
# I'll be forking my blip models into here...
##class Blip:
##	pass
##
##class Wavelet:
##	def __init__(self, digest = None):
##		self.digest = digest
##
class Document:
	'''A simple class to store and easily pass around wave snapshots. It has no
	facilities to submit and recieve updates over the network, this is handled
	by the plugin.'''
	def __init__(self, id=None, jsonInput=None):
		# Create a new document
		self.wavelets = []
		self.properties = {}
		self.id = id or "unspecified"
		open('~/.pytide/document','w').write(jsonInput)

	def toJSON(self):
		pass

class Digest:
	def __init__(title, id, participants, blipsTotal, blipsUnread, date, folder=None,features=[]):
		self.title = title
		self.id = id
		self.participants = participants
		self.blipsTotal = blipsTotal
		self.blipsUnread = blipsUnread
		self.date = date
		self.folder = folder
		self.features = features

class User:
	'''Used for contacts and participants and such. '''
	def __init__(self, name="", nick="", address = None, avatar = None):
		self.name = name
		self.nick = nick
		self.addr = address
		self.pict = avatar

class LoopingThread(threading.Thread):
	'''This class allows you to make a thready object that calls
	its function on an infinite loop, automatically working with
	the gtk.gdk mutex. Please note that when you subclass this,
	as you are meant to do, you are going to overwrite the PROCESS
	function, not the RUN function.'''
	def __init__(self, name=None,speed=3):
		threading.Thread.__init__(self, name=name)
		self.setDaemon(True)
		self.speed=speed
		self.stopper = threading.Event()

	def run(self):
		while 1:
			threads_enter()
#			logging.debug("LoopingThread")
			self.process()
			threads_leave()
			time.sleep(self.speed)

	def process(self):
		pass

# This space left intentionally blank for subclassing
# Although a bit of example code is here to get you started
class Plugin(LoopingThread):
	def __init__(self, network):
		LoopingThread.__init__(self, name="PyTideNetworkPlugin", speed=0.5)
		self.opqueues = []
		self.network = network

	def process(self):
		'''Handles stuff internally.
 
		Do not modify external resources in process(), leave that to the
		other functions. You don't want to make the program unstable, do ya?'''
		pass

	def subscribe(self, waveid):
		'''Start loading a wave document into the network. Returns a mostly-blank
		document, but not before creating a personal opqueue for it.'''
		d = Document(id=waveid)
		self.opqueues.append(OperationQueue(d))
		# start loading in plugin thread, sync to documents when network calls getUpdates()
		return d

	def unsubscribe(self, waveid):
		for doc in self.network.documents:
			if doc.id == waveid: 
				del doc
				return True
		return False

	def getUpdates(self):
		'''Does not return anything, is called by network to sync internal data to Document objects'''
		pass

	def query(self, query):
		'''Returns a list of (title, id, participants, blip count, unread count, date) tuples'''
		pass

	def submit(self):
		'''Push all local operations to server.'''
		pass
