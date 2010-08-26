# Model stuff has been moved to models.py
# Plugin base class will be in models.py as well
# Network object can be found in network.py

class ConnectionFailure(IOError):
	'''An error to be raised when the initialization process of a Network plugin fails.'''
	def __init__(self, reason, httpcode=None):
		self.httpcode = httpcode
		self.reason = reason
	def __str__(self):
		return "Connection error: %s - Code %s" % (self.reason, self.httpcode)
