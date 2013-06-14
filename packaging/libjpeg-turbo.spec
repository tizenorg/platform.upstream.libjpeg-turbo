%define major   8
%define minor   0
%define micro   2
%define srcver  1.2.1
%define libver  %{major}.%{minor}.%{micro}
# major number of library from jpeg8
%define cmajor  8

Name:           libjpeg-turbo
Version:        %{srcver}
Release:        0
Summary:        A MMX/SSE2 accelerated library for manipulating JPEG image files
License:        BSD-3-Clause
Group:          Graphics & UI Framework/Libraries
Url:            http://sourceforge.net/projects/libjpeg-turbo
Source0:        http://downloads.sourceforge.net/project/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        baselibs.conf
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

%build
autoreconf -fiv
%configure --disable-static \
           --with-jpeg8
make %{?_smp_mflags}

%check
make test libdir=%{_libdir}

%install
%makeinstall

# Fix perms
chmod -x README-turbo.txt release/copyright

# Remove unwanted files
rm -f %{buildroot}%{_libdir}/lib{,turbo}jpeg.la

rm %{buildroot}%{_bindir}/tjbench

# Remove docs, we'll select docs manually
rm -rf %{buildroot}%{_datadir}/doc/

%post -n libjpeg -p /sbin/ldconfig

%postun -n libjpeg -p /sbin/ldconfig

%docs_package

%files
%defattr(-,root,root)
%license release/copyright 
%{_bindir}/*

%files -n libjpeg
%defattr(-,root,root)
%{_libdir}/libturbojpeg.so
%{_libdir}/libjpeg.so.%{libver}
%{_libdir}/libjpeg.so.%{major}

%files -n libjpeg-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libjpeg.so
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c

%changelog
