import gtk



toolbtns = [
	["context-left", gtk.STOCK_GO_BACK], ["context-up", gtk.STOCK_GO_UP],
	["context-down", gtk.STOCK_GO_DOWN],
	["context-right", gtk.STOCK_GO_FORWARD]]



class Input(object):
	def __init__(self):
		return



class TV(object):
	def __init__(self, cfg, win):
		self.cfg = cfg
		self.win = win
		self.inputs = {}
		cfg.pullAttrs(self, ["name", "remote", "snd-remote", "default-input"])
		self.addToolbar()
		for elem in cfg.getElems("input"):
			self.addInput(elem)
		#self.addContextArrows()
		return


	def addToolbar(self):
		self.bin = gtk.HBox()
		#label = gtk.Label(self.name + ":")
		#label.show()
		#self.bin.pack_start(label, False, False, 10)
		self.bar = gtk.Toolbar()
		self.bar.show()
		self.bin.pack_end(self.bar)
		#self.bin.pack_end(gtk.HSeparator())
		self.win.top_bin.pack_start(self.bin)
		self.bin.show()
		return


	def addInput(self, cfg):
		input = Input()
		cfg.pullAttrs(input, ["name", "cmd", "snd-src", "remote",
							  "snd-remote", "key"])
		self.inputs[input.name] = input
		btn = gtk.ToolButton(None, input.name)
		btn.connect("clicked", self.inputCB, input)
		if input.key:
			(keyval, modifier) = gtk.accelerator_parse(input.key)
			if not keyval:
				print "Failed to parse key binding:", input.key
			else:
				btn.add_accelerator("clicked", self.win.top_group, keyval,
									modifier, gtk.ACCEL_VISIBLE)
		btn.show()
		self.bar.insert(btn, -1)
		return


	def addContextArrows(self):
		from mediarc import interface
		sep = gtk.SeparatorToolItem()
		sep.set_draw(True)
		sep.show()
		self.bar.insert(sep, -1)
		for toolbtn in toolbtns:
			img = gtk.Image()
			img.set_from_stock(toolbtn[1], gtk.ICON_SIZE_BUTTON)
			img.show()
			btn = gtk.ToolButton()
			btn.set_icon_widget(img)
			btn.connect("clicked", self.contextArrowCB, toolbtn[0])
			if toolbtn[0] in interface.bindings.toolbar.keys():
				accel = interface.bindings.toolbar[toolbtn[0]]
				(keyval, modifier) = gtk.accelerator_parse(accel)
				if not keyval:
					print "Failed to parse key binding:", accel
				else:
					btn.add_accelerator("clicked", self.win.top_group, keyval,
										modifier, gtk.ACCEL_VISIBLE)
			btn.set_flags(btn.flags() | gtk.CAN_DEFAULT)
			btn.show()
			self.bar.insert(btn, -1)
		return


	def selectDefInput(self):
		if getattr(self, "default-input"):
			self.selectInput(getattr(self, "default-input"))
		return


	def selectInput(self, name):
		input = self.inputs[name]
		from mediarc import remotes
		remote = remotes.remotes[self.remote]
		remote.doCmd(input.cmd)
		snd_remote = None
		if getattr(self, "snd-remote"):
			snd_remote = remotes.remotes[getattr(self, "snd-remote")]
		if getattr(input, "snd-remote"):
			snd_remote = remotes.remotes[getattr(input, "snd-remote")]
		if getattr(input, "snd-src"):
			snd_remote.setCurSrc(getattr(input, "snd-src"))
			remotes.selectSndRemote(snd_remote.name)
		if input.remote:
			remote = remotes.remotes[input.remote]
		self.win.selectRemote(remote.name)
		remotes.selectRemote(remote.name)
		return


	def inputCB(self, btn, input):
		print "inputCB", input.name
		self.selectInput(input.name)
		return


	def contextArrowCB(self, btn, name):
		print "contextArrowCB", name
		from mediarc import remotes
		if name == "context-vol+" and remotes.cur_snd_remote:
			remotes.cur_snd_remote.incCurSrc()
		elif name == "context-vol-" and remotes.cur_snd_remote:
			remotes.cur_snd_remote.decCurSrc()
		else:
			remotes.cur_remote.doContextArrow(name)
		return
