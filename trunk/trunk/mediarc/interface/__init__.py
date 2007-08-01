import gtk
from window import Window



_win = None



def init(config):
	global _win
	_win = Window(config)
	return


def addRemote(name):
	global _win
	return _win.addRemote(name)


def run():
	_win.win.present()
	gtk.main()
	return
