SUBDIRS = 

ACLOCAL_AMFLAGS = -I ../m4

mediarcdir = $(pkgdatadir)/mediarc
mediarc_DATA = $(srcdir)/*.py
mediarc_interfacedir = $(pkgdatadir)/mediarc/interface
mediarc_interface_DATA = $(srcdir)/interface/*.py
mediarc_remotesdir = $(pkgdatadir)/mediarc/remotes
mediarc_remotes_DATA = $(srcdir)/remotes/*.py
mediarc_serialdir = $(pkgdatadir)/mediarc/remotes/serial
mediarc_serial_DATA = $(srcdir)/remotes/serial/*.py
mediarc_oleviadir = $(pkgdatadir)/mediarc/remotes/serial/olevia
mediarc_olevia_DATA = $(srcdir)/remotes/serial/olevia/*.py

EXTRA_DIST = 
DISTCLEANFILES = 
MAINTAINERCLEANFILES = Makefile.in Makefile
MAINTAINERCLEANDIRS =

clean-local:
	find . -name '*.pyc' -exec rm {} \;
