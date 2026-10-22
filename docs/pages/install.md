---
description: Requirements, download, installation, updates and removal of the limanix client on macOS.
---

# Install

LimaNix is one binary for your Mac, `limanix`. It includes Lima and the module catalog: you don't install Lima or Nix separately.

## Requirements

| Requirement | Details                                                 |
| ----------- | ------------------------------------------------------- |
| macOS       | 26 or newer                                             |
| Mac         | Apple Silicon or Intel                                  |
| `ssh`       | In your `PATH`                                          |
| Account     | Your normal Mac user; run LimaNix without `sudo`        |
| Network     | Creating a VM downloads its base image and Nix packages |

A guest of the other architecture, such as an Intel guest on Apple Silicon, also needs QEMU. See [Resources and architecture](/vms/resources).

## Download

Download the binary for your Mac from [limanix.dev/download](https://limanix.dev/download) or from the [client releases](https://github.com/limanix/client/releases) on GitHub:

| Mac           | Binary          |
| ------------- | --------------- |
| Apple Silicon | `limanix-arm64` |
| Intel         | `limanix-amd64` |

To build the client from source instead, follow [Build a native client](https://github.com/limanix/client/blob/main/guides/development.md#build-a-native-client) in the client repository.

## Install the binary

For an Apple Silicon binary saved in `~/Downloads`:

::: code-group

```sh [Mac]
mkdir -p ~/.local/bin
install -m 755 ~/Downloads/limanix-arm64 ~/.local/bin/limanix
```

:::

On Intel, use `~/Downloads/limanix-amd64`. Adjust the path if you saved the file elsewhere.

## Add it to your PATH

::: code-group

```sh [Mac]
export PATH="$HOME/.local/bin:$PATH"
```

:::

The line applies to the current terminal. Add it to your shell's startup file to keep `~/.local/bin` in `PATH` for new terminal sessions.

## Check the installation

::: code-group

```sh [Mac]
limanix --version
limanix --help
```

:::

`--version` prints the client version, and `--help` lists the commands.

## The macOS approval prompt

The release binary has an ad-hoc signature with the virtualization entitlement, and Apple has not notarized it. If macOS asks you to approve opening the download, check that it came from limanix.dev or the client releases on GitHub before you allow it.

## Use the binary for your Mac

Run the binary that matches your Mac's hardware. VM operations reject `limanix-amd64` running under Rosetta on Apple Silicon. The native binary also runs a guest of the other architecture, with QEMU: for an Intel guest on Apple Silicon, use `limanix-arm64` with `resources.arch = "amd64"`. See [Resources and architecture](/vms/resources).

## Update the client

Download the new binary and run the same `install` command; it replaces the old one. Each client bundles its own catalog release, and existing VMs keep their system until you apply their file with the new client. For each VM, run this in the folder that holds its `limanix.toml`:

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

The update restarts the VM. [Changing a VM](/vms/update) explains what it does.

## Remove LimaNix

Removing the binary does not remove your VMs. Delete each VM first with `limanix delete NAME`: it removes the VM's disk and keeps its home on the Mac. Add `--remove-home` to remove the home too; LimaNix can no longer remove a home after its VM is deleted. Then remove the binary:

::: code-group

```sh [Mac]
rm ~/.local/bin/limanix
```

:::

These stay on your Mac:

| What                                                                                   | Where                                                                  |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Homes that `limanix delete` kept                                                       | Under `home.root`, `~/.limanix` by default; `delete` printed each path |
| LimaNix state, such as imported modules and records of kept homes                      | `~/Library/Application Support/Limanix`, or `LIMANIX_HOME` when set    |
| Your `limanix.toml` files and project folders                                          | Where you keep them                                                    |
| The network helper and Lima's sudoers rules, if `limanix network setup` installed them | `/opt/socket_vmnet/bin/socket_vmnet` and `/private/etc/sudoers.d/lima` |
