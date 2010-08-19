import os

def rel_to_abs(relpath):
	print __file__
	return os.path.abspath(os.path.join(os.curdir,relpath))
