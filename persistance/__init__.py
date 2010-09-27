from os import mkdir
import os.path

def init_dir(path="~/.pytide/"):
	expanded = os.path.expanduser(path)
	if not os.path.isdir(expanded):
		os.makedirs(expanded)
	return expanded
