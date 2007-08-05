import gtk, gobject
import mediarc



class Remote(object):

	def __init__(self, name, win, rows=10, cols=10):
		self.name = name
		self.win = win
		self.table_x = 0
		self.table_y = 0
		# Table setup
		self.table = gtk.Table(rows, cols, False)
		self.table.set_flags(gtk.CAN_DEFAULT)
		self.table.set_row_spacings(10)
		self.table.set_border_width(10)
		self.table.show()
		# Frame setup
		self.frame = gtk.Frame(name)
		self.frame.add(self.table)
		self.frame.set_label_align(0.5, 0.5)
		self.frame.show()
		return


	def addRow(self):
		self.table_x = 0
		self.table_y = self.table_y + 1
		return


	def addButton(self, btn, cb):
		name = btn.getAttribute("name")
		xa = btn.getAttribute("colspan")
		x = [-1, -1]
		if xa:
			x = xa.split("-")
		ya = btn.getAttribute("rowspan")
		y = [-1, -1]
		if ya:
			y = ya.split("-")
		if xa or ya:
			button = self.addButtonFull(name, cb, int(x[0]), int(x[1]),
										int(y[0]), int(y[1]))
		else:
			button = self.addButtonAuto(name, cb)
		type = btn.getAttribute("type")
		if type and len(type):
			self.mapStock(button, type, name)
		#if name == "power":
		#	agrp = gtk.AccelGroup()
		#	self.win.win.add_accel_group(agrp)
		#	button.add_accelerator("clicked", agrp, ord('P'),
		#						   0, gtk.ACCEL_VISIBLE)
		#	#gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		return button


	def addButtonAuto(self, name, cb):
		btn = gtk.Button(name)
		btn.pyr_name = name
		btn.connect("clicked", cb)
		btn.set_focus_on_click(False)
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
		return slider


	def mapStock(self, btn, type, name):
		isize = "large"
		#isize = "small"
		stock = None
		img = gtk.Image()
		label = ""
		if type == "power":
			return
		elif type == "number":
			img.set_from_file("%s/share/icons/%s/%s.png" % (mediarc.location,
															isize, name))
		elif type == "forward":
			stock = gtk.STOCK_MEDIA_FORWARD
		elif type == "next":
			stock = gtk.STOCK_MEDIA_NEXT
		elif type == "pause":
			stock = gtk.STOCK_MEDIA_PAUSE
		elif type == "play":
			stock = gtk.STOCK_MEDIA_PLAY
		elif type == "previous":
			stock = gtk.STOCK_MEDIA_PREVIOUS
		elif type == "record":
			stock = gtk.STOCK_MEDIA_RECORD
		elif type == "rewind":
			stock = gtk.STOCK_MEDIA_REWIND
		elif type == "stop":
			stock = gtk.STOCK_MEDIA_STOP
		elif type == "up":
			stock = gtk.STOCK_GO_UP
		elif type == "down":
			stock = gtk.STOCK_GO_DOWN
		elif type == "left":
			stock = gtk.STOCK_GO_BACK
		elif type == "right":
			stock = gtk.STOCK_GO_FORWARD
		elif type == "button":
			btn.set_image_position(gtk.POS_TOP)
			label = name
			img.set_from_file("%s/share/icons/btn.png" % (mediarc.location))
		else:
			stock = type
		if stock:
			img.set_from_stock(stock, gtk.ICON_SIZE_BUTTON)
		btn.set_label(label)
		btn.set_image(img)
		return
