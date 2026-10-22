---
description: How limanix, Lima, the catalog and lmx build and run a VM, and where LimaNix keeps its state.
---

# How it works

This page shows what runs where, how a change in `limanix.toml` reaches the VM, and where LimaNix keeps its state. Read it to understand what a command does, or before you recover from a failed one.

## The parts

| Part        | Runs on                   | What it does                                                                                                                  |
| ----------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `limanix`   | Mac                       | Reads `limanix.toml`, prepares the VM's system and runs every VM command.                                                     |
| Lima        | Mac, built into `limanix` | Runs the VM with Apple's Virtualization framework for a guest of the Mac's architecture, or with QEMU for the other one.      |
| The catalog | Mac, built into `limanix` | Shell components, toolchains and modules, with the Nixpkgs revision they build from. Each client bundles one catalog release. |
| NixOS       | VM                        | The Linux system of the VM, built from your file and the catalog.                                                             |
| `lmx`       | VM                        | The guest command: the welcome, `lmx status`, `lmx doctor`, `lmx help` and the clipboard commands.                            |
| `lmxd`      | VM                        | A root daemon under systemd that builds and checks each new system and keeps the Nix store from filling the disk.             |

`limanix` reaches the VM over SSH. `limanix shell` connects as your development account, and `limanix list` and `limanix doctor` ask `lmx` in the VM for its address, disk usage and checks. `lmxd` listens on no network port: the Mac reaches it only through SSH and `sudo lmx`.

A new VM boots from the base image of the bundled catalog release, which `limanix` downloads if needed. The client pins an `lmx` release, and the VM downloads it while it builds its system.

## How a change reaches the VM

`limanix create` and `limanix update` take the same path. Each run prepares a new generation: the complete system that your file describes.

1. **Check.** `limanix` parses and validates `limanix.toml`, then checks the Mac: the macOS version, a native binary, `ssh`, and QEMU when the guest needs it.
1. **Prepare.** It copies the selected modules into the inputs of the generation, pinned to the catalog's Nixpkgs revision. `create` also allocates the managed home and creates the VM. `update` keeps the VM and its home, checks the disk size, and stops a running VM before it changes the VM's Lima settings.
1. **Start.** It starts the VM with the inputs mounted read-only at `/mnt/limanix`.
1. **Hand over.** It stops the VM's own `lmx`, builds the `lmx` release that the generation pins, and runs that release's `lmxd` for the build. Because the build uses the new generation's `lmxd`, a new VM and one made by an older client take the same steps.
1. **Build.** That `lmxd` installs the environment files from `[env]`, makes room in the Nix store and builds the NixOS system for the next boot. `limanix` prints the build output.
1. **Restart.** After a successful build, `limanix` restarts the VM into the new system.
1. **Check and clean up.** `lmxd` checks the platform services, the shared folders and the development account. Then it removes the older system generations and their boot entries, and collects store paths that nothing references.
1. **Ready.** `limanix` waits until `lmxd` reports the generation converged, saves the VM as `ready` and removes old inputs.

A successful update leaves the VM running, even if it was stopped before. Editing `limanix.toml` alone changes nothing, and `limanix start` boots the saved system without reading the file.

## When a step fails

| What fails                      | What happens                                                                                                                                     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| The build                       | The VM does not restart and keeps its current system, and its own `lmxd` takes over again. The error is in the output on your Mac.               |
| The build, canceled with Ctrl-C | `limanix` cancels the build and brings back the VM's own `lmxd`. The VM keeps the system it ran, and the command ends with status 130.           |
| A check after the restart       | The new system runs, but the command fails with `Generation … is booted but unhealthy` and the reason. `limanix doctor dev-box` shows the check. |
| Only the cleanup                | The VM is ready with a warning, and `lmxd` tries again later.                                                                                    |

An update is not a transaction: completed steps are not undone. The VM may already be stopped, its Lima settings may have changed, or new environment files may be installed. Fix the cause and run `limanix update` again; [Troubleshooting](/troubleshooting) covers each case.

## The guest disk

LimaNix keeps only the applied system generation on the guest disk. `lmxd` collects unused Nix store paths when less than 20% of the disk is free, and below 10% the welcome and `limanix update` warn; your own roots, such as `nix-direnv` shells and `result` links, are never removed. [Files and storage](/vms/storage) shows how to make room or grow the disk.

## Where state lives

| State                              | Where it lives                                                                          | What to know                                                    |
| ---------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| VM identity and operation progress | The LimaNix state directory: `~/Library/Application Support/Limanix`, or `LIMANIX_HOME` | The identity stays readable when the progress record is damaged |
| The VM and its guest disk          | Lima's storage: `~/.lima`, or `LIMA_HOME`                                               | `limanix delete` removes the VM before LimaNix's own records    |
| Managed home                       | `home.root` on the Mac, `~/.limanix` by default                                         | Kept by `limanix delete`; `--remove-home` removes it            |
| Shared project folders             | Their own folders on the Mac                                                            | Changes in the VM change the original files                     |
| Applied system                     | The guest disk and its Nix store; only the applied generation is kept                   | Rebuilt from the saved generation inputs                        |

A lock per VM keeps two commands from changing the same VM at once; `limanix shell` does not take it. `limanix list --json` reports Lima's power state and the last LimaNix operation as separate values. A failed operation keeps the records and inputs needed to diagnose it. `LIMANIX_HOME` and `LIMA_HOME` do not move existing VMs: use the same values whenever you work with them. Read [Troubleshooting](/troubleshooting) before you remove any state by hand.
