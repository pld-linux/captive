#
# TODO:
#       - fix packages descriptions and groups
#       - make conditional builds switches working
#       - correct linking dependencies (now even not gnome connected libs are linked with gnome)
#       - check provides/requires
#
# Conditional build:
#%%bcond_without	gnome	# don't build gnome-vfs support
%bcond_without	lufs	# don't build LUFS support
#
Summary:	Captive - NTFS read/write filesystem for Linux
Summary(pl):	Captive - obs³uga NTFS dla Linuksa z odczytem i zapisem
Name:		captive
Version:	1.1.5
Release:	0.5
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://www.jankratochvil.net/project/captive/dist/%{name}-%{version}.tar.gz
# Source0-md5:	dfb7ce617745695e7a908609b9370fd6
Patch0:		%{name}-non_root_install.patch
Patch1:		%{name}-use_lufis.patch
Patch2:		%{name}-no_lufsd.patch
URL:		http://www.jankratochvil.net/project/captive/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk-doc
BuildRequires:	libxml2-devel >= 2.5.9
%{?with_lufs:BuildRequires:	lufs-devel}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	ntfsprogs-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libglade2-devel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	lufis
Provides:	group(captive)
Provides:	user(captive)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Captive project implements the first full read/write free access to
NTFS disk drives. You can mount your Microsoft Windows NT, 200x or XP
partition as a transparently accessible volume for your GNU/Linux.

This compatibility was achieved in the Wine way by using the original
Microsoft Windows ntfs.sys driver. It emulates the required subsystems
of the Microsoft Windows kernel by reusing one of the original
ntoskrnl.exe, ReactOS parts, or this project's own reimplementations,
on a case by case basis. Project includes the first open source
MS-Windows kernel API for Free operating systems. Involvement of the
original driver files was chosen to achieve the best and unprecedented
filesystem compatibility and safety.

%description -l pl
Projekt Captive implementuje pierwszy pe³ny, swobodny dostêp z
odczytem i zapisem do partycji NTFS. Pozwala zamontowaæ partycje z
Microsoft Windows NT, 200x i XP jako dostêpny w sposób przezroczysty
wolumen pod Linuksem.

Kompatybilno¶æ osi±gniêto metod± Wine poprzez u¿ycie oryginalnego
sterownika ntfs.sys. Captive emuluje wymagane podsystemy j±dra
Microsoft Windows poprzez wykorzystanie oryginalnego ntoskrnl.exe,
czê¶ci ReactOS-a lub w³asne implementacje z tego projektu w zale¿no¶ci
od danego przypadku. Projekt zawiera pierwsze API j±dra MS-Windows z
otwartymi ¼ród³ami dla wolnodostêpnych systemów operacyjnych. Wybrano
wykorzystanie plików oryginalnego sterownika aby osi±gn±æ lepsz±
kompatybilno¶æ i bezpieczeñstwo.

%package -n gnome-vfs2-module-captive
Summary:	Captive module for gnome-vfs
Summary(pl):	Modu³ captive dla gnome-vfs
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n gnome-vfs2-module-captive
Captive module for gnome-vfs.

%description -n gnome-vfs2-module-captive -l pl
Modu³ captive dla gnome-vfs.

%package install
Summary:	Windows filesystem drivers installer for captive
Summary(pl):	Instalator windowsowych sterowników systemu plików dla captive
Group:		Base/Utilities
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	ntfsprogs

%description install
Windows filesystem drivers installer for captive.

%description install -l pl
Instalator windowsowych sterowników systemu plików dla captive.

%package devel
Summary:	Captive - NTFS read/write filesystem for Linux
Summary(pl):	Captive - obs³uga NTFS dla Linuksa z odczytem i zapisem
Group:		Base/Utilities
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
This package contains header files and development libraries for captive.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe i biblioteki deweloperskie dla captive.

%package libs
Summary:	Captive - NTFS read/write filesystem for Linux
Summary(pl):	Captive - obs³uga NTFS dla Linuksa z odczytem i zapisem
Group:		Base/Utilities

%description libs
This package contains shared libraries for captive.

%description libs -l pl
Pakiet zawiera biblioteki dzielone dla captive.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cd src/libcaptive/sandbox
orbit-idl-2 sandbox.idl

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-lufs \
	--enable-install-pkg \
	--with-readline \
	--enable-sandbox-setuid=captive \
	--enable-sandbox-setgid=captive \
	--enable-sandbox-chroot=/var/lib/captive \
	--enable-man-pages \
	--enable-sbin-mountdir=/sbin \
	--enable-sbin-mount-fs=ntfs:fastfat:cdfs:ext2fsd \
	--with-orbit-line=link \
	--with-tmpdir=/tmp \
	--localstatedir=/var \
	--enable-gtk-doc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_docdir}
mv $RPM_BUILD_ROOT/usr/share/gtk-doc  $RPM_BUILD_ROOT%{_docdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid captive`" ]; then
	if [ "`/usr/bin/getgid captive`" != "141" ]; then
		echo "Error: group captive doesn't have gid=141. Correct this before installing captive." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 141 -r -f captive
fi
if [ -n "`/bin/id -u captive 2>/dev/null`" ]; then
	if [ "`/bin/id -u captive`" != "141" ]; then
		echo "Error: user captive doesn't have uid=141. Correct this before installing captive." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 141 -r -d /var/lib/captive -s /bin/false -c "Captive User" -g captive captive 1>&2
fi

%post 	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/captive-sandbox-server
%attr(755,root,root) /sbin/*
%{_mandir}/man1/captive-cmdline.1*
%{_mandir}/man1/captive-sandbox-server.1*
%{_mandir}/man7/*
%{_mandir}/man8/*
/var/lib/captive
/etc/w32-mod-id.captivemodid.xml

%files -n gnome-vfs2-module-captive
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/libcaptive-gnomevfs*.so
%{_sysconfdir}/gnome-vfs-2.0/modules/captive.conf

%files install
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/captive-install*
%{_mandir}/man1/captive-install*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaptive.so
%attr(755,root,root) %{_libdir}/liblufs-captivefs.so
%{_libdir}/lib*.la
%{_includedir}/captive
%{_gtkdocdir}/captive-apiref

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaptive-1.1.5.so
%attr(755,root,root) %{_libdir}/liblufs-captivefs-1.1.5.so
