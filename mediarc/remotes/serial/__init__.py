from types import *

import gtk
from mediarc import interface

SUPPORTED = False
try:
	from driver import Driver
	SUPPORTED = True
except:
	print "Failed to load pySerial module, skipping serial remotes"



drivers = {}



class Serial(object):
	def __init__(self, cfg):
		global drivers
		self.cfg = cfg
		cfg.pullAttrs(self, ["name", "manufacturer", "model", "device"])
		try:
			self.driver = drivers[self.manufacturer][self.model]
		except:
			print "For remote %s, invalid manufacturer and model: %s %s" % \
				  (self.name, self.manufacturer, self.model)
			return
		try:
			self.driver.initSerial(self.device)
		except Exception, e:
			print "For remote %s, failed to initialize serial device: %s" % \
				  (self.name, str(e))
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
				#if button.pyr_name in self.cmds.keys():
				#	button.pyr_cmd = self.cmds[button.pyr_name]
				#else:
				#	button.pyr_cmd = None
				#self.driver.prepareBtn(button)
			self.ui.addRow()
		return


	def buttonCB(self, button):
		print "Serial cb:", button.pyr_name
		cmd = None
		if button.pyr_cmd:
			cmd = button.pyr_cmd
		else:
			cmd = self.driver.chooseCmd(button)
		if cmd:
			if type(cmd) == ListType:
				for c in cmd:
					c.send()
			else:
				cmd.send()
		else:
			print "Error. Button %s had no Command set" % button.pyr_name
		return



def init(cfg):
	global drivers
	for elem in cfg.getElems("drivers/driver=serial"):
		driver = Driver(elem)
		if not driver.manufacturer in drivers.keys():
			drivers[driver.manufacturer] = {}
		drivers[driver.manufacturer][driver.model] = driver
	return


def new(cfg):
	if SUPPORTED:
		return Serial(cfg)
	return None
