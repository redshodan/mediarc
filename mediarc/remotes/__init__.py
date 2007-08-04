import alsa, lirc, serial



def init(cfg):
	for mod in [alsa, lirc, serial]:
		mod.init(cfg)
	for elem in cfg.getElems("remotes/remote"):
		load(elem)
	return


def load(cfg):
	driver = cfg.getAttribute("driver")
	if driver == "alsa":
		import alsa
		return alsa.new(cfg)
	elif driver == "lirc":
		import lirc
		return lirc.new(cfg)
	elif driver == "serial":
		import serial
		return serial.new(cfg)
	else:
		raise Exception("Invalid remote driver: %s" % driver)
	return
