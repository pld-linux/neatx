%define	snap	13
Summary:	Open Source NX server, similar to the commercial NX server from NoMachine
Name:		neatx
Version:	0.1
Release:	0.r%{snap}.1
License:	GPL v2
Group:		X11/Applications/Networking
# svn export http://neatx.googlecode.com/svn/trunk/ neatx
Source0:	%{name}-r%{snap}.tar.bz2
# Source0-md5:	4e4159c01b5561808c0f99ac20a1e8c3
URL:		http://code.google.com/p/neatx/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	python-devel
BuildRequires:	python-docutils
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	bash
Requires:	coreutils
Requires:	nc
Requires:	nx
Requires:	openssh-clients
Requires:	xorg-app-xauth
Requires:	xorg-app-xrdb
Requires:	xterm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Neatx is an Open Source NX server, similar to the commercial NX server
from NoMachine.

%prep
%setup -q -n %{name}

sed -i -e 's#NXAGENT =.*#NXAGENT = %{_bindir}/nxagent#g' lib/constants.py

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/neatx.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/neatx.conf

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 221 -d %{_libdir}/neatx/home -s %{_libdir}/neatx/nxserver-login-wrapper -g users -c "Neatx User" neatx

%post   -p <lua>
%lua_add_etc_shells %{_libdir}/neatx/nxserver-login-wrapper

%preun  -p <lua>
if arg[2] == 0 then
	%lua_remove_etc_shells %{_libdir}/neatx/nxserver-login-wrapper
end

%files
%defattr(644,root,root,755)

%doc doc/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/neatx.conf
%dir %{_libdir}/neatx
%attr(755,root,root) %{_libdir}/neatx/*
%{_datadir}/neatx
%dir %{py_sitescriptdir}/neatx
%{py_sitescriptdir}/neatx/*.py[co]
%dir %{py_sitescriptdir}/neatx/app
%{py_sitescriptdir}/neatx/app/*.py[co]
