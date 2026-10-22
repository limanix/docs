---
description: Create, start, stop, list, check and delete LimaNix VMs from your Mac.
---

# Using virtual machines

You manage each VM from your Mac with the `limanix` command. This page follows a VM from `create`
to `delete`.

## Commands

| Command                                | What it does                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| `limanix create --config limanix.toml` | Creates a VM and its managed home, builds its NixOS system and starts it       |
| `limanix start dev-box`                | Starts a stopped VM with the system it already has                             |
| `limanix stop dev-box`                 | Shuts the VM down and keeps its disk and managed home                          |
| `limanix shell dev-box`                | Opens a shell in the VM; see [Shell and sessions](/vms/shell)                  |
| `limanix update --config limanix.toml` | Applies your edited `limanix.toml` to the VM; see [Changing a VM](/vms/update) |
| `limanix list`                         | Lists your VMs with their state, address and disk usage                        |
| `limanix doctor dev-box`               | Checks the VM and tells you what to fix                                        |
| `limanix network check dev-box 8080`   | Checks why the Mac cannot reach a port in the VM; see [Network](/vms/network)  |
| `limanix delete dev-box`               | Deletes the VM and keeps its managed home                                      |

Run them as your normal Mac user, without `sudo`.

## How names work

`create` and `update` take the VM name from `name` in `limanix.toml`. All other commands take the
name as an argument, such as `dev-box`.

::: code-group

```toml [limanix.toml]
name = "dev-box"
```

:::

A name has 1 to 63 lowercase letters, digits and hyphens, and starts and ends with a letter or
digit. Changing `name` in the file points the file at a different VM; it does not rename the
existing one.

## Create a VM

::: code-group

```sh [Mac]
limanix create --config limanix.toml
```

:::

`--config` is required. Creation downloads the base image when needed, boots the VM, builds its
NixOS system from the file and restarts it into that system. At the end, it prints the VM name and
the path of the VM's managed home on the Mac. The first run needs network access for the image and
the packages.

`create` refuses a name that already has a VM; change that VM with `limanix update` instead. To
write the file, start with [The limanix.toml file](/config/).

## Start and stop

::: code-group

```sh [Mac]
limanix stop dev-box
limanix start dev-box
```

:::

`stop` shuts the VM down and keeps its disk and managed home. `start` boots the system the VM
already has: it does not read `limanix.toml` or apply your changes. Use `limanix update` for that.

## List your VMs

::: code-group

```sh [Mac]
limanix list
```

:::

| Column    | Shows                                                                                                                                              |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NAME`    | The VM name                                                                                                                                        |
| `STATUS`  | The power state from Lima, such as `Running` or `Stopped`; `Missing` when Lima has no VM for the record                                            |
| `STATE`   | The result of the last create, update or delete: `ready`, `error`, `interrupted` or `corrupt`; `creating`, `updating` or `deleting` while one runs |
| `ADDRESS` | The VM's IPv4 address; see [Network](/vms/network)                                                                                                 |
| `DISK`    | How much of the guest disk is used; see [Files and storage](/vms/storage)                                                                          |

A `-` in `ADDRESS` or `DISK` means the VM is stopped, did not answer within 10 seconds, or has no
address on the shared network. A line under a row names an error or a notice. `limanix list --json`
prints the same values for scripts.

`STATE` is a saved result, not a live check: `Stopped` with `ready` means the last create or update
succeeded and the VM was stopped afterwards. Starting or stopping a VM does not reset an `error`.
[Troubleshooting](/troubleshooting) explains `error`, `interrupted`, `Missing` and `corrupt`.

## Check a VM

::: code-group

```sh [Mac]
limanix doctor dev-box
```

:::

`doctor` prints one row per check, with a hint under each row that needs attention. It checks the VM
in Lima and its saved record (`vm`), the VM's address (`address`), then the guest itself: its
configuration, the `lmxd` daemon, the NixOS generations and, when space runs low, the disk. A
stopped VM, or one that another command is changing, shows only the `vm` row. When the guest does
not answer, a `guest` row replaces its checks.

Each check is `ok`, `warning`, `failed` or `unknown`. The command exits with status 1 when a check
failed, and `--json` prints the same checks. `doctor` repairs nothing and does not restart the VM.
Inside the VM, `lmx doctor` runs the guest's checks; see [The lmx command](/inside/lmx).

## Delete a VM

::: code-group

```sh [Mac]
limanix delete dev-box
```

:::

`delete` stops the VM if it runs, then removes its disk and its saved record. The managed home
stays on the Mac, and the command prints its path. Your `limanix.toml` and shared project folders
stay too. `delete` also cleans up a VM that Lima no longer has.

::: warning
`delete` does not ask for confirmation. Save what you need from the guest disk first; see
[Files and storage](/vms/storage).
:::

To remove the managed home and all its files as well:

::: code-group

```sh [Mac]
limanix delete dev-box --remove-home
```

:::

When deletion fails because Lima cannot stop the VM, add `--force`. `--force` does not remove the
home; add `--remove-home` only when you want the home gone too. To create the VM again from the same
file, see [Recreate a VM](/vms/storage#recreate-a-vm).
