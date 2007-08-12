import gtk



class Input(object):
	def __init__(self):
		return



class TV(object):
	def __init__(self, cfg, win):
		self.cfg = cfg
		self.win = win
		self.inputs = {}
		cfg.pullAttrs(self, ["name", "remote", "snd-remote"])
		self.addToolbar()
		for elem in cfg.getElems("input"):
			self.addInput(elem)
		return


	def addToolbar(self):
		self.bin = gtk.HBox()
		label = gtk.Label(self.name)
		label.show()
		self.bin.pack_start(label, False, False, 10)
		self.bar = gtk.Toolbar()
		self.bar.show()
		self.bin.pack_end(self.bar)
		self.bin.pack_end(gtk.HSeparator())
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
			btn.add_accelerator("clicked", self.win.top_group, keyval, modifier,
								gtk.ACCEL_VISIBLE)
		btn.show()
		self.bar.insert(btn, -1)
		return


	def inputCB(self, btn, input):
		print "inputCB", input.name
		from mediarc.remotes import remotes
		remote = remotes[self.remote]
		remote.doCmd(input.cmd)
		snd_remote = None
		if getattr(self, "snd-remote"):
			snd_remote = remotes[getattr(self, "snd-remote")]
		if getattr(input, "snd-remote"):
			snd_remote = remotes[getattr(input, "snd-remote")]
		if getattr(input, "snd-src"):
			snd_remote.setCurSrc(getattr(input, "snd-src"))
		if input.remote:
			remote = remotes[input.remote]
		self.win.selectRemote(remote.name)
		return
