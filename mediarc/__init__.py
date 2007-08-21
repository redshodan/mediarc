import sys
import gtk
import mydom, remotes, interface, ctl



location = None
version = None



def run(options):
	global location, version
	location = options.datadir
	version = options.version
	config = mydom.readNew(options.config)
	theme = config.getElem("config/theme")
	if ((not theme) or (theme and theme.getAttr("use-remotes") == "true")):
		gtk.rc_parse("%s/themes/MediaRC/gtk-2.0/gtkrc" % location)
	ctl.init(config)
	interface.init(config)
	remotes.init(config)
	interface.run()
	return
