import sys
import gtk
import mydom, remotes, interface, ctl



location = None



def run(options):
	global location
	location = options.datadir
	config = mydom.readNew(options.config)
	theme = config.getElem("config/theme")
	if theme and theme.getAttr("use-remotes") == "true":
		gtk.rc_parse("%s/themes/MediaRC/gtk-2.0/gtkrc" % location)
	ctl.init(config)
	interface.init(config)
	remotes.init(config)
	interface.run()
	return
