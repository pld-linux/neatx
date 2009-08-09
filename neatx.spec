%define	snap	38
Summary:	Open Source NX server, similar to the commercial NX server from NoMachine
Name:		neatx
Version:	0.1
Release:	0.r%{snap}.1
License:	GPL v2
Group:		X11/Applications/Networking
# svn export http://neatx.googlecode.com/svn/trunk/ neatx
Source0:	%{name}-r%{snap}.tar.bz2
# Source0-md5:	ce7c740ff099ba4e1a1f94209b18fe6d
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
Requires:	python-pexpect
Requires:	python-pygobject
Requires:	python-pygtk-gtk
Requires:	python-simplejson
Requires:	xorg-app-xauth
Requires:	xorg-app-xrdb
Requires:	xterm
Conflicts:	freenx-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Neatx is an Open Source NX server, similar to the commercial NX server
from NoMachine.

%prep
%setup -q -n %{name}

#sed -i -e 's#NXAGENT =.*#NXAGENT = "%{_bindir}/nxagent"#g' lib/constants.py
#sed -i -e 's#NETCAT =.*#NETCAT = "%{_bindir}/nc"#g' lib/constants.py

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/lib/neatx/{home/.ssh,sessions}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/neatx.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/neatx.conf
install extras/authorized_keys.nomachine $RPM_BUILD_ROOT/var/lib/neatx/home/.ssh/authorized_keys

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 160 -d /var/lib/neatx/home -s %{_libdir}/neatx/nxserver-login-wrapper -g users -G wheel -c "Neatx User" nx

%postun
if [ "$1" = "0" ]; then
	%userremove nx
fi

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
%dir /var/lib/neatx
%dir %attr(750,nx,root) /var/lib/neatx/home
%dir %attr(750,nx,root) /var/lib/neatx/home/.ssh
%config(noreplace) %verify(not md5 mtime size) /var/lib/neatx/home/.ssh/authorized_keys
%dir %attr(1777,root,root) /var/lib/neatx/sessions
%dir %{_libdir}/neatx
%attr(755,root,root) %{_libdir}/neatx/*
%{_datadir}/neatx
%dir %{py_sitescriptdir}/neatx
%{py_sitescriptdir}/neatx/*.py[co]
%dir %{py_sitescriptdir}/neatx/app
%{py_sitescriptdir}/neatx/app/*.py[co]
