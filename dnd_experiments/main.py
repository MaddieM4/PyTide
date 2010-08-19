import pygtk
pygtk.require('2.0')
import gtk

class WinMain:
	def pull(self, widget, drag_context):
		print "drag"

	def delete_event(self, widget, event, data=None):
		print "delete_event"
		return False

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window()
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.button = gtk.Button("Hello World")
		self.button.connect("drag_begin", self.pull)
		self.window.add(self.button)
		self.button.show()
		self.window.show()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	winmain = WinMain()
	winmain.main()
