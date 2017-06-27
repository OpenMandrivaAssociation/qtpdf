%define major 5
%define libname %mklibname qtpdf %{major}
%define devname %mklibname qtpdf -d
%define git 20170626

Name: qtpdf
Version: 0.0
%if 0%{?git}
Release: 0.%{git}.1
# git clone git://code.qt.io/qt-labs/qtpdf
# cd qtpdf ; git archive -o qtpdf-%{git}.tar --prefix qtpdf-%{git}/ origin/dev
Source0: %{name}-%{git}.tar.xz
# git clone https://pdfium.googlesource.com/pdfium
# cd pdfium ; git archive -o pdfium-%{git}.tar --prefix src/3rdparty/pdfium/ 8d5315004
Source1: pdfium-%{git}.tar.xz
%else
Release: 1
Source0: %{name}-%{version}.tar.xz
%endif
Summary: Qt library for PDF rendering
URL: http://blog.qt.io/blog/2017/01/30/new-qtpdf-qtlabs-module/
License: LGPLv3
Group: System/Libraries
BuildRequires: qmake5
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: python

%description
Qt library for PDF rendering

%package -n %{libname}
Summary: Qt library for PDF rendering
Group: System/Libraries

%description -n %{libname}
Qt library for PDF rendering

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name},
a Qt library for PDF rendering.

%package examples
Summary: Examples for the QtPdf library
Group: Development/C
Suggests: %{devname} = %{EVRD}

%description examples
Examples for the QtPdf library

%prep
%if 0%{?git}
%setup -qn %{name}-%{git} -a 1
%else
%setup -q -a 1
%endif
%{_libdir}/qt5/bin/syncqt.pl -version `pkg-config --modversion Qt5Core`
2to3 -w src/3rdparty/gyp2pri.py
qmake-qt5

%build
%make
cd examples/pdf/pdfviewer
qmake-qt5
%make

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}
cd examples/pdf/pdfviewer
%makeinstall_std INSTALL_ROOT=%{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp -a pdfviewer %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/applications
cat >%{buildroot}%{_datadir}/applications/%{name}.pdfviewer.desktop <<'EOF'
[Desktop Entry]
Type=Application
Terminal=false
Name=pdfviewer
GenericName=PDF document viewer
Comment=A PDF document viewer using QtPDF
Categories=Viewer;Office;
Keywords=viewer;document;presentation;pdf;
TryExec=pdfviewer
Exec=pdfviewer %F
MimeType=application/pdf;application/x-pdf;text/pdf;text/x-pdf;image/pdf;image/x-pdf;
EOF
chmod +x %{buildroot}%{_datadir}/applications/*.desktop

%files
%{_bindir}/*
%{_datadir}/applications/%{name}.pdfviewer.desktop

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.prl
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/Qt5Pdf
%{_libdir}/qt5/mkspecs/modules/*.pri

%files examples
%{_libdir}/qt5/examples/pdf
