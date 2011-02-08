Name:           mod_wsgi
Version:        3.2
Release:        3%{?dist}
Summary:        A WSGI interface for Python web applications in Apache

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://modwsgi.org
Source0:        http://modwsgi.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        wsgi.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
BuildRequires:  python-devel

%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q


%build
%configure --enable-shared
make LDFLAGS="-L%{_libdir}" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENCE README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/wsgi.conf
%{_libdir}/httpd/modules/mod_wsgi.so


%changelog
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

