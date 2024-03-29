import gtk, gobject
from remote import Remote
import mediarc
from mediarc.interface.menu import Menu


class Window(object):

	def __init__(self, cfg):
		self.cfg = cfg
		self.remotes = {}
		self.cur_remote = None
		self.cur_snd_remote = None
		self.icons_size = "large"
		self.win_mode = "single"
		self.loadConfig()
		self.initWindow()
		return


	def loadConfig(self):
		icons = self.cfg.getElem("config/icons")
		if icons and icons.getAttr("size"):
			self.icons_size = icons.getAttr("size")
		win = self.cfg.getElem("config/window")
		if win and win.getAttr("mode"):
			self.win_mode = win.getAttr("mode")
		return


	def initRemotes(self):
		if self.win_mode == "single":
			self.initSingle()
		elif self.win_mode == "tabbed":
			self.initTabbed()
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
		self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.win.set_title(fullname)
		self.win.set_icon_from_file("%s/icons/mediarc.png" % \
									(mediarc.location))
		self.win.set_default_size(50, 50)
		self.win.set_resizable(True)
		self.top_group = gtk.AccelGroup()
		self.win.add_accel_group(self.top_group)
		self.win.connect("delete_event", self.deleteEventCB)
		self.defSelectID = self.win.connect("map", self.defSelectCB)
		self.top_bin = gtk.VBox()
		self.top_bin.show()
		self.win.add(self.top_bin)
		return


	def initMenu(self):
		self.menu = Menu(self.cfg, self)
		return


	def deleteEventCB(self, widget, event):
		gtk.main_quit()
		return False


	def addRemote(self, name, type):
		remote = Remote(name, type, self)
		if self.win_mode == "single":
			self.bin.attach(remote.frame, self.counter, self.counter + 1,
								  1, 2)
			self.counter = self.counter + 1
		elif self.win_mode == "tabbed":
			self.bin.append_page(remote.frame, gtk.Label(name))
		self.menu.addRemote(remote)
		if not len(self.remotes):
			self.cur_remote = remote
			self.defremote = remote
		self.remotes[name] = remote
		return remote


	def selectRemote(self, name):
		for remote in self.remotes.itervalues():
			remote.unselect()
		self.cur_remote = self.remotes[name]
		self.cur_remote.select()
		return


	def selectSndRemote(self, name):
		self.cur_snd_remote = self.remotes[name]
		return


	def selectView(self, name):
		return


	def presentCB(self):
		print "Window.presentCB"
		#gtk.gdk.flush()
		#self.win.present()
		self.win.map()
		return False


	def defSelectCB(self, one):
		self.win.disconnect(self.defSelectID)
		gobject.idle_add(self.selectRemote, self.defremote.name)
		from mediarc import interface
		for key, tv in interface.tvs.iteritems():
			gobject.idle_add(tv.selectDefInput)
		return
