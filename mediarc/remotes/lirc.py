import socket
import gtk
import mediarc
from mediarc import interface
from mediarc import mydom



lirc_sock = None



class LIRC(object):
	def __init__(self, cfg):
		self.cfg = cfg
		cfg.pullAttrs(self, ["name", "id"])
		if cfg.get("command"):
			self.cmd = cfg.get("command")
		else:
			self.cmd = "SEND_ONCE %n %v"
		self.ui = interface.addRemote(self.name, "normal")
		for row in cfg.getElems("buttons/row"):
			for btn in row.getElems("button"):
				self.ui.addButton(btn, self.buttonCB)
			self.ui.addRow()
		return


	def buttonCB(self, button):
		self.doCmd(button.mrc_id)
		return


	def doCmd(self, cmdstr):
		print "lirc doCmd:", cmdstr
		global lirc_sock
		cmd = self.cmd.replace("%n", self.id)
		cmd = cmd.replace("%v", cmdstr)
		print "LIRC command %s, running: %s" % (cmdstr, cmd)
		lirc_sock.send(cmd + "\n")
		return False


	def doContextArrow(self, name):
		return



def init(cfg):
	global lirc_sock
	scfg = cfg.getElem("drivers/driver=lirc")
	if not scfg:
		path = "%s/share/drivers/lirc.xml" % (mediarc.location)
		cfg = mydom.readNew(path)
		scfg = cfg.getElem("driver")
	sname = scfg.getAttr("socket")
	lirc_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	print "connecting to LIRCD at", sname
	try:
		lirc_sock.connect(sname)
	except Exception, e:
		print "Failed to connect to LIRCD:"
		print e
		return None
	return


def new(cfg):
	return LIRC(cfg)
