import webgui
import json
from gui import rel_to_abs

class LoginWindow(webgui.browserWindow):
	def __init__(self, loginCallback):
		try:
			savelist = open('savedlogins')
			self.logins = json.loads(savelist.read())
			savelist.close()
		except IOError:
			self.logins = {'pairs':[]}
		print self.logins
		webgui.browserWindow.__init__(self, 
			rel_to_abs('gui/html/loginwindow.html'), 
			None,size=(300,170),
			minsize=(300,150),
			echo=True)
		self.loginCallback = loginCallback
		self.setTitle("Log in to PyTide")

	def process(self, data):
		if data == None: return
		elif data['type'] == 'logindata':
			self.loginCallback(data['username'],data['password'])
		elif data['type'] == 'ready' and len(self.logins['pairs']) > 0:
			self.send("setLogins('"+json.dumps(self.logins)+"')")

	def setStatus(self, status):
		self.send("setStatus('%s');" % status.replace("'","\'"))

	def destroy(self, widget, event):
		print "Destroying the universe from the login window"
		quit()

	def hide(self):
		self.window.hide()
