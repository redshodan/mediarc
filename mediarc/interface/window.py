import gtk
from remote import Remote



class Window(object):

	def __init__(self, cfg):
		self.cfg = cfg
		cfgwin = cfg.getElem("config/window")
		self.mode = cfgwin.getAttr("mode")
		if self.mode == "single":
			self.initSingle()
		elif self.mode == "tabbed":
			self.initTabbed()
		return


	def addRemote(self, name):
		remote = Remote(name, self)
		if self.mode == "single":
			self.container.attach(remote.frame, self.counter, self.counter + 1,
								  1, 2)
			self.counter = self.counter + 1
		elif self.mode == "tabbed":
			self.container.append_page(remote.frame, gtk.Label(name))
		return remote


	def deleteEvent(self, widget, event):
		gtk.main_quit()
		return False


	def initSingle(self):
		self.win = self.initWindow()
		self.container = gtk.Table(1, len(self.cfg.getElems("remotes/remote")))
		self.container.set_col_spacings(20)
		self.initContainer()
		self.counter = 1
		return


	def initTabbed(self):
		self.win = self.initWindow()
		self.container = gtk.Notebook()
		self.initContainer()
		return


	def initMultiple(self):
		return


	def initContainer(self):
		self.win.add(self.container)
		self.container.set_flags(gtk.CAN_DEFAULT)
		self.win.set_default(self.container)
		self.container.show()
		return


	def initWindow(self, name=None):
		fullname = "MediaRC"
		if name:
			fullname = "%s: %s" % (fullname, name)
		win = gtk.Window()
		win.set_title(fullname)
		win.set_default_size(50, 50)
		win.set_resizable(True)
		win.set_border_width(10);
		win.connect("delete_event", self.deleteEvent)
		return win


	def initAccels(self):
		agrp = gtk.AccelGroup()
		self.win.add_accel_group(agrp)
		self.global_btn = gtk.Button("global")
		self.global_btn.connect("clicked", self.globalBtnClickedCB)
		self.table.attach(self.global_btn, 0, 1, 0, 1)
		self.global_btn.hide()
		self.global_btn.add_accelerator("clicked", agrp, ord('P'),
										gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		return


	def globalBtnClickedCB(self, button):
		print "globalBtnClickedCB"
		self.win.present()
		return
