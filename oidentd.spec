Summary:	Ident server with masquerading support
Summary(pl):	Ident serwer z obs�ug� maskowanych adres�w IP
Name:		oidentd
Version:	1.7.1
Release:	3
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://download.sourceforge.net/pub/sourceforge/ojnk/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.users
Patch:		oidentd-1.7.1-ipv6.patch
URL:		http://ojnk.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
Prereq:		rc-inetd
Provides:	identserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
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
Oident jest serwerem us�ugi ident (zgodnym z rfc1413) dzia�aj�cym pod
kontrol� system�w operacyjnych takich jak Linux, FreeBSD, OpenBSD oraz
Solaris 2.x. Oident posiada wi�kszo�� funkcji programu pidentd oraz
troch� dodatkowych. Jedn� z nich jest to, �e oident pozwala
u�ytkownikom na zmian� swojej nazwy przesy�anej przez serwer na
dowoln� inn�. Dodatkowo wspiera przesy�anie odwo�a� do us�ugi ident
poprzez IP masqueradeing.

%prep
%setup  -q
%patch0 -p1

%build
aclocal
autoheader
autoconf
automake -a -c
%configure \
	--enable-ipv6 \
	--enable-newrandom
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/oidentd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/oidentd.users

gzip -9nf AUTHORS INSTALL NEWS README THANKS ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
%rc_inetd_post

%postun
%rc_inetd_postun

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/rc-inetd/oidentd
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/oidentd.users
%attr(755,root,root) %{_sbindir}/oidentd
%{_mandir}/man8/*
