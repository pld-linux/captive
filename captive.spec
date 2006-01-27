Summary:	Captive - NTFS read/write filesystem for Linux
Summary(pl):	Captive - obs³uga NTFS dla Linuksa z odczytem i zapisem
Name:		captive
Version:	1.1.6.1
Release:	1
License:	GPL
Group:		Base/Kernel
Source0:	http://www.jankratochvil.net/project/captive/dist/%{name}-%{version}.tar.gz
# Source0-md5:	81fcc21997cf46ad9440d1a1464a384e
Patch0:		%{name}-non_root_install.patch
Patch1:		%{name}-popt_link.patch
Patch2:		%{name}-configure_ac.patch
URL:		http://www.jankratochvil.net/project/captive/
BuildRequires:	ORBit2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	libfuse-devel >= 2.4.1
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.5.9
BuildRequires:	openssl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.202
Provides:	group(captive)
Provides:	user(captive)
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	ntfsprogs >= 1.8.0
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

%package devel
Summary:	Header files for captive library
Summary(pl):	Pliki nag³ówkowe biblioteki captive
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for captive.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki captive.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
# Fix not finished moving captive-sandbox-server to libdir
sed -i -e 's/--sandbox-server=@sbindir@/--sandbox-server=@libdir@/g' src/client/gnomevfs/captive.conf.in

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	--disable-static \
	--with-readline \
	--disable-bug-replay \
	--enable-lufs=no \
	--enable-fuse=yes \
	--disable-install-pkg \
	--enable-sandbox-setuid=captive \
	--enable-sandbox-setgid=captive \
	--enable-sandbox-chroot=/var/lib/captive \
	--enable-man-pages \
	--enable-sbin-mountdir=/sbin \
	--enable-sbin-mount-fs=ntfs:fastfat:cdfs:ext2fsd \
	--with-oribt-line=link \
	--with-tmpdir=/tmp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/libcaptive-gnomevfs.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 141 captive
%useradd -u 141 -r -d /var/lib/captive -s /bin/false -c "Captive User" -g captive captive

%postun 
if [ "$1" = "0" ]; then
	%userremove captive
	%groupremove captive
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/captive-cmdline
#%attr(755,root,root) %{_bindir}/captive-bug-replay was here earlier.
%%attr(755,root,root) %{_libdir}/captive-sandbox-server
%{_sysconfdir}/gnome-vfs-2.0/modules/*
%{_sysconfdir}/w32-mod-id.captivemodid.xml
%attr(755,root,root) %{_libdir}/libcaptive-*.so
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/libcaptive-gnomevfs*.so
%{_mandir}/man?/*
%{_var}/lib/captive

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaptive.so
%{_libdir}/libcaptive.la
%{_includedir}/captive
