aclocal -I ./m4 \
&& autoheader \
&& autoconf  \
&& automake --add-missing --foreign \
&& ./configure $@
