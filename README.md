# SoftEther Stable Packaging for Enterprise Linux 9 (EL9)

This repository provides **SoftEther VPN Stable** packaging for
**Enterprise Linux 9 (AlmaLinux / Rocky Linux / RHEL 9)**.

The purpose of this repository is to offer a **clean, policy‑compliant SRPM**
that users can rebuild on their own systems using `mock` or `rpmbuild`.

Binary RPM packages are **not** provided.
Users are expected to **rebuild the SRPM themselves**.

---

## ✨ Features

### Versioned command names

To avoid conflicts with future SoftEther VPN 5.x:

- `/usr/bin/vpncmd4`
- `/usr/libexec/softeher4/vpnserver`

etc.

Internal binaries are placed under: `/usr/libexec/softether4/`

This ensures **SoftEther4 and SoftEther5 can coexist**.

---

## ✔ Fully EPEL/Fedora‑style packaging

- libexec separation  
- systemd unit files included
- correct licensing (ASL 2.0)
- no empty maintainer scripts
- correct file permissions
- rpmlint clean
- mock clean build verified

---

## 🔧 How to Build

```sh
rpmbuild --rebuild softether4-*.src.rpm
```

## 📜 License

Packaging files follow the same licenses as SoftEther VPN:

- Apache License 2.0

This repository is a **source-only** repository. It does **not** function as a yum/dnf binary repository.
