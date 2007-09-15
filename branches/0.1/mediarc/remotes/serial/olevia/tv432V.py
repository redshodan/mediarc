####
#### This definition should work for both Olevia 432 and 427 TVs. It has only
#### been tested on a 432 TV.
####


from mediarc.remotes.serial import Command
from mediarc import mydom


SRC_TUNER = 0
SRC_COMPOSITE = 1
SRC_SVIDEO = 2
SRC_COMPONENT = 3
SRC_HDMI = 4
SRC_VGA = 5
SRC_VGA_COMPONENT = 6



class tv432V(object):
	def __init__(self, cfg, serial):
		global commands
		self.serial = serial
		self.tv_powered = True
		self.tv_source = SRC_TUNER
		self.tv_muted = False
		self.tv_vol = 0
		#self.serial.initSerial(cfg.getAttribute("device"), 1, 115200)
		#self.serial.setCmds(commands)
		self.readState()
		return


	def readState(self):
		print "Reading TV state"
		return


	def getDefaultBtnCfg(self):
		return mydom.createFrom(defaultBtnCfg)


	def prepareBtn(self, btn):
		#if btn.pyr_name == "power":
		#	btn.pyr_cmd_on =
		return


	def gotResponse(self, cmd, resp):
		print "gotResponse", cmd, resp
		return


	def chooseCmd(self, button):
		if button.pyr_name == "power":
			if self.tv_powered:
				self.tv_powered = False
				return [self.serial.cmds["power off"],
						self.serial.cmds["read power status"]]
			else:
				self.tv_powered = True
				return [self.serial.cmds["power on"],
						self.serial.cmds["read power status"]]


def new(cfg, serial):
	return tv432V(cfg, serial)
