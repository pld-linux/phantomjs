# NOTES
# - fedora's attempt to package this: https://bugzilla.redhat.com/show_bug.cgi?id=891461
#
# Conditional build:
%bcond_with	system_qcommandline
%bcond_with	system_qt
%bcond_without	tests		# build without tests

%define	qtbase	5.5.1
Summary:	Headless WebKit with a JavaScript API
Name:		phantomjs
Version:	2.1.1
Release:	3
License:	BSD
Group:		Applications/Networking
Source0:	https://github.com/ariya/phantomjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	db2d71e67e3557a977c2f269f1ec7fee
Source1:	http://download.qt.io/official_releases/qt/5.5/%{qtbase}/submodules/qtbase-opensource-src-%{qtbase}.tar.xz
# Source1-md5:	687e2b122fa2c3390b5e20a166d38038
Source2:	http://download.qt.io/official_releases/qt/5.5/%{qtbase}/submodules/qtwebkit-opensource-src-%{qtbase}.tar.xz
# Source2-md5:	681328edb539b8fa3a273b38c90b3e31
Patch0:		%{name}-qt.patch
Patch1:		%{name}-env.patch
Patch3:		0003-unbundle-mongoose.patch
Patch5:		0005-unbundle-qt.patch
Patch6:		0006-unbundle-linenoise.patch
Patch7:		0007-unbundle-QCommandLine.patch
# See get-source.sh how to generate these diffs
Patch101:	qtbase.diff.xz
# Patch101-md5:	8e8fb4b12c672ecd128fbcf1fccd964b
Patch102:	qtwebkit.diff.xz
# Patch102-md5:	ab3a7372ea3f7bb6326e666ffad7acda
Patch201:	qtwebkit-icu59.patch
Patch202:	qtwebkit-new-char-types.patch
URL:		http://phantomjs.org/
BuildRequires:	linenoise-devel
BuildRequires:	mongoose-devel
%{?with_system_qcommandline:BuildRequires:	qcommandline-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with system_qt}
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5WebKit-devel
%else
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	gcc >= 5:4.0
BuildRequires:	gperf
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libproxy-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre16-devel >= 8.30
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	ruby
BuildRequires:	ruby-modules
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
%endif
%if %{with tests}
BuildRequires:	fontconfig
%endif
%{?with_system_qt:Requires:	Qt5Gui-platform-xcb}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and
native support for various web standards: DOM handling, CSS selector,
JSON, Canvas, and SVG. It can be used for screen scraping and web
testing. It includes an implementation of the WebDriver API.

%prep
%setup -q %{!?with_system_qt:-a1 -a2}

%if %{without system_qt}
rmdir src/qt/{qtbase,qtwebkit}
mv qtbase-* src/qt/qtbase
mv qtwebkit-* src/qt/qtwebkit

%patch -P101 -p1 -d src/qt/qtbase
%patch -P102 -p1 -d src/qt/qtwebkit

%patch -P201 -p1 -d src/qt/qtwebkit
%patch -P202 -p1 -d src/qt/qtwebkit

# https://github.com/ariya/phantomjs/issues/13930
# otherwise we get this error:
# https://bugreports.qt.io/browse/QTBUG-48626
touch src/qt/qtbase/.git
touch src/qt/qtwebkit/.git
touch src/qt/3rdparty/.git

# change QMAKE FLAGS to build
# define QMAKE_STRIP to true, so we get useful -debuginfo pkgs
cd src/qt/qtbase
%{__sed} -i -e '
	s|^\(QMAKE_COMPILER *\)=.*gcc|\1= %{__cc}|;
	s|^\(QMAKE_CC *\)=.*gcc|\1= %{__cc}|;
	s|^\(QMAKE_CXX *\)=.*g++|\1= %{__cxx}|;
	s|^\(QMAKE_CFLAGS_OPTIMIZE .*\)=|\1 = %{rpmcppflags} %{rpmcflags}|;
	s|^\(QMAKE_LFLAGS *\)+=.*|\1+= %{rpmldflags}|;
	s|^\(QMAKE_STRIP *\)=.*|\1= :|;
	' \
	mkspecs/common/g++-base.conf \
	mkspecs/common/gcc-base.conf \
	mkspecs/common/linux.conf
cd -
%endif

# remove bundled sources
rm -r src/mongoose
%{?with_system_qt:rm -r src/qt}
rm -r src/linenoise
%{?with_system_qcommandline:rm -r src/qcommandline}

#%%patch0 -p1
%patch -P1 -p1
%patch -P3 -p1
%{?with_system_qt:%patch5 -p1}
%patch -P6 -p1
%{?with_system_qcommandline:%patch7 -p1}

%build
qtconfig() {
	for a in "$@"; do
		echo --qt-config="$a"
	done
}
webkit_config() {
	for a in "$@"; do
		echo --webkit-qmake-args="$a"
	done
}
qtconfig=" \
	-v \
	-accessibility \
	-fontconfig \
	-force-pkg-config \
	-largefile \
	-libproxy \
	-no-gstreamer \
	-no-icu \
	-no-journald \
	-no-sql-db2 \
	-no-sql-ibase \
	-no-sql-mysql \
	-no-sql-oci \
	-no-sql-odbc \
	-no-sql-psql \
	-no-sql-sqlite \
	-no-sql-sqlite2 \
	-no-sql-tds \
	-no-tslib \
	-no-xcb-xlib \
	-no-xinput2 \
	-no-xkbcommon-evdev \
	-openssl-linked \
	-system-freetype \
	-system-harfbuzz \
	-system-libjpeg \
	-system-libpng \
	-system-pcre \
	-system-proxies \
	-system-zlib \
"

webkit_config="
	WEBKIT_CONFIG-=build_tests
	WEBKIT_CONFIG-=have_glx
	WEBKIT_CONFIG-=have_qtquick
	WEBKIT_CONFIG-=have_qtsensors
	WEBKIT_CONFIG-=have_qttestlib
	WEBKIT_CONFIG-=have_qttestsupport
	WEBKIT_CONFIG-=have_sqlite3
	WEBKIT_CONFIG-=have_xcomposite
	WEBKIT_CONFIG-=have_xrender
	WEBKIT_CONFIG-=use_libxml2
	WEBKIT_CONFIG-=use_webp
	WEBKIT_CONFIG-=xslt

	WEBKIT_TOOLS_CONFIG-=build_imagediff
	WEBKIT_TOOLS_CONFIG-=build_minibrowser
	WEBKIT_TOOLS_CONFIG-=build_qttestsupport
	WEBKIT_TOOLS_CONFIG-=build_test_npapi
	WEBKIT_TOOLS_CONFIG-=build_wtr
"
#	WEBKIT_TOOLS_CONFIG-=build_testbrowser
%{__python} -u build.py \
	$(qtconfig $qtconfig) \
	$(webkit_config $webkit_config) \
	--confirm --release

%if %{with tests}
# note, these cookie tests fail with non-C locale:
# - module/cookiejar/to-map.js
# - module/webpage/cookies.js
LC_ALL=C test/run-tests.py -v
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/phantomjs $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.BSD CONTRIBUTING.md ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%{_examplesdir}/%{name}-%{version}
