# NOTES
# - fedora's attempt to package this: https://bugzilla.redhat.com/show_bug.cgi?id=891461
#
# Conditional build:
%bcond_with	system_qcommandline
%bcond_with	system_qt

Summary:	Headless WebKit with a JavaScript API
Name:		phantomjs
Version:	2.1.1
Release:	0.2
License:	BSD
Group:		Applications/Networking
Source0:	https://github.com/ariya/phantomjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	db2d71e67e3557a977c2f269f1ec7fee
# https://github.com/ariya/phantomjs/tree/2.1.1/src/qt
Source1:	https://github.com/Vitallium/qtbase/archive/b5cc0083a5766e773885e8dd624c51a967c17de0.tar.gz
# Source1-md5:	ae375f9f522409ae262e949cd90bf880
Source2:	https://github.com/Vitallium/qtwebkit/archive/e7b74331d695bfa8b77e39cdc50fc2d84a49a22a.tar.gz
# Source2-md5:	94daad678e91ff9049ba26eb9e32febf
Patch0:		%{name}-qt.patch
Patch1:		%{name}-env.patch
Patch3:		0003-unbundle-mongoose.patch
Patch5:		0005-unbundle-qt.patch
Patch6:		0006-unbundle-linenoise.patch
Patch7:		0007-unbundle-QCommandLine.patch
URL:		http://phantomjs.org/
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5WebKit-devel
BuildRequires:	coffee-script
BuildRequires:	giflib-devel
BuildRequires:	linenoise-devel
BuildRequires:	mongoose-devel
%{?with_system_qcommandline:BuildRequires:	qcommandline-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	Qt5Gui-platform-xcb
Requires:	coffee-script
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

#%patch0 -p1
%patch1 -p1
%patch3 -p1
%{?with_system_qt:%patch5 -p1}
%patch6 -p1
%{?with_system_qcommandline:%patch7 -p1}

%build
%{__python} build.py --confirm --release

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
