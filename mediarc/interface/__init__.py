import gtk
from window import Window
from bindings import Bindings
from tv import TV
from statusicon import StatusIcon



win = None
bindings = None
tvs = {}
status = None



def init(cfg):
	global win, bindings, tvs, status
	bindings = Bindings(cfg)
	win = Window(cfg)
	win.initMenu()
	for elem in cfg.getElems("tv"):
		tv = TV(elem, win)
		tvs[tv.name] = tv
	win.initRemotes()
	status = StatusIcon(cfg, win)
	return


def addRemote(name):
	global win
	return win.addRemote(name)


def run():
	win.win.show()
	win.win.present()
	gtk.main()
	return
