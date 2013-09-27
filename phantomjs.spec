Summary:	Headless WebKit with a JavaScript API
Name:		phantomjs
Version:	1.9.0
Release:	1
License:	BSD
Group:		Applications/Networking
URL:		http://phantomjs.org/
Source0:	http://phantomjs.googlecode.com/files/%{name}-%{version}-source.zip
# Source0-md5:	a779eb301cac2df9f366be5b2d17cef7
Patch1:		0001-gifwriter-bgcolor-narrowing.patch
Patch2:		0002-unbundle-giflib.patch
Patch3:		0003-unbundle-mongoose.patch
Patch4:		0004-unbundle-breakpad.patch
Patch5:		0005-unbundle-qt.patch
Patch6:		0006-unbundle-linenoise.patch
Patch7:		0007-unbundle-QCommandLine.patch
Patch8:		0008-unbundle-coffee-script.patch
BuildRequires:	QtWebKit-devel
BuildRequires:	coffee-script
BuildRequires:	giflib-devel
BuildRequires:	linenoise-devel
BuildRequires:	mongoose-devel
BuildRequires:	qcommandline-devel
BuildRequires:	unzip
Requires:	coffee-script

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

%patch1 -p1 -b.gifwriter-bgcolor-narrowing
%patch2 -p1 -b.giflib
%patch3 -p1 -b.mongoose
%patch4 -p1 -b.breakpad
%patch5 -p1 -b.qt
%patch6 -p1 -b.linenoise
%patch7 -p1 -b.qcommandline
%patch8 -p1 -b.coffee-script

%build
export CFLAGS="%{rpmcflags}"
qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

cp bin/phantomjs $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.BSD CONTRIBUTING.md ChangeLog examples/
%attr(755,root,root) %{_bindir}/%{name}
