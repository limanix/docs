---
description: Every table and key of limanix.toml, with its type, allowed values and default.
---

# limanix.toml

`limanix.toml` describes one VM. `limanix create` and `limanix update` read it on the Mac; editing the file changes nothing until you run one of them. [The limanix.toml file](/config/) explains the layout with examples.

## File rules

- The file is TOML in UTF-8. Top-level keys come before the first table.
- Unknown keys and wrong types are rejected, including typos such as `resources.cpus`.
- An omitted key keeps its default, listed in [Defaults](#defaults). Some defaults are examples: two shared folders, two environment variables and TCP port `8080`. Remove them with an empty list or table.
- An empty string does not ask for a default: `source = ""` is an error, while `APP_ENV = ""` is an empty value.
- An error names the key without its value, such as `limanix: resources.cpu: must be positive`.

## Top-level keys

::: code-group

```toml [limanix.toml]
schema_version = 1
name = "dev-box"
```

:::

| Key              | Type            | Default               | Description                                                                                                                                                                                                   |
| ---------------- | --------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schema_version` | integer         | `1`                   | Version of the file format, independent of the LimaNix release. Only `1` is supported.                                                                                                                        |
| `name`           | string          | `"example-box"`       | VM name: 1 to 63 lowercase letters, digits and hyphens, starting and ending with a letter or digit. `create` and `update` select the VM by this name. Changing it selects another VM; it does not rename one. |
| `mounts`         | array of tables | two example mounts    | Shared folders, see [`[[mounts]]`](#mounts). `mounts = []` shares none.                                                                                                                                       |
| `env`            | table           | two example variables | Guest environment, see [`[env]`](#env). `env = {}` sets none.                                                                                                                                                 |

Guide: [The limanix.toml file](/config/).

## `[user]`

The regular account inside the guest and its sudo access.

::: code-group

```toml [limanix.toml]
[user]
name = "dev"
home = "/home/dev"
sudo = true
```

:::

| Key    | Type    | Default       | Description                                                                                                                                                                                          |
| ------ | ------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name` | string  | `"dev"`       | Username of the development account that `limanix shell` opens: a lowercase letter or `_`, then lowercase letters, digits, `_` or `-`, up to 32 characters. `root` and `limanix-admin` are reserved. |
| `home` | string  | `"/home/dev"` | Home directory of that account, where the managed home is mounted. Follows the [guest path rules](#guest-paths).                                                                                     |
| `sudo` | boolean | `true`        | Passwordless `sudo` inside the guest. It grants no rights on the Mac.                                                                                                                                |

`name` and `home` are [fixed at creation](#fixed-at-creation). The account uses the numeric UID of your Mac account for shared files; its name can differ from your Mac account's name.

Guide: [Environment and theme](/config/environment).

## `[resources]`

Guest architecture and compute resources.

::: code-group

```toml [limanix.toml]
[resources]
arch = "arm64"
cpu = 4
mem = "8GiB"
disk = "10GiB"
```

:::

| Key    | Type                   | Default   | Description                                                                                                                                                                                                                                                          |
| ------ | ---------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `arch` | `"arm64"` or `"amd64"` | `"arm64"` | Guest architecture. Your Mac's own, `arm64` on Apple Silicon or `amd64` on Intel, runs with Apple's Virtualization framework. The other one runs with QEMU, which you install on the Mac, and needs [`limanix network setup`](/reference/cli#limanix-network-setup). |
| `cpu`  | integer                | `4`       | Guest CPU count, a positive integer.                                                                                                                                                                                                                                 |
| `mem`  | string                 | `"8GiB"`  | Guest memory size in whole GiB.                                                                                                                                                                                                                                      |
| `disk` | string                 | `"10GiB"` | Guest system disk size in whole GiB. Shared folders are not on this disk. `update` can grow it but not shrink it.                                                                                                                                                    |

A size is a positive whole number followed by `GiB`, such as `"8GiB"`. `"8GB"`, `"1.5GiB"`, `"0GiB"` and `"08GiB"` are rejected. `arch` is [fixed at creation](#fixed-at-creation).

Guide: [Resources and architecture](/vms/resources).

## `[home]`

Storage on the Mac for the home directory of the guest user.

::: code-group

```toml [limanix.toml]
[home]
root = "~/.limanix"
```

:::

| Key    | Type   | Default        | Description                                                                                                                                                                                       |
| ------ | ------ | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root` | string | `"~/.limanix"` | Directory on the Mac under which LimaNix creates the VM's managed home, `<root>/<name>-<id>`, and mounts it read-write at `user.home`. Follows the [host path rules](#host-paths). Cannot be `/`. |

`root` is [fixed at creation](#fixed-at-creation). `limanix create` prints the path of the managed home, and `limanix list --json` shows it in `home`.

Guide: [Files and storage](/vms/storage).

## `[shell]`

Shell, prompt, editor and multiplexer of the development account.

::: code-group

```toml [limanix.toml]
[shell]
preset = "terminal"
prompt = "pure"
editor = "astronvim"
multiplexer = "tmux"
dotfiles = "~/dotfiles"
```

:::

| Key           | Type                                  | Default                                | Description                                                                                                                                                                                                                                                                                                           |
| ------------- | ------------------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `preset`      | `"terminal"` or `"minimal"`           | `"terminal"`                           | `terminal` is Zsh with Oh My Zsh, the CLI tools, Lazygit, Yazi and the GitHub CLI. `minimal` is Bash with the CLI tools.                                                                                                                                                                                              |
| `prompt`      | `"pure"`, `"starship"` or `"none"`    | `"pure"`; `"none"` with `minimal`      | Zsh prompt of the `terminal` preset. `none` leaves the prompt to your startup files. With `minimal` it must be `none`.                                                                                                                                                                                                |
| `editor`      | `"astronvim"`, `"neovim"` or `"none"` | `"astronvim"`; `"none"` with `minimal` | `astronvim` is Neovim configured with language servers for the chosen toolchains. `neovim` is plain Neovim.                                                                                                                                                                                                           |
| `multiplexer` | `"tmux"` or `"none"`                  | `"tmux"`; `"none"` with `minimal`      | Terminal multiplexer. It also provides the sessions of `limanix shell --session`.                                                                                                                                                                                                                                     |
| `dotfiles`    | string                                | `""`                                   | Directory of your dotfiles on the Mac, mounted read-write at `/mnt/dotfiles`. Each new shell links its top-level entries that start with `.`, and the entries of its `.config`, into the home, leaving existing files alone. Empty mounts none. Follows the [host path rules](#host-paths); the directory must exist. |

`none` leaves a component out of the VM. With `preset = "minimal"`, the defaults of `prompt`, `editor` and `multiplexer` are `none`; name an editor or a multiplexer to add it.

Guides: [Shell](/config/shell), [Dotfiles](/config/dotfiles).

## `[toolchains]`

Language toolchains, one version each. An empty or omitted key installs none.

::: code-group

```toml [limanix.toml]
[toolchains]
go = "1.27"
rust = "stable"
python = "3.14"
nodejs = "26"
```

:::

| Key      | Type   | Default | Description                                                                                                                                                                                      |
| -------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `go`     | string | `""`    | Go line, with gopls, Delve and GCC.                                                                                                                                                              |
| `rust`   | string | `""`    | Default toolchain of rustup, which installs it at the first start after a change: `stable`, `beta`, `nightly`, a dated channel such as `nightly-2026-10-01`, or a Rust version such as `1.90.0`. |
| `python` | string | `""`    | Python line, with virtualenv and Pyright.                                                                                                                                                        |
| `nodejs` | string | `""`    | Node.js line, with npm, npx and the TypeScript language server.                                                                                                                                  |

A line is a version such as `1.27` and must exist in the catalog of your client: `limanix modules list` shows each line as a selector of kind `toolchains`, such as `lmx:go-1.27`. An unknown line fails with the lines the catalog has.

Guide: [Toolchains](/config/toolchains).

## `[nixos]`

Modules that configure the guest system, and packages to install.

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:docker"]
packages = ["jq", "unstable:kubernetes-helm"]
```

:::

| Key        | Type             | Default | Description                                                                                                                                                                                                                                                                                                                     |
| ---------- | ---------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `modules`  | array of strings | `[]`    | Selected modules: `lmx:NAME` or `lmx:NAME-VERSION` from the catalog built into the client, or `third-party:NAME` imported with `limanix modules add`. Without a version, the module's default version is selected. Repeated selectors and several versions of a module are accepted. An empty list selects no optional modules. |
| `packages` | array of strings | `[]`    | Commands from the guest's nixpkgs by attribute path, such as `jq` or `python3Packages.ipython`. `unstable:NAME` takes the package from the catalog's nixos-unstable revision. Naming a package allows its license. A command that another package of the guest also provides fails the build.                                   |

`[shell]` and `[toolchains]` choose the other catalog modules. A shell component or a toolchain in `modules` fails with the table that chooses it, such as `nixos.modules[0]: lmx:go is a toolchain; choose its version in [toolchains], such as go = "1.27"`. The `terminal` preset also installs the GitHub CLI, `gh`; a package of the same name in `packages` takes its place.

Guides: [Modules and packages](/config/modules), [The catalog](/modules/).

## `[theme]`

Colors of the guest.

::: code-group

```toml [limanix.toml]
[theme]
flavor = "system"
```

:::

| Key      | Type                                                          | Default    | Description                                                                                                                                                                                                                           |
| -------- | ------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `flavor` | `"system"`, `"latte"`, `"frappe"`, `"macchiato"` or `"mocha"` | `"system"` | Colors of `lmx` and the catalog modules. `system` uses the terminal's own colors and background: the guest follows the theme of your terminal. `latte` is a light Catppuccin flavor; `frappe`, `macchiato` and `mocha` are dark ones. |

Guide: [Environment and theme](/config/environment).

## `[network]`

Guest network.

::: code-group

```toml [limanix.toml]
[network]
mode = "shared"
```

:::

| Key    | Type       | Default    | Description                                                                                                   |
| ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| `mode` | `"shared"` | `"shared"` | Shared network with NAT. The Mac reaches the guest at the guest's own IP address, which `limanix list` shows. |

Guide: [Network](/vms/network).

## `[network.ports]`

Inbound ports of the guest firewall.

::: code-group

```toml [limanix.toml]
[network.ports]
tcp = [8080]
udp = []
```

:::

| Key   | Type              | Default  | Description                                                                                                                                |
| ----- | ----------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `tcp` | array of integers | `[8080]` | Inbound TCP ports in the guest firewall. Services listen on a guest network interface and are reached at `<guest-ip>:<port>` from the Mac. |
| `udp` | array of integers | `[]`     | Inbound UDP ports in the guest firewall.                                                                                                   |

A port is an integer from 1 to 65535. The lists only open the firewall: they do not start services or forward ports of the Mac, and `localhost` on the Mac does not reach them. Selected modules can open ports of their own, also when the lists are empty.

Guide: [Network](/vms/network).

## `[env]`

Guest-wide environment for login sessions and for system and user services.

::: code-group

```toml [limanix.toml]
[env]
APP_ENV = "development"
APP_PORT = "8080"
```

:::

| Key    | Type   | Default | Description                                                                                                                                                                                                                                          |
| ------ | ------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NAME` | string | none    | The environment variable `NAME`. A name has ASCII letters, digits and `_`, and does not start with a digit. A value is a string, also for numbers, and may be empty. Values are literal: `"$TOKEN"` is the text `$TOKEN`, not a variable of the Mac. |

Without `env` in the file, the guest gets `APP_ENV = "development"` and `APP_LOG_LEVEL = "debug"`. A table you write replaces them entirely. An empty `[env]` table, or `env = {}` before the first table, sets none.

The values are plaintext. They are written to runtime files and installed under `/etc/limanix`, readable by root and by the development account's group. They stay outside the Nix store, but this is not encrypted secret storage.

Guide: [Environment and theme](/config/environment).

## `[[mounts]]`

Directories of the Mac mounted inside the guest. Each `[[mounts]]` block is one shared folder.

::: code-group

```toml [limanix.toml]
[[mounts]]
source = "."
target = "/workspace"
mode = "rw"
```

:::

| Key      | Type             | Default  | Description                                                                                                                                  |
| -------- | ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `source` | string           | required | Directory on the Mac to mount inside the guest. Follows the [host path rules](#host-paths); it must exist when you run `create` or `update`. |
| `target` | string           | required | Mount destination inside the guest. Follows the [guest path rules](#guest-paths).                                                            |
| `mode`   | `"rw"` or `"ro"` | `"rw"`   | Mount access inside the guest: read-write or read-only.                                                                                      |

- Targets cannot overlap: `/workspace` and `/workspace/cache` cannot both be targets.
- A target cannot be `user.home` or a directory above it. A target inside the home, such as `/home/dev/.config/nvim`, is allowed.
- Without `mounts` in the file, the guest gets two example mounts: `~/projects/my-project` at `/workspace` (`rw`) and `~/.ssh/limanix` at `/mnt/git-keys` (`ro`). Their sources must exist. Your own `[[mounts]]` blocks replace them, and `mounts = []` before the first table removes them. The managed home is mounted in any case.

A read-write mount shares the same files with the Mac: a change or a deletion on either side changes both.

Guide: [Shared folders](/config/mounts).

## Host paths

`home.root`, `shell.dotfiles` and `mounts.source` are paths on the Mac.

- A leading `~` is your home on the Mac. `$HOME` and other variables stay literal.
- A relative path is resolved from the directory of `limanix.toml`, not from the directory where you run the command. For a symlinked `limanix.toml`, the directory of the real file counts. Symlinks inside the path are resolved.

## Guest paths

`user.home` and `mounts.target` are paths inside the VM.

- A path is absolute, starts with a single `/` and is not `/` itself.
- It contains no spaces, tabs, line breaks, `:` or `..` components. Repeated slashes and `.` components are normalized.
- These destinations and everything below them are reserved for the guest system: `/etc`, `/boot`, `/usr`, `/var`, `/nix`, `/run`, `/dev`, `/proc`, `/sys`, `/bin`, `/sbin`, `/mnt/limanix`, `/mnt/dotfiles` and `/home/limanix-admin`. `/home` is not available either: it would cover `/home/limanix-admin`.

## Fixed at creation

| Key                                                     | Behavior                                                                |
| ------------------------------------------------------- | ----------------------------------------------------------------------- |
| `resources.arch`, `user.name`, `user.home`, `home.root` | `update` rejects a change. Create a new VM and copy the files you need. |
| `resources.disk`                                        | `update` can raise it. It cannot shrink.                                |
| `name`                                                  | Another name selects another VM.                                        |

Every other key changes with `limanix update`, which restarts the VM.

## Defaults

An empty `limanix.toml` is the same as this file. [`limanix first-config`](/reference/cli#limanix-first-config) writes the same defaults with a comment for each setting, and shows the empty `dotfiles` and toolchain keys as commented-out examples.

::: code-group

```toml [limanix.toml]
schema_version = 1
name = "example-box"

[user]
name = "dev"
home = "/home/dev"
sudo = true

[resources]
arch = "arm64"
cpu = 4
mem = "8GiB"
disk = "10GiB"

[home]
root = "~/.limanix"

[shell]
preset = "terminal"
prompt = "pure"
editor = "astronvim"
multiplexer = "tmux"
dotfiles = ""

[toolchains]
go = ""
rust = ""
python = ""
nodejs = ""

[nixos]
modules = []
packages = []

[theme]
flavor = "system"

[network]
mode = "shared"

[network.ports]
tcp = [8080]
udp = []

[env]
APP_ENV = "development"
APP_LOG_LEVEL = "debug"

[[mounts]]
mode = "rw"
source = "~/projects/my-project"
target = "/workspace"

[[mounts]]
mode = "ro"
source = "~/.ssh/limanix"
target = "/mnt/git-keys"
```

:::

The mounts, the environment variables and TCP port `8080` are examples. To start without them, put `mounts = []` and `env = {}` before the first table and set `tcp = []` in `[network.ports]`.
