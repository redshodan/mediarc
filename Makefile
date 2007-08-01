PWD=$(shell pwd)


all: loc


loc: bin/mediarc

bin/mediarc: Makefile bin/mediarc.in
	sed "s?__LOCATION__?\"$(PWD)\"?" bin/mediarc.in > $@
	chmod +x $@

svnignore:
	misc/svnignore-update.sh

clean:
	rm -rf bin/mediarc
	find -name '*.pyc' -exec rm {} \;


.PHONY: loc
