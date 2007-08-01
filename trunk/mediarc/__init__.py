import sys
import mydom, remotes, interface



location = None



def run(the_loc):
	global location
	location = the_loc
	config = mydom.readNew("config")
	interface.init(config)
	remotes.init(config)
	interface.run()
	return
