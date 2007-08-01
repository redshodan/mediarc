import re, commands, os, sys
import gtk
import mediarc
from mediarc import interface



LIMITS = re.compile("\s*Limits: Playback ([0-9]+) - ([0-9]+)")
LEFT = re.compile("\s*Front Left: Playback ([0-9]+) \\[[0-9]+\\%\\] [!(off|on)]*\\[(off|on)\\].*")
RIGHT = re.compile("\s*Front Right: Playback ([0-9]+) \\[[0-9]+\\%\\] [!(off|on)]*\\[(off|on)\\].*")



class Control(object):
	def __init__(self, name, step, ui, card):
		self.name = name
		self.step = step
		self.ui = ui
		self.card = card
		# amixer
		self.code = 0
		self.output = None
		self.limits = [None, None]
		self.left = None
		self.right = None
		# UI
		self.slider = None
		self.btn = None
		# fire it all up
		self.setup()
		return


	def setup(self):
		self.getValue()
		# button
		self.btn = gtk.Button()
		self.btn.set_use_stock(False)
		self.btn.connect("released", self.buttonCB)
		self.btn.show()
		# slider
		self.slider = self.ui.addSlider(self.name, self.sliderCB)
		self.slider.set_digits(0)
		self.slider.set_inverted(True)
		adj = self.slider.get_adjustment()
		val = float(self.left[0]) / float(self.limits[1]) * 100
		adj.set_all(val, 0, 100, float(self.step), float(self.step) * 2, 0)
		self.ui.table.attach(self.btn, self.slider.pyr_idx,
							 self.slider.pyr_idx + 1, self.ui.table_y + 1,
							 self.ui.table_y + 2, gtk.SHRINK, gtk.SHRINK)
		self.setValue(val)
		self.updateBtn()
		return



	def sliderCB(self, slider):
		self.setValue(slider.get_value())
		return


	def buttonCB(self, button):
		self.toggleMute()
		return


	def getValue(self):
		cmd = "amixer -c %s get %s" % (self.card, self.name)
		(self.code, self.output) = commands.getstatusoutput(cmd)
		if self.code != 0:
			print "Failed to get volume:"
			print self.output
			return
		for line in self.output.split("\n"):
			line = line.strip()
			if LIMITS.match(line):
				self.limits[0] = LIMITS.sub("\\1", line)
				self.limits[1] = LIMITS.sub("\\2", line)
			elif LEFT.match(line):
				val = LEFT.sub("\\1 \\2", line)
				self.left = val.split(" ")
			elif RIGHT.match(line):
				val = RIGHT.sub("\\1 \\2", line)
				self.right = val.split(" ")
		return


	def setValue(self, val):
		cval = ((float(self.limits[1]) - float(self.limits[0])) * (val / 100.0))
		cmd = "amixer -c %s set %s %s" % (self.card, self.name, cval)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			print "Failed to set volume:"
			print ret[1]
			return
		if self.slider.get_value() != val:
			self.slider.set_value(val)
		return


	def toggleMute(self):
		if self.left[1] == "off":
			val = "on"
		else:
			val = "off"
		cmd = "amixer -c %s set %s %s" % (self.card, self.name, val)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			print "Failed to toggle mute:"
			print ret[1]
			return
		self.left[1] = val
		self.updateBtn()
		return


	def updateBtn(self):
		if self.left[1] == "off":
			img = gtk.Image()
			img.set_from_file(mediarc.location + "/share/icons/muted.png")
			self.btn.set_image(img)
		else:
			img = gtk.Image()
			img.set_from_file(mediarc.location + "/share/icons/unmuted.png")
			self.btn.set_image(img)
		return



class ALSA(object):
	def __init__(self, cfg):
		self.cfg = cfg
		self.card = cfg.getAttribute("card")
		self.name = "card%s" % self.card
		self.ui = interface.addRemote(self.name)
		self.ctls = {}
		sources = cfg.getElems("source")
		self.ui.table.resize(len(sources), 1)
		for source in sources:
			name = source.getAttribute("name")
			step = source.getAttribute("step")
			if not step:
				step = 2
			print "adding", name, "step", step
			self.ctls[name] = Control(name, step, self.ui, self.card)
		return




def new(cfg):
	return ALSA(cfg)
