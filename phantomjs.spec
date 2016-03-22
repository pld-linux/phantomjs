# NOTES
# - fedora's attempt to package this: https://bugzilla.redhat.com/show_bug.cgi?id=891461
#
# Conditional build:
%bcond_with	system_qcommandline

Summary:	Headless WebKit with a JavaScript API
Name:		phantomjs
Version:	2.1.1
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	https://github.com/ariya/phantomjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	db2d71e67e3557a977c2f269f1ec7fee
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
%setup -q

# remove bundled sources
rm -r src/mongoose
rm -r src/qt
rm -r src/linenoise
%{?with_system_qcommandline:rm -r src/qcommandline}

#%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%{?with_system_qcommandline:%patch7 -p1}

%build
qmake-qt5
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -fPIC"

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
