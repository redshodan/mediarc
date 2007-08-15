import socket, gobject



def init(cfg):
	elem = mode = None
	elem = cfg.getElem("config/ctl")
	if elem:
		mode = elem.getAttr("mode")
	if mode and mode != "enable":
		print "Control socket configured off, not starting"
		return
	address = elem.getAttr("address")
	if not address: address = "localhost"
	port = elem.getAttrInt("port")
	if not port: port = 2424
	print "Setting up control socket on %s:%d" % (address, port)
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((address, port))
		sock.listen(5)
		gobject.io_add_watch(sock, gobject.IO_IN | gobject.IO_HUP | gobject.IO_ERR,
							ctlSockCB)
	except Exception, e:
		print "Failed to setup control socket:"
		print e
	return


def ctlSockCB(sock, condition):
	print "ctlSockCB"
	if gobject.IO_IN & condition:
		print "Accepting new client connection on control socket"
		try:
			(newsock, address) = sock.accept()
			print "New connection from:", address
			newsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			newf = newsock.makefile()
			sock.close()
			gobject.io_add_watch(newf,
								 gobject.IO_IN | gobject.IO_HUP | gobject.IO_ERR,
								 cliSockCB, address)
		except Exception, e:
			print "Failed to accept client connection on control socket:"
			print e
		return True
	if gobject.IO_HUP & condition or gobject.IO_ERR & condition:
		print "Error on control socket, closing it down"
		try:
			sock.close()
		except: pass
		return False
	return True


def cliSockCB(sock, condition, address):
	try:
		print "cliSockCB"
		if gobject.IO_IN & condition:
			cmd = sock.readline()
			if not cmd or not len(cmd):
				print "Closing connection from:", address
				sock.close()
				return False
			print "read from %s: %s" % (str(address), cmd)
			return True
		if gobject.IO_HUP & condition or gobject.IO_ERR & condition:
			print "Error on control socket, closing it down"
			sock.close()
			return False
	except Exception, e:
		print "Failed to read from client connection:"
		print e
		try:
			sock.close()
		except: pass
	return False
