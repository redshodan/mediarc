SUBDIRS = drivers etc icons mediarc themes

ACLOCAL_AMFLAGS = -I m4

# Binary
bin_SCRIPTS = bin/mediarc bin/mediarc-remote

# Docs
docfilesdir = $(docdir)
docfiles_DATA = README COPYING

EXTRA_DIST = \
	autogen.sh \
	configure.ac \
	Makefile.am \
	bin/mediarc.in \
	bin/mediarc-remote.in

DISTCLEANFILES = \
	bin/mediarc \
	bin/mediarc-remote

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
