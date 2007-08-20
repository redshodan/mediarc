import gtk
import mediarc



about_text = \
"==========================\n\
MediaRC version __VERSION__"



class About(object):
	def __init__(self):
		self.win = gtk.Window()
		buff = gtk.TextBuffer()
		buff.set_text(about_text.replace("__VERSION__", mediarc.version))
		self.text = gtk.TextView(buff)
		self.text.set_justification(gtk.JUSTIFY_CENTER)
		self.text.set_cursor_visible(False)
		self.text.set_editable(False)
		self.text.set_border_width(10)
		self.close = gtk.Button("Close")
		self.close.connect("clicked", self.closeCB)
		vbox = gtk.VBox()
		self.win.add(vbox)
		vbox.pack_start(self.text, True, True)
		vbox.pack_end(self.close, True, False, 10)
		self.win.show_all()
		self.win.present()
		return


	def closeCB(self, btn):
		self.win.hide()
		return
