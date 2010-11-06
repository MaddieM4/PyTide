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

__all__ = []

domain_mapping = {}

with open("./NetworkTools/plugins/domain_mapping.txt", "r") as f:

    for i in f.readlines():

        pair = i.split()
        domain_mapping[pair[0]] = (pair[1], pair[2])
        if pair[1] not in __all__:
            __all__.append(pair[1])
            
print __all__

def get_domain_connection(domain):
    if domain in domain_mapping:
        plugin_tuple = domain_mapping[domain]
        plugin_module = __import__("NetworkTools.plugins.%s" % plugin_tuple[0],
                                   fromlist = plugin_tuple[1])
        try:
            print plugin_module
            print plugin_tuple
            print dir(plugin_module)
            plugin = getattr(plugin_module, plugin_tuple[1])
        except AttributeError, e:
            print "AttributeError handled!"
            print "CONNECTION PLUGIN COULD NOT BE IMPORTED"
            plugin = False
    
        return plugin
    
    else:
        return False
