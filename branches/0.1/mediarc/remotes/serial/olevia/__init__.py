

def load(cfg, serial):
	model = cfg.getAttribute("model")
	if model == "432V":
		import tv432V
		return tv432V.new(cfg, serial)
	else:
		raise Exception("Invalid Olevia TV model: %s" % model)
	return
