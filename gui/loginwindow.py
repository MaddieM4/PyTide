import webgui
import json
from gui import rel_to_abs

class LoginWindow(webgui.browserWindow):
	def __init__(self, loginCallback):
		try:
			savelist = open('savedlogins')
			logins = json.loads(savelist.read())
			savelist.close()
		except IOError:
			logins = {'pairs':[]}
		print logins
		webgui.browserWindow.__init__(self, 
			rel_to_abs('gui/html/loginwindow.html'), 
			None,size=(300,170),
			minsize=(300,150),
			echo=True)
		self.loginCallback = loginCallback
		self.setTitle("Log in to PyTide")
		if len(logins['pairs']) > 0:
			self.send("setLogins('"+json.dumps(logins)+"')")

	def process(self, data):
		if data != None and data['type'] == 'logindata':
			self.loginCallback(data['username'],data['password'])

	def setStatus(self, status):
		self.send("setStatus('%s');" % status.replace("'","\'"))

	def destroy(self, widget, event):
		print "Destroying the universe from the login window"
		quit()

	def hide(self):
		self.window.hide()
