# IUS spec file for python36u-mod_wsgi, forked from Fedora

%global srcname mod_wsgi
%global python python36

%if %{defined el6}
%global __python3 /usr/bin/python3.6
%endif

%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Name:           %{python}-%{srcname}
Version:        4.6.2
Release:        2%{?dist}
Summary:        A WSGI interface for Python web applications in Apache
License:        ASL 2.0
URL:            https://modwsgi.readthedocs.io/
Source0:        https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz#/mod_wsgi-%{version}.tar.gz
Patch0:		mod_wsgi-4.6.2-exports.patch
BuildRequires:  httpd-devel < 2.4.10
BuildRequires:  %{python}-devel
BuildRequires:  %{python}-setuptools
Requires:       %{python}-setuptools
Requires:       httpd-mmn = %{_httpd_mmn}
Provides:       %{srcname} = %{version}

# Rename from python36u-mod_wsgi
Provides:       python36u-mod_wsgi = %{version}-%{release}
Provides:       python36u-mod_wsgi%{?_isa} = %{version}-%{release}
Obsoletes:      python36u-mod_wsgi < 4.6.2-2

# Suppress auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -qn %{srcname}-%{version}
%patch0 -p1

%build
export LDFLAGS="$RPM_LD_FLAGS -L%{_libdir}"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=%{__python3}
make %{?_smp_mflags}
%py3_build


%install
make install DESTDIR=%{buildroot} LIBEXECDIR=%{_httpd_moddir}
mv %{buildroot}%{_httpd_moddir}/mod_wsgi{,_python%{python3_version}}.so

cat > wsgi.conf << EOF
# NOTE:
# Only one mod_wsgi can be loaded at a time.
# Don't attempt to load if already loaded.
<IfModule !wsgi_module>
    LoadModule wsgi_module modules/mod_wsgi_python%{python3_version}.so
</IfModule>
EOF

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -Dpm 644 wsgi.conf %{buildroot}%{_httpd_confdir}/wsgi-python%{python3_version}.conf
%else
# httpd >= 2.4.x
install -Dpm 644 wsgi.conf %{buildroot}%{_httpd_modconfdir}/10-wsgi-python%{python3_version}.conf
%endif

%py3_install

%files
%license LICENSE
%doc CREDITS.rst README.rst
%config(noreplace) %{_httpd_modconfdir}/*wsgi-python%{python3_version}.conf
%{_httpd_moddir}/mod_wsgi_python%{python3_version}.so
%{python3_sitearch}/mod_wsgi-*.egg-info
%{python3_sitearch}/mod_wsgi
%{_bindir}/mod_wsgi-express


%changelog
* Fri Sep 20 2019 Carl George <carl@george.computer> - 4.6.2-2
- Rename to python36-mod_wsgi
- Switch to EPEL python3 macros

* Tue Mar 06 2018 Ben Harper <ben.harper@rackspace.com> - 4.6.2-1.ius
- Latest upstream
- add Patch1, adapted from Fedora:
  https://src.fedoraproject.org/rpms/mod_wsgi/c/c8a7642dcf4742963337e1c4e15b1263951c6ce6

* Fri Dec 15 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.24-1.ius
- Latest upstream
- update URL from Fedora:
  https://src.fedoraproject.org/rpms/mod_wsgi/c/5585f33d82e1f027384d70df753b545ac7ab36de
- build mod_wsgi-express from Fedora:
  https://src.fedoraproject.org/rpms/mod_wsgi/c/241a680c246d91f55a733aa1f45a480697c28ff4

* Thu Nov 16 2017 Carl George <carl@george.computer> - 4.5.21-1.ius
- Latest upstream

* Mon Oct 02 2017 Carl George <carl@george.computer> - 4.5.19-1.ius
- Latest upstream

* Tue Aug 29 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.18-1.ius
- Latest upstream

* Fri Jul 07 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.17-1.ius
- Latest upstream
- add EL6 support

* Fri Mar 24 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.15-1.ius
- Latest upstream

* Fri Mar 10 2017 Carl George <carl.george@rackspace.com> - 4.5.14-2.ius
- Generate configuration file in spec

* Fri Mar 03 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.14-1.ius
- Latest upstream
- Port from Fedora to IUS

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Jakub Dorňák <jakub.dornak@misli.cz> - 4.5.13-1
- Update to 4.5.13

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.5.9-2
- Rebuild for Python 3.6

* Mon Dec 05 2016 Matthias Runge <mrunge@redhat.com> - 4.5.9-1
- upgrade to 4.5.9 (rhbz#1180445)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 Richard W.M. Jones <rjones@redhat.com> - 4.4.8-1
- Upstream to 4.4.8.
- This version includes the fix for the segfault described in RHBZ#1178851.

* Mon Jan  5 2015 Jakub Dorňák <jdornak@redhat.com> - 4.4.3-1
- update to new upstream version 4.4.3 (#1176914)

* Wed Dec 17 2014 Jan Kaluza <jkaluza@redhat.com> - 4.4.1-1
- update to new upstream version 4.4.1 (#1170994)

* Wed Nov 19 2014 Jan Kaluza <jkaluza@redhat.com> - 4.3.2-1
- update to new upstream version 4.3.2 (#1104526)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Luke Macken <lmacken@redhat.com> - 3.5-1
- Update to 3.5 to fix CVE-2014-0240 (#1101863)
- Remove all of the patches, which have been applied upstream
- Update source URL for new the GitHub upstream

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 3.4-14
- rebuild for Python 3.4

* Mon Apr 28 2014 Matthias Runge <mrunge@redhat.com> - 3.4.13
- do not use conflicts between mod_wsgi packages (rhbz#1087943)

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 3.4-12
- fix _httpd_mmn expansion in absence of httpd-devel

* Fri Jan 10 2014 Matthias Runge <mrunge@redhat.com> - 3.4-11
- added python3 subpackage (thanks to Jakub Dorňák), rhbz#1035876

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  8 2013 Joe Orton <jorton@redhat.com> - 3.4-9
- modernize spec file (thanks to rcollet)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Jan Kaluza <jkaluza@redhat.com> - 3.4-7
- compile with -fno-strict-aliasing to workaround Python
  bug http://www.python.org/dev/peps/pep-3123/

* Thu Nov 22 2012 Joe Orton <jorton@redhat.com> - 3.4-6
- use _httpd_moddir macro

* Thu Nov 22 2012 Joe Orton <jorton@redhat.com> - 3.4-5
- spec file cleanups

* Wed Oct 17 2012 Joe Orton <jorton@redhat.com> - 3.4-4
- enable PR_SET_DUMPABLE in daemon process to enable core dumps

* Wed Oct 17 2012 Joe Orton <jorton@redhat.com> - 3.4-3
- use a NULL c->sbh pointer with httpd 2.4 (possible fix for #867276)
- add logging for unexpected daemon process loss

* Wed Oct 17 2012 Matthias Runge <mrunge@redhat.com> - 3.4-2
- also use RPM_LD_FLAGS for build bz. #867137

* Mon Oct 15 2012 Matthias Runge <mrunge@redhat.com> - 3.4-1
- update to upstream release 3.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Joe Orton <jorton@redhat.com> - 3.3-6
- add possible fix for daemon mode crash (#831701)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 3.3-5
- move wsgi.conf to conf.modules.d

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 3.3-4
- rebuild for httpd 2.4

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 3.3-3
- prepare for httpd 2.4.x

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 James Bowes <jbowes@redhat.com> 3.3-1
- update to 3.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  9 2010 Josh Kayse <joshkayse@fedoraproject.org> - 3.2-1
- update to 3.2

* Sun Mar 07 2010 Josh Kayse <joshkayse@fedoraproject.org> - 3.1-2
- removed conflicts as it violates fedora packaging policy

* Sun Mar 07 2010 Josh Kayse <joshkayse@fedoraproject.org> - 3.1-1
- update to 3.1
- add explicit enable-shared
- add conflicts mod_python < 3.3.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 James Bowes <jbowes@redhat.com> 2.5-1
- Update to 2.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3-2
- Rebuild for Python 2.6

* Tue Oct 28 2008 Luke Macken <lmacken@redhat.com> 2.3-1
- Update to 2.3

* Mon Sep 29 2008 James Bowes <jbowes@redhat.com> 2.1-2
- Remove requires on httpd-devel

* Wed Jul 02 2008 James Bowes <jbowes@redhat.com> 2.1-1
- Update to 2.1

* Mon Jun 16 2008 Ricky Zhou <ricky@fedoraproject.org> 1.3-4
- Build against the shared python lib.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 James Bowes <jbowes@redhat.com> 1.3-2
- Require httpd

* Sat Jan 05 2008 James Bowes <jbowes@redhat.com> 1.3-1
- Update to 1.3

* Sun Sep 30 2007 James Bowes <jbowes@redhat.com> 1.0-1
- Initial packaging for Fedora

