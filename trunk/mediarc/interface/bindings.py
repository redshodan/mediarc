import gtk
import mediarc
from mediarc import mydom



class Bindings(object):
	def __init__(self, cfg):
		self.cfg = cfg
		path = "%s/share/config/bindings.xml" % (mediarc.location)
		self.defcfg = mydom.readNew(path)
		self.globl = {}
		self.tmpls = {}
		self.load(self.defcfg)
		self.load(self.cfg)
		return


	def load(self, cfg):
		globl = cfg.getElem("bindings/global")
		if globl:
			self.loadInto(globl, self.globl)
		tmpls = cfg.getElem("bindings/remote-template")
		if tmpls:
			self.loadInto(tmpls, self.tmpls)
		return


	def loadInto(self, cfg, map):
		for binding in cfg.getElems("binding"):
			type = binding.getAttr("type")
			key = binding.getAttr("key")
			map[type] = key
		return

