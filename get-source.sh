#!/bin/sh
# Make branch diff of official qtbase and qtwebkit against phantomjs branch
#
# Author: Elan Ruusamäe <glen@pld-linux.org>
set -e

specfile=phantomjs.spec
qt_base=git://code.qt.io/qt
phantom_base=https://github.com/Vitallium
tag=v5.5.1

# refs of submodules
# https://github.com/ariya/phantomjs/tree/2.1.1/src/qt
phantom_qtbase=b5cc008
phantom_qtwebkit=e7b7433

fetch_package() {
	local package=$1

	# use the ref dir to save downloads
	# it can be previous .git dir
	# mv qtcore.git qtcore.git.ref
	# mv qtwebkit.git qtwebkit.git.ref
	local ref_dir=$package.git.ref
	test -d $ref_dir || unset ref_dir

	if [ ! -d $GIT_DIR ]; then
		install -d $GIT_DIR
		git init --bare
		git remote add origin $qt_base/$package.git
		git remote add phantom $phantom_base/$package.git
	fi

	git fetch --depth 1 origin +refs/tags/$tag:refs/tags/$tag

	# don't know where the ref lives, fetch all
	git fetch phantom
}

filter() {
	filterdiff -p1 \
		-x '*.qdoc' \
		-x '*/.git*' \
		-x '.git*' \
		-x '.tag' \
		-x 'INSTALL' \
		-x 'tests/*' \
		-x 'doc/*' \
		-x 'bin/findtr' \
		-x 'bin/fixqt4headers.pl' \
		-x 'bin/syncqt.pl' \
		-x 'src/3rdparty/freetype/*' \
	| sed -re '/^(diff --git|index|(new|old) |Binary files)/d'
}

dropin() {
	local dropin=./dropin
	test -x $dropin || dropin=../dropin
	test -x $dropin || return
	$dropin "$@"
}

md5() {
	local builder=./builder
	test -x $builder || builder=../builder
	test -x $builder || builder=$(which builder 2>/dev/null)
	test -x $builder || return
	$builder -ncs -5 "$@"
}

get_package() {
	local package=$1 ref=$2
	echo >&2 ">> $package $tag..$ref"
	export GIT_DIR=$package.git
	fetch_package $package
	git diff $tag..$ref --diff-filter=MA > diff.tmp
	filter < diff.tmp > filtered.tmp
	mv filtered.tmp $package.diff
	xz -9f $package.diff
	dropin $package.diff.xz
	echo >&2 "<<"
}

get_package qtbase $phantom_qtbase
get_package qtwebkit $phantom_qtwebkit
md5 $specfile
