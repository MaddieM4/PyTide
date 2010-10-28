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

from os import makedirs
import os.path

default_subfolders = ['cache', 
		'cache/outbound',
		'cache/contacts',
		'cache/documents',
		'attachments']

def validate_dir(path="~/.pytide/"):
	expanded = os.path.expanduser(path)
	if not os.path.isdir(expanded):
		os.makedirs(expanded)
	return expanded

def init_dir(path="~/.pytide/", subfolders = default_subfolders):
	expanded = validate_dir(path)
	for folder in subfolders:
		validate_dir(os.path.join(expanded,folder))
	return expanded
