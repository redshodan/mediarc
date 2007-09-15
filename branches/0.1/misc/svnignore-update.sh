#!/bin/bash


EXCLUDES="$*"
VCS='svn'   # Valid values: svn or svk
TOP=`pwd`
DIRS=`find . -type d | grep -v .svn`

for DIR in ${DIRS}; do
	cd $TOP
	cd $DIR
	${VCS} propset svn:ignore -F ${TOP}/misc/svnignore .
	echo "	$DIR"
done
cd ${TOP}

# Adjust special cases
for FILE in `find ${TOP} -name svnignore`; do
    cp -f ${TOP}/misc/svnignore /tmp/svnignore-tmp
    cat ${FILE} >> /tmp/svnignore-tmp
    cd `dirname ${FILE}`
    ${VCS} propset svn:ignore -F /tmp/svnignore-tmp .
    rm /tmp/svnignore-tmp
    cd ${TOP}
done
