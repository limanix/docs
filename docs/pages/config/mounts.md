---
description: Share folders of your Mac with a VM.
---

# Shared folders

Each `[[mounts]]` entry shares a folder of your Mac with the VM. Both sides see the same files: you edit them on the Mac and run your tools in the VM.

## Share your project

::: code-group

```toml [limanix.toml]
[[mounts]]
source = "."
target = "/workspace"
mode = "rw"
```

:::

| Key      | Value                                                                |
| -------- | -------------------------------------------------------------------- |
| `source` | The folder on the Mac. Required.                                     |
| `target` | Where the folder appears in the VM, an absolute path. Required.      |
| `mode`   | `rw` to read and write, the default, or `ro` for read-only in the VM |

`"."` is the folder that holds `limanix.toml`. Apply the change with `limanix update --config limanix.toml`; see [Changing a VM](/vms/update). In the VM, `cd /workspace` then opens your project, and `lmx info` lists the shared folders.

## Share several folders

Repeat the block for each folder:

::: code-group

```toml [limanix.toml]
[[mounts]]
source = "."
target = "/workspace"
mode = "rw"

[[mounts]]
source = "../fixtures"
target = "/mnt/fixtures"
mode = "ro"
```

:::

Each source must be a folder that exists when you create or update the VM: create `../fixtures` on the Mac first. With `ro`, programs in the VM can read `/mnt/fixtures` but not change it.

## Paths on the Mac

Relative sources resolve from the folder that holds `limanix.toml`, wherever you run the command. For `~/projects/my-project/limanix.toml`:

| In the file    | On the Mac                       |
| -------------- | -------------------------------- |
| `"."`          | `~/projects/my-project`          |
| `"./fixtures"` | `~/projects/my-project/fixtures` |
| `"../shared"`  | `~/projects/shared`              |
| `"~/projects"` | `projects` in your home folder   |

Only a leading `~` expands. `$HOME` and `${PROJECT}` stay literal text: the file does not read shell variables. If `limanix.toml` is a symlink, paths resolve from the real file's folder.

## Paths in the VM

A target is an absolute path other than `/`, without whitespace, `:` or `..` parts. Two mounts cannot overlap: `/workspace` and `/workspace/cache` are rejected as two targets.

A mount cannot replace your home folder in the VM or a folder above it. A mount inside it works, such as `/home/dev/.config/nvim` when your home is `/home/dev`.

These paths and everything below them belong to the VM's system: `/etc`, `/boot`, `/usr`, `/var`, `/nix`, `/run`, `/dev`, `/proc`, `/sys`, `/bin`, `/sbin`, `/mnt/limanix`, `/mnt/dotfiles` and `/home/limanix-admin`. `/home` itself is reserved too.

## Remove all mounts

Without a `mounts` setting, the VM gets two example mounts: `~/projects/my-project` at `/workspace` and `~/.ssh/limanix` at `/mnt/git-keys`. To have no mounts, put `mounts = []` before the first table and remove every `[[mounts]]` block:

::: code-group

```toml [limanix.toml]
schema_version = 1
name = "dev-box"
mounts = []

[shell]
preset = "minimal"
```

:::

Your home folder in the VM stays shared. With the defaults, it lives on the Mac under `~/.limanix` and appears at `/home/dev`; [Files and storage](/vms/storage) explains it.

## Changes in the VM change the Mac

A read-write mount is the Mac folder itself, and so is your home folder in the VM. Editing, creating or deleting a file in the VM changes it on the Mac. `limanix delete` leaves shared folders on the Mac, and it keeps your home folder unless you add `--remove-home`.

::: warning
A mount is not a backup. Deleting files in `/workspace` deletes them from your project on the Mac.
:::

Use `mode = "ro"` for a folder that programs in the VM should only read.
