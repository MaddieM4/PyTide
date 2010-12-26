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
	while True:
            threads_enter()
#	    logging.debug("LoopingThread")
	    self.process()
	    threads_leave()
	    time.sleep(self.speed)

    def process(self):
	pass # raise Exception("method 'process' not defined by subclass")
