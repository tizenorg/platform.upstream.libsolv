Name:           libsolv
Version:        0.2.3
Release:        0
Url:            git://gitorious.org/opensuse/libsolv.git
Source:         libsolv-%{version}.tar.bz2

%bcond_without enable_static
%bcond_without disable_shared
%bcond_without perl_binding
%bcond_without python_binding

BuildRequires:  db4-devel
BuildRequires:  expat-devel
BuildRequires:  fdupes
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rpm-devel
BuildRequires:  zlib-devel

%if %{with perl_binding}
BuildRequires:  perl
BuildRequires:  swig
%endif
%if %{with python_binding}
%global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(True);")
BuildRequires:  python-devel
BuildRequires:  swig
%endif

Summary:        A new approach to package dependency solving
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++

%description
A new approach to package dependency solving

%if !%{with disable_shared}
%package -n libsolv
Summary:        A new approach to package dependency solving
Group:          Development/Libraries/C and C++

%description -n libsolv
A new approach to package dependency solving

%endif
%package devel
Summary:        A new approach to package dependency solving
Group:          Development/Libraries/C and C++
Requires:       libsolv-tools = %version
%if !%{with disable_shared}
Requires:       libsolv = %version
%endif
Requires:       rpm-devel

%description devel
Development files for libsolv, a new approach to package dependency solving

%package tools
Summary:        A new approach to package dependency solving
Group:          Development/Libraries/C and C++
Obsoletes:      satsolver-tools < 0.18
Provides:       satsolver-tools = 0.18
Requires:       gzip bzip2 coreutils findutils

%description tools
A new approach to package dependency solving.

%package demo
Summary:        Applications demoing the libsolv library
Group:          System/Management
Requires:       curl
%if 0%{?fedora_version} || 0%{?rhel_version} >= 600 || 0%{?centos_version} >= 600
Requires:       gnupg2
%endif
%if 0%{?suse_version}
Requires:       gpg2
%endif

%description demo
Applications demoing the libsolv library.

%package -n python-solv
%if 0%{?py_requires:1}
%py_requires
%endif
Summary:        Python bindings for the libsolv library
Group:          Development/Languages/Python

%description -n python-solv
Python bindings for sat solver.

%package -n perl-solv
Requires:       perl = %{perl_version}
Summary:        Perl bindings for the libsolv library
Group:          Development/Languages/Perl

%description -n perl-solv
Perl bindings for sat solver.

%prep
%setup -n libsolv-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$CFLAGS"

CMAKE_FLAGS=
CMAKE_FLAGS="-DSUSE=1"

cmake   $CMAKE_FLAGS \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB=%{_lib} \
	-DCMAKE_VERBOSE_MAKEFILE=TRUE \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	%{?with_enable_static:-DENABLE_STATIC=1} \
	%{?with_disable_shared:-DDISABLE_SHARED=1} \
	%{?with_perl_binding:-DENABLE_PERL=1} \
	%{?with_python_binding:-DENABLE_PYTHON=1} \
	-DUSE_VENDORDIRS=1 \
	-DCMAKE_SKIP_RPATH=1
make %{?jobs:-j %jobs}

%install
make DESTDIR=$RPM_BUILD_ROOT install
%if %{with python_binding}
pushd $RPM_BUILD_ROOT/%{python_sitearch}
python %py_libdir/py_compile.py *.py
python -O %py_libdir/py_compile.py *.py
popd
%endif
# we want to leave the .a file untouched
export NO_BRP_STRIP_DEBUG=true

%clean
rm -rf "$RPM_BUILD_ROOT"

%if !%{with disable_shared}
%post -n libsolv -p /sbin/ldconfig

%postun -n libsolv -p /sbin/ldconfig

%files -n libsolv
%defattr(-,root,root)
%doc LICENSE*
%{_libdir}/libsolv.so.*
%{_libdir}/libsolvext.so.*
%endif

%files tools
%defattr(-,root,root)
%if 0%{?suse_version}
%exclude %{_bindir}/helix2solv
%endif
%exclude %{_bindir}/solv
%{_bindir}/*

%files devel
%defattr(-,root,root)
%if %{with enable_static}
%{_libdir}/libsolv.a
%{_libdir}/libsolvext.a
%endif
%if !%{with disable_shared}
%{_libdir}/libsolv.so
%{_libdir}/libsolvext.so
%endif
%{_includedir}/solv
%if 0%{?suse_version}
%{_bindir}/helix2solv
%endif
%{_datadir}/cmake/Modules/*

%files demo
%defattr(-,root,root)
%{_bindir}/solv

%if %{with perl_binding}
%files -n perl-solv
%defattr(-,root,root)
%{perl_vendorarch}/*
%endif

%if %{with python_binding}
%files -n python-solv
%defattr(-,root,root)
%{python_sitearch}/*
%endif

%changelog
