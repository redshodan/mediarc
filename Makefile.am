SUBDIRS =

ACLOCAL_AMFLAGS = -I m4

bin_SCRIPTS = bin/mediarc

docfilesdir = $(docdir)
docfiles_DATA = \
	README \
	COPYING

mediarcdir = $(pkgdatadir)/mediarc
mediarc_DATA = \
	$(srcdir)/mediarc/*.py

mediarc_interfacedir = $(pkgdatadir)/mediarc/interface
mediarc_interface_DATA = \
	$(srcdir)/mediarc/interface/*.py

mediarc_remotesdir = $(pkgdatadir)/mediarc/remotes
mediarc_remotes_DATA = \
	$(srcdir)/mediarc/remotes/*.py

mediarc_serialdir = $(pkgdatadir)/mediarc/remotes/serial
mediarc_serial_DATA = \
	$(srcdir)/mediarc/remotes/serial/*.py

mediarc_oleviadir = $(pkgdatadir)/mediarc/remotes/serial/olevia
mediarc_olevia_DATA = \
	$(srcdir)/mediarc/remotes/serial/olevia/*.py

EXTRA_DIST = \
	$(docfiles_DATA) \
	$(mediarc_DATA) \
	autogen.sh \
	scripts/mediarc.in

DISTCLEANFILES = \
	bin/mediarc

MAINTAINERCLEANFILES = \
	configure \
	Makefile.in \
	ltmain.sh \
	missing \
	mkinstalldirs \
	install-sh \
	compile \
	depcomp \
	config.guess \
	config.log \
	config.sub \
	config.status \
	config.h.in \
	aclocal.m4

MAINTAINERCLEANDIRS = \
	autom4te.cache \
	build \
	dist

.PHONY: svnignore
svnignore:
	misc/svnignore-update.sh

clean-local:
	find mediarc -name '*.pyc' -exec rm {} \;
