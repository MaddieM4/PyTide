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

import NetworkTools
from persistance.config import Config
import persistance.cache

import threading
import Queue
from models import threads, operation, plugin
import json

import plugins

class PluginProxy(object):
    METHODS = ('_accepts',
               '_query',
               '_contacts',
               '_me',) + tuple(dir(plugin.Plugin))
    def __getattr__(self, attr):
        try:
            r = super(PluginProxy, self).__getattr__(attr)
        except AttributeError:
            if hasattr(self.__plugin, attr):
                return getattr(self.__plugin, attr)
            elif hasattr(self.__plugincls, attr):
                return getattr(self.__plugincls, attr)
            raise

    def __init__(self):
        self.__plugincls = None
        self.__connected = False
        self.hasplugincls = False
        
    def __call__(self, domain):
        try:
            self.__plugincls = plugins.get_plugin(domain)
            self.hasplugincls = True
        except Exception:
            print "Exception while getting plugin for %s" % domain
            print "Reraising from PluginProxy instance, method __call__"
            raise
               
    def connect(self, **kwargs):
        if not self.hasplugincls:
            raise Exception("PluginProxy 'connect' called before plugin established")
        else:
            plugincls = self.__plugincls
        if hasattr(plugincls, '_accepts'):
            plugin_args = self.__plugincls._accepts()
            for kw, arg in kwargs.items():
                if kw in plugin_args:
                    plugin_args[kw] = arg
            self.__plugin = plugincls(**plugin_args)
        else:
            print "Plugins are required to define _accepts"
            print "\t%s does not define _accepts" % plugincls
            raise NotImplementedError

class Network(threads.LoopingThread):
    '''The Network object is a thread, and it communicates between the connection plugin
    (also a thread) and the rest of the program. It holds the "official" version of every
    wavelet in its own memory.

    It handles the application of operations, notifying the appropriate objects in reg
    when stuff happens, and the management of connection plugins. '''

    def __init__(self, reg):
        super(Network, self).__init__(name="PyTideNetwork", speed=.1)
        self.registry = reg
        self.connection = PluginProxy()
        self._status = "No connection"
        self.wavelets = []
        self.contacts = []
        # start loading configs now. Let access block later if necessary
        self.savedlogins = Config(namespace="savedlogins")
        self.savedlogins.setAutoTimer(3)
        self.loginWindow = self.registry.newLoginWindow(self.connect, self.savedlogins)
        self.start()

    def process(self):
        if self.is_connected():
            pass
            #self.connection.sync()

    def query(self, wlcallback, query, startpage=0, errcallback=None):
        ''' External function - send a query to the plugin '''
        def callback(results):
            self._query(results, wlcallback)
        def err(e):
            self.plugin_error(e, errcallback)
        self.connection.query(query, startpage, callback, err)

    def _query(self, results, wlcallback):
        ''' Expects a models.SearchResults from the plugin '''
        self.registry.setIcon('active')
        wlcallback(results)

    def connect(self, username, password):
        print "Network connecting to %s" % username
        domain = username.split('@')[1]
        print 'About to get connection from plugins.'
        connection = PluginProxy(domain)
        print 'Got connection from plugins.'
        if self.connection.hasplugincls:
            try:
                self.status("Connecting to Server")
                self.connection.connect(username=username,
                                        password=password,
                                        domain=domain)
                self.status("Connected")
                self.loginWindow.hide()
                self.registry.newWaveList()
                self.saveLogin(username, password,)
                return True
            except NetworkTools.ConnectionFailure, e:
                self.status("Connection Failed - Your internet may be down or your login data incorrect")
                return False
            except IOError as e:
                self.status("IOError while connecting:\n\t" + str(e))
        else:
            self.status("No plugin found")

    def openURL(self, address, destroyCallback=None):
        print "Network.openURL(%s)" % address
        return self.registry.newBrowserWindow(address,destroyCallback=destroyCallback)

    def status(self, status_str):
        self._status = status_str
        if self.loginWindow != None:
            self.loginWindow.setStatus(self._status)
        print "Network status: %s" % self._status

    def is_connected(self):
        if self.connection == None:
            return False
        else:
            return True

    def participantMeta(self,address):
        ascii = ord(address.lower()[0])
        if ascii >=97 and ascii <= 122:
            avatar = "img/profile/"+address.lower()[0]+".jpg"
        else:
            avatar = "img/profile_base.png"
        return {'nick':address,
                'address':address,
                'avatar':avatar,
                }

    def saveLogin(self, uname, pword):
        self.savedlogins.set({uname:pword})

    def getContacts(self, callback, errcallback=None):
        '''Return a list of all your personal contacts.'''
        def err(e):
            self.plugin_error(e, errcallback)
        return self.connection.get_contacts(callback, err)

    def subscribe(doclocation):
        d = self.connection.subscribe(doclocation)
        self.documents.append(d)
        self.opqueues.append(models.OperationQueue(d))
        return d

    def unsubscribe(doclocation):
        for q in self.opqueues:
            if q.wavelet.location == doclocation:
                q.addOp(ops.CLOSE())
                return True
        return False

    def plugin_error(self, error, errcallback=None):
        print type(error)
        self.registry.setIcon('error')
        if errcallback != None:
            errcallback(error)
