import gtk



class Menu(object):
	def __init__(self, cfg, win):
		self.cfg = cfg
		self.win = win
		self.remote_count = 0
		self.bar = gtk.MenuBar()
		self.win.top_bin.pack_start(self.bar, False)
		self.bar.show()
		self.bar.set_pack_direction(gtk.PACK_DIRECTION_LTR)
		self.initFile()
		self.initView()
		self.initRemotes()
		return


	def initFile(self):
		file = self.makeItem("File", self.bar)
		self.file = self.makeSubMenu(file)
		self.makeItem("About", self.file, self.menuAboutCB)
		self.makeItem("Exit", self.file, self.menuQuitCB, None, "<ctl>Q",
					  self.win.top_group)
		return


	def initView(self):
		view = self.makeItem("View", self.bar)
		self.view = self.makeSubMenu(view)
		mode = self.makeItem("Mode", self.view)
		mode = self.makeSubMenu(mode)
		self.makeItem("Single", mode, self.selectViewCB, "single",
					  "<ctl>S", self.win.top_group)
		self.makeItem("Tabbed", mode, self.selectViewCB, "tabbed",
					  "<ctl>T", self.win.top_group)
		self.makeItem("Multiple", mode, self.selectViewCB, "multiple",
					  "<ctl>M", self.win.top_group)
		return


	def initRemotes(self):
		remotes = self.makeItem("Remotes", self.bar)
		self.remotes = self.makeSubMenu(remotes)
		return


	def makeSubMenu(self, parent):
		m = gtk.Menu()
		parent.set_submenu(m)
		return m


	def makeItem(self, name, parent, cb=None, param=None, accel=None,
				 group=None):
		mi = gtk.MenuItem(name)
		parent.append(mi)
		mi.show()
		if cb:
			if param:
				mi.connect("activate", cb, param)
			else:
				mi.connect("activate", cb)
		if accel:
			(key, mod) = gtk.accelerator_parse(accel)
			mi.add_accelerator("activate", group, key, mod, gtk.ACCEL_VISIBLE)
		return mi


	def addRemote(self, name):
		self.remote_count = self.remote_count + 1
		self.makeItem(name, self.remotes, self.selectRemoteCB, name,
					  "F%d" % self.remote_count, self.win.top_group)
		return


	def menuAboutCB(self, widget):
		print "AboutCB"
		return False


	def menuQuitCB(self, widget):
		gtk.main_quit()
		return False


	def selectRemoteCB(self, menu, name):
		self.win.selectRemote(name)
		return


	def selectViewCB(self, menu, name):
		print "selectViewCB", name
		self.win.selectView(name)
		return
