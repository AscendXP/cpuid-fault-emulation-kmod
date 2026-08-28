%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global __akmods_install true
%endif
Name:           cpuid-fault-emulation-kmod
Version:        1
Release:        1%{?dist}
Summary:        Linux CPUID fault emulation kernel module
License:        GPL-2.0-only
URL:            https://github.com/AscendXP/cpuid-test
Source0:        cpuid_fault_emulation.zip
Source1:        cpuid-fault-emulation.service
BuildRequires:  kmodtool
BuildRequires:  unzip
BuildRequires:  systemd-rpm-macros
%{?systemd_ordering}
%{expand:%(kmodtool --target %{_target_cpu} --repo fedora --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}

%description
Provides CPUID fault emulation support through a native kernel module.
(Developed by LinUwUx)

%package common
Summary:        Common files for CPUID fault emulation kernel module
BuildArch:      noarch

%description common
This package provides the systemd service unit and common assets for the
CPUID fault emulation kernel module.

%prep
%setup -q -c -n %{name}-%{version}

for kernel_version in %{?kernel_versions}; do
    mkdir -p ../_kmod_build_${kernel_version%%___*}
    cp -a . ../_kmod_build_${kernel_version%%___*}/
    mv ../_kmod_build_${kernel_version%%___*} .
done

%build
for kernel_version in %{?kernel_versions}; do
    kdir="${kernel_version##*___}"
    kver="${kernel_version%%___*}"
    make V=1 %{?_smp_mflags} -C ${kdir} M=${PWD}/_kmod_build_${kver} KERNEL=${kver} modules
done

%install
for kernel_version in %{?kernel_versions}; do
    install -D -m 644 _kmod_build_${kernel_version%%___*}/cpuid_fault_emulation.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/cpuid_fault_emulation.ko
done
%{?akmod_install}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/cpuid-fault-emulation.service

%post common
%systemd_post cpuid-fault-emulation.service

%preun common
%systemd_preun cpuid-fault-emulation.service

%postun common
%systemd_postun_with_restart cpuid-fault-emulation.service

%posttrans common
if grep -qw umip /proc/cpuinfo; then
    echo -e "\033[1;31mREMINDER:\033[0m Your CPU supports UMIP. Add \033[1mclearcpuid=umip\033[0m to your kernel parameters and reboot."
fi

if grep -qw cpuid_fault /proc/cpuinfo; then
    echo "Native CPUID faulting detected; package is unnecessary."
else
    echo "Native CPUID faulting not detected; enabling CPUID fault emulation service."
    if [ -x /usr/bin/systemctl ]; then
        /usr/bin/systemctl enable --now cpuid-fault-emulation.service || :
    fi
    echo -e "\033[31mREMINDER:\033[0m For Secure Boot: ensure your akmods MOK key is enrolled in shim via mokutil."
fi

%files common
%{_unitdir}/cpuid-fault-emulation.service

%changelog
