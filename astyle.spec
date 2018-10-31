Summary:	Reindenter and reformatter of C++, C and Java source code
Name:		astyle
Version:	2.04
Release:	6
License:	LGPLv3+
Group:		Development/C
Url:		http://astyle.sourceforge.net/
Source0:	http://internap.dl.sourceforge.net/sourceforge/astyle/astyle_%{version}_linux.tar.gz

%description
Artistic Style is a series of filters that automatically reindent and reformat
C/C++/Java source files. These can be used from a command line, or they can be
incorporated as classes in another C++ program.

%files
%doc doc/*
%{_bindir}/astyle

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}

%build
cd build/gcc
%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 build/gcc/bin/astyle %{buildroot}%{_bindir}/astyle

