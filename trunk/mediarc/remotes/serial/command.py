class Command(object):
	def __init__(self, cfg):
		self.name = cfg.getAttr("name")
		self.hexstr = cfg.get("send")
		self.cmd = ""
		for hex in self.hexstr.split(" "):
			self.cmd = "%s%c" % (self.cmd, int(hex, 0))
		self.responses = {}
		self.readcnt = 0
		#for response in responses:
		#	hexstr = ""
		#	for hex in response[0]:
		#		hexstr = "%s%c" % (hexstr, hex)
		#	self.responses[hexstr] = response[1]
		#	self.readcnt = len(hexstr)
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



