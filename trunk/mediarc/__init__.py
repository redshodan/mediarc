import sys
import gtk
import mydom, remotes, interface, ctl



location = None



def run(the_loc):
	global location
	location = the_loc
	config = mydom.readNew("config")
	theme = config.getElem("config/theme")
	if theme and theme.getAttr("use-remotes") == "true":
		gtk.rc_parse("%s/share/themes/MediaRC/gtk-2.0/gtkrc" % location)
	ctl.init(config)
	interface.init(config)
	remotes.init(config)
	interface.run()
	return
