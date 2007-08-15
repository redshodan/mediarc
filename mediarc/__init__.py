import sys
import mydom, remotes, interface, ctl



location = None



def run(the_loc):
	global location
	location = the_loc
	config = mydom.readNew("config")
	ctl.init(config)
	interface.init(config)
	remotes.init(config)
	interface.run()
	return
