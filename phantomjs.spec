Summary:	Headless WebKit with a JavaScript API
Name:		phantomjs
Version:	1.9.7
Release:	4
License:	BSD
Group:		Applications/Networking
Source0:	https://bitbucket.org/ariya/phantomjs/downloads/%{name}-%{version}-source.zip
# Source0-md5:	5d308d2db7d8b494f99dbb5664447547
Patch0:		giflib5.patch
Patch1:		0001-gifwriter-bgcolor-narrowing.patch
Patch2:		0002-unbundle-giflib.patch
Patch3:		0003-unbundle-mongoose.patch
Patch4:		0004-unbundle-breakpad.patch
Patch5:		0005-unbundle-qt.patch
Patch6:		0006-unbundle-linenoise.patch
Patch7:		0007-unbundle-QCommandLine.patch
Patch8:		0008-unbundle-coffee-script.patch
Patch9:		no-qcodecs.patch
URL:		http://phantomjs.org/
BuildRequires:	QtWebKit-devel
BuildRequires:	coffee-script
BuildRequires:	giflib-devel
BuildRequires:	linenoise-devel
BuildRequires:	mongoose-devel
BuildRequires:	qcommandline-devel
BuildRequires:	unzip
Requires:	coffee-script
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and
native support for various web standards: DOM handling, CSS selector,
JSON, Canvas, and SVG. It can be used for screen scraping and web
testing. It includes an implementation of the WebDriver API.

%prep
%setup -q

# remove bundled sources
rm -r src/gif/config.h
rm -r src/gif/egif_lib.c
rm -r src/gif/gif_err.c
rm -r src/gif/gif_hash.c
rm -r src/gif/gif_hash.h
rm -r src/gif/gif_lib.h
rm -r src/gif/gif_lib_private.h
rm -r src/gif/gifalloc.c
rm -r src/gif/quantize.c
rm -r src/mongoose
rm -r src/qt
rm -r src/linenoise
rm -r src/qcommandline
rm -r src/coffee-script
rm -r src/breakpad

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
qmake-qt4
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}"

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
