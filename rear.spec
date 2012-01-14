Name: rear
Version: 1.7.25
Release: 3%{?dist}
Summary: Relax and Recover (ReaR) is a Linux Disaster Recovery framework

Group: Applications/Archiving
License: GPLv2+
URL: http://rear.sourceforge.net
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# all RPM based systems seem to have this
Requires: mingetty binutils iputils tar gzip ethtool
Requires: iproute redhat-lsb
%if 0%{?fedora_version} >= 9
Requires: genisoimage rpcbind
%else
Requires: mkisofs portmap
%endif
%ifarch %ix86 x86_64 amd64
Requires: syslinux
%endif

%description
Relax and Recover (abbreviated rear) is a highly modular disaster recovery
framework for GNU/Linux based systems, but can be easily extended to other
UNIX alike systems. The disaster recovery information (and maybe the backups)
can be stored via the network, local on hard disks or USB devices, DVD/CD-R,
tape, etc. The result is also a bootable image that is capable of booting via
PXE, DVD/CD and USB media.

Relax and Recover integrates with other backup software and provides integrated
bare metal disaster recovery abilities to the compatible backup software.

%prep
%setup -q
 
%build
# no code to compile - all bash scripts

%install
rm -rf $RPM_BUILD_ROOT
# create directories
mkdir -vp \
	$RPM_BUILD_ROOT%{_mandir}/man8 \
	$RPM_BUILD_ROOT%{_datadir} \
	$RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/rear

# copy rear components into directories
cp -av usr/share/rear $RPM_BUILD_ROOT%{_datadir}/
cp -av usr/sbin/rear $RPM_BUILD_ROOT%{_sbindir}/
cp -av etc/rear $RPM_BUILD_ROOT%{_sysconfdir}/

# patch rear main script with correct locations for rear components
sed -i	-e 's#^CONFIG_DIR=.*#CONFIG_DIR="%{_sysconfdir}/rear"#' \
	-e 's#^SHARE_DIR=.*#SHARE_DIR="%{_datadir}/rear"#' \
	-e 's#^VAR_DIR=.*#VAR_DIR="%{_localstatedir}/lib/rear"#' \
	$RPM_BUILD_ROOT%{_sbindir}/rear

# update man page with correct locations
sed	-e 's#/etc#%{_sysconfdir}#' \
	-e 's#/usr/sbin#%{_sbindir}#' \
	-e 's#/usr/share#%{_datadir}#' \
	-e 's#/usr/share/doc/packages#%{_docdir}#' \
	doc/rear.8 >$RPM_BUILD_ROOT%{_mandir}/man8/rear.8

# remove doc files under  $RPM_BUILD_ROOT/usr/share/rear
rm -f $RPM_BUILD_ROOT%{_datadir}/rear/README
rm -f $RPM_BUILD_ROOT%{_datadir}/rear/CHANGES
rm -f $RPM_BUILD_ROOT%{_datadir}/rear/COPYING
rm -rf $RPM_BUILD_ROOT%{_datadir}/rear/doc/*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING CHANGES README
%doc doc/README.doc doc/relax-recover-*
%{_sbindir}/rear
%{_datadir}/rear
%{_localstatedir}/lib/rear
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/rear


%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 04 2010 Gratien D'haese <gdha at sourceforge.net> - 1.7.25-1
- added the %%ifarch part for syslinux to avoid warning on ppc/ppc64
- fixed bugzilla 600217 (missing Fedora links)

* Mon May 09 2010 Gratien D'haese <gdha at sourceforge.net> - 1.7.24-1
- added release entry

* Fri Jan 09 2010 Gratien D'haese <gdha at sourceforge.net> - 1.7.23-1
- added release entry

* Mon Nov 16 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.22-1
- Changed Requires fields for Fedora 10 and higher

* Thu Apr 02 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.20-1
- update %%_localstatedir/rear to %%_localstatedir/lib/rear

* Mon Mar 16 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.19-1
- updated description, made the spec file a bit more readable
- changed BuildArchives in BuildArch

* Sun Mar 15 2009 Schlomo Schapiro <rear at schlomo.schapiro.org> - 1.7.18-1
- updated spec file to support openSUSE 11.1

* Fri Mar 13 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.17-1
- do not gzip man page in spec file - rpmbuild will do this for us
- added extra %%doc line for excluding man page from doc itself

* Thu Feb 26 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.16-1
- make the spec better readable and removed not spec related items in changelog

* Tue Feb 04 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.15-1
- update the Fedora spec file with the 1.7.14 items
- added VAR_DIR (%%{_localstatedir}) variable to rear for /var/rear/recovery system data

* Thu Jan 29 2009 Schlomo Schapiro <rear at schlomo.schapiro.org> - 1.7.14-1
- added man page

* Tue Jan 20 2009 Gratien D'haese <gdha at sourceforge.net> - 1.7.13-1
- add COPYING license file

* Wed Dec 17 2008 Gratien D'haese <gdha at sourceforge.net> - 1.7.10-1
- remove contrib entry from %%doc line in spec file

* Mon Dec 01 2008 Gratien D'haese <gdha at sourceforge.net> - 1.7.9-1
- copy rear.sourcespec according OS_VENDOR
- correct rear.spec file according comment 11 of bugzilla #468189

* Mon Oct 27 2008 Gratien D'haese <gdha at sourceforge.net> - 1.7.8-1
- Fix rpmlint error/warnings for Fedora packaging
- updated the Summary line and %%install section

* Thu Oct 24 2008 Gratien D'haese <gdha at sourceforge.net> - 1.7.7-1
- rewrote rear.spec for Fedora Packaging request

* Tue Aug 28 2006 Schlomo Schapiro <rear at schlomo.schapiro.org> - 1.0-1
- Initial RPM Release
