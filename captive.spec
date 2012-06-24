
# TODO: rename spec to captive

#
## %_bcond_without	gnome	# don't build gnome-vfs support
%bcond_without	lufs	# don't build LUFS support
#
Summary:	Captive - NTFS read/write filesystem for Linux
Summary(pl):	Captive - obs�uga NTFS dla Linuksa z odczytem i zapisem
Name:		captive
Version:	1.1.5
Release:	0.1
License:	GPL
Group:		Base/Kernel
Source0:	http://www.jankratochvil.net/project/captive/dist/%{name}-%{version}.tar.gz
# Source0-md5:	dfb7ce617745695e7a908609b9370fd6
URL:		http://www.jankratochvil.net/project/captive/
BuildRequires:	ORBit2-devel
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
Projekt Captive implementuje pierwszy pe�ny, swobodny dost�p z
odczytem i zapisem do partycji NTFS. Pozwala zamontowa� partycje z
Microsoft Windows NT, 200x i XP jako dost�pny w spos�b przezroczysty
wolumen pod Linuksem.

Kompatybilno�� osi�gni�to metod� Wine poprzez u�ycie oryginalnego
sterownika ntfs.sys. Captive emuluje wymagane podsystemy j�dra
Microsoft Windows poprzez wykorzystanie oryginalnego ntoskrnl.exe,
cz�ci ReactOS-a lub w�asne implementacje z tego projektu w zale�no�ci
od danego przypadku. Projekt zawiera pierwsze API j�dra MS-Windows z
otwartymi �r�d�ami dla wolnodost�pnych system�w operacyjnych. Wybrano
wykorzystanie plik�w oryginalnego sterownika aby osi�gn�� lepsz�
kompatybilno�� i bezpiecze�stwo.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
