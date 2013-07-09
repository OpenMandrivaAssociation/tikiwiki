
%if %{_use_internal_dependency_generator}
%define __noautoreq 'pear(\\(smarty.*\\|lib.*\\|tiki.*\\|db.*\\|pear.*\\|File/iCal.*\\|PHPUnit.*\\|Zend.*\\|Minify.*\\))'
%else
%define _requires_exceptions pear(\\(smarty.*\\|lib.*\\|tiki.*\\|db.*\\|pear.*\\|File/iCal.*\\|PHPUnit.*\\|Zend.*\\|Minify.*\\))
%endif.


Name:       tikiwiki
Version:    6.6
Release:    5
Summary:    A PHP-based CMS/Groupware web application with a full Wiki environment
License:    LGPLv2
Group:      System/Servers
URL:        http://www.tikiwiki.org
Source:     http://prdownloads.sourceforge.net/%{name}/tiki-%{version}.tar.bz2
Patch0:     tikiwiki-6.4-use-external-pear-modules.patch
Patch1:     tikiwiki-6.0-use-external-smarty.patch
Patch2:     tikiwiki-6.4-bootstrap.patch
Patch3:     tikiwiki-6.0-fix-Zend-module.patch
Requires:   php-pdo_mysql
Requires:   php-gd
#Requires:   php-smarty
Requires:   apache-mod_php
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
TikiWiki is an open source CMS/Groupware web application which provides
a full Wiki environment, as well as Articles, Sections/Categories,
User/Group Management (including optional LDAP), Polls and Quizzes,
File and Image Galleries, Forums, Weblogs, Calendars, Chat, Maps
and much more.

%prep
%setup -q -n tiki-%{version}
%patch0 -p 1
#patch1 -p 1
%patch2 -p 1
%patch3 -p 1

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp *.php %{buildroot}%{_datadir}/%{name}
cp *.png %{buildroot}%{_datadir}/%{name}
cp robots.txt %{buildroot}%{_datadir}/%{name}
cp license.txt %{buildroot}%{_datadir}/%{name}
cp favicon.ico %{buildroot}%{_datadir}/%{name}

for dir in css doc img images installer \
    lang lib maps modules pics; do 
    cp -pr $dir %{buildroot}%{_datadir}/%{name}
done

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}

# writable directories
for dir in backups db dump files styles temp templates templates_c whelp; do
    cp -pr $dir %{buildroot}%{_localstatedir}/lib/%{name}
    chmod 2775 %{buildroot}%{_localstatedir}/lib/%{name}/$dir
    pushd %{buildroot}%{_datadir}/%{name}
    ln -s ../../..%{_localstatedir}/lib/%{name}/$dir .
    popd
done

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/modules
mv %{buildroot}%{_datadir}/%{name}/modules/cache \
    %{buildroot}%{_localstatedir}/lib/%{name}/modules
chmod 2755 %{buildroot}%{_localstatedir}/lib/%{name}/modules/cache
pushd %{buildroot}%{_datadir}/%{name}/modules
ln -s ../../../..%{_localstatedir}/lib/%{name}/modules/cache .
popd

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/img
for dir in wiki wiki_up trackers; do
    mv %{buildroot}%{_datadir}/%{name}/img/$dir \
        %{buildroot}%{_localstatedir}/lib/%{name}/img
    chmod 2775 %{buildroot}%{_localstatedir}/lib/%{name}/img/$dir
    pushd %{buildroot}%{_datadir}/%{name}/img
    ln -s ../../../..%{_localstatedir}/lib/%{name}/img/$dir .
    popd
done

# configuration file
install -d -m 755 %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/%{name}.conf
pushd %{buildroot}%{_localstatedir}/lib/%{name}/db
ln -s ../../../..%{_sysconfdir}/%{name}.conf local.php
popd

# this is not a pear lib
mv %{buildroot}%{_datadir}/%{name}/lib/pear/Minify \
    %{buildroot}%{_datadir}/%{name}/lib/

# do not ship private copies of php libs
rm -rf %{buildroot}%{_datadir}/%{name}/lib/pear
#rm -rf %{buildroot}%{_datadir}/%{name}/lib/smarty

# cleanup
find %{buildroot}%{_datadir}/%{name} -name .htaccess -o -name README \
    | xargs rm -f
find %{buildroot}%{_localstatedir}/lib/%{name} -name .htaccess -o -name README \
    | xargs rm -f

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Tikiwiki Apache configuration
Alias /tikiwiki/styles %{_localstatedir}/lib/%{name}/styles
Alias /tiki/styles %{_localstatedir}/lib/%{name}/styles
Alias /tikiwiki %{_datadir}/%{name}
Alias /tiki %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
    Options -FollowSymLinks
    Require all granted
</Directory>

<Directory %{_datadir}/%{name}/installer>
    <FilesMatch "\.ph(p(3|4)?|tml)$">
        Deny from all
    </FilesMatch>
</Directory>

<Directory %{_datadir}/%{name}/img>
    <FilesMatch "\.ph(p(3|4)?|tml)$">
        Deny from all
    </FilesMatch>
</Directory>

<Directory %{_datadir}/%{name}/images>
    <FilesMatch "\.ph(p(3|4)?|tml)$">
        Deny from all
    </FilesMatch>
</Directory>

<Directory %{_datadir}/%{name}/lib>
    <FilesMatch "\.ph(p(3|4)?|tml)$">
        Deny from all
    </FilesMatch>
</Directory>

<Directory %{_datadir}/%{name}/lib/fckeditor>
    <FilesMatch "\.ph(p(3|4)?|tml)$">
        Allow from all
    </FilesMatch>
</Directory>

<Directory %{_datadir}/%{name}/lib/fckeditor_tiki>
    <FilesMatch "\.ph(p(3|4)?|tml)$">
        Allow from all
    </FilesMatch>
</Directory>

<Directory %{_datadir}/%{name}/lang>
    Deny from all
</Directory>

<Directory %{_datadir}/%{name}/modules>
    Deny from all
</Directory>

<Directory %{_localstatedir}/lib/%{name}/styles>
    Allow from all
</Directory>

<Directory %{_localstatedir}/lib/%{name}/db>
    Deny from all
</Directory>

# Below part is required to enable SEFURLs

EOF

cat _htaccess >> %{buildroot}%{_webappconfdir}/%{name}.conf

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%doc INSTALL README
%{_datadir}/tikiwiki
%attr(-,apache,apache) %{_localstatedir}/lib/tikiwiki
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %attr(-,apache,apache) %{_sysconfdir}/%{name}.conf


%changelog
* Fri Jan 20 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 6.6-1mdv2011.0
+ Revision: 762926
- new version 6.6
- new version 6.5 (include bugfixes and security patches)
- Update to 6.4

* Mon Dec 13 2010 Guillaume Rousse <guillomovitch@mandriva.org> 6.0-1mdv2011.0
+ Revision: 620645
- new version

* Thu Oct 28 2010 Guillaume Rousse <guillomovitch@mandriva.org> 5.3-1mdv2011.0
+ Revision: 589824
- new version
- strip private versions of pear libs and smarty

* Tue Jan 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-3mdv2010.1
+ Revision: 493876
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Thu Sep 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-2mdv2010.0
+ Revision: 428430
- don't forget to reload apache configuration after installation

* Wed Sep 02 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-1mdv2010.0
+ Revision: 424583
- new version
- use FHS setup
- TODO: drop private pear modules

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 1.9.10.1-4mdv2009.0
+ Revision: 261536
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.9.10.1-3mdv2009.0
+ Revision: 254541
- rebuild

* Sun Mar 02 2008 Olivier Blin <blino@mandriva.org> 1.9.10.1-1mdv2008.1
+ Revision: 177775
- 1.9.10.1
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Oct 28 2007 Funda Wang <fwang@mandriva.org> 1.9.8.3-1mdv2008.1
+ Revision: 102874
- update to new version 1.9.8.3

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.9.7-2mdv2008.0
+ Revision: 90337
- rebuild

* Thu Sep 06 2007 Funda Wang <fwang@mandriva.org> 1.9.7-1mdv2008.0
+ Revision: 80553
- New version 1.9.7
- Import tikiwiki



* Tue Nov 01 2005 Michael Scherer <misc@mandriva.org> 1.9.2-1mdk
- New release 1.9.2

* Wed Oct 26 2005 Michael Scherer <misc@mandriva.org> 1.9.1.1-1mdk
- New release 1.9.1.1, as reported by Franck Martin ( security fix )
- mkrel
- rpmbuildupdatable

* Mon Sep 12 2005 Franck Martin <franck@sopac.org> 1.9.1-1mdk
- security fix release

* Thu Jul 21 2005 Franck Martin <franck@sopac.org> 1.9.0-1mdk
- new release

* Tue Apr 13 2004 Olivier Blin <blino@mandrake.org> 1.8.2-1mdk
- fix rights on files
- new release

* Wed Mar 03 2004 Franck Martin <franck@sopac.org> 1.8-1mdk
- First Mandrake release
- From Olivier Blin <blino@mandrake.org> :
  - own dir
  - fix setup.sh not to chown/chgrp files
  - replace Copyright tag by License tag
  - use System/Servers group
