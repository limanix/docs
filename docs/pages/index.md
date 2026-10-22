---
description: LimaNix runs NixOS development machines on your Mac, declared in one TOML file.
---

# What is LimaNix?

LimaNix runs Linux development machines on your Mac. You describe a virtual machine in one file, `limanix.toml`, and the `limanix` command creates it: a NixOS system with your shell, languages, services and packages.

LimaNix is for developers on a Mac who want their tools and services to run on Linux while the editor and project files stay on the Mac. You don't need to know Nix, and you don't install Lima or Nix on the Mac.

## Why LimaNix

### One file declares the whole machine

`limanix.toml` lives beside your project and describes the VM: its resources, account, shared folders, environment, firewall ports, shell, toolchains, modules and packages. A few lines choose the tools:

::: code-group

```toml [limanix.toml]
[shell]
preset = "terminal"

[toolchains]
go = "1.27"
python = "3.14"

[nixos]
modules = ["lmx:docker", "lmx:postgres"]
packages = ["kubectl"]
```

:::

### NixOS builds before the VM restarts

`limanix update` builds the new system inside the VM and restarts the VM only when the build succeeds. When a build fails, the VM keeps the system it had. After the restart, LimaNix checks the new system before it removes the old one.

### A catalog of modules that fit together

Shell components, toolchains and services come from a catalog bundled with the client. They share one theme and know about each other: each toolchain connects its language server to the editor. Anything else comes from nixpkgs, and a NixOS module of your own plugs into the same system.

### Tools inside the VM

Every VM comes with `lmx`. It greets you with a welcome when you open a shell, `lmx status` and `lmx doctor` show how the VM is doing and what to fix, and `lmx help` explains what each module gives you. `pbcopy` and `pbpaste` reach the Mac clipboard.

### Your Mac stays in charge of files

Project folders you share stay on the Mac and appear in the VM as you edit them. Your home inside the VM is kept on the Mac too, under `~/.limanix` by default: it survives updates and stays when you delete the VM.

## What's in the box

- [`limanix`](/vms/): one binary for the Mac, with Lima built in, that creates, updates, starts, stops and deletes VMs and opens a shell in them.
- [Shell](/config/shell): Zsh with Oh My Zsh and the Pure prompt, AstroNvim, tmux, Lazygit, Yazi and the GitHub CLI, or Bash with the command-line tools.
- [Toolchains](/config/toolchains): Go, Rust, Python and Node.js, each with its language server.
- [Modules](/modules/): Docker, PostgreSQL, Google Cloud CLI, Claude Code, Posting and Harlequin.
- [Packages](/config/modules#install-packages): any command from nixpkgs, or a newer release from nixos-unstable.
- [Shared folders](/config/mounts) and [dotfiles](/config/dotfiles): your project and your settings from the Mac, in every VM.
- [`lmx`](/inside/lmx): status, checks and help inside the VM.
- [Clipboard](/inside/clipboard): `pbcopy` and `pbpaste` to the Mac clipboard, also inside tmux.
- [Network](/vms/network): reach services at the VM's address, and check why a port does not answer.

To try it, follow the [Quick start](/quick-start).
