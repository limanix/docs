---
description: Set the CPU, memory, disk and guest architecture of a VM.
---

# Resources and architecture

The `[resources]` table sets the size of a VM and the architecture of its Linux system. This page
covers the settings, how to change them, and what a guest of another architecture needs.

## Set resources

::: code-group

```toml [limanix.toml]
[resources]
arch = "arm64"
cpu = 4
mem = "8GiB"
disk = "40GiB"
```

:::

| Setting | Value                                                    | Default   |
| ------- | -------------------------------------------------------- | --------- |
| `arch`  | Guest architecture: `arm64` or `amd64`                   | `"arm64"` |
| `cpu`   | Number of virtual CPUs, a positive whole number          | `4`       |
| `mem`   | Memory in whole GiB, as a quoted string such as `"8GiB"` | `"8GiB"`  |
| `disk`  | Size of the guest disk in whole GiB, such as `"40GiB"`   | `"10GiB"` |

`GiB` is the only unit: `"8GB"`, `"1.5GiB"`, `"0GiB"` and `"08GiB"` are rejected. A setting you
leave out keeps its default: `[resources]` with only `cpu = 2` keeps the default architecture,
memory and disk. On an Intel Mac, set `arch = "amd64"`.

`disk` covers only the guest disk; the managed home and shared folders live on the Mac. Leave room
for Docker images and volumes, Kubernetes clusters and build caches. See
[Files and storage](/vms/storage).

## Change resources

Edit `[resources]` and run `limanix update --config limanix.toml`. The update stops a running VM,
applies the new sizes and starts it again; see [Changing a VM](/vms/update).

| Setting      | With `update`                                                          |
| ------------ | ---------------------------------------------------------------------- |
| `cpu`, `mem` | Can change                                                             |
| `disk`       | Can grow; a smaller size is rejected                                   |
| `arch`       | Fixed when the VM is created; create a new VM for another architecture |

`update` compares `disk` with the disk's actual size, which an earlier failed update may already
have grown.

## Choose the guest architecture

The guest architecture and your Mac decide how the VM runs:

| Mac           | `arch`  | Runs with                      | Network                                    |
| ------------- | ------- | ------------------------------ | ------------------------------------------ |
| Apple Silicon | `arm64` | Apple Virtualization framework | Native NAT                                 |
| Intel         | `amd64` | Apple Virtualization framework | Native NAT                                 |
| Apple Silicon | `amd64` | QEMU                           | Lima shared network through `socket_vmnet` |
| Intel         | `arm64` | QEMU                           | Lima shared network through `socket_vmnet` |

A guest that matches your Mac needs neither QEMU nor `socket_vmnet`. LimaNix spells the
architectures `arm64` and `amd64`, not Nix's `aarch64` and `x86_64`.

## Run a guest of another architecture

Prepare the Mac before you create the VM. Install QEMU, and make the emulator for the guest
architecture available in your Mac's `PATH`:

| Guest `arch` | Executable            |
| ------------ | --------------------- |
| `amd64`      | `qemu-system-x86_64`  |
| `arm64`      | `qemu-system-aarch64` |

Then prepare the network as your regular Mac user, in an interactive terminal:

::: code-group

```sh [Mac]
limanix network setup
```

:::

The command checks the existing Lima network setup. When something must be installed, it shows the
paths and asks for confirmation before it runs `sudo`:

| Item                   | Location                             |
| ---------------------- | ------------------------------------ |
| Bundled network helper | `/opt/socket_vmnet/bin/socket_vmnet` |
| Lima sudoers rules     | `/private/etc/sudoers.d/lima`        |

An existing sudoers file is backed up before it is replaced. LimaNix and QEMU keep running as your
user. `limanix create` and `limanix update` of a QEMU guest offer the same installation in an
interactive terminal; in a noninteractive run, they report that the setup is required instead.

## Use the client for your Mac

Run the `limanix` binary built for your Mac's hardware: `limanix-arm64` on Apple Silicon,
`limanix-amd64` on Intel. VM commands reject the Intel binary running through Rosetta on Apple
Silicon. For an Intel guest on Apple Silicon, use the `arm64` client with `arch = "amd64"`.
