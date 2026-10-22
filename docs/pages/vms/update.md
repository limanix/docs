---
description: Apply an edited limanix.toml to an existing VM with limanix update.
---

# Changing a VM

Editing `limanix.toml` does not change a VM, and neither does installing a new `limanix` binary.
`limanix update` applies the file to the VM and restarts it.

## Apply a change

Save your work in the VM first: the update restarts the VM, which ends its sessions and services.
Then edit `limanix.toml` and apply it:

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

`update` finds the VM by `name` in the file. When it succeeds, open a shell and check the tool or
service you changed. Start again any service that you run by hand.

## What an update does

Each update gives the VM a new generation: the complete system that your `limanix.toml` describes.

1. The Mac checks the file and prepares the new generation.
2. If the VM runs, the update stops it. It then applies the new CPU, memory and disk settings.
3. The VM starts with its current system and builds the new generation. The build output appears in
   your terminal.
4. After a successful build, the VM restarts into the new generation.
5. The VM checks its system services, shared folders and your account, then removes the older
   generations.
6. The update marks the VM `ready` in `limanix list`.

A successful update leaves the VM running, even when it was stopped before. Before the build, the VM
makes room in its Nix store; a nearly full disk causes a warning, not a failure. See
[Files and storage](/vms/storage#keep-the-guest-disk-from-filling-up).

## What stays and what can change

An update keeps the VM itself: its guest disk, its managed home and your shared folders. You can
change CPU and memory, grow the disk, and change the shell, toolchains, modules, packages, dotfiles,
theme, environment, ports, mounts and `user.sudo`.

These settings are fixed when the VM is created:

| Setting          | Holds                                             |
| ---------------- | ------------------------------------------------- |
| `resources.arch` | The guest architecture                            |
| `user.name`      | The username in the VM                            |
| `user.home`      | The home path in the VM                           |
| `home.root`      | The folder on the Mac that holds the managed home |

An update that changes one of them fails with
`an update cannot change architecture, username, or managed-home paths`. Revert the change, or
create a new VM and copy the files you need.

The disk can grow but not shrink: `update` rejects a `disk` smaller than the disk's actual size,
which an earlier failed update may already have grown. See
[Resources and architecture](/vms/resources).

## When an update fails

A build error, such as a package name that does not exist, stops the update before the restart. The
VM keeps its current system, and the reason is in the output. Fix the file and run `limanix update`
again.

An update does not undo the steps it finished before it failed: the VM may already be stopped, have
its new CPU, memory and disk settings, or have new environment files. `limanix list` shows `error`
in `STATE`, and `limanix start` does not clear it: `start` boots the current system and does not
read your corrected file. Run `limanix update` again instead.

If the new generation boots but fails its checks, the update reports
`Generation … is booted but unhealthy` with the reason, and `limanix doctor dev-box` shows the
failing check. [Troubleshooting](/troubleshooting) covers the other errors.

## Cancel an update

Press Ctrl-C while `limanix update` builds. The build stops, the VM keeps running the generation it
ran before, and the command exits with status 130.

## A warning after success

`VM 'dev-box' is ready, but lmx reported: Finalizing generation … failed` means the new generation
runs, but the older ones could not be removed yet. The VM tries again after 15 minutes. Inside the
VM, `sudo lmx logs finalize` shows why the removal failed.

## Notices in the VM

When a built generation waits for a restart, the welcome in the VM shows a line such as:

::: code-group

```text [VM]
▲ restart  generation 4a1f9c2 is built; run limanix update on the Mac
```

:::

A short word also appears in tmux's status line, or outside tmux in the `pure` or `starship`
prompt:

| Word       | Meaning                                                | What to do                                          |
| ---------- | ------------------------------------------------------ | --------------------------------------------------- |
| `apply`    | The Mac handed over a generation that is not built yet | Run `limanix update` on the Mac                     |
| `applying` | An update is building right now                        | Wait for `limanix update` to finish                 |
| `restart`  | A new generation is built and waits for a restart      | Run `limanix update` on the Mac; it restarts the VM |

`lmx status` and `lmx doctor` in the VM show the same state; see [The lmx command](/inside/lmx).
