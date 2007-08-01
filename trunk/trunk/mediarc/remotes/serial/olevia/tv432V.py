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


power_on_resp = [
	[[0x06, 0x05, 0x90, 0x01, 0x9C], "on"],
	["", "off"]
	]

commands = [
	Command("power on", [0xF0, 0xF9, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
						 0x00, 0x08, 0xFF]),
	Command("power off", [0xBE, 0x05, 0x27, 0x00, 0xEA]),
	Command("mute", [0xBE, 0x05, 0x25, 0x09, 0xF1]),
	Command("1", [0xBE, 0x05, 0x25, 0x11, 0xF9]),
	Command("2", [0xBE, 0x05, 0x25, 0x12, 0xFA]),
	Command("3", [0xBE, 0x05, 0x25, 0x13, 0xFB]),
	Command("4", [0xBE, 0x05, 0x25, 0x14, 0xFC]),
	Command("5", [0xBE, 0x05, 0x25, 0x15, 0xFD]),
	Command("6", [0xBE, 0x05, 0x25, 0x16, 0xFE]),
	Command("7", [0xBE, 0x05, 0x25, 0x17, 0xFF]),
	Command("8", [0xBE, 0x05, 0x25, 0x18, 0x00]),
	Command("9", [0xBE, 0x05, 0x25, 0x19, 0x01]),
	Command("0", [0xBE, 0x05, 0x25, 0x10, 0xF8]),
	Command("return", [0xBE, 0x05, 0x25, 0x1A, 0x02]),
	Command("dash", [0xBE, 0x05, 0x25, 0x59, 0x41]),
	Command("mts", [0xBE, 0x05, 0x25, 0x40, 0x28]),
	Command("menu", [0xBE, 0x05, 0x25, 0x04, 0xEC]),
	Command("enter", [0xBE, 0x05, 0x25, 0x1B, 0x03]),
	Command("up", [0xBE, 0x05, 0x25, 0x45, 0x2D]),
	Command("down", [0xBE, 0x05, 0x25, 0x4A, 0x32]),
	Command("right", [0xBE, 0x05, 0x25, 0x07, 0xEF]),
	Command("left", [0xBE, 0x05, 0x25, 0x0A, 0xF2]),
	Command("favorite", [0xBE, 0x05, 0x25, 0x46, 0x2E]),
	Command("display", [0xBE, 0x05, 0x25, 0x1E, 0x06]),
	Command("vol+", [0xBE, 0x05, 0x25, 0x02, 0xEA]),
	Command("vol-", [0xBE, 0x05, 0x25, 0x03, 0xEB]),
	Command("chan+", [0xBE, 0x05, 0x25, 0x00, 0xE8]),
	Command("chan-", [0xBE, 0x05, 0x25, 0x01, 0xE9]),
	Command("source", [0xBE, 0x05, 0x25, 0x0B, 0xF3]),
	Command("tv", [0xBE, 0x05, 0x25, 0x0D, 0xF5]),
	Command("composite", [0xBE, 0x05, 0x25, 0x4D, 0x35]),
	Command("component", [0xBE, 0x05, 0x25, 0x49, 0x31]),
	Command("hdmi", [0xBE, 0x05, 0x25, 0x5D, 0x45]),
	Command("cc", [0xBE, 0x05, 0x25, 0x48, 0x30]),
	Command("aspect", [0xBE, 0x05, 0x25, 0x56, 0x3E]),
	Command("vgasync", [0xBE, 0x05, 0x25, 0x50, 0x38]),
	Command("lighting", [0xBE, 0x05, 0x25, 0x20, 0x08]),
	Command("time", [0xBE, 0x05, 0x25, 0x21, 0x09]),
	Command("sleep", [0xBE, 0x05, 0x25, 0x22, 0x0A]),
	Command("info", [0xBE, 0x05, 0x25, 0x23, 0x0B]),
	Command("vga", [0xBE, 0x05, 0x25, 0x0A, 0xF3]),
	Command("vgacomp", [0xBE, 0x05, 0x25, 0x0B, 0xF4]),
	Command("read power status", [0xBE, 0x05, 0x90, 0x00, 0x53], power_on_resp)
	]

defaultBtnCfg = """
<remote>
  <buttons>
    <row>
      <button name='power' type='power' x='0-8'/>
    </row>
    <row>
      <button name='1' type='number'/>
	  <button name='2' type='number'/>
	  <button name='3' type='number'/>
	</row>
	<row>
      <button name='4' type='number'/>
	  <button name='5' type='number'/>
	  <button name='6' type='number'/>
	</row>
    <row>
      <button name='7' type='number'/>
	  <button name='8' type='number'/>
	  <button name='9' type='number'/>
	</row>
  </buttons>
</remote>
"""



class tv432V(object):
	def __init__(self, cfg, serial):
		global commands
		self.serial = serial
		self.tv_powered = True
		self.tv_source = SRC_TUNER
		self.tv_muted = False
		self.tv_vol = 0
		self.serial.initSerial(cfg.getAttribute("device"), 1, 115200)
		self.serial.setCmds(commands)
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