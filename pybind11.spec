%global debug_package %{nil}
%bcond_without tests
Name:    pybind11
Version: 2.8.1
Release: 1
Summary: Seamless operability between C++11 and Python
License: BSD
URL:	 https://github.com/pybind/pybind11
Source0: https://github.com/pybind/pybind11/archive/refs/tags/v%{version}.tar.gz


BuildRequires: make cmake eigen3-devel gcc-c++
BuildRequires: python3-devel python3-setuptools
#BuildRequires: python3-numpy python3-pytest


%description
pybind11 is a lightweight header-only library that exposes C++ types 
in Python and vice versa, mainly to create Python bindings of existing 
C++ code.

%package devel
Summary:  Development headers for pybind11
Provides: %{name}-static = %{version}-%{release}
Requires: cmake

%description devel
This package contains the development headers for pybind11.

%package -n     python3-%{name}
Summary:        %{summary}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
pybind11 is a lightweight header-only library that exposes C++ types 
in Python and vice versa, mainly to create Python bindings of existing 
C++ code.


%prep
%autosetup -n %{name}-%{version} -p1


%build
pys=""
pys="$pys python3"
for py in $pys; do
    mkdir $py
    %cmake -B $py -DCMAKE_BUILD_TYPE=Debug -DPYTHON_EXECUTABLE=%{_bindir}/$py -DPYBIND11_INSTALL=TRUE -DUSE_PYTHON_INCLUDE_DIR=FALSE %{!?with_tests:-DPYBIND11_TEST=OFF}
    %make_build -C $py
done

%py3_build


%check
#make -C python3 check %{?_smp_mflags}


%install
%make_install -C python3
PYBIND11_USE_CMAKE=true %py3_install "--install-purelib" "%{python3_sitearch}"


%files devel
%license LICENSE
%doc README.rst
%{_includedir}/pybind11/
%{_datadir}/cmake/pybind11/
%{_bindir}/pybind11-config

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info


%changelog
* Sat Dec 11 2021 zhouwenpei <zhouwenpei1@huawei.com> - 2.8.1-1
- package init
