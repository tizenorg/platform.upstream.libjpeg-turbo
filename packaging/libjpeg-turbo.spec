%define major   8
%define minor   0
%define micro   2
%define srcver  1.4.2
%define libver  %{major}.%{minor}.%{micro}
# major number of library from jpeg8
%define cmajor  8

Name:           libjpeg-turbo
Version:        %{srcver}
Release:        1
Summary:        A MMX/SSE2 accelerated library for manipulating JPEG image files
License:        BSD-2.0
Group:          Graphics & UI Framework/Libraries
Url:            http://sourceforge.net/projects/libjpeg-turbo
Source0:        http://downloads.sourceforge.net/project/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        baselibs.conf
Source1001: 	libjpeg-turbo.manifest
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  yasm

%description
The libjpeg-turbo package contains a library of functions for manipulating
JPEG images.

%package -n libjpeg

Version:        %{libver}
Release:        0
Summary:        The MMX/SSE accelerated JPEG compression/decompression library
Group:          Graphics & UI Framework/Libraries

Provides:       libjpeg = %{version}
Provides:       libjpeg8
Obsoletes:      libjpeg < %{version}

%description -n libjpeg
This library contains MMX/SSE accelerated functions for manipulating
JPEG images.

%package -n libjpeg-devel
Version:        %{libver}
Release:        0
Summary:        Development Tools for applications which will use the Libjpeg Library
Group:          Graphics & UI Framework/Development

Provides:       libjpeg-turbo-devel
Requires:       libjpeg = %{version}
Provides:       libjpeg-devel = %{version}
Provides:       libjpeg8-devel
Obsoletes:      libjpeg-devel < %{version}
%if "%{major}" != "%{cmajor}"
Conflicts:      libjpeg-devel
%endif

%description -n libjpeg-devel
The libjpeg-devel package includes the header files and libraries
necessary for compiling and linking programs which will manipulate JPEG
files using the libjpeg library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
autoreconf -fiv
%configure --enable-shared --disable-static --with-jpeg8
make %{?_smp_mflags}

#%check
#make test libdir=%{_libdir}

%install
%makeinstall
mkdir -p %{buildroot}/usr/share/license
cp -rf %{_builddir}/%{name}-%{srcver}/COPYING %{buildroot}/usr/share/license/%{name}
# Fix perms
chmod -x README-turbo.txt

# Remove unwanted files
rm -f %{buildroot}%{_libdir}/lib{,turbo}jpeg.la

rm %{buildroot}%{_bindir}/tjbench

# Remove docs, we'll select docs manually
rm -rf %{buildroot}%{_datadir}/doc/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libjpeg -p /sbin/ldconfig

%postun -n libjpeg -p /sbin/ldconfig

%docs_package

%files
%{_datadir}/license/%{name}
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/*

%files -n libjpeg
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libturbojpeg.so.*
%{_libdir}/libjpeg.so.%{libver}
%{_libdir}/libjpeg.so.%{major}

%files -n libjpeg-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libturbojpeg.so
%{_libdir}/libjpeg.so
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c

%changelog
