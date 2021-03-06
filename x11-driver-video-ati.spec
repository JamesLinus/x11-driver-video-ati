%global _disable_ld_no_undefined 1
# When updating this driver, please update ldetect-lst with new pci ids.
# for example:
# merge2pcitable.pl ati_pciids_csv src/pcidb/ati_pciids.csv pcitable > pcitable.new
# - Anssi

Name:		x11-driver-video-ati
Epoch:		1
Version:	7.6.1
Release:	5
Summary:	X.org driver for ATI Technologies
Group:		System/X11
License:	MIT
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-ati-%{version}.tar.bz2
BuildRequires:	pkgconfig(libdrm) >= 2.4.54
BuildRequires:	pkgconfig(libdrm_radeon) >= 2.4.54
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	pkgconfig(xorg-server) >= 1.18
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(udev) >= 186
Requires:	udev
Requires:	x11-server-common %(xserver-sdk-abi-requires videodrv)
Conflicts:	xorg-x11-server < 7.0
Conflicts:	x11-driver-video-ati_6.7
Suggests:	radeon-firmware

Patch10:	radeon-6.12.2-lvds-default-modes.patch
Patch13:	fix-default-modes.patch
# (tpg) this is needed to get VDPAU works out of box
Requires:	%{_lib}vdpau-driver-r600
Requires:	%{_lib}vdpau-driver-radeonsi
Requires:	%{_lib}dri-drivers-radeon

%description
x11-driver-video-ati is the X.org driver for ATI Technologies.

%prep
%setup -qn xf86-video-ati-%{version}
%patch10 -p1 -b .lvds
%patch13 -p1 -b .def

%build
autoreconf -iv
# FIXME
# As of 7.4.0, clang 3.5-0.211571.1, the X server crashes on startup
# if x11-driver-video-ati is built with clang
# (tpg) let's try with clang
#export CC=gcc
#export CXX=g++

%configure --disable-static --enable-glamor
%make

%install
%makeinstall_std

# these only work in UMS, which is not supported
rm -rf %{buildroot}%{moduledir}/multimedia/

%files
%{_libdir}/xorg/modules/drivers/radeon_drv.so
%{_libdir}/xorg/modules/drivers/ati_drv.so
#%{_libdir}/xorg/modules/multimedia/theatre200_drv.so
#%{_libdir}/xorg/modules/multimedia/theatre_detect_drv.so
#%{_libdir}/xorg/modules/multimedia/theatre_drv.so
%{_mandir}/man4/ati.*
%{_mandir}/man4/radeon.*
