class Command(object):
	def __init__(self, cfg):
		self.cfg = cfg
		self.name = cfg.getAttr("name")
		if not cfg.get("send"):
			print "Command %s is missing <send> tag" % self.name
			return
		self.cmd = ""
		for hex in cfg.get("send").split(" "):
			self.cmd = "%s%c" % (self.cmd, int(hex, 0))
		self.responses = {}
		self.readcnt = 0
		for response in cfg.getElems("response"):
			hexstr = ""
			for hex in response.getText().split(" "):
				if len(hex):
					hexstr = "%s%c" % (hexstr, int(hex, 0))
			self.responses[hexstr] = response.getAttr("name")
			self.readcnt = len(hexstr)
		return
