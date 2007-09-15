import gtk
from about import About



toolbtns = [
	["context-vol+", "Vol+"], ["context-vol-", "Vol-"],
	["context-playpause", "Play/Pause"],
	["context-stop", "Stop"], ["context-forward", "Forward"],
	["context-reverse", "Reverse"]]



class Menu(object):
	def __init__(self, cfg, win):
		self.cfg = cfg
		self.win = win
		self.about = None
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
		self.makeItem("Exit", self.file, self.menuQuitCB)
		return

	def initView(self):
		view = self.makeItem("View", self.bar)
		self.view = self.makeSubMenu(view)
		self.makeItem("Single", self.view, self.selectViewCB, "single")
		self.makeItem("Tabbed", self.view, self.selectViewCB, "tabbed")
		#self.makeItem("Multiple", self.view, self.selectViewCB, "multiple")
		return


	def initRemotes(self):
		remotes = self.makeItem("Remotes", self.bar)
		self.remotes = self.makeSubMenu(remotes)
		return


	def makeSubMenu(self, parent):
		m = gtk.Menu()
		parent.set_submenu(m)
		return m


	def makeItem(self, name, parent, cb=None, param=None, accel=None):
		from mediarc import interface
		mi = gtk.MenuItem(name)
		parent.append(mi)
		mi.show()
		if cb:
			if param:
				mi.connect("activate", cb, param)
			else:
				mi.connect("activate", cb)
		if not accel and name in interface.bindings.menu.keys():
			accel = interface.bindings.menu[name]
		if accel:
			(keyval, modval) = gtk.accelerator_parse(accel)
			if not keyval:
				print "Failed to parse key binding:", accel
			else:
				mi.add_accelerator("activate", self.win.top_group, keyval,
								   modval, gtk.ACCEL_VISIBLE)
		return mi


	def addRemote(self, remote):
		self.remote_count = self.remote_count + 1
		self.makeItem(remote.name, self.remotes, self.selectRemoteCB,
					  remote.name, "<shift>F%d" % self.remote_count)
		return


	def initActions(self):
		from mediarc import interface
		actions= self.makeItem("Actions", self.bar)
		self.actions = self.makeSubMenu(actions)
		for toolbtn in toolbtns:
			tv = interface.tvs.values()[0]
			accel = None
			if toolbtn[0] in interface.bindings.toolbar.keys():
				accel = interface.bindings.toolbar[toolbtn[0]]
			self.makeItem(toolbtn[1], self.actions, tv.contextArrowCB,
						  toolbtn[0], accel)
		return


	def menuAboutCB(self, widget):
		if not self.about:
			self.about = About()
		self.about.win.present()
		return False


	def menuQuitCB(self, widget):
		gtk.main_quit()
		return False


	def selectRemoteCB(self, menu, name):
		print "selectRemoteCB", name
		self.win.selectRemote(name)
		return


	def selectViewCB(self, menu, name):
		print "selectViewCB", name
		self.win.selectView(name)
		return
