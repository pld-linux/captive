Summary:	Captive NTFS
Summary(pl):	Captive NTFS
Name:		captive
Version:	1.1.5
Release:	0
License:	GPL (?)
Group:		Base/Kernel
Source0:	http://www.jankratochvil.net/ptoject/%{name}/dist/%{name}-%{version}.tar.gz
#BuildRequires:
#Requires:
URL:
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
- -- empty --

%description -l pl
- -- pusty --

%prep
%setup -q

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
