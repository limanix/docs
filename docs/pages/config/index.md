---
description: How limanix.toml is laid out, what each table configures and what a VM gets for the settings you leave out.
---

# The limanix.toml file

A `limanix.toml` file describes one VM: its resources, your account, the shell, languages, modules, shared folders and environment. This page shows where the file lives, how it is laid out and what the VM gets for settings you leave out.

## Where the file lives

Keep `limanix.toml` in your project folder and create the VM from there:

::: code-group

```sh [Mac]
cd ~/projects/my-project
limanix create --config limanix.toml
```

:::

`limanix create` and `limanix update` need `--config` and read the VM name from the file. The other commands take the name directly, such as `limanix shell dev-box`.

Relative paths in the file resolve from the folder that holds `limanix.toml`, wherever you run the command. A mount source of `"."` is the project folder itself.

Editing the file changes nothing by itself. Apply it with `limanix update --config limanix.toml`, which restarts the VM; see [Changing a VM](/vms/update). `limanix start` boots the VM as it was, without reading the file.

## The tables at a glance

| In the file                    | Configures                                             | Page                                                                   |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| `schema_version`, `name`       | The file format version and the VM name                | [Below](#schema-version-and-name)                                      |
| `[resources]`                  | Architecture, CPUs, memory and disk                    | [Resources and architecture](/vms/resources)                           |
| `[user]`                       | Your account in the VM                                 | [Environment and theme](/config/environment#set-up-your-account)       |
| `[home]`                       | Where your home folder in the VM is kept on the Mac    | [Files and storage](/vms/storage)                                      |
| `[shell]`                      | Shell preset, prompt, editor, multiplexer and dotfiles | [Shell](/config/shell), [Dotfiles](/config/dotfiles)                   |
| `[toolchains]`                 | Go, Rust, Python and Node.js                           | [Toolchains](/config/toolchains)                                       |
| `[nixos]`                      | Catalog modules and packages                           | [Modules and packages](/config/modules)                                |
| `[theme]`                      | Colors                                                 | [Environment and theme](/config/environment#choose-a-theme)            |
| `[network]`, `[network.ports]` | Network mode and firewall ports                        | [Network](/vms/network)                                                |
| `[env]`                        | Environment variables                                  | [Environment and theme](/config/environment#set-environment-variables) |
| `[[mounts]]`                   | Shared folders                                         | [Shared folders](/config/mounts)                                       |

The [limanix.toml reference](/reference/config) lists every key with its type and default.

## TOML basics

The file uses TOML. In the [project example](#example-files) below:

| In the file                | Meaning                                                                   |
| -------------------------- | ------------------------------------------------------------------------- |
| `schema_version = 1`       | A top-level setting; top-level settings come before the first table       |
| `[resources]`              | A table; it holds the settings below it, up to the next table header      |
| `[network.ports]`          | A table inside `network`                                                  |
| `[[mounts]]`               | One entry in the list of shared folders; repeat the block for each folder |
| `tcp = [8080]`, `udp = []` | Lists in square brackets; an empty list selects nothing                   |
| `# Save this file…`        | A comment                                                                 |

Values have types: `cpu = 4` is an integer, `sudo = true` a boolean and `mem = "8GiB"` a string. LimaNix rejects unknown keys and wrong types, and the error names the key. This catches typos such as `cpus` for `cpu` in `[resources]`.

## Schema version and name

::: code-group

```toml [limanix.toml]
schema_version = 1
name = "dev-box"
```

:::

`schema_version` is the version of the file format, not of the client. Keep it at `1`, the only version.

`name` is the VM's name: 1 to 63 lowercase letters, digits or hyphens, starting and ending with a letter or digit. Without it, the VM is called `example-box`. Changing the name in the file selects a different VM; it does not rename the existing one.

## Settings you leave out

A setting you leave out keeps its default. Some defaults are examples, such as the mounts and the environment variables: write an empty list or table to remove them.

| Your file                             | What the VM gets                                                                                    |
| ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| No `mounts` setting                   | Two example mounts: `~/projects/my-project` at `/workspace` and `~/.ssh/limanix` at `/mnt/git-keys` |
| `mounts = []`                         | No shared folders besides your home folder                                                          |
| One or more `[[mounts]]`              | Those mounts instead of the examples                                                                |
| No `[env]` table                      | `APP_ENV = "development"` and `APP_LOG_LEVEL = "debug"`                                             |
| An empty `[env]` table, or `env = {}` | No variables                                                                                        |
| An `[env]` table with entries         | Exactly those variables                                                                             |
| No `tcp` in `[network.ports]`         | TCP port 8080 open                                                                                  |
| `tcp = []`                            | No TCP ports from this setting; modules can still open their own                                    |
| No `[shell]` table                    | The `terminal` preset with Pure, AstroNvim and tmux                                                 |
| `preset = "minimal"` alone            | Bash and the CLI tools; `prompt`, `editor` and `multiplexer` become `none`                          |
| No `[toolchains]` table               | No toolchains                                                                                       |
| No `dotfiles`                         | No dotfiles                                                                                         |
| No `modules`, or `modules = []`       | No optional modules; the shell and toolchains still apply                                           |
| No `packages`                         | No packages besides the GitHub CLI of the `terminal` preset                                         |
| `[resources]` with only `cpu = 2`     | Two CPUs; the architecture, memory and disk keep their defaults                                     |
| No `[theme]` table                    | The `system` flavor: your terminal's own colors                                                     |

An empty string is a value, not a default: `source = ""` is an error, and `APP_ENV = ""` sets an empty variable.

::: warning
The example mounts need both folders on your Mac, and `limanix create` fails without them. Write `mounts = []` before the first table, or list your own `[[mounts]]`.
:::

## Example files

| Example   | What it sets up                                                                                                                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Minimal   | Bash and the CLI tools on 2 CPUs, 4 GiB of memory and a 16 GiB disk, with no shared project folder, environment variables, modules or open ports      |
| Project   | The `terminal` shell, your project folder at `/workspace`, TCP port 8080 open and `APP_ENV` set, on 4 CPUs, 8 GiB of memory and a 10 GiB disk         |
| Workbench | The `terminal` shell with Go, Python and Node.js, Docker, Posting, Harlequin, `kubectl` and `k9s`, and your project at `/workspace`, on a 40 GiB disk |

The project example, saved as `limanix.toml` in your project folder:

::: code-group

```toml [limanix.toml]
# Save this file in your project directory as limanix.toml.
# Apple Silicon: arm64. Intel Mac: change resources.arch to amd64.
schema_version = 1
name = "dev-box"

[resources]
arch = "arm64"
cpu = 4
mem = "8GiB"
disk = "10GiB"

[user]
name = "dev"
home = "/home/dev"
sudo = true

[home]
root = "~/.limanix"

[shell]
preset = "terminal"

[nixos]
modules = []

[network]
mode = "shared"

[network.ports]
tcp = [8080]
udp = []

[env]
APP_ENV = "development"

[[mounts]]
source = "."
target = "/workspace"
mode = "rw"
```

:::

It targets Apple Silicon; on an Intel Mac, set `arch = "amd64"`. Opening port 8080 does not start an application, and `modules = []` adds no modules.

To start from the client's own example instead, run `limanix first-config` in your project folder. It writes `limanix.toml` with the defaults and the example mounts, and it overwrites an existing `limanix.toml`.
