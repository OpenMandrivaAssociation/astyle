Name:           astyle
Version:        1.24
Release:        %mkrel 2
Epoch:          0
Summary:        Reindenter and reformatter of C++, C and Java source code
License:        LGPLv3+
Group:          Development/C
URL:            http://astyle.sourceforge.net/
Source0:        http://internap.dl.sourceforge.net/sourceforge/astyle/astyle_%{version}_linux.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Artistic Style is a series of filters that automatically reindent and reformat
C/C++/Java source files. These can be used from a command line, or they can be
incorporated as classes in another C++ program.

%prep
%setup -q -n astyle

%build
(cd build/gcc && %{make} CFLAGS="%{optflags}")

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 0755 build/gcc/bin/astyle %{buildroot}%{_bindir}/astyle

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755) 
%doc doc/*
%attr(0755,root,root) %{_bindir}/astyle
