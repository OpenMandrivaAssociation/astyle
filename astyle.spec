%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Reindenter and reformatter of C++, C and Java source code
Name:		astyle
Version:	3.1
Release:	1
License:	LGPLv3+
Group:		Development/C
Url:		http://astyle.sourceforge.net/
Source0:	https://netix.dl.sourceforge.net/project/astyle/astyle/astyle%%20%{version}/astyle_%{version}_linux.tar.gz
BuildRequires:	java-devel
Requires:	%{libname}

%description
Artistic Style is a series of filters that automatically reindent and reformat
C/C++/Java source files. These can be used from a command line, or they can be
incorporated as classes in another C++ program.

%files
%doc doc/*
%{_bindir}/astyle

#----------------------------------------------------------------------------
%package -n %{libname}
Summary:	Library for Artistic Style
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library as well as the JNI version.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}.*
%{_libdir}/lib%{name}j.so.%{major}.*

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
%autosetup -p1 -n %{name}

#fix rights
chmod 644 doc/*

%build
%set_build_flags
export JAVA_HOME=%{_prefix}/lib/jvm/java
%make_build -C build/clang CC=%{__cc} CFLAGS="%{optflags}" LDFLAGS="%{ldflags}" prefix=%{_prefix} release shared java
cd build/clang/bin/
# libastyle
    ln -s lib%{name}.so.%{version} lib%{name}.so.%{major}
    ln -s lib%{name}.so.%{major} lib%{name}.so
# libastylej (jni)
    ln -s lib%{name}j.so.%{version} lib%{name}j.so.%{major}
    ln -s lib%{name}j.so.%{major} lib%{name}j.so
cd ..


%install
install -Dm755 build/clang/bin/%{name} %{buildroot}%{_bindir}/%{name}

# libastyle version
v="3.1.0"

install -Dm755 build/clang/bin/lib%{name}.so."$v" %{buildroot}%{_libdir}/lib%{name}.so."$v"
cp -P build/clang/bin/lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
cp -P build/clang/bin/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so

# libastylej (jni)
install -Dm755 build/clang/bin/lib%{name}j.so."$v" %{buildroot}%{_libdir}/lib%{name}j.so."$v"
cp -P build/clang/bin/lib%{name}j.so.%{major} %{buildroot}%{_libdir}/lib%{name}j.so.%{major}
cp -P build/clang/bin/lib%{name}j.so %{buildroot}%{_libdir}/lib%{name}j.so

install -Dm644 src/%{name}.h %{buildroot}%{_includedir}/%{name}.h

