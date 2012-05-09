%bcond_with gtk
%bcond_without qt

Name:       cr3
Version:    3.0.57.6
Release:    %mkrel 1
Summary:    A multiplatform e-book viewer
Group:      Applications/Text
License:    GPL
URL:        http://sourceforge.net/projects/crengine/

#
# git archive --format=tar \
#     --remote=git://crengine.git.sourceforge.net/gitroot/crengine/crengine \
#     --prefix=cr3-3.0.57.6/ cr3.0.57-6 | gzip > cr3-3.0.57.6.tar.gz
#
Source0:    %{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	png-devel
BuildRequires:	jpeg-devel
BuildRequires:	libfreetype6-devel
BuildRequires:	fontconfig-devel

%define common_description \
Cool Reader 3 is a multiplatform e-book viewer with support of TXT, \
FB2, HTML, RTF, CHM, EPUB, TRC file formats.  Fully supports FB2 \
format:  tables, footnotes, CSS based formatting.  Autodetects TXT \
file format and encoding, and reflows it for easy reading.  Supports \
table of contents, search, bookmarks.  Supports window and fullscreen \
modes, paperbook-like pages or scroll view.  Book formatting is \
customizable using CSS files.

%description
%{common_description}

#--------------------------------------------------------------------

%if %{with qt}
%package qt
Summary:	A multiplatform e-book viewer using QT
Buildrequires:	qt4-devel
Requires:	libqtcore4
Requires:	libqtgui4
Requires:	%{name}-common = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description qt
%{commmon_description}

This package is the QT version.

%files qt
%{_bindir}/%{name}-qt
%endif

#--------------------------------------------------------------------

%if %{with gtk}
%package gtk
Summary:	A multiplatform e-book viewer using GTK
Buildrequires:	libwxgtk2.8-devel
Requires:	libwxgtk2.8
Requires:	%{name}-common = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description gtk
%{common_description}

This package is the version using wxWidgets.

%files gtk
%{_bindir}/%{name}-gtk
%endif

#--------------------------------------------------------------------

%package common
Summary:	Miscellaneous files for CoolReader3 the e-book viewer

%description common
Miscellaneous files for CoolReader3 the e-book viewer

%files common
%{_datadir}/applications/*
%{_datadir}/%{name}
%doc %{_docdir}/%{name}
%{_mandir}/man1/*
%{_datadir}/pixmaps/*

#--------------------------------------------------------------------

%prep
%setup -q

%build

%if %{with qt}
%cmake -DGUI=QT -DMAX_IMAGE_SCALE_MUL=2 -DDOC_DATA_COMPRESSION_LEVEL=3 -DDOC_BUFFER_SIZE=0x1400000 -DENABLE_ANTIWORD=0 -DCMAKE_BUILD_TYPE=Release
%make
cd -
mv build buildqt
%endif

%if %{with gtk}
%cmake -DGUI=WX -DCMAKE_BUILD_TYPE=Release
%make
cd -
mv build buildwx
%endif

%install
%if %{with qt}
mv buildqt build
%makeinstall_std -C build
mv %{buildroot}/usr/bin/cr3{,-qt}
mv build buildqt
%endif

%if %{with gtk}
mv buildwx build
%makeinstall_std -C build
mv %{buildroot}/usr/bin/cr3{,-gtk}
mv build buildwx
%endif
