#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Vector-Optimized Library of Kernels
Summary(pl.UTF-8):	Vector-Optimized Library of Kernels - biblioteka jąder zoptymalizowanych wektorowo
Name:		volk
Version:	3.1.2
Release:	2
License:	LGPL v3+
Group:		Libraries
Source0:	https://www.libvolk.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	04d83692c9292324f311ebe9b93bf2cf
Patch0:		%{name}-pld.patch
URL:		https://www.libvolk.org/
BuildRequires:	cmake >= 3.8
BuildRequires:	cpu_features-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gcc >= 6:4.7
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	orc-devel >= 0.4.12
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-Mako >= 0.4.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	orc >= 0.4.12
Conflicts:	gnuradio < 3.9.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VOLK is the Vector-Optimized Library of Kernels. It is a library that
contains kernels of hand-written SIMD code for different mathematical
operations. Since each SIMD architecture can be very different and no
compiler has yet come along to handle vectorization properly or highly
efficiently, VOLK approaches the problem differently.

%description -l pl.UTF-8
VOLK (Vector-Optimized Library of Kernels) biblioteka jąder
zoptymalizowanych wektorowo. Zawiera jądra ręcznie pisanego kodu SIMD
do różnych operacji matematycznych. Ponieważ każda architektura SIMD
może bardzo się różnić id innych, a nie każdy kompilator potrafi
dobrze i wydajnie obsłużyć każdą wektoryzację, VOLK ma różne podejścia
do problemu.

%package devel
Summary:	Header files for VOLK library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki VOLK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for VOLK library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki VOLK.

%package apidocs
Summary:	API documentation for VOLK library
Summary(pl.UTF-8):	Dokumentacja API biblioteki VOLK
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for VOLK library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki VOLK.

%prep
%setup -q
%patch -P 0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DVOLK_PYTHON_DIR=%{py3_sitescriptdir}

%{__make}

%if %{with apidocs}
%{__make} volk_doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# update to PEP3147 scheme
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/volk_modtool/*.py[co]
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

# remove empty dirs
rmdir $RPM_BUILD_ROOT%{_includedir}/volk/asm/{neon,orc,riscv}
rmdir $RPM_BUILD_ROOT%{_includedir}/volk/asm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md docs/CHANGELOG.md
%attr(755,root,root) %{_bindir}/volk-config-info
%attr(755,root,root) %{_bindir}/volk_modtool
%attr(755,root,root) %{_bindir}/volk_profile
%attr(755,root,root) %{_libdir}/libvolk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvolk.so.3.1
%{py3_sitescriptdir}/volk_modtool

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvolk.so
%{_includedir}/volk
%{_pkgconfigdir}/volk.pc
%{_libdir}/cmake/volk

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/html/{search,*.css,*.html,*.js,*.png}
%endif
