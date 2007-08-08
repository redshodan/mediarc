import gtk
from remote import Remote
from mediarc.interface.menu import Menu
from mediarc.interface.statusicon import StatusIcon



class Window(object):

	def __init__(self, cfg):
		self.cfg = cfg
		cfgwin = cfg.getElem("config/window")
		self.mode = cfgwin.getAttr("mode")
		if self.mode == "single":
			self.initSingle()
		elif self.mode == "tabbed":
			self.initTabbed()
		self.menu = Menu(cfg, self)
		self.status_icon = StatusIcon(cfg, self)
		return


	def addRemote(self, name):
		remote = Remote(name, self)
		if self.mode == "single":
			self.bin.attach(remote.frame, self.counter, self.counter + 1,
								  1, 2)
			self.counter = self.counter + 1
		elif self.mode == "tabbed":
			self.bin.append_page(remote.frame, gtk.Label(name))
		self.menu.addRemote(name)
		return remote


	def deleteEventCB(self, widget, event):
		gtk.main_quit()
		return False


	def initSingle(self):
		self.win = self.initWindow()
		self.bin = gtk.Table(1, len(self.cfg.getElems("remotes/remote")))
		self.bin.set_col_spacings(20)
		self.initBin()
		self.counter = 1
		return


	def initTabbed(self):
		self.win = self.initWindow()
		self.bin = gtk.Notebook()
		self.initBin()
		return


	def initMultiple(self):
		return


	def initBin(self):
		self.top_bin.pack_end(self.bin)
		self.bin.set_flags(gtk.CAN_DEFAULT)
		self.win.set_default(self.bin)
		self.bin.set_border_width(10)
		self.bin.show()
		return


	def initWindow(self, name=None):
		fullname = "MediaRC"
		if name:
			fullname = "%s: %s" % (fullname, name)
		win = gtk.Window()
		win.set_title(fullname)
		win.set_default_size(50, 50)
		win.set_resizable(True)
		win.connect("delete_event", self.deleteEventCB)
		win.show()
		self.top_bin = gtk.VBox()
		self.top_bin.show()
		win.add(self.top_bin)
		return win
