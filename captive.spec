#
# Conditional build:
#%%bcond_without	gnome	# don't build gnome-vfs support
%bcond_without	lufs	# don't build LUFS support
#
Summary:	Captive - NTFS read/write filesystem for Linux
Summary(pl):	Captive - obs³uga NTFS dla Linuksa z odczytem i zapisem
Name:		captive
Version:	1.1.5
Release:	0.1
License:	GPL
Group:		Base/Kernel
Source0:	http://www.jankratochvil.net/project/captive/dist/%{name}-%{version}.tar.gz
# Source0-md5:	dfb7ce617745695e7a908609b9370fd6
Patch0:		%{name}-non_root_install.patch
Patch1:		%{name}-popt_link.patch
URL:		http://www.jankratochvil.net/project/captive/
BuildRequires:	ORBit2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	libxml2-devel >= 2.5.9
%{?with_lufs:BuildRequires:	lufs-devel}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
#%{__libtoolize}
#%{__aclocal} -I macros
#%{__autoconf}
#%{__autoheader}
#%{__automake}
%configure \
	--enable-shared \
	--disable-static \
	--with-readline \
	--disable-bug-replay \
	--enable-lufs=auto \
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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/gnome-vfs-2.0/modules/*
%{_libdir}/lib*
%{_libdir}/gnome-vfs-2.0/modules/*
%{_includedir}/captive/*
%{_mandir}/man?/*
%{_var}/lib/captive/
