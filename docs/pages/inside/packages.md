---
description: Install a package for your user without changing limanix.toml.
---

# Packages on the fly

When no module or toolchain gives you a tool, take it straight from Nixpkgs, the package collection of NixOS. You run these commands inside the VM, for your own account, and none of them needs `sudo`.

## Try a tool without installing it

::: code-group

```sh [VM]
nix shell nixpkgs#openssl --command openssl version
```

:::

This runs one command with the tool. Without `--command`, `nix shell nixpkgs#openssl` opens a shell with the tool on your `PATH`; `exit` drops it again.

## Install a package

::: code-group

```sh [VM]
nix profile add nixpkgs#ripgrep
```

:::

The package goes into your profile and stays there until you remove it. `nixpkgs` here is the VM's own NixOS release: the same package set that the system and the modules use. A tool you add shares their libraries, and nothing is downloaded twice.

## List and remove packages

| Task                                    | Command                      |
| --------------------------------------- | ---------------------------- |
| List what you installed                 | `nix profile list`           |
| Remove a package                        | `nix profile remove ripgrep` |
| Free the disk space of removed packages | `nix profile wipe-history`   |

Older versions of your profile keep removed packages on disk until you run `nix profile wipe-history`. `lmx` never deletes them when it cleans up the disk; see [Make room on the disk](/inside/lmx#make-room-on-the-disk).

## Find a package name

Search [search.nixos.org](https://search.nixos.org/packages) in the channel of your VM's NixOS release. `nixos-version` shows it, such as 26.05.

## Profile or limanix.toml

Your profile belongs to this VM. A tool that every VM of yours should have belongs in `limanix.toml`, where it is part of the system that the VM is built from:

::: code-group

```toml [limanix.toml]
[nixos]
packages = ["tree"]
```

:::

| Use                          | When                                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `nix shell`                  | You need a tool once                                                                                            |
| `nix profile add`            | You want to keep a tool for yourself in this VM                                                                 |
| `packages` in `limanix.toml` | Every VM made from the file should have it; `limanix update` applies it and restarts the VM                     |
| `[toolchains]` or a module   | A language, or a tool that needs more than its package, such as a service or the language server for the editor |

[Modules and packages](/config/modules#install-packages) explains the `packages` list, and [Toolchains](/config/toolchains) the languages.
