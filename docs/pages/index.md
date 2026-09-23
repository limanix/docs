# Limanix

Linux development environments on macOS, configured with TOML and NixOS modules.

Keep your project and editor on your Mac; run tools, services, and builds inside
a Linux virtual machine. Limanix uses Lima to run the VM and NixOS to configure
the guest system.

## How it works

1. Describe your environment in a TOML file: resources, modules, shared folders, and environment variables.
2. Create a Linux VM with the tools and services your project needs.
3. Edit files on macOS and build, test, and run your project inside the VM.

## Project repositories

- [Client](https://github.com/limanix/client) — the Limanix command-line application.
- [Modules](https://github.com/limanix/modules) — the standard NixOS module catalog.
- [Documentation](https://github.com/limanix/docs) — this website.

## Maintaining Limanix

The [release process](releases/index.md) explains how module releases reach
supported clients and how their documentation is published.

```{toctree}
:hidden:
:maxdepth: 2
:caption: Project

releases/index
```
