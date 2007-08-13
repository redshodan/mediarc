import alsa, lirc, serial



remotes = {}
cur_remote = None
cur_snd_remote = None



def init(cfg):
	global remotes, cur_remote, cur_snd_remote
	for mod in [alsa, lirc, serial]:
		mod.init(cfg)
	for elem in cfg.getElems("remotes/remote"):
		remote = load(elem)
		if not len(remotes):
			cur_remote = remote
		remotes[remote.name] = remote
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
	return None


def selectRemote(name):
	global remotes, cur_remote
	cur_remote = remotes[name]
	return


def selectSndRemote(name):
	global remotes, cur_snd_remote
	cur_snd_remote = remotes[name]
	return
