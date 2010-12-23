#           Licensed to the Apache Software Foundation (ASF) under one
#           or more contributor license agreements.  See the NOTICE file
#           distributed with this work for additional information
#           regarding copyright ownership.  The ASF licenses this file
#           to you under the Apache License, Version 2.0 (the
#           "License"); you may not use this file except in compliance
#           with the License.  You may obtain a copy of the License at

#             http://www.apache.org/licenses/LICENSE-2.0

#           Unless required by applicable law or agreed to in writing,
#           software distributed under the License is distributed on an
#           "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#           KIND, either express or implied.  See the License for the
#           specific language governing permissions and limitations
#           under the License.
from ..DNS.lazy import mxlookup
from NetworkTools import ConnectionFailure
__all__ = ['get_plugin', ]

domain_mapping = {}
protocol_mapping = {}
with open("./NetworkTools/plugins/domain_mapping.txt", "r") as f:
    for i in f.readlines():
        entry = i.split()
        domain_mapping[entry[0]] = entry[1]

with open("./NetworkTools/plugins/protocol_mapping.txt", "r") as f:
    for i in f.readlines():
        entry = i.split()
        if entry[0] in protocol_mapping:
            protocol_mapping[entry[0]].append(([entry[1], entry[2]]))
        else:
            protocol_mapping[entry[0]] = [(entry[1], entry[2])]
        if entry[1] not in __all__:
            __all__.append(entry[1])

def get_protocol(domain):
    """Attempt to identify the protocol used by domain"""
    # check if the domain has been used before (and if so return protocol used)
    if domain in domain_mapping:
        return domain_mapping[domain]
    # test for Google Wave Data API
    # runs an mx lookup, to check if the domain is an apps domain.
    for i in "nat":
        try:
            mx = mxlookup(domain)
        except DNSError, e:
            pass
        else:
            break
        if (i == 't') and (not mx):
            mx = []
    for pri, loc in mx:
        if loc.endswith("google.com"):
            protocol = "google_data"
            with open("./NetworkTools/plugins/domain_mapping.txt", "a") as f:
                f.write(' '.join((domain, protocol)))
            return protocol
    # no other tests known
    return False
    
def get_plugin(domain):
    protocol = get_protocol(domain)
    if not protocol:
        raise ConnectionFailure("Could not identify protocol")
    if protocol in protocol_mapping:
        for mod, cls in protocol_mapping[protocol]:
            try:
                ##plugin_module = __import__('..%s' % mod,
                ##                           fromlist = cls)
                exec('from %s import %s as plugin' % (mod, cls))
            except AttributeError, e:
                print "AttributeError:", e
            except ImportError, e:
                print "ImportError:", e
            else:
                return plugin
    # If no protocols could be found or imported:
    raise ConnectionFailure("No plugin available: protocol %s" % protocol)

# -------------------- FOLLOWING CODE DOESN'T WORK YET ------------------------
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
