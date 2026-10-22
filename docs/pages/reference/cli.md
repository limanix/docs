---
description: Every command, argument and flag of the limanix command on the Mac, with defaults and exit statuses.
---

# limanix command

`limanix` runs on your Mac. It creates, changes, starts and opens the VMs that your `limanix.toml` files describe. Run it as your regular Mac user, without `sudo`. [Using virtual machines](/vms/) shows the everyday workflow.

## Usage

::: code-group

```sh [Mac]
limanix COMMAND [ARGUMENTS] [FLAGS]
```

:::

`limanix` without a command prints its help. `create` and `update` take the VM name from the `name` setting of the file you pass with `--config`; the other VM commands take the name as an argument.

| Flag              | Type    | Default | Description                                                      |
| ----------------- | ------- | ------- | ---------------------------------------------------------------- |
| `-h`, `--help`    | boolean | `false` | Print the help of `limanix` or of the command it follows.        |
| `-v`, `--version` | boolean | `false` | Print the version of the client. Only `limanix` itself takes it. |

Errors go to standard error as `limanix: MESSAGE`.

### Exit status

| Status | Meaning                                                                                                                           |
| ------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `0`    | Success.                                                                                                                          |
| `1`    | The command failed. `limanix doctor` and `limanix network check` also exit with `1`, after printing every check, when one failed. |
| `2`    | Usage error, such as an unknown command, a missing argument or a missing `--config`.                                              |
| `130`  | The command was interrupted, for example with Ctrl-C.                                                                             |
| Other  | `limanix shell` exits with the status of the guest command or shell.                                                              |

### Environment variables

| Variable       | Default                                 | Description                                                                                         |
| -------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `LIMANIX_HOME` | `~/Library/Application Support/Limanix` | LimaNix state: VM records, prepared configurations and imported modules.                            |
| `LIMA_HOME`    | `~/.lima`                               | Lima's instances, each in a directory with its host agent logs `ha.stdout.log` and `ha.stderr.log`. |

Neither variable moves existing VMs or homes. Use the same values for every command that works on an existing VM.

## `limanix create`

Create a VM from a configuration file.

::: code-group

```sh [Mac]
limanix create --config FILE
```

:::

| Flag       | Type   | Default  | Description                        |
| ---------- | ------ | -------- | ---------------------------------- |
| `--config` | string | required | Path to the VM configuration file. |

`create` reads the VM name from the file, allocates the VM and its managed home, builds the NixOS system, restarts the VM into it and checks the development account. It prints the build output, then `Created NAME. Managed home: PATH`. It downloads the base image when needed; the first run needs network access for the image and the Nix dependencies.

A name that already has saved state is rejected with `VM 'NAME' already has state; use update or delete`. When `create` fails after the VM exists, `limanix list` shows it with the state `error`: fix the problem and run `limanix update` with the same file.

Guide: [Using virtual machines](/vms/).

## `limanix update`

Apply a configuration to an existing VM and restart it.

::: code-group

```sh [Mac]
limanix update --config FILE
```

:::

| Flag       | Type   | Default  | Description                        |
| ---------- | ------ | -------- | ---------------------------------- |
| `--config` | string | required | Path to the VM configuration file. |

`update` selects the VM by the `name` in the file, keeps its disk and managed home, builds the new system in the VM and restarts it. It prints the build output, then `Updated NAME.` The VM is running afterwards, even if it was stopped before.

- A failed build does not restart the VM, which keeps its current system. Steps before the failure are not undone: the VM may be stopped, its Lima settings may have changed, or new environment files may be installed.
- Ctrl-C during the build cancels it in the VM, starts the guest's own `lmxd` again and exits with status `130`.
- `resources.arch`, `user.name`, `user.home` and `home.root` are fixed when the VM is created. `resources.disk` can grow but not shrink.

Guide: [Changing a VM](/vms/update).

## `limanix start`

Start an existing VM.

::: code-group

```sh [Mac]
limanix start NAME
```

:::

| Argument | Type   | Default  | Description |
| -------- | ------ | -------- | ----------- |
| `NAME`   | string | required | VM name.    |

`start` boots the saved VM and prints `Started NAME.` It does not read `limanix.toml`, rebuild the system or reset an earlier operation error: `limanix update` does that.

Guide: [Using virtual machines](/vms/).

## `limanix stop`

Stop a VM and keep its disk and home.

::: code-group

```sh [Mac]
limanix stop NAME
```

:::

| Argument | Type   | Default  | Description |
| -------- | ------ | -------- | ----------- |
| `NAME`   | string | required | VM name.    |

`stop` shuts the VM down and prints `Stopped NAME.` Running processes in the VM end.

Guide: [Using virtual machines](/vms/).

## `limanix shell`

Open a shell in a VM as the development user, or run one command there.

::: code-group

```sh [Mac]
limanix shell NAME [--session SESSION | -- COMMAND ...]
```

:::

| Argument or flag | Type    | Default  | Description                                                                                         |
| ---------------- | ------- | -------- | --------------------------------------------------------------------------------------------------- |
| `NAME`           | string  | required | VM name.                                                                                            |
| `COMMAND ...`    | strings | none     | Guest command and its arguments, after `--`. They reach the guest unchanged, without a guest shell. |
| `--session`      | string  | none     | Create or attach to a named persistent session; requires a session provider in the VM.              |

- Without a command, `shell` opens the login shell of the development user in their home: Zsh with the `terminal` preset, Bash with `minimal`. `exit` returns to the Mac; the VM keeps running.
- With `-- COMMAND`, the command starts in the user's home, and `limanix shell` exits with its status. For `cd`, pipes or variables, run a guest shell such as `bash -lc '...'`. Single quotes keep the Mac's shell from expanding them first.
- `--session SESSION`, or `--session=SESSION`, goes before or after the VM name, at most once, with a nonempty name. It runs `limanix-session SESSION` in the VM, which creates the session or attaches to it with the provider: `multiplexer = "tmux"` in [`[shell]`](/config/shell) or a module. Without a provider, the VM names the setting to add and the command exits with status `127`. The tmux provider rejects names containing `.` or `:`.
- `--session` cannot be combined with a guest command.
- A stopped VM fails with `VM 'NAME' is not running; use limanix start NAME`.

::: code-group

```sh [Mac]
limanix shell dev-box
limanix shell dev-box --session work
limanix shell dev-box -- id
limanix shell dev-box -- bash -lc 'cd /workspace && pwd'
```

:::

Guide: [Shell and sessions](/vms/shell).

## `limanix list`

List the VMs that LimaNix manages.

::: code-group

```sh [Mac]
limanix list [--json]
```

:::

| Flag     | Type    | Default | Description                  |
| -------- | ------- | ------- | ---------------------------- |
| `--json` | boolean | `false` | Print machine-readable JSON. |

| Column    | Content                                                                                                                                                                 |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NAME`    | VM name.                                                                                                                                                                |
| `STATUS`  | Lima's power state, such as `Running` or `Stopped`. `Missing` when no Lima instance matches the saved VM, or its identity record cannot be read.                        |
| `STATE`   | The last LimaNix operation: `ready`, `error` or `interrupted`; `creating`, `updating` or `deleting` while one runs; `corrupt` when the operation record cannot be read. |
| `ADDRESS` | The guest's IPv4 address on the shared network, or `-` when none was read.                                                                                              |
| `DISK`    | Used share of the guest disk, by bytes or, when they are scarcer, by inodes, such as `97% inodes`. `-` when the VM is stopped or did not answer.                        |

Under a row, `list` prints the saved error of the last operation and a notice that says what to do, such as `the guest has no lmx yet; run limanix update`. `ADDRESS` and `DISK` come from `lmx status`, which `list` runs in each running VM with a 10-second limit. Without VMs, it prints `No VMs managed by Limanix.`

`--json` prints an array with one object per VM:

| Field       | Value                                                                                         |
| ----------- | --------------------------------------------------------------------------------------------- |
| `name`      | VM name.                                                                                      |
| `status`    | As `STATUS`; `null` when no Lima instance matches.                                            |
| `state`     | As `STATE`; `null` when the operation record cannot be read.                                  |
| `arch`      | Guest architecture, `arm64` or `amd64`.                                                       |
| `address`   | Guest IPv4 address, or an empty string.                                                       |
| `disk`      | `bytes`, `free_bytes`, `inodes` and `free_inodes` of the guest disk, or `null` when not read. |
| `home`      | Path of the managed home on the Mac.                                                          |
| `lima_name` | Name of the Lima instance.                                                                    |
| `error`     | Saved error of the last operation, or `null`.                                                 |
| `notice`    | What to do to make the guest answer. Present only when there is a notice.                     |

`arch`, `home`, `lima_name` and `status` are `null` when the VM's identity record cannot be read.

Guide: [Using virtual machines](/vms/).

## `limanix doctor`

Check a VM, its address and the guest owner `lmx`.

::: code-group

```sh [Mac]
limanix doctor NAME [--json]
```

:::

| Argument or flag | Type    | Default  | Description                  |
| ---------------- | ------- | -------- | ---------------------------- |
| `NAME`           | string  | required | VM name.                     |
| `--json`         | boolean | `false`  | Print machine-readable JSON. |

`doctor` prints one row per check: its status, its name and a message, with a hint below when there is something to do. A status is `ok`, `warning`, `failed` or `unknown`.

| Check                                                | What it checks                                                                                                                                                                        |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vm`                                                 | The saved record and Lima: the VM runs, and its last create or update completed.                                                                                                      |
| `address`                                            | The guest has an IPv4 address on the shared network.                                                                                                                                  |
| `config`, `owner`, `generations`, `disk`, `dotfiles` | The checks of [`lmx doctor`](/reference/lmx#lmx-doctor) in the VM: its configuration, `lmxd`, the NixOS generations, a low disk, and the dotfiles links when `shell.dotfiles` is set. |
| `guest`                                              | Takes the place of the guest checks when the guest gives no answer.                                                                                                                   |

A VM that is stopped, or that another `limanix` command is changing, shows only `vm`. `doctor` does not repair or restart anything. It exits with status `1` when a check failed; a warning does not fail it. `--json` prints an object with `name` and `checks`, each check with `check`, `status`, `message` and, when there is one, `hint`.

Guide: [Using virtual machines](/vms/). Problems by symptom: [Troubleshooting](/troubleshooting).

## `limanix delete`

Delete a VM, and keep its managed home on the Mac unless you ask otherwise.

::: code-group

```sh [Mac]
limanix delete NAME [--force] [--remove-home]
```

:::

| Argument or flag | Type    | Default  | Description                                                     |
| ---------------- | ------- | -------- | --------------------------------------------------------------- |
| `NAME`           | string  | required | VM name.                                                        |
| `--force`        | boolean | `false`  | Force Lima to stop and delete the VM.                           |
| `--remove-home`  | boolean | `false`  | Also remove this VM's managed home on the Mac and its contents. |

`delete` stops a running VM, then removes its guest disk, its Lima instance and its saved record. It prints `Deleted NAME.` and, without `--remove-home`, `Preserved managed home: PATH`. It also removes the record of a VM whose Lima instance is already missing.

- There is no confirmation prompt.
- Your `limanix.toml` and the folders shared with `[[mounts]]` stay on the Mac.
- `--force` does not imply `--remove-home`.
- A preserved home is not attached to a new VM of the same name. After the VM is deleted, `delete --remove-home` can no longer remove it; keep the printed path to clean it up by hand.

Guide: [Files and storage](/vms/storage).

## `limanix network setup`

Install the bundled `socket_vmnet` helper and Lima's sudoers rules, with administrator approval.

::: code-group

```sh [Mac]
limanix network setup
```

:::

Only a guest whose architecture differs from the Mac's needs it: that guest runs with QEMU on Lima's shared network. Run it as your regular user in an interactive terminal. It checks the existing setup and, when something must be installed, shows the paths and asks before it runs `sudo`:

| Item               | Path                                 |
| ------------------ | ------------------------------------ |
| Network helper     | `/opt/socket_vmnet/bin/socket_vmnet` |
| Lima sudoers rules | `/private/etc/sudoers.d/lima`        |

An existing helper must pass the checks; an existing sudoers file is backed up before it is replaced. `create` and `update` of a QEMU guest offer the same installation in an interactive terminal; without one they fail with `socket_vmnet setup is required; run limanix network setup in an interactive terminal`. Automatic setup supports only Lima's standard helper, runtime and sudoers paths.

`limanix network` without a subcommand prints its help.

Guide: [Resources and architecture](/vms/resources).

## `limanix network check`

Check why a port in the VM may be unreachable from the Mac.

::: code-group

```sh [Mac]
limanix network check NAME PORT [--udp] [--json]
```

:::

| Argument or flag | Type    | Default  | Description                            |
| ---------------- | ------- | -------- | -------------------------------------- |
| `NAME`           | string  | required | VM name.                               |
| `PORT`           | integer | required | Port number from 1 to 65535.           |
| `--udp`          | boolean | `false`  | Check a UDP port instead of a TCP one. |
| `--json`         | boolean | `false`  | Print machine-readable JSON.           |

The checks run in this order:

| Check      | What it checks                                                                  |
| ---------- | ------------------------------------------------------------------------------- |
| `vm`       | The VM runs, and its last create or update completed.                           |
| `address`  | The guest has an IPv4 address on the shared network.                            |
| `firewall` | The guest firewall opens the port for its protocol.                             |
| `listener` | Something listens on the port on an address other than loopback.                |
| `process`  | Which process and user hold the socket, when something listens.                 |
| `connect`  | The Mac connects to the address and port within 3 seconds. Only for a TCP port. |

The command exits with status `1` when a check failed. `--json` prints an object with `name`, `port`, `protocol` and `checks`, as in `limanix doctor`.

::: code-group

```sh [Mac]
limanix network check dev-box 8080
```

:::

Guide: [Network](/vms/network).

## `limanix modules list`

List the modules you can select.

::: code-group

```sh [Mac]
limanix modules list [--json]
```

:::

| Flag     | Type    | Default | Description                  |
| -------- | ------- | ------- | ---------------------------- |
| `--json` | boolean | `false` | Print machine-readable JSON. |

Each row shows a selector, its kind and its description, or the error of an imported module that fails the registry checks: modules first, then toolchains, then shell components. The kind says where `limanix.toml` chooses the entry:

| Kind         | Chosen in                                                |
| ------------ | -------------------------------------------------------- |
| `modules`    | `[nixos] modules`, by selector, such as `lmx:docker`.    |
| `toolchains` | `[toolchains]`, by line: `lmx:go-1.27` is `go = "1.27"`. |
| `shell`      | `[shell]`.                                               |

The list comes from the catalog built into the client and from your imported modules. It does not download anything or evaluate Nix code. `--json` prints an array of objects with these fields:

| Field         | Value                                                                          |
| ------------- | ------------------------------------------------------------------------------ |
| `name`        | Full selector, such as `lmx:docker`, `lmx:go-1.27` or `third-party:my-tools`.  |
| `source`      | `lmx` or `third-party`.                                                        |
| `kind`        | `modules`, `toolchains` or `shell`. Imported modules are `modules`.            |
| `description` | Catalog description, or `Locally imported NixOS module`.                       |
| `error`       | `null`, or a diagnostic for an imported module that fails the registry checks. |

`limanix modules` without a subcommand is a usage error.

Guide: [The catalog](/modules/).

## `limanix modules add`

Import a directory with a `default.nix` as a module of your own.

::: code-group

```sh [Mac]
limanix modules add NAME DIRECTORY
```

:::

| Argument    | Type   | Default  | Description                                                                                                                                         |
| ----------- | ------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NAME`      | string | required | Module name without `third-party:`: up to 63 lowercase letters, digits and single hyphens, with every hyphen-separated part starting with a letter. |
| `DIRECTORY` | string | required | Directory with a regular file named `default.nix` at its root. It may be relative, absolute or start with `~`.                                      |

`add` copies the whole directory, hidden files included, into the module registry and prints `Imported third-party:NAME.` Select it in `limanix.toml` as `third-party:NAME`.

- It checks the structure, not the Nix code: errors in the code appear when a VM is built.
- Symlinks and special files inside the directory are rejected.
- An existing name is refused. Remove the module first to import a new version.
- Later edits to the source directory do not reach the copy.

Guide: [Your own modules](/modules/custom).

## `limanix modules remove`

Remove an imported module from the registry.

::: code-group

```sh [Mac]
limanix modules remove NAME
```

:::

| Argument | Type   | Default  | Description                                         |
| -------- | ------ | -------- | --------------------------------------------------- |
| `NAME`   | string | required | Name of an imported module, without `third-party:`. |

`remove` prints `Removed third-party:NAME from the catalog.` It removes only imported modules; the `lmx:` modules belong to the client. A VM that selects the module keeps its current system, but its next `create` or `update` fails until you import the module again or remove the selector.

Guide: [Your own modules](/modules/custom).

## `limanix first-config`

Write an example `limanix.toml`.

::: code-group

```sh [Mac]
limanix first-config [PATH]
```

:::

| Argument | Type   | Default           | Description                                      |
| -------- | ------ | ----------------- | ------------------------------------------------ |
| `PATH`   | string | current directory | Existing directory to write `limanix.toml` into. |

`first-config` writes the [defaults](/reference/config#defaults) with a comment for each setting, then prints `Wrote` and the path of the file. It overwrites an existing `limanix.toml` in that directory, rejects one that is a symlink, and does not create missing directories. The example includes sample mounts and environment variables; check them before you run `create`.

Guide: [The limanix.toml file](/config/).

## `limanix help`

Print the help of a command.

::: code-group

```sh [Mac]
limanix help [COMMAND ...]
```

:::

| Argument      | Type    | Default | Description                                  |
| ------------- | ------- | ------- | -------------------------------------------- |
| `COMMAND ...` | strings | none    | Command to explain, such as `network check`. |

`limanix help COMMAND` is the same as `limanix COMMAND --help`. Without a command, it prints the help of `limanix`.
