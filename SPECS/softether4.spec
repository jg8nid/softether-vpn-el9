%global se_srcdir SoftEtherVPN_Stable-4.44-9807-rtm
Name:			softether4
Version:		4.44.9807
Release:		1%{?dist}
Summary:		SoftEther VPN Server, Client and Command-line tools

License:		ASL 2.0
URL:			https://www.softether.org/
Source0:		https://codeload.github.com/SoftEtherVPN/SoftEtherVPN_Stable/tar.gz/refs/tags/v4.44-9807-rtm?filename=SoftEtherVPN_Stable-4.44-9807-rtm.tar.gz
Source1:		softether4-vpnbridge.service
Source2:		softether4-vpnclient.service
Source3:		softether4-vpnserver.service
Source4:		vpncmd4
Source5:		vpncmd4.1

Patch0:			increase-nat-sessions.patch
Patch1:			log-db-pid-dir.patch
Patch2:			unrestrict-enterprise-functions.patch
Patch3:			fix-type-missmatch.patch
Patch4:			add-protorype.patch
Patch5:			replace-getch.patch

BuildRequires:	dos2unix
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	systemd
BuildRequires:	systemd-rpm-macros

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
SoftEther VPN ("SoftEther" means "Software Ethernet") is a powerful,
multi-OS and easy-to-use multi-protocol VPN software. It supports
SSL-VPN (HTTPS), as well as OpenVPN, IPsec, L2TP, MS-SSTP, L2TPv3
and EtherIP tunneling protocols and has a clone function to support
OpenVPN clients.

This package includes FHS-compliant patches and systemd integration
for HPEL systems.

%prep
%setup -q -n %{se_srcdir}
dos2unix ChangeLog LICENSE README *.TXT
dos2unix src/Cedar/*.*
dos2unix src/Mayaqua/*.*
%autopatch -p1
%{__sed} -i \
	-e "s|@@SE_DBDIR@@|/var/lib/%{name}|g" \
	-e "s|@@SE_LOGDIR@@|/var/log/%{name}|g" \
	-e "s|@@SE_PIDDIR@@|/run/%{name}|g" \
	src/Mayaqua/FileIO.c

%build
cp src/makefiles/linux_64bit.mak Makefile
sed -i \
	-e "s|OPTIONS_COMPILE_RELEASE=|OPTIONS_COMPILE_RELEASE=%{optflags} |g" \
	-e "s|OPTIONS_LINK_RELEASE=|OPTIONS_LINK_RELEASE=%{?__global_ldflags} |g" \
	Makefile
make

%install
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

install -m 0755 bin/vpnbridge/vpnbridge %{buildroot}%{_libexecdir}/%{name}/
install -m 0755 bin/vpnserver/vpnserver %{buildroot}%{_libexecdir}/%{name}/
install -m 0755 bin/vpnclient/vpnclient %{buildroot}%{_libexecdir}/%{name}/
install -m 0755 bin/vpncmd/vpncmd %{buildroot}%{_libexecdir}/%{name}/
install -m 0644 bin/vpnserver/hamcore.se2 %{buildroot}%{_libexecdir}/%{name}/

# systemd unit
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/

# shell script
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/

# man page
install -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man1/

%post
%systemd_post softether4-vpnbridge.service
%systemd_post softether4-vpnclient.service
%systemd_post softether4-vpnserver.service

%preun
%systemd_preun softether4-vpnbridge.service
%systemd_preun softether4-vpnclient.service
%systemd_preun softether4-vpnserver.service

%postun
# systemd cleanup
%systemd_postun softether4-vpnbridge.service
%systemd_postun softether4-vpnclient.service
%systemd_postun softether4-vpnserver.service

%files
%license LICENSE
%doc AUTHORS.TXT
%doc ChangeLog
%doc README
%doc THIRD_PARTY.TXT
%doc WARNING.TXT

%{_libexecdir}/%{name}/vpnbridge
%{_libexecdir}/%{name}/vpnclient
%{_libexecdir}/%{name}/vpncmd
%{_libexecdir}/%{name}/vpnserver
%{_libexecdir}/%{name}/hamcore.se2
%{_bindir}/vpncmd4
%{_mandir}/man1/vpncmd4.1.gz
%{_unitdir}/softether4-vpnbridge.service
%{_unitdir}/softether4-vpnclient.service
%{_unitdir}/softether4-vpnserver.service

%changelog
* Tue May 12 2026 Mitsu <mitsu@vsict.com> - 4.44.9807-1
- Initial EL9 package
