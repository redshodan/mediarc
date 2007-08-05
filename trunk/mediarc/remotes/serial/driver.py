import serial
from command import Command
import mediarc
from mediarc import mydom



class Driver(object):
	def __init__(self, cfg):
		self.cfg = cfg
		cfg.pullAttrs(self, ["name", "manufacturer", "model"])
		port = cfg.getElem("port")
		port.pullAttrs(self, ["timeout", "baudrate", "databits", "parity",
							  "stopbits", "xonxoff", "rtscts"])
		self.cmds = {}
		for elem in cfg.getElems("commands/command"):
			cmd = Command(elem)
			self.cmds[cmd.name] = cmd
		self.btns = {}
		for button in cfg.getElems("buttons/row/button"):
			name = button.getAttr("name")
			self.btns[name] = []
			for command in button.getElems("command"):
				self.btns[name].append(command.getAttr("name"))
		return


	def initSerial(self, device):
		if not device: device = "/dev/ttyS0"
		self.device = device
		if not self.timeout: self.timeout = 1
		if not self.baudrate: self.baudrate = 115200
		if not self.databits: self.databits = 8
		if not self.parity: self.parity = 'N'
		if not self.stopbits: self.stopbits = 1
		if not self.xonxoff: self.xonxoff = 0
		if not self.rtscts: self.rtscts = 0
		self.serial = serial.Serial()
		self.serial.port = self.device
		self.serial.timeout = int(self.timeout)
		self.serial.baudrate = int(self.baudrate)
		self.serial.bytesize = int(self.databits)
		self.serial.stopbits = int(self.stopbits)
		self.serial.parity = self.parity
		self.serial.xonxoff = int(self.xonxoff)
		self.serial.rtscts = int(self.rtscts)
		self.serial.open()
		return


	def send(self, cmd):
		self.serial.write(cmd.cmd)
		if cmd.readcnt:
			ret = self.serial.read(cmd.readcnt)
			if ret and ret in cmd.responses.keys():
				resp = cmd.responses[ret]
			elif not ret or ret == "":
				resp = cmd.responses[""]
			#self.gotResponseCB(self, cmd, resp)
			print "got response:", resp
		return


	def getDefaultBtnCfg(self):
		return self.cfg.getElem("buttons")


	def getBtnCmds(self, name):
		return self.cmds[name]



def load(manufacturer, model):
	path = "%s/share/drivers/serial/%s/%s.xml" % \
		   (mediarc.location, manufacturer, model)
	cfg = mydom.readNew(path)
	return Driver(cfg.getElem("driver"))
