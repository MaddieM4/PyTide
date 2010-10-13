#
# Copyright Notice:
#
# Copyright 2010    Nathanael Abbotts (nat.abbotts@gmail.com),
#                   Philip Horger,
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
#

import threading
from gtk.gdk import threads_enter, threads_leave
import time

import wave

class LoopingThread(threading.Thread):
    '''This class allows you to make a thready object that calls
    its function on an infinite loop, automatically working with
    the gtk.gdk mutex. Please note that when you subclass this,
    as you are meant to do, you are going to overwrite the PROCESS
    function, not the RUN function.'''
    def __init__(self, name=None,speed=3):
    	super(LoopingThread, self).__init__(name=name)
    	self.setDaemon(True)
    	self.speed=speed
    	self.stopper = threading.Event()

    def run(self):
	while 1:
            threads_enter()
#	    logging.debug("LoopingThread")
	    self.process()
	    threads_leave()
	    time.sleep(self.speed)

    def process(self):
	pass

# This space left intentionally blank for subclassing
# Although a bit of example code is here to get you started
class Plugin(LoopingThread):
    def __init__(self, network):
	super(Plugin, self).__init__(name="PyTideNetworkPlugin", speed=0.5)
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
	d = wave.Document(id=waveid)
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
