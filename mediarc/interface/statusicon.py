import gtk



class StatusIcon(object):
	def __init__(self, cfg, win):
		self.cfg = cfg
		self.win = win
		self.status_icon = gtk.status_icon_new_from_stock(gtk.STOCK_CLEAR)
		self.status_icon.set_visible(True)
		return
