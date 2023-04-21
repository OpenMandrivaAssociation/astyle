%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Reindenter and reformatter of C++, C and Java source code
Name:		astyle
Version:	3.2.1
Release:	1
License:	LGPLv3+
Group:		Development/C
Url:		http://astyle.sourceforge.net/
Source0:	https://netix.dl.sourceforge.net/project/astyle/astyle/astyle%%20%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	jdk-current
BuildRequires:	cmake
BuildRequires:	ninja
Requires:	%{libname}

%description
Artistic Style is a series of filters that automatically reindent and reformat
C/C++/Java source files. These can be used from a command line, or they can be
incorporated as classes in another C++ program.

%files
%doc %{_docdir}/%{name}/html/*.html
%{_bindir}/astyle
%doc %{_mandir}/man1/astyle.1*

#----------------------------------------------------------------------------
%package -n %{libname}
Summary:	Library for Artistic Style
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library as well as the JNI version.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/lib%{name}j.so.%{major}*

%package -n %{devname}
Summary:	Development files for using %{name} library
Group:		Development/C
Provides:	lib%{name}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for using %{name} library.

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}j.so
%{_includedir}/%{name}.h

%prep
%autosetup -p1

# fix rights
chmod 644 doc/*

# (tpg) adjust libdir
sed -i -e "s/DESTINATION lib/DESTINATION %{_lib}/" build/cmake/InstallOptions.cmake

mkdir -p ../build-binary
mkdir -p ../build-shared
cp -af * ../build-binary ||:
cp -af * ../build-shared ||:

. %{_sysconfdir}/profile.d/90java.sh
# (tpg) build libries
%cmake \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_JAVA_LIBS=ON \
	-DJAVA_HOME="$JAVA_HOME" \
	-DJAVA_AWT_LIBRARY="$JAVA_HOME/lib/libjawt.so" \
	-G Ninja

# (tpg) build shared
cd ../../build-shared
%cmake \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_JAVA_LIBS=OFF \
	-DJAVA_HOME="$JAVA_HOME" \
	-DJAVA_AWT_LIBRARY="$JAVA_HOME/lib/libjawt.so" \
	-G Ninja

# (tpg) build binary
cd ../../build-binary
%cmake \
	-DBUILD_SHARED_LIBS=OFF \
	-DBUILD_JAVA_LIBS=OFF \
	-DJAVA_HOME="$JAVA_HOME" \
	-DJAVA_AWT_LIBRARY="$JAVA_HOME/lib/libjawt.so" \
	-G Ninja

%build
%ninja_build -C build
%ninja_build -C ../build-shared/build
%ninja_build -C ../build-binary/build

%install
install -m644 -D ./src/astyle.h %{buildroot}%{_includedir}/astyle.h

%ninja_install -C build
%ninja_install -C ../build-shared/build
%ninja_install -C ../build-binary/build

