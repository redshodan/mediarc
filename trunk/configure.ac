AC_INIT([MediaRC - A media remote control program],
		[0.1.0],[http://mediarc.googlecode.com],[mediarc])
AC_PREREQ([2.59])
AM_INIT_AUTOMAKE([1.8])
AC_CONFIG_HEADER(config.h)
AC_CONFIG_MACRO_DIR([m4])
AM_MAINTAINER_MODE

AC_PROG_INSTALL

dnl python
AM_PATH_PYTHON([2.4])
if test "x$PYTHON" = "x:"; then
	AC_MSG_ERROR([Python not found])
fi

dnl pygtk and gtk+
PKG_CHECK_MODULES([PYGTK], [gtk+-2.0 >= 2.6.0 pygtk-2.0 >= 2.6.0])

ACLOCAL_AMFLAGS="\${ACLOCAL_FLAGS}"
AC_SUBST(ACLOCAL_AMFLAGS)

AS_AC_EXPAND(DATADIR, "${datadir}")
AS_AC_EXPAND(LIBDIR, ${libdir})
AS_AC_EXPAND(DOCDIR, "${docdir}")

AC_SUBST(VERSION)
AC_SUBST(PACKAGE)
AC_SUBST(DATADIR)
AC_SUBST(LIBDIR)
AS_AC_EXPAND(DATADIR, "${DATADIR}")
AC_SUBST(DOCDIR)
AS_AC_EXPAND(DOCDIR, "${DOCDIR}")

AC_CONFIG_FILES([ 
	Makefile
    bin/mediarc
], [chmod +x bin/mediarc])
AC_OUTPUT
