import gtk, gobject
import mediarc



class Remote(object):

	def __init__(self, name, win, rows=10, cols=10):
		self.name = name
		self.win = win
		self.defwidget = None
		self.selected = True
		self.accels = gtk.AccelGroup()
		self.win.win.add_accel_group(self.accels)
		self.table_x = 0
		self.table_y = 0
		# Table setup
		self.table = gtk.Table(rows, cols, False)
		self.table.set_row_spacings(10)
		self.table.set_border_width(10)
		self.table.show()
		# Frame setup
		self.frame = gtk.Frame(name)
		self.frame.add(self.table)
		self.frame.set_label_align(0.5, 0.5)
		self.frame.set_shadow_type(gtk.SHADOW_NONE)
		self.frame.show()
		return


	def addRow(self):
		self.table_x = 0
		self.table_y = self.table_y + 1
		return


	def addButton(self, cfg, cb):
		name = cfg.getAttribute("name")
		xa = cfg.getAttribute("colspan")
		x = [-1, -1]
		if xa:
			x = xa.split("-")
		ya = cfg.getAttribute("rowspan")
		y = [-1, -1]
		if ya:
			y = ya.split("-")
		if xa or ya:
			button = self.addButtonFull(name, cb, int(x[0]), int(x[1]),
										int(y[0]), int(y[1]))
		else:
			button = self.addButtonAuto(name, cb)
		type = cfg.getAttribute("type")
		if type and len(type):
			self.mapStock(button, type, name)
		self.setBtnAccel(cfg, button)
		if not self.defwidget:
			self.defwidget = button
		return button


	def addButtonAuto(self, name, cb):
		btn = gtk.Button(name)
		btn.pyr_name = name
		btn.connect("clicked", cb)
		btn.set_flags(gtk.CAN_DEFAULT | gtk.CAN_FOCUS)
		btn.set_focus_on_click(True)
		self.table.attach(btn, self.table_x, self.table_x + 1, self.table_y,
						  self.table_y + 1, gtk.FILL, gtk.FILL)
		self.table_x = self.table_x + 1
		btn.show()
		return btn


	def addButtonFull(self, name, cb, x1, x2, y1=-1, y2=-1, xop=gtk.FILL,
					  yop=gtk.FILL):
		btn = gtk.Button(name)
		btn.pyr_name = name
		btn.connect("clicked", cb)
		if x1 == -1:
			x1 = self.table_x
			x2 = self.table_x + 1
		if y1 == -1:
			y1 = self.table_y
			y2 = self.table_y + 1
		self.table.attach(btn, x1, x2, y1, y2, xop, yop)
		self.table_x = x2
		self.table_y = y1
		btn.show()
		return btn


	def setBtnAccel(self, cfg, btn):
		from mediarc import interface
		key = cfg.getAttr("key")
		type = cfg.getAttr("type")
		accel = None
		if not key and not type:
			return
		elif not key and type in interface.bindings.tmpls.keys():
			accel = interface.bindings.tmpls[type]
		elif key:
			accel = key
		if accel:
			(keyval, modifier) = gtk.accelerator_parse(accel)
			btn.add_accelerator("clicked", self.accels, keyval, modifier,
								gtk.ACCEL_VISIBLE)
		return


	def addSlider(self, name, cb):
		adj = gtk.Adjustment(0, 0, 100, 1, 5, 0)
		slider = gtk.VScale(adj)
		slider.set_value_pos(gtk.POS_BOTTOM)
		slider.connect("value-changed", cb)
		frame = gtk.Frame(name)
		frame.add(slider)
		self.frame.set_label_align(0.5, 0.5)
		frame.show()
		self.table.attach(frame, self.table_x, self.table_x + 1, self.table_y,
						  self.table_y + 1)
		slider.show()
		slider.pyr_name = name
		slider.pyr_idx = self.table_x
		self.table_x = self.table_x + 1
		if not self.defwidget:
			self.defwidget = slider
		return slider


	def mapStock(self, btn, type, name):
		stock = None
		img = gtk.Image()
		label = ""
		if type == "power":
			return
		elif type == "number":
			img.set_from_file("%s/share/icons/%s/%s.png" % \
							  (mediarc.location, self.win.icons_size, name))
		elif type == "pause":
			stock = gtk.STOCK_MEDIA_PAUSE
		elif type == "play":
			stock = gtk.STOCK_MEDIA_PLAY
		elif type == "stop":
			stock = gtk.STOCK_MEDIA_STOP
		elif type == "record":
			stock = gtk.STOCK_MEDIA_RECORD
		elif type == "skipleft":
			stock = gtk.STOCK_MEDIA_PREVIOUS
		elif type == "skipright":
			stock = gtk.STOCK_MEDIA_NEXT
		elif type == "forward":
			stock = gtk.STOCK_MEDIA_FORWARD
		elif type == "rewind":
			stock = gtk.STOCK_MEDIA_REWIND
		elif type == "up":
			stock = gtk.STOCK_GO_UP
		elif type == "down":
			stock = gtk.STOCK_GO_DOWN
		elif type == "left":
			stock = gtk.STOCK_GO_BACK
		elif type == "right":
			stock = gtk.STOCK_GO_FORWARD
		elif type == "playpause":
			img.set_from_file("%s/share/icons/playpause.png" % \
							  (mediarc.location))
		elif type == "button":
			btn.set_image_position(gtk.POS_TOP)
			label = name
			img.set_from_file("%s/share/icons/btn.png" % (mediarc.location))
		elif type == "plus":
			btn.set_image_position(gtk.POS_TOP)
			label = name
			stock = gtk.STOCK_ADD
		elif type == "minus":
			btn.set_image_position(gtk.POS_TOP)
			label = name
			stock = gtk.STOCK_REMOVE
		else:
			stock = type
		if stock:
			img.set_from_stock(stock, gtk.ICON_SIZE_BUTTON)
		btn.set_label(label)
		btn.set_image(img)
		return


	def select(self, force=False):
		if not self.selected or force:
			self.selected = True
			self.win.win.add_accel_group(self.accels)
			self.frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
			if self.defwidget:
				self.defwidget.grab_focus()
		return


	def unselect(self, force=False):
		if self.selected or force:
			self.selected = False
			self.win.win.remove_accel_group(self.accels)
			self.frame.set_shadow_type(gtk.SHADOW_NONE)
		return
