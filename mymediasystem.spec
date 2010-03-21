#
# Conditional build:
%bcond_without	lirc		# without lirc support
#
%define	sname	mms
%define	snap	2252
Summary:	My Media System
Name:		mymediasystem
Version:	1.1.0
Release:	0.%{snap}.1
License:	GPL v2+
Group:		Applications/Multimedia
#Source0:	http://mms.sunsite.dk/%{sname}-%{version}.tgz
Source0:	http://mms.mymediasystem.net/mms110/nightly-snapshot/%{sname}-%{version}-%{snap}.tgz
# Source0-md5:	f985b9d481b10684d708d2c02e0d4643
Patch0:		%{name}-build.patch
Patch1:		%{name}-epg.patch
Patch2:		%{name}-imdb.patch
Patch3:		%{name}-moviedb.patch
Patch4:		%{name}-dirlisting.patch
Patch5:		%{name}-po_pl.patch
URL:		http://mymediasystem.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL-devel
BuildRequires:	binutils >= 2.19.51.0.4
BuildRequires:	boost-devel
BuildRequires:	commoncpp2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	imlib2-devel
BuildRequires:	libtool
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	ncurses-devel
BuildRequires:	pcre-cxx-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sqlite3-devel
BuildRequires:	taglib-devel
BuildRequires:	xine-lib-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
Requires:	fonts-TTF-DejaVu
Requires:	iconv
Requires:	wget
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
My Media System is an application that manages, displays and plays
media content such as videos, music, pictures, and more. MMS runs
perfectly on anything from a Set-Top-Box connected to your TV-Set, to
your specially tailored multimedia PC and HD display.

%prep
%setup -q -n %{sname}-%{version}-%{snap}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--enable-clock \
	--enable-evdev \
	%{?with_lirc:--enable-lirc} \
	--enable-notify-area \
	--enable-opengl \
	--enable-python \
	--enable-res-switch \
	--enable-weather \
	--disable-fancy-game \
	--disable-inotify \
	--disable-optimization

%{__make} \
	CC="%{__cc} %{rpmcflags}" \
	CXX="%{__cxx} %{rpmcxxflags} -L/lib"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CC="%{__cc} %{rpmcflags}" \
	CXX="%{__cxx} %{rpmcxxflags} -L/lib" \
	DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_datadir}/mms/fonts
rm -f DejaVuSansCondensed*
ln -sf %{_datadir}/fonts/TTF/DejaVuSansCondensed.ttf .
ln -sf %{_datadir}/fonts/TTF/DejaVuSansCondensed-Bold.ttf .
cd -

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/plugins/python/*.pdf
%attr(755,root,root) %{_bindir}/mms*
%dir %{_sysconfdir}/mms
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms/*Config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms/ClockAlarms
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms/genericplayer.ops
%dir %{_sysconfdir}/mms/input
%dir %{_sysconfdir}/mms/input/evdev
%dir %{_sysconfdir}/mms/input/keyboard
%dir %{_sysconfdir}/mms/input/lirc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms/input/evdev/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms/input/keyboard/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms/input/lirc/*
%{_sysconfdir}/mms/scripts
%dir %{_libdir}/mms
%dir %{_libdir}/mms/plugins
%attr(755,root,root) %{_libdir}/mms/alarm.sh
%attr(755,root,root) %{_libdir}/mms/plugins/*
%attr(755,root,root) %{py_sitedir}/mmsv2*.so
%{_datadir}/mms
%attr(777,root,root) /var/cache/mms
%{_mandir}/man1/mms*.1*
%lang(de) %{_mandir}/de/man1/mms*.1*
