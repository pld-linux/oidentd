Summary:	Ident server with masquerading support
Summary(pl):	Serwer ident z obs³ug± maskowanych adresów IP
Name:		oidentd
Version:	2.0.7
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/ojnk/%{name}-%{version}.tar.gz
# Source0-md5:	cf1c017496b066b45ffe3d7a303fd6ad
Source1:	%{name}.init
Source2:	%{name}.users
Source3:	%{name}.sysconfig
Source4:	%{name}.conf
URL:		http://ojnk.sourceforge.net/
BuildRequires:	bison
BuildRequires:	flex
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	identserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	linux-identd
Obsoletes:	linux-identd-inetd
Obsoletes:	linux-identd-standalone
Obsoletes:	midentd
Obsoletes:	nidentd
Obsoletes:	pidentd

%description
Oidentd is an ident (rfc1413) daemon that runs on Linux, FreeBSD,
OpenBSD and Solaris 2.x. Oidentd supports most features of pidentd
plus more. Most notably, oidentd allows users to specify the identd
response that the server will output when a successful lookup is
completed. Oidentd supports IP masqueraded connections on Linux, and
is able to forward requests to hosts that masq through the host on
which oidentd runs.

%description -l pl
Oident jest serwerem us³ugi ident (zgodnym z rfc1413) dzia³aj±cym pod
kontrol± systemów operacyjnych takich jak Linux, FreeBSD, OpenBSD oraz
Solaris 2.x. Oident posiada wiêkszo¶æ funkcji programu pidentd oraz
trochê dodatkowych. Jedn± z nich jest to, ¿e oident pozwala
u¿ytkownikom na zmianê swojej nazwy przesy³anej przez serwer na
dowoln± inn±. Dodatkowo wspiera przesy³anie odwo³añ do us³ugi ident
poprzez IP masqueradeing.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{sysconfig,rc.d/init.d}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/oidentd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/oidentd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/oidentd_masq.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/oidentd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/oidentd ]; then
	/etc/rc.d/init.d/oidentd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/oidentd start\" to start inet server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/oidentd ]; then
		/etc/rc.d/init.d/oidentd stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README ChangeLog
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/oidentd_masq.conf
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/oidentd.conf
%attr(755,root,root) %{_sbindir}/oidentd
%attr(754,root,root) /etc/rc.d/init.d/oidentd
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/oidentd
%{_mandir}/man8/*
%{_mandir}/man5/*
