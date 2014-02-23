Summary:	Device manager for Logitech's Unifying Receiver peripherals
Name:		solaar
Version:	0.9.2
Release:	0.1
License:	GPL v2
Group:		Development/Languages/Python
Source0:	https://github.com/pwr/Solaar/archive/%{version}.tar.gz
# Source0-md5:	2a6ea17150cf030b09ff802cb454358b
URL:		https://github.com/pwr/Solaar
BuildRequires:	python-modules
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildArch:	noarch
Requires:	python3-pyudev
%pyrequires_eq	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Solaar is a Linux device manager for Logitech's Unifying Receiver
peripherals. It is able to pair/unpair devices to the receiver,
and for most devices read battery status.

It comes in two flavors, command-line and GUI. Both are able to list
the devices paired to a Unifying Receiver, show detailed info for each
device, and also pair/unpair supported devices with the receiver.

%package gui
Summary:	GUI for Solaar
Group:		X11/Applications
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	gtk+3
Requires:	python3-modules
Requires:	python3-pygobject3

%description gui
Solaar GUI application using GTK+3.

%prep
%setup -qn Solaar-%{version}

%build
%{__python3} setup.py build -b python3

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d

%{__python3} setup.py build -b python3 install \
	--optimize=2		\
	--root=$RPM_BUILD_ROOT	\
	--skip-build

install rules.d/42-logitech-unify-permissions.rules \
	$RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_icon_cache hicolor

%postun gui
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README.md
%attr(755,root,root) %{_bindir}/solaar-cli
%{py3_sitescriptdir}/hidapi
%{py3_sitescriptdir}/logitech_receiver
%{py3_sitescriptdir}/solaar
%{py3_sitescriptdir}/solaar-%{version}-py*.egg-info
%{_prefix}/lib/udev/rules.d/*.rules

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/solaar
%{_datadir}/solaar
%{_desktopdir}/solaar.desktop
%{_iconsdir}/hicolor/*/apps/solaar.svg
%{_sysconfdir}/xdg/autostart/solaar.desktop

