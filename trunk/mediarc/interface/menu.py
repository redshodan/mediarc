import gtk



class Menu(object):
	def __init__(self, cfg, win):
		self.cfg = cfg
		self.win = win
		self.remotes = {}
		self.top_group = gtk.AccelGroup()
		self.win.win.add_accel_group(self.top_group)
		self.bar = gtk.MenuBar()
		self.win.top_bin.pack_start(self.bar, False)
		self.bar.show()
		self.bar.set_pack_direction(gtk.PACK_DIRECTION_LTR)
		self.initFile()
		return


	def initFile(self):
		file = self.makeItem("File", self.bar)
		self.file = self.makeSubMenu(file)
		self.makeItem("About", self.file, self.menuAboutCB)
		self.makeItem("Exit", self.file, self.menuQuitCB, "<ctl>Q",
					  self.top_group)
		return


	def makeSubMenu(self, parent):
		m = gtk.Menu()
		parent.set_submenu(m)
		return m


	def makeItem(self, name, parent, cb=None, accel=None, group=None):
		mi = gtk.MenuItem(name)
		parent.append(mi)
		mi.show()
		if cb:
			mi.connect("activate", cb)
		if accel:
			(key, mod) = gtk.accelerator_parse(accel)
			mi.add_accelerator("activate", group, key, mod, gtk.ACCEL_VISIBLE)
		return mi


	def addRemote(self, name):
		remotes = self.makeItem(name, self.bar)
		self.remotes[name] = remotes = self.makeSubMenu(remotes)
		return


	def menuAboutCB(self, widget):
		print "AboutCB"
		return False


	def menuQuitCB(self, widget):
		gtk.main_quit()
		return False
