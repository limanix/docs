---
description: Check, diagnose and explore a VM from inside with lmx.
---

# The lmx command

Every VM comes with `lmx`, a command that tells you how the VM is doing, finds what is wrong and says what to do about it. This page walks through it by task; [lmx command](/reference/lmx) lists every command and option.

Most `lmx` commands need no `sudo`; run `lmx logs` and `lmx store reserve` with it.

## The welcome

Each new shell session starts with a summary of the VM: its name and state, NixOS version and architecture, the running generation and when it was updated, CPUs, memory, uptime and free disk space, its addresses and open ports, the shared folders and the selected modules. Below them are a few commands to start with. Run `lmx welcome` to show it again.

A generation is the complete system that your `limanix.toml` describes; each `limanix update` builds a new one. Beside the VM name is its state: `ready` when the VM runs the configuration you applied and it passed its checks, `applying` while an update builds, and `checking` while a new generation is checked. When something needs attention, the state turns into a warning, and each problem gets a line below the columns with the command that helps:

::: code-group

```text [VM]
  ▲ failed   postgresql.service; run systemctl status postgresql.service
  ▲ disk low 8% of space free on the guest disk; run sudo lmx store reserve
  ▲ restart  generation 4a1f9c2 is built; run limanix update on the Mac
```

:::

## Check the state

::: code-group

```console [VM]
$ lmx status
Generation    desired 0123456789ab, built 0123456789ab, booted 0123456789ab
Disk          8.0 GiB of 16 GiB free
Network       enp0s1 192.0.2.10
Failed units  none
Owner         lmxd 0.1.0, idle
```

:::

| Line         | Tells you                                                                                                                                                                           |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Generation   | The generation the Mac handed over (`desired`), the one built for the next boot (`built`) and the one running now (`booted`). When all three match, the VM runs what you asked for. |
| Disk         | Free space on the disk that holds the Nix store                                                                                                                                     |
| Network      | The VM's addresses, the ones the Mac connects to                                                                                                                                    |
| Failed units | System services that failed                                                                                                                                                         |
| Owner        | The version of `lmxd` and what it is doing right now                                                                                                                                |

`Condition` lines below them say where the VM stands and why, such as a generation that waits for a restart. A fact that cannot be read shows as `unknown`, with a `Problem` line that explains it. Run `sudo lmx status` to read every fact: without `sudo`, the generation the Mac handed over may show as `unknown`.

### Status words in tmux and the prompt

The tmux status line, or the Pure or Starship prompt outside tmux, shows a short word when the VM needs attention. It comes from `lmx status --short` and stays empty while all is well.

| Word       | Means                                                   | What to do                                    |
| ---------- | ------------------------------------------------------- | --------------------------------------------- |
| `degraded` | The running generation failed its health check          | Run `lmx doctor`, then `sudo lmx logs health` |
| `finalize` | The update works, but removing older generations failed | Nothing urgent: `lmxd` tries again later      |
| `disk-low` | Less than 10% of the disk is free                       | Run `sudo lmx store reserve`                  |
| `restart`  | A new generation is built and waits for a restart       | Run `limanix update` on the Mac               |
| `applying` | An update is being built                                | Wait for `limanix update` to finish           |
| `apply`    | The Mac handed over a generation that is not built yet  | Run `limanix update` on the Mac               |
| `lmxd?`    | `lmxd` did not answer in time                           | Run `lmx doctor`                              |

## Find what is wrong

::: code-group

```console [VM]
$ lmx doctor
ok      config      /etc/lmx/config.json is valid; generation 0123456789ab.
ok      owner       lmxd 0.1.0 answers.
warning generations Generation 0123456789ab is built; restart the VM to boot it.
                    Restart the VM from the Mac; limanix update does it.
```

:::

Each line is one check, and the indented line under a finding says what to do. `lmx doctor` checks the configuration of `lmx`, whether `lmxd` answers with the same version as `lmx`, the generations and the disk. When `limanix.toml` names [dotfiles](/config/dotfiles), it also checks that they are linked. It works even when `lmxd` is down.

| Status    | Means                                                                 |
| --------- | --------------------------------------------------------------------- |
| `ok`      | Fine                                                                  |
| `warning` | Worth knowing; nothing is broken                                      |
| `failed`  | Broken; `lmx doctor` exits with status 1                              |
| `unknown` | Your account may not read what the check needs; run `sudo lmx doctor` |

::: tip
On the Mac, `limanix doctor dev-box` runs the same checks and adds the VM's state and address.
:::

## Get help

`lmx help`, or `lmx` alone, shows the VM, your account, the selected modules and the commands inside the VM and on the Mac. It also lists the help topics: `lmx help TOPIC` shows what a module gives you, such as `lmx help python`, with the versions this VM runs, its commands, common tasks and a link to its guide. A topic with a version, such as `python-3.12`, works too.

For one command, add `--help`, such as `lmx status --help`. `lmx info` shows the kernel, the disk, the shared folders and the failed services.

## Read the output of an update

`lmxd` writes the output of its jobs to the journal, and `lmx logs` shows the latest run of a kind:

| Command                  | Shows                                     |
| ------------------------ | ----------------------------------------- |
| `sudo lmx logs apply`    | The build of a generation                 |
| `sudo lmx logs health`   | The health check after a restart          |
| `sudo lmx logs finalize` | The removal of older generations          |
| `sudo lmx logs collect`  | The last cleanup of the Nix store         |
| `sudo lmx logs roots`    | The last report of what still holds space |

An update builds in one boot and restarts into the next. Read its build output with `sudo lmx logs apply --previous`.

## Check a port

::: code-group

```sh [VM]
lmx net check 8080
```

:::

When the Mac cannot reach a service in the VM, this checks whether the VM's firewall opens the port, whether anything listens on it on an address the Mac can reach, and which program holds it. Add `--udp` for a UDP port. On the Mac, `limanix network check dev-box 8080` runs the same checks and then tries to connect. See [Network](/vms/network).

## Check your dotfiles

`lmx dotfiles` shows which entries of your [dotfiles](/config/dotfiles) are linked into your home, which links are missing and which of your own files are in the way. It changes nothing. `lmx dotfiles link` makes the links now; every new shell does it too.

## Make room on the disk

`lmxd` keeps the Nix store from filling the disk. When less than 20% is free, it removes store paths that nothing uses; below 10%, the welcome and `lmx status` warn. To make room now:

::: code-group

```sh [VM]
sudo lmx store reserve
```

:::

It cleans up at once when less than 20% is free, waits for the cleanup to finish and prints how much it freed. Packages that something still uses stay on disk, such as those of `nix-direnv` shells, of `result` links from `nix build` and of older versions of your [profile](/inside/packages); `sudo lmx logs roots` lists what holds them. Remove what you no longer need, then run `sudo lmx store reserve` again. If the disk is still too small, give the VM a bigger one; see [Resources and architecture](/vms/resources).

## What lmxd does in the background

`lmxd` is a small daemon that does the work that must not depend on your terminal:

- It checks the disk 5 minutes after boot and then every 15 minutes, and cleans the Nix store when space runs low.
- It builds the update you start with `limanix update` on the Mac. A dropped connection does not stop the build.
- After the restart, it checks the new generation, then removes the older ones.

When `lmxd` is down, your shell, files and services keep working; updates and store cleanup wait until it is back. `lmx doctor` says what failed, and the next `limanix update` starts `lmxd` again.

## Other commands

| Command                                     | Does                                                                                     |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `lmx version`                               | Prints the version of `lmx` and of the contract it speaks with the Mac                   |
| `lmx session NAME`                          | Opens a named session, like `limanix-session NAME`; see [Shell and sessions](/vms/shell) |
| `lmx clipboard copy`, `lmx clipboard paste` | The same as `pbcopy` and `pbpaste`; see [Clipboard](/inside/clipboard)                   |
