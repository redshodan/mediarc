import socket
import gtk
from mediarc import interface



lirc_sock = None



class LIRC(object):
	def __init__(self, cfg):
		self.cfg = cfg
		self.name = cfg.getAttribute("name")
		if cfg.get("command"):
			self.cmd = cfg.get("command")
		else:
			self.cmd = "SEND_ONCE %n %v"
		self.ui = interface.addRemote(self.name)
		for row in cfg.getElems("buttons/row"):
			for btn in row.getElems("button"):
				self.ui.addButton(btn, self.buttonCB)
			self.ui.addRow()
		return


	def buttonCB(self, button):
		global lirc_sock
		cmd = self.cmd.replace("%n", self.name)
		cmd = cmd.replace("%v", button.pyr_name)
		print "LIRC callback %s, running: %s" % (button.pyr_name, cmd)
		lirc_sock.send(cmd + "\n")
		return False



def new(cfg):
	global lirc_sock
	if not lirc_sock:
		lirc_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		print "connecting to LIRCD"
		try:
			lirc_sock.connect("/dev/lircd")
		except Exception, e:
			print "Failed to connect to LIRCD:"
			print e
			return None
	return LIRC(cfg)
