import gtk
from remote import Remote



class Window(object):

	def __init__(self, config):
		self.win = gtk.Window()

		# Window setup
		self.win.set_title("MediaRC")
		self.win.set_default_size(300, 300)
		self.win.set_resizable(True)
		self.win.set_border_width(10);
		self.win.connect("delete_event", self.deleteEvent)

		# Table setup
		
		self.table = gtk.Table(1, len(config.getElems("remotes/remote")))
		self.win.add(self.table)
		self.table.set_flags(gtk.CAN_DEFAULT)
		self.table.set_col_spacings(20)
		self.win.set_default(self.table)
		self.table.show()

		self.counter = 1
		return


	def addRemote(self, name):
		remote = Remote(name, self)
		self.table.attach(remote.frame, self.counter, self.counter + 1, 1, 2)
		self.counter = self.counter + 1
		return remote


	def deleteEvent(self, widget, event):
		gtk.main_quit()
		return False
