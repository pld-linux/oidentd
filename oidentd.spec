Summary:	Ident server with masquerading support
Summary(pl.UTF-8):	Serwer ident z obsługą maskowanych adresów IP
Name:		oidentd
Version:	3.1.0
Release:	2
License:	GPL v2
Group:		Networking/Daemons
Source0:	https://github.com/janikrabe/oidentd/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	88508a22bdf499315c200e308bfefa7e
Source1:	%{name}.init
Source2:	%{name}.users
Source3:	%{name}.sysconfig
Source4:	%{name}.conf
Source5:	%{name}.inetd
Source6:	%{name}.socket
Source7:	%{name}@.service
# https://github.com/janikrabe/oidentd/commit/0f4ccf4e5d5a0f286e353df3631c9f33292167cf
Patch0:		%{name}-configure-attribute-checks.patch
URL:		https://oidentd.janikrabe.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libnetfilter_conntrack-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	ruby-asciidoctor
Requires:	%{name}-init = %{version}-%{release}
Provides:	identserver
Obsoletes:	linux-identd
Obsoletes:	linux-identd-inetd
Obsoletes:	linux-identd-standalone
Obsoletes:	midentd
Obsoletes:	nidentd
Obsoletes:	pidentd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Oidentd is an ident (rfc1413) daemon that runs on Linux, FreeBSD,
OpenBSD and Solaris 2.x. Oidentd supports most features of pidentd
plus more. Most notably, oidentd allows users to specify the identd
response that the server will output when a successful lookup is
completed. Oidentd supports IP masqueraded connections on Linux, and
is able to forward requests to hosts that masq through the host on
which oidentd runs.

%description -l pl.UTF-8
Oident jest serwerem usługi ident (zgodnym z rfc1413) działającym pod
kontrolą systemów operacyjnych takich jak Linux, FreeBSD, OpenBSD oraz
Solaris 2.x. Oident posiada większość funkcji programu pidentd oraz
trochę dodatkowych. Jedną z nich jest to, że oident pozwala
użytkownikom na zmianę swojej nazwy przesyłanej przez serwer na
dowolną inną. Dodatkowo wspiera przesyłanie odwołań do usługi ident
poprzez IP masqueradeing.

%package inetd
Summary:	Ident server with masquerading support
Summary(pl.UTF-8):	Serwer ident z obsługą maskowanych adresów IP
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Provides:	%{name}-init = %{version}-%{release}
Obsoletes:	oidentd-standalone
Conflicts:	%{name} <= 2.0.7-1

%description inetd
This package allows to start oidentd as inetd service.

%description inetd -l pl.UTF-8
Ten pakiet pozwala na wystartowanie oidentd jako servis inetd.

%package standalone
Summary:	Ident server with masquerading support
Summary(pl.UTF-8):	Serwer ident z obsługą maskowanych adresów IP
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Requires:	systemd-units >= 38
Provides:	%{name}-init = %{version}-%{release}
Obsoletes:	oidentd-inetd
Conflicts:	%{name} <= 2.0.7-1

%description standalone
This package allows to start oidentd as standalone daemon.

%description standalone -l pl.UTF-8
Ten pakiet pozwala na wystartowanie oidentd jako samodzielnego demona.

%prep
%setup -q
%patch -P0 -p1
# shipped man pages name /usr/local/etc; make regenerates them with sysconfdir
%{__rm} doc/oidentd.8 doc/oidentd.conf.5 doc/oidentd_masq.conf.5

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-ipv6 \
	--enable-libnfct \
	--enable-masq
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{sysconfig/rc-inetd,rc.d/init.d},%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/oidentd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/oidentd
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/oidentd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/oidentd_masq.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/oidentd.conf
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdunitdir}/oidentd.socket
cp -p %{SOURCE7} $RPM_BUILD_ROOT%{systemdunitdir}/oidentd@.service
# keep systemd-sysv-generator from turning the init script into a second listener
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/oidentd.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%banner %{name} -e <<EOF
###################################################################
#                                                                 #
# NOTICE:                                                         #
# You need to load 'tcp_diag' kernel module for oidentd to use    #
# netlink interface instead of (very slow) /proc/net/tcp          #
#                                                                 #
###################################################################
EOF

%post standalone
/sbin/chkconfig --add %{name}
%service oidentd restart
%systemd_post oidentd.socket

%preun standalone
if [ "$1" = "0" ]; then
	%service oidentd stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun oidentd.socket

%postun standalone
%systemd_reload

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README ChangeLog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/oidentd_masq.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/oidentd.conf
%attr(755,root,root) %{_sbindir}/oidentd
%{_mandir}/man8/*
%{_mandir}/man5/*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/oidentd

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/oidentd
%{systemdunitdir}/oidentd.service
%{systemdunitdir}/oidentd.socket
%{systemdunitdir}/oidentd@.service
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/oidentd
