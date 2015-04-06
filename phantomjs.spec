%bcond_with	system_qcommandline
Summary:	Headless WebKit with a JavaScript API
Name:		phantomjs
Version:	2.0.0
Release:	2
License:	BSD
Group:		Applications/Networking
Source0:	https://bitbucket.org/ariya/phantomjs/downloads/%{name}-%{version}-source.zip
# Source0-md5:	feabe9064100e241d21347739312e64d
Patch0:		phantomjs-qt.patch
Patch1:		phantomjs-env.patch

Patch3:		0003-unbundle-mongoose.patch
Patch4:		phantomjs-disable-breakpad.patch
Patch5:		0005-unbundle-qt.patch
Patch6:		0006-unbundle-linenoise.patch
Patch7:		0007-unbundle-QCommandLine.patch
URL:		http://phantomjs.org/
BuildRequires:	Qt5WebKit-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	coffee-script
BuildRequires:	giflib-devel
BuildRequires:	linenoise-devel
BuildRequires:	mongoose-devel
%{?with_system_qcommandline:BuildRequires:	qcommandline-devel}
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
rm -r src/mongoose
rm -r src/qt
rm -r src/linenoise
%{?with_system_qcommandline:rm -r src/qcommandline}
rm -r src/breakpad

%patch0 -p1
%patch1 -p1

%patch3 -p1
%patch4 -p1
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
