---
description: Where the files of a VM live, what deleting it removes and how its disk keeps free space.
---

# Files and storage

A VM keeps files in three places: on its own disk, in a home folder on your Mac, and in the project
folders you share. This page shows which is which, what each command keeps, and how the guest disk
keeps free space.

## Where your files live

| Place         | Where the files are                                                                | After `limanix delete`                      |
| ------------- | ---------------------------------------------------------------------------------- | ------------------------------------------- |
| Guest disk    | Inside the VM, outside shared folders; holds NixOS and data written outside mounts | Removed                                     |
| Managed home  | On the Mac beneath `~/.limanix`; appears at `/home/dev` inside the VM              | Kept by default; `--remove-home` removes it |
| Project mount | A Mac folder that appears in the VM, such as at `/workspace`                       | Kept on the Mac                             |

The managed home and read-write project mounts share their files with the Mac: an edit or a deletion
on either side changes the same file. A mount is not a backup. To share a project folder, see
[Shared folders](/config/mounts).

## The guest disk

The guest disk holds NixOS, the Nix store and every file outside the shared folders, including
service data under `/var`, such as Docker images and volumes. It keeps only the NixOS system the VM
runs; each update removes the older ones. Its size is `disk` in `[resources]`; see
[Resources and architecture](/vms/resources).

## The managed home

Each VM gets its own home folder on the Mac, at `<home.root>/<name>-<id>`, and sees it at
`user.home`. With the defaults, the home of `dev-box` could be `~/.limanix/dev-box-a1b2c3d4e5f6`,
mounted at `/home/dev`:

::: code-group

```toml [limanix.toml]
[user]
home = "/home/dev"

[home]
root = "~/.limanix"
```

:::

The suffix is generated: `limanix create` prints the actual path, and the `home` field of
`limanix list --json` shows it. The home holds your files, the dotfiles you keep in it and caches
that live in the home. A relative `root` is resolved from the folder of `limanix.toml`, and `~` is
the home of your Mac account. `home.root` and `user.home` cannot change after the VM is created.

## What each command keeps

| Command                             | Guest disk            | Managed home               | Project folders                 |
| ----------------------------------- | --------------------- | -------------------------- | ------------------------------- |
| `stop`, `start`                     | Kept                  | Kept                       | Kept                            |
| `update`                            | Kept and reconfigured | Kept                       | Kept; mount settings can change |
| `delete`, with or without `--force` | Removed               | Kept                       | Kept                            |
| `delete --remove-home`              | Removed               | Removed with all its files | Kept                            |

LimaNix has no snapshot or backup command. Before you delete a VM, keep `limanix.toml` and your
module folders, back up the home and project folders you need, and export data that lives only on
the guest disk, such as databases or Docker volumes. The TOML recreates the system, not your data.

## Recreate a VM

After a delete, `limanix create --config limanix.toml` creates a new VM from the same file, with a
new, empty managed home. The old home stays at the path that `delete` printed, and LimaNix does not
attach it again. Copy the files you need into the new home or a project folder.

Once the VM is deleted, `limanix delete --remove-home` can no longer remove its old home. Keep the
printed path and remove that folder yourself when you no longer need it.

## Keep the guest disk from filling up

The VM cleans its Nix store by itself:

| Free space on the guest disk | What happens                                                                                                                      |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Less than 20%                | The `lmxd` daemon removes store paths that nothing uses anymore. It checks every 15 minutes and also cleans up after each update. |
| Less than 10%                | The welcome and `lmx status` warn, `lmxd` logs what still holds space, and `limanix update` warns before it starts.               |

Low space never blocks an update. `limanix list` shows the used share of the disk in `DISK`; inside
the VM, `lmx info` shows it too.

The cleanup never deletes what is still in use: the running system, garbage-collector roots such as
`nix-direnv` shells and `result` links from `nix build`, and data outside the Nix store, such as
Docker images and volumes under `/var/lib/docker`.

### Make room

When the disk stays full, look at what holds space in the VM:

::: code-group

```sh [VM]
lmx info
sudo lmx logs roots
```

:::

`lmx info` shows the usage. `sudo lmx logs roots` shows the roots that `lmxd` logged when less than
10% was free; `sudo nix-store --gc --print-roots` lists the roots now. Remove what you no longer
need, such as an old `result` link, a project's `.direnv` folder or Docker data with
`docker system prune`. Then collect the store paths they kept:

::: code-group

```sh [VM]
sudo lmx store reserve
```

:::

The command collects right away when less than 20% is free, waits for the collection and prints the
usage before and after. `sudo nix-store --gc` collects whatever the free space.

If that is not enough, raise `disk` in `[resources]` and run `limanix update` on the Mac. Tools you
removed from your own `nix profile` stay on disk until `nix profile wipe-history`; see
[Packages on the fly](/inside/packages).

## On the Mac

Lima keeps the guest disk under `~/.lima`, or `LIMA_HOME` when set. LimaNix keeps its records of
each VM in `~/Library/Application Support/Limanix`, or `LIMANIX_HOME` when set. Leave both to the
`limanix` commands, and read [Troubleshooting](/troubleshooting) before you change anything there.
