
#
## %_bcond_without	gnome	# don't build gnome-vfs support
## %_bcond_without lufs	# don't build LUFS support

Summary:	Captive NTFS
Summary(pl):	Captive NTFS
Name:		captive
Version:	1.1.5
Release:	0
License:	GPL
Group:		Base/Kernel
Source0:	http://www.jankratochvil.net/project/%{name}/dist/%{name}-%{version}.tar.gz
# Source0-md5:	dfb7ce617745695e7a908609b9370fd6
BuildRequires:	gnome-vfs
Requires:	ntfsprogs >= 1.8.0
URL:		http://www.jankratochvil.net/project/%{name}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
- -- empty --

%description -l pl
- -- pusty --

%prep
%setup -q -n %{name}-%{version}

#%patch

%build
./configure --prefix=%{_prefix}
%{__make} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} install

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
