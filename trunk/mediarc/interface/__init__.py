import gtk
from window import Window
from bindings import Bindings



win = None
bindings = None



def init(config):
	global win, bindings
	win = Window(config)
	bindings = Bindings(config)
	return


def addRemote(name):
	global win
	return win.addRemote(name)


def run():
	win.win.present()
	gtk.main()
	return
