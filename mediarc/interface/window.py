import gtk
from remote import Remote
from mediarc.interface.menu import Menu
from mediarc.interface.statusicon import StatusIcon



class Window(object):

	def __init__(self, cfg):
		self.cfg = cfg
		self.remotes = {}
		self.icons_size = "large"
		self.win_mode = "single"
		self.loadConfig()
		self.initWindow()
		if self.win_mode == "single":
			self.initSingle()
		elif self.win_mode == "tabbed":
			self.initTabbed()
		self.menu = Menu(cfg, self)
		self.status_icon = StatusIcon(cfg, self)
		return


	def loadConfig(self):
		icons = self.cfg.getElem("config/icons")
		if icons and icons.getAttr("size"):
			self.icons_size = icons.getAttr("size")
		win = self.cfg.getElem("config/window")
		if win and win.getAttr("mode"):
			self.win_mode = win.getAttr("mode")
		return


	def initSingle(self):
		self.bin = gtk.Table(1, len(self.cfg.getElems("remotes/remote")))
		self.bin.set_col_spacings(20)
		self.initBin()
		self.counter = 1
		return


	def initTabbed(self):
		self.bin = gtk.Notebook()
		self.initBin()
		return


	def initBin(self):
		self.top_bin.pack_end(self.bin)
		self.bin.set_border_width(10)
		self.bin.show()
		return


	def initWindow(self, name=None):
		fullname = "MediaRC"
		if name:
			fullname = "%s: %s" % (fullname, name)
		self.win = gtk.Window()
		self.win.set_title(fullname)
		self.win.set_default_size(50, 50)
		self.win.set_resizable(True)
		self.top_group = gtk.AccelGroup()
		self.win.add_accel_group(self.top_group)
		self.win.connect("delete_event", self.deleteEventCB)
		#self.defSelectID = self.win.connect("map", self.defSelectCB)
		self.top_bin = gtk.VBox()
		self.top_bin.show()
		self.win.add(self.top_bin)
		return


	def deleteEventCB(self, widget, event):
		gtk.main_quit()
		return False


	def addRemote(self, name):
		remote = Remote(name, self)
		if self.win_mode == "single":
			self.bin.attach(remote.frame, self.counter, self.counter + 1,
								  1, 2)
			self.counter = self.counter + 1
		elif self.win_mode == "tabbed":
			self.bin.append_page(remote.frame, gtk.Label(name))
		self.menu.addRemote(remote)
		if not len(self.remotes):
			self.defremote = remote
		self.remotes[name] = remote
		return remote


	def selectRemote(self, name):
		for remote in self.remotes.itervalues():
			remote.unselect()
		self.remotes[name].select()
		return


	def selectView(self, name):
		return


	def defSelectCB(self, one):
		print "defSelectCB"
		self.win.disconnect(self.defSelectID)
		self.selectRemote(self.defremote.name)
		return
