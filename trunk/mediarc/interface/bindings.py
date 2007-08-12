import mediarc
from mediarc import mydom



class Bindings(object):
	def __init__(self, cfg):
		self.cfg = cfg
		path = "%s/share/config/bindings.xml" % (mediarc.location)
		self.defcfg = mydom.readNew(path)
		self.menu = {}
		self.tmpls = {}
		self.load(self.defcfg)
		self.load(self.cfg)
		return


	def load(self, cfg):
		menu = cfg.getElem("bindings/menu")
		if menu:
			self.loadInto(menu, self.menu)
		tmpls = cfg.getElem("bindings/remote-template")
		if tmpls:
			self.loadInto(tmpls, self.tmpls)
		return


	def loadInto(self, cfg, map):
		for binding in cfg.getElems("binding"):
			type = binding.getAttr("type")
			key = binding.getAttr("key")
			name = binding.getAttr("name")
			if name:
				if not type in map.keys():
					map[type] = {}
				map[type][name] = key
			else:
				map[type] = key
		return
