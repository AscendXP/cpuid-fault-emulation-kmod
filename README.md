# Fedora kmod Packaging for CPUID Fault Emulation

This project provides kernel module packaging for CPUID fault emulation, specifically targeted at **Universal Blue** and **Fedora Atomic Desktop** images, where **DKMS is not available**.

**Description:**  
Linux CPUID fault emulation kernel module (Developed by LinUwUx). Provides CPUID fault emulation support through a native kernel module and systemd service integration.

## Installation (Fedora / RHEL Standard)

Enable the Copr repository and install all required packages:

```bash
sudo dnf copr enable ascendxps/AscendXP
sudo dnf install akmod-cpuid-fault-emulation cpuid-fault-emulation-kmod-common
```

## Installation (Fedora Atomic / Universal Blue / Bazzite)

Fedora Atomic, Universal Blue, and Bazzite systems use `rpm-ostree` for package layering.

Enable the Copr repository and install the AKMOD package:

```bash
sudo curl -sL https://copr.fedorainfracloud.org/coprs/ascendxps/AscendXP/repo/fedora-$(rpm -E %fedora)/ascendxps-AscendXP-fedora-$(rpm -E %fedora).repo -o /etc/yum.repos.d/_copr_ascendxps-AscendXP.repo
sudo rpm-ostree install akmod-cpuid-fault-emulation cpuid-fault-emulation-kmod-common
```

**Reboot the system to apply the changes:**

```bash
systemctl reboot
```

**After reboot, enable and start the CPUID fault emulation service:**

```bash
sudo systemctl enable --now cpuid-fault-emulation.service
```
