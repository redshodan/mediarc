from types import *

import gtk
from mediarc import interface

SUPPORTED = False
try:
	import driver
	SUPPORTED = True
except:
	print "Failed to load pySerial module, skipping serial remotes"



class Serial(object):
	def __init__(self, cfg):
		self.cfg = cfg
		cfg.pullAttrs(self, ["name", "manufacturer", "model", "device"])
		try:
			self.driver = driver.load(self.manufacturer, self.model)
		except Exception, e:
			print "For remote %s, invalid manufacturer and model: %s %s" % \
				  (self.name, self.manufacturer, self.model)
			print e
			return
		try:
			self.driver.initSerial(self.device)
		except Exception, e:
			print "For remote %s, failed to initialize serial device: %s" % \
				  (self.name, str(e))
		self.btns = {}
		self.loadUI()
		return


	def loadUI(self):
		self.ui = interface.addRemote(self.name)
		cfg = self.cfg
		buttons = cfg.getElem("buttons")
		if not buttons:
			buttons = self.driver.getDefaultBtnCfg()
		for row in buttons.getElems("row"):
			for btn in row.getElems("button"):
				button = self.ui.addButton(btn, self.buttonCB)
				button.pyr_cmds = []
				for elem in btn.getElems("command"):
					cmd = self.driver.getBtnCmds(elem.getAttr("name"))
					if not cmd:
						print "Invalid command %s for button %s" % \
							  (cmd, button.pyr_name)
					else:
						button.pyr_cmds.append(cmd)
						self.btns[button.pyr_name] = button
			self.ui.addRow()
		return


	def buttonCB(self, button):
		print "Serial cb:", button.pyr_name
		for cmd in button.pyr_cmds:
			self.driver.send(cmd)
		if not len(button.pyr_cmds):
			print "Error. Button %s had no command set" % button.pyr_name
		return


	def doCmd(self, cmdstr):
		print "Serial doCmd:", cmdstr
		cmd = self.driver.getBtnCmds(cmdstr)
		self.driver.send(cmd)
		return



def init(cfg):
	return


def new(cfg):
	if SUPPORTED:
		return Serial(cfg)
	return None
