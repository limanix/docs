---
description: Find a problem by its symptom, then read its cause and the fix.
---

# Troubleshooting

Find the symptom below. Each section gives the cause and the fix, and every command says where it runs: on the Mac or in the VM. The examples use a VM named `dev-box`.

Start with the output of the command that failed: it names the problem. Then check the VM from the Mac:

::: code-group

```sh [Mac]
limanix doctor dev-box
```

:::

`limanix doctor` prints one row per check, with a hint under each problem, and exits with status `1` when a check failed. It does not repair or restart anything. [Collect diagnostics](#collect-diagnostics) lists the other places to look.

## limanix refuses to run on this Mac

`create` and `update` check the Mac before they change anything, and every command that works on a VM refuses a binary for the wrong architecture. They stop with one of these messages:

| Message                                                                                                   | Fix                                                                                                     |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `host macOS is older than this build's minimum: need … or newer, found …`                                 | Update macOS. The current client needs macOS 26 or newer.                                               |
| `this Limanix binary is running under Rosetta on Apple Silicon; use limanix-arm64 for VM operations`      | Install `limanix-arm64`. An Intel guest on Apple Silicon also uses it, with `resources.arch = "amd64"`. |
| `this Limanix binary is built for …, but the host is …; use the matching native binary for VM operations` | Install the binary for your Mac: `limanix-arm64` on Apple Silicon, `limanix-amd64` on Intel.            |
| `make the system SSH client available in PATH`                                                            | Add the directory of `ssh` to your `PATH`. `command -v ssh` prints its path once it is found.           |
| `this Limanix build does not include the native macOS VZ driver`                                          | Install a release binary. A client you build yourself must be a native build that includes the driver.  |

See [Install](/install).

## limanix create fails before the VM starts

`create` checks the file, the selected modules and the Mac, then prepares the managed home and the Lima instance. These messages stop it before the VM starts; `update` runs the same checks.

| Message                                                                                            | Fix                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `required flag --config was not provided`                                                          | Name the file: `limanix create --config limanix.toml`.                                                                                                 |
| A key and a problem, such as `resources.mem: …`, or `config: invalid TOML at line …, column …`     | Fix that key. Unknown keys and wrong types are rejected, including typos such as `resources.cpus`. See [limanix.toml](/reference/config).              |
| An error about a path from `[[mounts]]`, or one that starts with `shell.dotfiles:`                 | Create the directory or correct the path. A relative path starts from the directory of `limanix.toml`, not from the directory of your terminal.        |
| `… set home.root to a writable directory`                                                          | Set `[home] root` to a directory your Mac account can write to.                                                                                        |
| `run Limanix as your regular host user, not root`                                                  | Run the command without `sudo`.                                                                                                                        |
| `VM '…' already has state; use update or delete`                                                   | A VM of this name exists. Check `limanix list`, then run `limanix update` to retry it, or `limanix delete` only if you mean to remove it.              |
| `unknown standard module "lmx:…"; use limanix modules list`                                        | Compare the selector with `limanix modules list`.                                                                                                      |
| `module "third-party:…": cannot read module directory: …`                                          | Import the module with `limanix modules add` before you select it.                                                                                     |
| `nixos.modules[0]: lmx:go is a toolchain; choose its version in [toolchains], such as go = "1.27"` | Choose a toolchain in `[toolchains]`, and a shell component, such as `lmx:tmux`, in `[shell]`. `[nixos] modules` takes only modules of kind `modules`. |
| `toolchains.go: the bundled catalog has no go line "…"; choose one of …`                           | Choose one of the listed lines. `limanix modules list` shows them too, such as `lmx:go-1.27`.                                                          |
| `… SSH socket path needs … bytes (maximum …); use a shorter VM name or storage path`               | Use a shorter VM name or a shorter `LIMA_HOME`. Changing `LIMA_HOME` does not move existing VMs.                                                       |

## limanix create names a folder you did not configure

The error names a path in your home on the Mac that ends in `projects/my-project` or `.ssh/limanix`, which you never set up.

Cause: your `limanix.toml` has no `mounts` setting. An omitted setting keeps its default, and the default mounts are two examples: `~/projects/my-project` at `/workspace` and `~/.ssh/limanix` at `/mnt/git-keys`. Their folders must exist. The same applies to `[env]`, whose default has two example variables, and to `tcp` in `[network.ports]`, whose default opens port `8080`.

Fix: write your own `[[mounts]]` blocks, or remove the examples with `mounts = []` before the first table:

::: code-group

```toml [limanix.toml]
schema_version = 1
name = "dev-box"
mounts = []
env = {}
```

:::

See [Defaults](/reference/config#defaults) and [Shared folders](/config/mounts).

## limanix create or update fails while building the system

The build runs in the VM after the checks. When it fails, the VM is not restarted and keeps the system it runs. The reason is in the output of the command; inside the VM, `sudo lmx logs apply` shows the build again.

| Cause                                                                                         | Fix                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A name in `[nixos] packages` is not a package                                                 | Correct it. Names are attribute paths in the guest's nixpkgs: search them at [search.nixos.org](https://search.nixos.org/packages) in the channel of the guest's NixOS release, or `unstable` for `unstable:` names. |
| Two packages provide the same command                                                         | The error names both. Keep one of them.                                                                                                                                                                              |
| A package's license is refused although you listed it                                         | Naming a package allows it by the last part of its name. When the package's own name differs, the nixpkgs error names it, and a NixOS module of yours can allow it with `nixpkgs.config.allowUnfreePackages`.        |
| A module of your own does not build                                                           | Fix its files, then import them again: `limanix modules remove NAME`, `limanix modules add NAME DIRECTORY`.                                                                                                          |
| `No space left on device`, or `guest disk is full; raise resources.disk or remove guest data` | See [The guest disk is full](#the-guest-disk-is-full).                                                                                                                                                               |

A failed operation does not undo the steps before it: the VM may be stopped, its Lima settings may have changed, or new environment files may be installed. `limanix list` shows the VM with the state `error` and the saved error under its row.

After you fix the cause, run `limanix update` with a file of the same VM name. This also applies after a failed `create`: a second `create` for a name with saved state is rejected.

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

`limanix start` is not a retry. It boots the saved VM without your corrected file and keeps the error.

## A library listed in packages cannot be imported

Cause: `[nixos] packages` is for packages that bring their own commands. A library such as `python3Packages.requests` installs, but a program cannot import it.

Fix: install the library in the project's environment, such as a Python venv, or use a module. See [Modules and packages](/config/modules).

## limanix create fails for a guest of the other architecture

An `amd64` guest on Apple Silicon, or an `arm64` guest on Intel, runs with QEMU on Lima's shared network. It needs QEMU and the network helper on the Mac; `create` and `update` stop with one of these messages when something is missing.

| Message                                                                                | Fix                                                                                                                                    |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `install QEMU and make qemu-system-x86_64 available in PATH`, or `qemu-system-aarch64` | Install QEMU and put the executable for the guest in your `PATH`: `qemu-system-x86_64` for `amd64`, `qemu-system-aarch64` for `arm64`. |
| `socket_vmnet setup is required; run limanix network setup in an interactive terminal` | Run `limanix network setup` in a terminal. It asks before it uses `sudo`.                                                              |
| `socket_vmnet setup declined; no privileged files were changed`                        | Run `limanix network setup` again and accept, or use a guest of your Mac's architecture.                                               |
| `run network setup as your regular user; …`                                            | Run `limanix network setup` without `sudo`.                                                                                            |
| `automatic setup requires Lima's default socketVMNet, varRun and sudoers paths; …`     | Your Mac uses custom Lima network paths. The administrator of that setup configures the helper and its authorization.                  |

::: code-group

```sh [Mac]
limanix network setup
```

:::

See [Resources and architecture](/vms/resources).

## The VM does not start

`limanix start dev-box` fails, or `limanix list` shows a `STATUS` other than `Running` or `Stopped`, such as `Broken`.

Cause: Lima could not boot the VM. Its host agent writes the reason to log files.

Fix:

1. Run `limanix doctor dev-box`. Its `vm` check shows what Lima reports.
1. Find the name of the Lima instance in `lima_name` of `limanix list --json`.
1. Read `ha.stderr.log` and `ha.stdout.log` in the directory of that instance under `~/.lima`, or under `LIMA_HOME` when you set it.

::: code-group

```sh [Mac]
limanix doctor dev-box
limanix list --json
```

:::

## A command waits for another network operation

The command prints `Waiting for another Limanix network lifecycle operation` and pauses.

Cause: starts, stops and deletions that share a Lima directory take turns with their network changes.

Fix: wait. The command continues when the other operation is done, or stops when you press Ctrl-C.

## limanix update is rejected

| Message                                                                                                    | Cause and fix                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `an update cannot change architecture, username, or managed-home paths; create a new VM for these changes` | `resources.arch`, `user.name`, `user.home` and `home.root` are fixed at creation. Revert the change, or create a new VM and copy the files you need. |
| `shrinking the guest disk is not supported`                                                                | Set `resources.disk` to at least the current size. An earlier failed update may already have enlarged the disk.                                      |
| `lima did not report the disk size; update was not started`                                                | LimaNix cannot check that the disk would not shrink. Read the Lima message in the output before you try again.                                       |
| `another operation is running for VM "dev-box"`                                                            | Another `limanix` command is changing this VM. Let it finish, or cancel it in its own terminal. Do not delete lock files to get around it.           |

See [Changing a VM](/vms/update).

## limanix update reports that the generation is booted but unhealthy

The update ends with `Generation … is booted but unhealthy` and a reason, or the tmux status line or the prompt shows `degraded`.

Cause: the VM runs the new system, but its health check failed. The check looks at the platform services such as `sshd` and the Lima guest agent, the mounts `/mnt/limanix` and the home, and a login shell of the development account. `lmxd` checks again every minute.

Fix: find the failed part, correct `limanix.toml` or the module, and run `limanix update` again.

::: code-group

```sh [Mac]
limanix doctor dev-box
```

:::

::: code-group

```sh [VM]
lmx doctor
sudo lmx logs health
```

:::

When the reason names a unit, `systemctl status UNIT` in the VM shows more.

## limanix update warns that finalizing failed

The update ends with `VM 'dev-box' is ready, but lmx reported: Finalizing generation … failed`, or the tmux status line or the prompt shows `finalize`.

Cause: the new system works. `lmxd` could not yet remove the older generations or rewrite their boot entries.

Fix: nothing urgent. `lmxd` tries again after 15 minutes. To see why it failed, run in the VM:

::: code-group

```sh [VM]
sudo lmx logs finalize
```

:::

## An update was interrupted

Ctrl-C during `limanix update` cancels the build in the VM, starts the guest's own `lmxd` again and exits with status `130`. The VM keeps the system it ran before.

When the message says `cannot confirm the guest apply stopped`, the build may still run in the VM. Check it, stop it and start the regular `lmxd` again:

::: code-group

```sh [VM]
systemctl status lmx-transient.service
sudo systemctl stop lmx-transient.service
sudo systemctl start lmx.service
```

:::

The next `limanix update` does both too.

`limanix list` shows `interrupted` when a create, update or delete ended without finishing and no process is working on it. After an interrupted create or update, fix the cause from the original output and run `limanix update`. After an interrupted delete, check whether it had `--remove-home` before you run it again.

## limanix list shows error, Missing or corrupt

| `limanix list` shows | Cause                                                                                                                     | Fix                                                                                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `STATE` `error`      | The last create, update or delete failed. The line under the row names the state file.                                    | Fix the reported problem, then run `limanix update`, or `limanix delete` to remove the VM.                                                                                                 |
| `STATUS` `Missing`   | No Lima instance matches the saved VM. Commands report `lima instance for 'dev-box' is missing; delete its saved record`. | Check that `LIMA_HOME` and `LIMANIX_HOME` are the same as when you created the VM. If the instance is really gone, `limanix delete dev-box` removes the record and keeps the managed home. |
| `STATE` `corrupt`    | The operation record of the VM cannot be read.                                                                            | `start`, `stop` and `delete` still work while the identity record is valid; `update` does not. `delete` removes the guest disk: save the data you need first.                              |

Do not edit or delete the records in the state directory to get around an error. LimaNix uses them to know which Lima instance and which home belong to a VM.

## limanix shell says the VM is not running

The message is `VM 'dev-box' is not running; use limanix start dev-box`.

Fix: start the VM, then open the shell.

::: code-group

```sh [Mac]
limanix start dev-box
limanix shell dev-box
```

:::

## The VM shows Running, but limanix shell fails

Cause: `Running` is Lima's power state. It does not mean that a build finished or that the development account is ready.

Fix:

1. Check `STATE` and the lines under the VM in `limanix list`.
1. If a `create` or `update` still runs, let it finish.
1. Check access with `limanix shell dev-box -- true`.
1. Run `limanix doctor dev-box`.

Keep the SSH or guest error when the shell still fails.

## limanix shell --session says no session provider is configured

The VM prints `No session provider is configured in this VM.` and the setting that adds one; the command exits with status `127`.

Cause: a named session needs a provider, such as `multiplexer = "tmux"` in `[shell]`. The `terminal` preset has it by default; `minimal` has none.

Fix: add the provider and apply the change.

::: code-group

```toml [limanix.toml]
[shell]
multiplexer = "tmux"
```

:::

::: code-group

```sh [Mac]
limanix update --config limanix.toml
limanix shell dev-box --session work
```

:::

Other messages about sessions:

| Message or symptom                                  | Fix                                                                         |
| --------------------------------------------------- | --------------------------------------------------------------------------- |
| `--session cannot be combined with a guest command` | Open the session without a command, or run the command without `--session`. |
| `--session requires a nonempty session name`        | Give the session a name, such as `--session work`.                          |
| `--session may only be specified once`              | Pass one `--session`.                                                       |
| tmux rejects the session name                       | Use a name without `.` or `:`, such as `work` or `project-api`.             |

See [Shell and sessions](/vms/shell).

## A command run with limanix shell uses values from the Mac

`limanix shell dev-box -- echo $HOME` prints your home on the Mac, or `cd` and pipes do not work.

Cause: `limanix shell` passes the command and its arguments to the VM unchanged, without a shell. The shell on your Mac expands `$HOME` before `limanix` runs.

Fix: run a shell in the VM and put the command in single quotes:

::: code-group

```sh [Mac]
limanix shell dev-box -- bash -lc 'cd /workspace && pwd'
limanix shell dev-box -- bash -lc 'printf "%s\n" "$HOME"'
```

:::

## lmx status shows Owner unknown, or the prompt shows lmxd?

Cause: `lmxd` does not answer. Your shell, files and services keep working; updates and the cleanup of the Nix store wait until it is back.

Fix: run `lmx doctor` in the VM. Its `owner` check says what failed. Then check the units and the log of `lmxd`:

::: code-group

```sh [VM]
lmx doctor
systemctl status lmx.socket lmx.service
journalctl -u lmx
```

:::

`limanix update` on the Mac starts `lmxd` again as part of the update. When `owner` warns that `lmxd` and `lmx` have different versions, restart the VM: both then come from the booted generation.

## Every shell starts with "lmx: the dotfiles at /mnt/dotfiles are not mounted"

Cause: the VM no longer sees the folder that `dotfiles` in `[shell]` names. Its mount failed, or the folder was moved or deleted on the Mac; then the message is `cannot read the dotfiles at /mnt/dotfiles`. Your links stay until the folder is back.

Fix: correct the path in `limanix.toml` if the folder moved, then run `limanix update` on the Mac; the update mounts the folder again. `lmx doctor` shows the same problem as a failed `dotfiles` check.

## A dotfile from the Mac has no effect in the VM

Run `lmx dotfiles` in the VM.

| Line       | Cause                                                                            | Fix                                                                                                                                                         |
| ---------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `conflict` | A file, a folder or a link of your own is in the way. LimaNix never replaces it. | Move it aside, for example with `mv ~/.zshrc ~/.zshrc.guest`, and open a new shell.                                                                         |
| `missing`  | The link is not made yet.                                                        | Open a new shell, or run `lmx dotfiles link`.                                                                                                               |
| No line    | The entry is not linked at all.                                                  | Only top-level names that start with `.` and the entries of `.config` are linked. `.git`, `.github`, `.gitignore`, `.gitmodules` and `.DS_Store` never are. |

See [Dotfiles](/config/dotfiles).

## A port in the VM is unreachable from the Mac

Check the port from the Mac. Add `--udp` for a UDP port.

::: code-group

```sh [Mac]
limanix network check dev-box 8080
```

:::

The command runs its checks in order and prints a hint under a failed one:

| Failed check | Cause                                                                 | Fix                                                                                                                                                      |
| ------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vm`         | The VM is stopped, or its last create or update did not complete.     | Run `limanix start dev-box`, or fix the problem and run `limanix update`.                                                                                |
| `address`    | The guest reported no IPv4 address on the shared network.             | See [limanix list shows - as the address](#limanix-list-shows-as-the-address).                                                                           |
| `firewall`   | The guest firewall does not open the port for its protocol.           | Add the port to `[network.ports]` and run `limanix update`. An HTTP server needs its TCP port; the same number under `udp` is another rule.              |
| `listener`   | Nothing listens on the port, or only on `127.0.0.1`.                  | Start the service and make it listen on `0.0.0.0` or on the guest address.                                                                               |
| `connect`    | The guest checks passed, but the Mac cannot connect within 3 seconds. | The connection stops on the Mac: check a VPN, a firewall, and the Local Network permission of your terminal app in System Settings › Privacy & Security. |

::: code-group

```toml [limanix.toml]
[network.ports]
tcp = [8080]
```

:::

- Docker opens the ports it publishes with its own firewall rules. `network.ports` has no say over them, and removing a port from it does not close a port that Docker publishes. `lmx net check` warns when Docker's proxy holds the socket.
- An authentication or permission error comes from the service's own access rules. Opening another firewall port does not change it.
- After an update, start a service you run by hand again: the update restarts the VM.

See [Network](/vms/network).

## localhost on the Mac does not reach a service in the VM

Cause: LimaNix turns off Lima's automatic port forwarding. `localhost:8080` on the Mac is not the port `8080` of the VM.

Fix: connect to the address of the VM, which `limanix list` shows in `ADDRESS`, such as `http://ADDRESS:8080`. The address is not fixed; check it again when you reconnect.

## limanix list shows - as the address

Cause: `ADDRESS` comes from `lmx status`, which `list` runs in each running VM with a 10-second limit. `-` means that the VM is stopped, did not answer in time, or has no IPv4 address on the shared network. The notice `the guest has no lmx yet; run limanix update` under the row means that an older client created the VM.

Fix: check access first, then the VM.

::: code-group

```sh [Mac]
limanix shell dev-box -- true
limanix doctor dev-box
```

:::

For the notice, run `limanix update --config limanix.toml` with the file of that VM: the update installs `lmx`.

## The guest disk is full

Builds fail with `No space left on device`, `create` or `update` stops with `guest disk is full; raise resources.disk or remove guest data`, the `DISK` column of `limanix list` is high, or the welcome and the prompt warn `disk low` or `disk-low`.

Cause: LimaNix keeps only the applied system generation and removes unreferenced store paths after each `create` and `update`, and whenever less than 20% of the disk is free. What remains is in use: the applied system, garbage-collector roots such as `nix-direnv` shells and `result` links, older versions of your `nix profile`, and data outside the Nix store, such as Docker images and volumes under `/var/lib/docker`.

Fix:

1. See the usage with `lmx info`, and what keeps store paths alive with `sudo nix-store --gc --print-roots`. `sudo lmx logs roots` shows the list that `lmxd` wrote when less than 10% was free.
1. Remove what you no longer need, for example with `docker system prune`, by deleting a project's `.direnv` folder or a `result` link, or with `nix profile wipe-history` for tools you removed from your profile.
1. Collect the freed store paths. `sudo lmx store reserve` collects while less than 20% is free; `sudo nix-store --gc` collects in any case.

::: code-group

```sh [VM]
lmx info
sudo nix-store --gc --print-roots
sudo lmx logs roots
sudo lmx store reserve
```

:::

When that is not enough, give the VM a larger disk: raise `resources.disk` in `limanix.toml` and apply it. A disk cannot shrink.

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

See [Files and storage](/vms/storage).

## pbcopy or pbpaste does not reach the Mac clipboard

`pbcopy` and `pbpaste` in the VM talk to the terminal on your Mac with OSC 52 escape sequences, or through tmux inside tmux. The terminal must allow it.

| Message or symptom                                                                                                       | Cause                                                               | Fix                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `pbcopy` copies nothing                                                                                                  | The terminal does not accept clipboard writes.                      | Allow OSC 52 clipboard access in the terminal's settings.                                                                  |
| `pbpaste` prints `The terminal did not share its clipboard. Allow clipboard reads in its settings, or paste with Cmd+V.` | The terminal refused the read, or did not answer within 10 seconds. | Allow clipboard reads in the terminal's settings. Reads usually need one more permission than writes. Or paste with Cmd+V. |
| `pbcopy needs the terminal of a limanix shell session.`, or the same for `pbpaste`                                       | The command has no terminal to talk to.                             | Run it in an interactive shell opened with `limanix shell dev-box`.                                                        |

See [Clipboard](/inside/clipboard) for the settings of common terminals.

## Collect diagnostics

The output of the failed command is the main source for build and guest errors. The saved error of an operation holds a recovery message and the path of its state file, not the whole build log.

On the Mac:

::: code-group

```sh [Mac]
limanix --version
limanix doctor dev-box
limanix list --json
```

:::

- `limanix doctor dev-box --json` prints the same checks as JSON.
- Lima writes the output of its host agent to `ha.stdout.log` and `ha.stderr.log` in the directory of each instance under `~/.lima`, or under `LIMA_HOME`. `lima_name` in `limanix list --json` names the instance.
- LimaNix keeps its state in `~/Library/Application Support/Limanix`, or in `LIMANIX_HOME` when you set it. Use the same `LIMANIX_HOME` and `LIMA_HOME` for every command: a different value shows different VMs.

In the VM:

::: code-group

```sh [VM]
lmx version
sudo lmx doctor
sudo lmx status
sudo lmx logs apply --previous
sudo journalctl -u lmx
```

:::

| Command                  | Shows                                      |
| ------------------------ | ------------------------------------------ |
| `sudo lmx logs apply`    | The build of a generation.                 |
| `sudo lmx logs health`   | The health check after a restart.          |
| `sudo lmx logs finalize` | The removal of older generations.          |
| `sudo lmx logs collect`  | The last cleanup of the Nix store.         |
| `sudo lmx logs roots`    | The last report of what still holds space. |

Add `--previous` to read the boot before the current one. An update builds in one boot and restarts into the next: its build output is in `sudo lmx logs apply --previous`.

When you report a problem, include the client version and the exact command, the error with the output around it, the JSON listing of the VM, the relevant parts of `limanix.toml`, the architecture of your Mac, and whether the failure happened during `create`, `update`, `start` or `shell`. Read logs and configuration before you share them: environment values, paths and guest output can contain private data.
