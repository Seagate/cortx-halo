%define name infra_mon
%define version 0.0.1
%define unmangled_version 0.0.1
%define release 1

Summary: Component monitor for Halo
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: Seagate
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Ajay Srivastava <ajay.srivastava@seagate.com>
Url: https://github.com/Seagate/halo-mon

%description


# Halo Infra Monitor


## Installation Steps

cd infra/mon/
python3 setup.py bdist_rpm
cd dist
yum install -y infra_mon-0.0.1*.noarch.rpm


## Thank You!

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
