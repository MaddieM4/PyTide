from os import makedirs
import os.path

default_subfolders = ['cache', 'cache/outbound',
		'contacts',
		'attachments']

def init_dir(path="~/.pytide/"):
	expanded = os.path.expanduser(path)
	if not os.path.isdir(expanded):
		os.makedirs(expanded)
	for folder in default_subfolders:
		if not os.path.isdir(os.path.join(expanded,folder)):
			os.makedirs(os.path.join(expanded,folder))
	return expanded
