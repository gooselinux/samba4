%define main_release 23
%define samba4_version 4.0.0

%define talloc_version 2.0.1
%define tdb_version 1.1.8
%define tevent_version 0.9.8
%define ldb_version 0.9.10

%define pre_release alpha11

%define tarball_name samba-4.0.0%{pre_release}

%define samba4_release %{main_release}.%{pre_release}%{?dist}
# We need a higher talloc release to address previous releases done as
# part of the samba3 package.
%define talloc_release %{main_release}%{?dist}
%define tdb_release %{main_release}%{?dist}
%define tevent_release %{main_release}%{?dist}
%define ldb_release %{main_release}%{?dist}

# Most of these subpackages are disabled because they are not
# needed by OpenChange, and to avoid file conflicts with Samba3.
%define enable_samba4  0
%define enable_client  0
%define enable_common  0
%define enable_python  0
%define enable_winbind 0
%define enable_talloc  0
%define enable_tdb     0
%define enable_tevent  0
%define enable_ldb     1

# Install libraries not needed by OpenChange.
%define all_libraries  0

%{!?python_libdir: %define python_libdir %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1,1)")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Licensing Note: Some of the libraries are GPLv3+, others are LGPLv3+.
# The rest of the code is GPLv3+.  Library licensing is still volatile,
# and subject to change.

Name: samba4
Version: %{samba4_version}
Release: %{samba4_release}
Group: System Environment/Daemons
Summary: The Samba4 CIFS and AD client and server suite
License: GPLv3+ and LGPLv3+
URL: http://www.samba.org/
Source: http://download.samba.org/samba/ftp/samba4/%{tarball_name}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Red Hat specific replacement-files
Source1: %{name}.log
Source4: %{name}.sysconfig
Source5: %{name}.init

Patch1: samba-4.0.0alpha6-GIT-3508a66-undefined-comparison_fn_t.patch

Requires(pre): /usr/sbin/groupadd

%if %enable_samba4
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service
%endif

%if %enable_common
Requires(pre): %{name}-common = %{version}-%{release}
%endif

Requires: logrotate
Requires: pam
Requires: perl(Parse::Yapp)

BuildRequires: e2fsprogs-devel
BuildRequires: libacl-devel
BuildRequires: libaio-devel
BuildRequires: libattr-devel
BuildRequires: ncurses-devel
BuildRequires: pam-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Parse::Yapp)
BuildRequires: popt-devel
BuildRequires: python-devel
BuildRequires: readline-devel
BuildRequires: sed
BuildRequires: autoconf
BuildRequires: openldap-devel
BuildRequires: libxslt
BuildRequires: docbook-style-xsl

%if ! %enable_talloc
BuildRequires: libtalloc-devel >= %{talloc_version}
%endif
%if ! %enable_tdb
BuildRequires: libtdb-devel >= %{tdb_version}
%endif
%if ! %enable_tevent
BuildRequires: libtevent-devel >= %{tevent_version}
%endif
%if ! %enable_ldb
BuildRequires: libldb-devel >= %{ldb_version}
%endif

%description

Samba 4 is the ambitious next version of the Samba suite that is being
developed in parallel to the stable 3.0 series. The main emphasis in
this branch is support for the Active Directory logon protocols used
by Windows 2000 and above.

%if %enable_client
%package client
Summary: Samba client programs
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description client
The %{name}-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.
%endif

%package libs
Summary: Samba libraries
Group: Applications/System

%description libs
The %{name}-libs package contains the libraries needed by programs that
link against the SMB, RPC and other protocols provided by the Samba suite.

%if %enable_python
%package python
Summary: Samba Python libraries
Group: Applications/System
Requires: %{name}-libs = %{version}-%{release}

%description python
The %{name}-python package contains the Python libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python programs.
%endif

%package devel
Summary: Developer tools for Samba libraries
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.

%package pidl
Summary: Perl IDL compiler
Group: Development/Tools
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description pidl
The %{name}-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols

%if %enable_common
%package common
Summary: Files used by both Samba servers and clients
Group: Applications/System
Requires: %{name}-libs = %{version}-%{release}

%description common
%{Name}-common provides files necessary for both the server and client
packages of Samba.
%endif

%if %enable_winbind
%package winbind
Summary: Samba winbind
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description winbind
The samba-winbind package provides the winbind NSS library, and some
client tools.  Winbind enables Linux to be a full member in Windows
domains and to use Windows user and group accounts on Linux.
%endif

%if %enable_talloc
%package -n libtalloc
Group: Development/Libraries
Summary: A hierarchical allocator
Version: %{talloc_version}
Release: %{talloc_release}

%description -n libtalloc
A library that implements a hierarchical allocator with destructors.

%package -n libtalloc-devel
Group: Development/Libraries
Summary: Developer tools for the Talloc library
Version: %{talloc_version}
Release: %{talloc_release}
Requires: libtalloc = %{talloc_version}-%{talloc_release}

%description -n libtalloc-devel
Header files needed to develop programs that link against the Talloc library.
%endif

%if %enable_tdb
%package -n libtdb
Group: Development/Libraries
Summary: A bdb like database engine
Version: %{tdb_version}
Release: %{tdb_release}

%description -n libtdb
A library that implements a single key database with transactions support.

%package -n tdb-tools
Group: Development/Libraries
Summary: Tools to manage TDB files
Version: %{tdb_version}
Release: %{tdb_release}
Requires: libtdb >= %{tdb_version}

%description -n tdb-tools
Tools to manage TDB files

%package -n libtdb-devel
Group: Development/Libraries
Summary: Developer tools for the TDB library
Version: %{tdb_version}
Release: %{tdb_release}
Requires: libtdb = %{tdb_version}-%{tdb_release}

%description -n libtdb-devel
Header files needed to develop programs that link against the TDB library.
%endif

%if %enable_tevent
%package -n libtevent
Group: Development/Libraries
Summary: An event system library
Version: %{tevent_version}
Release: %{tevent_release}
Requires: libtalloc >= %{talloc_version}

%description -n libtevent
A library that implements an event driven system, that uses epoll/select to
fire events when file status changes, supports also timer events.

%package -n libtevent-devel
Group: Development/Libraries
Summary: Developer tools for the tevent library
Version: %{tevent_version}
Release: %{tevent_release}
Requires: libtevent = %{tevent_version}-%{tevent_release}
Requires: libtalloc-devel >= %{talloc_version}

%description -n libtevent-devel
Header files needed to develop programs that link against the tevent library.
%endif

%if %enable_ldb
%package -n libldb
Group: Development/Libraries
Summary: A schema-less, ldap like, API and database
Version: %{ldb_version}
Release: %{ldb_release}
Requires: libtalloc >= %{talloc_version}
Requires: libtdb >= %{tdb_version}
Requires: libtevent >= %{tevent_version}

%description -n libldb
An extensible library that implements and LDAP like API to access remote LDAP
servers, or use local tdb databases.

%package -n ldb-tools
Group: Development/Libraries
Summary: Tools to manage LDB files
Version: %{ldb_version}
Release: %{ldb_release}
Requires: libldb >= %{ldb_version}

%description -n ldb-tools
Tools to manage LDB files

%package -n libldb-devel
Group: Development/Libraries
Summary: Developer tools for the LDB library
Version: %{ldb_version}
Release: %{ldb_release}
Requires: libldb = %{ldb_version}-%{ldb_release}
Requires: libtdb-devel >= %{tdb_version}
Requires: libtalloc-devel >= %{talloc_version}
Requires: libtevent-devel >= %{tevent_version}

%description -n libldb-devel
Header files needed to develop programs that link against the LDB library.
%endif

%prep
%setup -q -n %{tarball_name}

# copy Red Hat specific scripts

%patch1 -p1 -b .undefined-comparison_fn_t

mv source4/VERSION source4/VERSION.orig
sed -e 's/SAMBA_VERSION_VENDOR_SUFFIX=$/&%{release}/' < source4/VERSION.orig > source4/VERSION
#cd source4
#script/mkversion.sh
#cd ..

# For now copy libraries into another part of the tree, because the samba4
# build would fail if it finds standalone bits already built
mkdir -p standalone/lib
cp -a lib/replace standalone/lib/replace
%if %enable_talloc
cp -a lib/talloc standalone/lib/talloc
%endif
%if %enable_tdb
cp -a lib/tdb standalone/lib/tdb
%endif
%if %enable_tevent
cp -a lib/tevent standalone/lib/tevent
%endif
%if %enable_ldb
cp -a source4/lib/ldb standalone/lib/ldb
%endif

%build
%define shared_build_dir %{_sourcedir}/standalone/sbtmp
export LD_LIBRARY_PATH=%{shared_build_dir}/lib
export CFLAGS="$RPM_OPT_FLAGS -I%{shared_build_dir}/include -fno-strict-aliasing"

# talloc
%if %enable_talloc
pushd standalone/lib/talloc
./autogen.sh
%configure --with-shared-build-dir=%{shared_build_dir}
make shared-build %{?_smp_mflags}
popd
%endif

# tdb
%if %enable_tdb
pushd standalone/lib/tdb
./autogen.sh
%configure --with-shared-build-dir=%{shared_build_dir}
make shared-build %{?_smp_mflags}
popd
%endif

# tevent
%if %enable_tevent
pushd standalone/lib/tevent
./autogen.sh
%configure --with-shared-build-dir=%{shared_build_dir}
make shared-build %{?_smp_mflags}
popd
%endif

# ldb
%if %enable_ldb
pushd standalone/lib/ldb
./autogen.sh
%configure --with-shared-build-dir=%{shared_build_dir}
make shared-build  # %{?_smp_mflags}  XXX Causes build failure on F10
popd
%endif

export LD_LIBRARY_PATH

cd source4

%configure \
  --enable-fhs \
  --with-lockdir=/var/lib/%{name} \
  --with-piddir=/var/run \
  --with-privatedir=/var/lib/%{name}/private \
  --with-logfilebase=/var/log/%{name} \
  --sysconfdir=%{_sysconfdir}/%{name} \
  --with-winbindd-socket-dir=/var/run/winbind \
  --with-ntp-signd-socket-dir=/var/run/ntp_signd \
  --disable-gnutls

# Build PIDL for installation into vendor directories before
# 'make proto' gets to it.
(cd ../pidl && %{__perl} Makefile.PL INSTALLDIRS=vendor )

# Builds using PIDL the IDL and many other things.
#make proto
#make everything
make

%install
rm -rf $RPM_BUILD_ROOT

cd source4

# Don't call 'make install' as we want to call out to the PIDL
# install manually.
make install DESTDIR=$RPM_BUILD_ROOT

# Undo the PIDL install, we want to try again with the right options.
rm -rf $RPM_BUILD_ROOT%{_libdir}/perl5
rm -rf $RPM_BUILD_ROOT%{_datadir}/perl5

# Install PIDL.
( cd ../pidl && make install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT )

# Clean out crap left behind by the PIDL install.
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

cd ..

%if %enable_samba4
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%endif

mkdir -p $RPM_BUILD_ROOT/var/run/winbindd
mkdir -p $RPM_BUILD_ROOT/var/run/ntp_signd
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}/winbindd_privileged
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}/
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}/old

mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}/private
mkdir -p $RPM_BUILD_ROOT/var/lib/%{name}/sysvol

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%if %enable_samba4
# Install other stuff.
install -m755 %{SOURCE5} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
install -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%endif

%if %enable_winbind
mkdir -p $RPM_BUILD_ROOT%{_lib}
ln -sf ../%{_libdir}/libnss_winbind.so  $RPM_BUILD_ROOT%{_lib}/libnss_winbind.so.2
%else
rm $RPM_BUILD_ROOT%{_bindir}/ntlm_auth
rm $RPM_BUILD_ROOT%{_bindir}/wbinfo
rm $RPM_BUILD_ROOT%{_libdir}/libnss_winbind.so
%endif

# libs {
mkdir -p $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}

# }

# Clean out some stuff we don't want in the Fedora package.
rm $RPM_BUILD_ROOT%{_bindir}/mount.cifs
rm $RPM_BUILD_ROOT%{_bindir}/umount.cifs
#rm $RPM_BUILD_ROOT%{_bindir}/epdump
rm $RPM_BUILD_ROOT%{_bindir}/gentest
rm $RPM_BUILD_ROOT%{_bindir}/getntacl
rm $RPM_BUILD_ROOT%{_bindir}/locktest
rm $RPM_BUILD_ROOT%{_bindir}/masktest
#rm $RPM_BUILD_ROOT%{_bindir}/minschema
rm $RPM_BUILD_ROOT%{_bindir}/ndrdump
rm $RPM_BUILD_ROOT%{_bindir}/nsstest
rm $RPM_BUILD_ROOT%{_bindir}/setnttoken
rm $RPM_BUILD_ROOT%{_bindir}/smbtorture
#rm $RPM_BUILD_ROOT%{_bindir}/subunitrun
#depending on the environemnt this file might or might not be generated
rm -f $RPM_BUILD_ROOT%{_bindir}/tdbtorture

# Avoids a file conflict with perl-Parse-Yapp.
rm -rf $RPM_BUILD_ROOT%{perl_vendorlib}/Parse/Yapp

# Remove files for disabled subpackages.
%if ! %enable_samba4
#rm $RPM_BUILD_ROOT%{_bindir}/mymachinepw
rm $RPM_BUILD_ROOT%{_sbindir}/provision
rm $RPM_BUILD_ROOT%{_sbindir}/samba
rm $RPM_BUILD_ROOT%{_sbindir}/upgradeprovision
rm -r $RPM_BUILD_ROOT%{_datadir}/samba/setup
%endif
%if ! %enable_client
rm $RPM_BUILD_ROOT%{_bindir}/nmblookup
rm $RPM_BUILD_ROOT%{_bindir}/smbclient
rm $RPM_BUILD_ROOT%{_bindir}/cifsdd
%endif
%if ! %enable_common
rm $RPM_BUILD_ROOT%{_bindir}/net
rm $RPM_BUILD_ROOT%{_bindir}/regdiff
rm $RPM_BUILD_ROOT%{_bindir}/regpatch
rm $RPM_BUILD_ROOT%{_bindir}/regshell
rm $RPM_BUILD_ROOT%{_bindir}/regtree
rm $RPM_BUILD_ROOT%{_bindir}/testparm
%endif
%if ! %all_libraries
rm $RPM_BUILD_ROOT%{_libdir}/libdcerpc_atsvc.so
rm $RPM_BUILD_ROOT%{_libdir}/libdcerpc_atsvc.so.*
rm $RPM_BUILD_ROOT%{_libdir}/libgensec.so
rm $RPM_BUILD_ROOT%{_libdir}/libgensec.so.*
rm $RPM_BUILD_ROOT%{_libdir}/libregistry.so
rm $RPM_BUILD_ROOT%{_libdir}/libregistry.so.*
rm $RPM_BUILD_ROOT%{_libdir}/libtorture.so
rm $RPM_BUILD_ROOT%{_libdir}/libtorture.so.*
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/dcerpc_atsvc.pc
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gensec.pc
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/registry.pc
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/torture.pc
rm $RPM_BUILD_ROOT%{_includedir}/samba-4.0/gensec.h
rm $RPM_BUILD_ROOT%{_includedir}/samba-4.0/registry.h
%endif

# the samba4 build process rebuilds libraries internally,
# but we want to use the standalone build for now.
rm $RPM_BUILD_ROOT%{_libdir}/libldb.so*
#rm $RPM_BUILD_ROOT%{_bindir}/ad2oLschema
rm $RPM_BUILD_ROOT%{_bindir}/ldbadd
rm $RPM_BUILD_ROOT%{_bindir}/ldbdel
rm $RPM_BUILD_ROOT%{_bindir}/ldbedit
rm $RPM_BUILD_ROOT%{_bindir}/ldbmodify
rm $RPM_BUILD_ROOT%{_bindir}/ldbrename
rm $RPM_BUILD_ROOT%{_bindir}/ldbsearch
rm $RPM_BUILD_ROOT%{_bindir}/oLschema2ldif
rm -f $RPM_BUILD_ROOT%{_bindir}/tdbbackup
rm -f $RPM_BUILD_ROOT%{_bindir}/tdbdump
rm -f $RPM_BUILD_ROOT%{_bindir}/tdbtool


# talloc
%if %enable_talloc
pushd standalone/lib/talloc
make install DESTDIR=$RPM_BUILD_ROOT
ln -s libtalloc.so.%{talloc_version} $RPM_BUILD_ROOT%{_libdir}/libtalloc.so
popd
%endif

# tdb
%if %enable_tdb
pushd standalone/lib/tdb
make install DESTDIR=$RPM_BUILD_ROOT
ln -s libtdb.so.%{tdb_version} $RPM_BUILD_ROOT%{_libdir}/libtdb.so
popd
%endif

# tevent
%if %enable_tevent
pushd standalone/lib/tevent
make install DESTDIR=$RPM_BUILD_ROOT
ln -s libtevent.so.%{tevent_version} $RPM_BUILD_ROOT%{_libdir}/libtevent.so
popd
%endif

# ldb
%if %enable_ldb
pushd standalone/lib/ldb
make install DESTDIR=$RPM_BUILD_ROOT
ln -s -f libldb.so.%{ldb_version} $RPM_BUILD_ROOT%{_libdir}/libldb.so
mkdir $RPM_BUILD_ROOT%{_libdir}/ldb
popd
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a

%if ! %enable_python
rm -r $RPM_BUILD_ROOT%{python_sitearch}/*
rm -fr $RPM_BUILD_ROOT%{python_libdir}/lib
%endif

# These may be created in non mock systems, but we do not want to package them
# for now
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ad2oLschema.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/oLschema2ldif.1
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/talloc.i

# This makes the right links, as rpmlint requires that
# the ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n $RPM_BUILD_ROOT%{_libdir}

# Fix up permission on perl install.
%{_fixperms} $RPM_BUILD_ROOT%{perl_vendorlib}

# Fix up permissions in source tree, for debuginfo.
find source4/heimdal -type f | xargs chmod -x

%clean
rm -fr %{shared_build_dir}
rm -rf $RPM_BUILD_ROOT

%pre
%if %enable_winbind
getent group wbpriv >/dev/null || groupadd -g 88 wbpriv
%endif
exit 0

%post
%if %enable_samba4
/sbin/chkconfig --add %{name}
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif
exit 0

%preun
%if %enable_samba4
if [ $1 = 0 ] ; then
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}
fi
%endif
exit 0

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%if %enable_talloc
%post -n libtalloc
/sbin/ldconfig

%postun -n libtalloc
/sbin/ldconfig
%endif

%if %enable_tdb
%post -n libtdb
/sbin/ldconfig

%postun -n libtdb
/sbin/ldconfig
%endif

%if %enable_tevent
%post -n libtevent
/sbin/ldconfig

%postun -n libtevent
/sbin/ldconfig
%endif

%if %enable_ldb
%post -n libldb
/sbin/ldconfig

%postun -n libldb
/sbin/ldconfig
%endif


%files
%defattr(-,root,root,-)
%doc COPYING WHATSNEW4.txt
%if %enable_samba4
%{_bindir}/mymachinepw
%{_bindir}/smbstatus
%{_sbindir}/provision
%{_sbindir}/samba
%{_sbindir}/upgradeprovision
%{_datadir}/samba/setup
%dir /var/lib/%{name}/sysvol
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0700,root,root) %dir /var/log/%{name}
%attr(0700,root,root) %dir /var/log/%{name}/old
%endif

%files libs
%defattr(-,root,root,-)
%doc PFIF.txt
%dir %{_datadir}/samba
%{_datadir}/samba/*.dat
%{_libdir}/libdcerpc.so.*
%{_libdir}/libdcerpc_samr.so.*
%{_libdir}/libndr.so.*
%{_libdir}/libndr_standard.so.*
%{_libdir}/libsamba-hostconfig.so.*
%{_libdir}/libsamba-util.so.*
#%{_libdir}/libtorture.so.*
#Only needed if Samba's build produces plugins
#%{_libdir}/samba
%dir %{_sysconfdir}/%{name}
#Need to mark this as being owned by Samba, but it is normally created
#by the provision script, which runs best if there is no existing
#smb.conf
#%config(noreplace) %{_sysconfdir}/%{name}/smb.conf
%if %all_libraries
%{_libdir}/libdcerpc_atsvc.so.*
%{_libdir}/libgensec.so.*
%{_libdir}/libregistry.so.*
%endif

%if %enable_winbind
%files winbind
%defattr(-,root,root,-)
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_libdir}/libnss_winbind.so
/%{_lib}/libnss_winbind.so.2
%dir /var/run/winbindd
%attr(750,root,wbpriv) %dir /var/lib/%{name}/winbindd_privileged
%endif

%if %enable_python
%files python
%defattr(-,root,root,-)
%{python_sitearch}/*
%{python_libdir}/lib
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/samba-4.0
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc_samr.so
%{_libdir}/libndr.so
%{_libdir}/libndr_standard.so
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/libsamba-util.so
#%{_libdir}/libtorture.so
%{_libdir}/pkgconfig/dcerpc.pc
%{_libdir}/pkgconfig/dcerpc_samr.pc
%{_libdir}/pkgconfig/ndr.pc
%{_libdir}/pkgconfig/ndr_standard.pc
%{_libdir}/pkgconfig/samba-hostconfig.pc
#%{_libdir}/pkgconfig/torture.pc
%if %all_libraries
%{_libdir}/libdcerpc_atsvc.so
%{_libdir}/libgensec.so
%{_libdir}/libregistry.so
%{_libdir}/pkgconfig/dcerpc_atsvc.pc
%{_libdir}/pkgconfig/gensec.pc
%{_libdir}/pkgconfig/registry.pc
%{_includedir}/samba-4.0/gen_ndr
%endif

%files pidl
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man1/pidl*
%{_mandir}/man3/Parse*
%attr(755,root,root) %{_bindir}/pidl

%if %enable_client
%files client
%defattr(-,root,root,-)
%{_bindir}/nmblookup
%{_bindir}/smbclient
%{_bindir}/cifsdd
%endif

%if %enable_common
%files common
%defattr(-,root,root,-)
%{_bindir}/net
%{_bindir}/testparm
%{_bindir}/regdiff
%{_bindir}/regpatch
%{_bindir}/regshell
%{_bindir}/regtree

%dir /var/lib/%{name}
%attr(700,root,root) %dir /var/lib/%{name}/private
# We don't want to put a smb.conf in by default, provision should create it
#%config(noreplace) %{_sysconfdir}/%{name}/smb.conf
%endif

%if %enable_talloc
%files -n libtalloc
%defattr(-,root,root,-)
%{_libdir}/libtalloc.so.*

%files -n libtalloc-devel
%defattr(-,root,root,-)
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc.3.gz
%endif

%if %enable_tdb
%files -n libtdb
%defattr(-,root,root,-)
%{_libdir}/libtdb.so.*

%files -n tdb-tools
%defattr(-,root,root,-)
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
#FIXME: currently not installed in standalone build
#%{_mandir}/man8/tdbbackup.8*
#%{_mandir}/man8/tdbdump.8*
#%{_mandir}/man8/tdbtool.8*

%files -n libtdb-devel
%defattr(-,root,root,-)
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc
%endif

%if %enable_tevent
%files -n libtevent
%defattr(-,root,root,-)
%{_libdir}/libtevent.so.*

%files -n libtevent-devel
%defattr(-,root,root,-)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc
%endif

%if %enable_ldb
%files -n libldb
%defattr(-,root,root,-)
%{_libdir}/libldb.so.*
%dir %{_libdir}/ldb
#%{_libdir}/ldb/*

%files -n ldb-tools
%defattr(-,root,root,-)
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_bindir}/ldbtest
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*
#%{_mandir}/man1/ad2oLschema.1.gz
#%{_mandir}/man1/oLschema2ldif.1.gz

%files -n libldb-devel
%defattr(-,root,root,-)
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb.h
%{_libdir}/libldb.so
%{_libdir}/pkgconfig/ldb.pc
%{_mandir}/man3/ldb.3.gz
%endif

%changelog
* Mon Jun 07 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-23.alpha11
- Add "-fno-strict-aliasing" to CFLAGS (RH bug #596209)

* Mon Feb 01 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-22.alpha11
- Upgrade to alpha11 (RH bug #560025)

* Fri Jan 29 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-19.1.alpha8_git20090916
- Fix rpmlint warnings.

* Mon Jan 11 2010 Stepan Kasal <skasal@redhat.com> - 4.0.0-19.alpha8_git20090916
- fix typo in samba4_release
- rebuild against perl-5.10.1

* Thu Dec 03 2009 Dennis Gregorovic <dgregor@redhat.com> - 4.0.0-18.1alpha8_git20090916.1
- Rebuilt for RHEL 6

* Thu Sep 17 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-18.1.alpha8_git20090916
- Need docbook stuff to build man pages

* Thu Sep 17 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-18.alpha8_git20090916
- Fix broken dependencies

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-17.alpha8_git20090916
- Upgrade to alpha8-git20090916

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-16.alpha7
- Stop building libtevent, it is now an external package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-15.2alpha7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-15.2alpha7
- Fix dependency

* Sat May 09 2009  Simo Sorce <ssorce@redhat.com> - 4.0.0-15.1alpha7
- Don't build talloc and tdb, they are now separate packages

* Mon Apr 06 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-14alpha7
- Fix a build issue in samba4-common (RH bug #494243).

* Wed Mar 25 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-13alpha7
- rebuild with correct CFLAGS (also fixes debuginfo)

* Tue Mar 10 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-12alpha7
- Second part of fix for the ldb segfault problem from upstream

* Mon Mar 09 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-11alpha7
- Add upstream patch to fix a problem within ldb

* Sun Mar 08 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-10alpha7
- Remove ldb.pc from samba4-devel (RH bug #489186).

* Wed Mar  4 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-9alpha7
- Make talloc,tdb,tevent,ldb easy to exclude using defines
- Fix package for non-mock "dirty" systems by deleting additional
  files we are not interested in atm

* Wed Mar  4 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-8alpha7
- Fix typo in Requires

* Mon Mar  2 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-7alpha7
- Compile and have separate packages for additional samba libraries
  Package in their own packages: talloc, tdb, tevent, ldb

* Fri Feb 27 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-4.alpha7
- Update to 4.0.0alpha7

* Wed Feb 25 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-3.alpha6
- Formal package review cleanups.

* Mon Feb 23 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-2.alpha6
- Disable subpackages not needed by OpenChange.
- Incorporate package review feedback.

* Mon Jan 19 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-1.alpha6
- Update to 4.0.0alpha6

* Wed Dec 17 2008 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-0.8.alpha6.GIT.3508a66
- Fix another file conflict: smbstatus

* Fri Dec 12 2008 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-0.7.alpha6.GIT.3508a66
- Disable the winbind subpackage because it conflicts with samba-winbind
  and isn't needed to support OpenChange.

* Fri Dec 12 2008 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-0.6.alpha6.GIT.3508a66
- Update to the GIT revision OpenChange is now requiring.

* Fri Aug 29 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.5.alpha5.fc10
- Fix licence tag (the binaries are built into a GPLv3 whole, so the BSD licence need not be mentioned)

* Fri Jul 25 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.4.alpha5.fc10
- Remove talloc and tdb dependency (per https://bugzilla.redhat.com/show_bug.cgi?id=453083)
- Fix deps on chkconfig and service to main pkg (not -common) 
  (per https://bugzilla.redhat.com/show_bug.cgi?id=453083)

* Mon Jul 21 2008 Brad Hards <bradh@frogmouth.ent> - 0:4.0.0-0.3.alpha5.fc10
- Use --sysconfdir instead of --with-configdir
- Add patch for C++ header compatibility

* Mon Jun 30 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.2.alpha5.fc9
- Update per review feedback
- Update for alpha5

* Thu Jun 26 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.1.alpha4.fc9
- Rework Fedora's Samba 3.2.0-1.rc2.16 spec file for Samba4
