---
description: Answers to common questions about LimaNix, from supported Macs to files, updates and containers.
---

# Frequently asked questions

## Is LimaNix free?

Yes. LimaNix is open source under the Apache License 2.0. The source is on [GitHub](https://github.com/limanix).

## Which Macs does it support?

Apple Silicon and Intel Macs with macOS 26 or newer. The client also needs `ssh` in your `PATH`. See [Install](/install).

## Do I need to know Nix?

No. `limanix.toml` covers the shell, toolchains, modules and packages. When you need more, a NixOS module of your own plugs into the same VM; see [Your own modules](/modules/custom).

## Do I need to install Lima or Nix?

No. Lima is built into the `limanix` binary, and Nix runs inside the VM. Only a guest of the other architecture, such as an Intel guest on Apple Silicon, needs QEMU on the Mac; see [Resources and architecture](/vms/resources).

## How is it different from Lima?

LimaNix runs its VMs with Lima, built into the `limanix` binary. On top it adds a NixOS system built from your file, a catalog of modules that work together, and updates that build before the VM restarts. [How it works](/architecture) shows the parts.

## Can I run containers?

Yes. Add `lmx:docker` to the modules, and Docker Engine with Compose runs inside the VM. Images, containers and volumes live on the VM's disk, which `limanix delete` removes. See [Docker](/modules/docker).

## Where do my files live?

Project folders stay on your Mac and are shared into the VM. Your home inside the VM is kept on the Mac too: it survives updates and stays when you delete the VM. The system and anything written outside shared folders live on the VM's disk; see [Files and storage](/vms/storage).

## Can I use my editor on the Mac?

Yes. Share the project folder with the VM, edit it on the Mac and run builds and tests in the VM; both sides see the same files. For language servers to see the project's Linux dependencies, open the project at its path in the VM, with AstroNvim inside the VM or with your editor's remote development support, which you set up yourself. See [Shared folders](/config/mounts).

## How do I add a package?

Name it in `[nixos] packages`, such as `packages = ["tree"]`, and run `limanix update --config limanix.toml`. To try a tool in one VM without changing the file, run `nix shell nixpkgs#tree` inside the VM. See [Modules and packages](/config/modules#install-packages) and [Packages on the fly](/inside/packages).

## Does editing limanix.toml change the VM?

Not by itself. `limanix update --config limanix.toml` applies the file and restarts the VM. `limanix start` boots the saved system without reading the file. See [Changing a VM](/vms/update).

## What happens when an update fails to build?

The VM does not restart into the new system and keeps its current one, and the build error appears on your Mac. Fix the file and run `limanix update` again. Earlier steps are not undone: the VM's Lima settings may have changed and new `[env]` values may be installed; see [Troubleshooting](/troubleshooting).

## How do I reach a server running in the VM?

Add the port to `[network.ports]` and run `limanix update`, make the server listen on `0.0.0.0`, and connect to the address that `limanix list` shows for the VM. LimaNix does not forward ports to the Mac's `localhost`. See [Network](/vms/network).

## How do I delete a VM but keep its home?

Run `limanix delete dev-box`. It removes the VM's disk, keeps its home on the Mac and prints the home's path; `--remove-home` removes the home too. A new VM gets a new, empty home: copy what you need from the old one. See [Files and storage](/vms/storage).
