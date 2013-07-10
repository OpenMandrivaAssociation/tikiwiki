%define _requires_exceptions pear(\\(smarty.*\\|lib.*\\|tiki.*\\|db.*\\|pear.*\\|File/iCal.*\\|PHPUnit.*\\|Zend.*\\|Minify.*\\))

Name:		tikiwiki
Version:	6.0
Release:	%mkrel 1
Summary:	A PHP-based CMS/Groupware web application with a full Wiki environment
License:	LGPL
Group:		System/Servers
URL:		http://www.tikiwiki.org
Source0:	http://prdownloads.sourceforge.net/%{name}/tiki-%{version}.tar.bz2
Patch0:		tikiwiki-6.0-use-external-pear-modules.patch
Patch1:		tikiwiki-6.0-use-external-smarty.patch
Patch2:		tikiwiki-5.3-bootstrap.patch
Patch3:		tikiwiki-6.0-fix-Zend-module.patch
Requires:	php-pdo
Requires:	php-gd
Requires:	apache-mod_php
BuildArch:	noarch

%description
TikiWiki is an open source CMS/Groupware web application which provides
a full Wiki environment, as well as Articles, Sections/Categories,
User/Group Management (including optional LDAP), Polls and Quizzes,
File and Image Galleries, Forums, Weblogs, Calendars, Chat, Maps
and much more.

%prep
%setup -q -n tiki-%{version}
%patch0 -p 1
%patch2 -p 1
%patch3 -p 1

%build

%install
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
Alias /tikiwiki %{_datadir}/%{name}

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
EOF

%files
%doc INSTALL README
%{_datadir}/tikiwiki
%attr(-,apache,apache) %{_localstatedir}/lib/tikiwiki
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %attr(-,apache,apache) %{_sysconfdir}/%{name}.conf
