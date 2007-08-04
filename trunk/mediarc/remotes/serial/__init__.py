from types import *

SUPPORTED = False
try:
	import serial
	SUPPORTED = True
except:
	print "Failed to load pySerial module, skipping serial remotes"

import gtk
from mediarc import interface
import olevia



class Command(object):
	def __init__(self, name, hexstr, responses = []):
		self.name = name
		self.hexstr = hexstr
		self.cmd = ""
		for hex in self.hexstr:
			self.cmd = "%s%c" % (self.cmd, hex)
		self.responses = {}
		self.readcnt = 0
		for response in responses:
			hexstr = ""
			for hex in response[0]:
				hexstr = "%s%c" % (hexstr, hex)
			self.responses[hexstr] = response[1]
			self.readcnt = len(hexstr)
		return


	def setSerial(self, serial):
		self.serial = serial
		return


	def send(self):
		self.serial.serial.write(self.cmd)
		if self.readcnt:
			ret = self.serial.serial.read(self.readcnt)
			if ret and ret in self.responses.keys():
				resp = self.responses[ret]
			elif not ret or ret == "":
				resp = self.responses[""]
			self.serial.driver.gotResponse(self, resp)
		return




class Serial(object):
	def __init__(self, cfg):
		self.cfg = cfg
		self.name = cfg.getAttribute("name")
		self.serial = None
		self.cmds = {}
		self.manufacturer = cfg.getAttribute("manufacturer")
		self.loadDriver()
		self.loadUI()
		return


	def loadDriver(self):
		if self.manufacturer == "olevia":
			self.driver = olevia.load(self.cfg, self)
		return


	def loadUI(self):
		self.ui = interface.addRemote(self.name)
		cfg = self.cfg
		buttons = cfg.getElem("buttons")
		if buttons.getAttribute("type") == "default":
			cfg = self.driver.getDefaultBtnCfg()
		for row in cfg.getElems("buttons/row"):
			for btn in row.getElems("button"):
				button = self.ui.addButton(btn, self.buttonCB)
				if button.pyr_name in self.cmds.keys():
					button.pyr_cmd = self.cmds[button.pyr_name]
				else:
					button.pyr_cmd = None
				self.driver.prepareBtn(button)
			self.ui.addRow()
		return


	def initSerial(self, port="/dev/ttyS0", timeout=1, baudrate=115200,
				   databits=8, parity='N', stopbits=1, xonxoff=0, rtscts=0):
		self.serial = serial.Serial()
		self.serial.port = port
		self.serial.timeout = timeout
		self.serial.baudrate = baudrate
		self.serial.bytesize = databits
		self.serial.stopbits = stopbits
		self.serial.parity = parity
		self.serial.xonxoff = xonxoff
		self.serial.rtscts = rtscts
		print "Serial settings:"
		print self.serial
		print "Opening serial port"
		self.serial.open()
		return


	def setCmds(self, cmds):
		for cmd in cmds:
			cmd.setSerial(self)
			self.cmds[cmd.name] = cmd
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



def new(cfg):
	if SUPPORTED:
		return Serial(cfg)
