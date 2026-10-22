---
description: Install LimaNix, create a NixOS VM from limanix.toml, open a shell in it and apply a change.
---

# Quick start

This page takes you from the download to a shell in a NixOS VM, then through a change and cleanup. You need macOS 26 or newer on an Apple Silicon or Intel Mac.

## Install the client

Download `limanix-arm64` for Apple Silicon or `limanix-amd64` for Intel from [limanix.dev/download](https://limanix.dev/download), then install it:

::: code-group

```sh [Mac]
mkdir -p ~/.local/bin
install -m 755 ~/Downloads/limanix-arm64 ~/.local/bin/limanix
export PATH="$HOME/.local/bin:$PATH"
limanix --version
```

:::

On Intel, use `~/Downloads/limanix-amd64`. [Install](/install) covers the requirements, the macOS approval prompt and updates.

## Write limanix.toml

Save this file as `limanix.toml` in your project folder, such as `~/projects/my-project`:

::: code-group

```toml [limanix.toml]
schema_version = 1
name = "dev-box"
mounts = []
env = {}

[user]
name = "dev"
home = "/home/dev"
sudo = true

[resources]
arch = "arm64"
cpu = 2
mem = "4GiB"
disk = "16GiB"

[home]
root = "~/.limanix"

[shell]
preset = "minimal"

[nixos]
modules = []

[network]
mode = "shared"

[network.ports]
tcp = []
udp = []
```

:::

On Intel, change `arch` to `"amd64"`. The file declares a VM named `dev-box` with 2 CPUs, 4 GiB of memory and a 16 GiB disk, a `dev` account with passwordless `sudo` inside the VM, and the minimal shell: Bash with Git and the command-line tools.

Keep the empty lists and tables. A setting you leave out takes the built-in example's value, and that example shares two sample folders that must exist on your Mac. [The limanix.toml file](/config/) explains the layout and defaults.

## Create the VM

::: code-group

```sh [Mac]
cd ~/projects/my-project
limanix create --config limanix.toml
```

:::

LimaNix downloads the base image if needed, boots the VM, builds its NixOS system and restarts the VM into it. The first run needs network access for the image and Nix packages. When it finishes, the command prints the VM name and the path of the VM's home on your Mac, under `~/.limanix`. `limanix list` now shows `dev-box` as `Running` and `ready`.

## Open a shell

::: code-group

```sh [Mac]
limanix shell dev-box
```

:::

You are `dev` in `/home/dev`, on Linux. The shell opens with a welcome from `lmx`: the VM's state, its NixOS version and architecture, CPUs, memory and free disk, its address and open ports, the shared folders and modules, and commands to try. Look around:

::: code-group

```sh [VM]
uname -s
lmx help
lmx welcome
exit
```

:::

`lmx help` lists the commands in the VM and on the Mac, and `lmx welcome` shows the welcome again. `exit` returns you to the Mac; the VM keeps running.

## Change the VM

Share your project with the VM and add a package. In `limanix.toml`, remove the line `mounts = []`, add `packages` to the `[nixos]` table, and add a `[[mounts]]` entry at the end of the file:

::: code-group

```toml [limanix.toml]
[nixos]
modules = []
packages = ["tree"]

[[mounts]]
source = "."
target = "/workspace"
mode = "rw"
```

:::

`.` is the folder that holds `limanix.toml`. The update restarts the VM: save any work in it, then apply the file:

::: code-group

```sh [Mac]
limanix update --config limanix.toml
limanix shell dev-box -- tree --version
limanix shell dev-box -- ls /workspace
```

:::

The update builds the new system first and restarts the VM only when the build succeeds. If the build fails, the VM keeps its current system and the error is in the output. In the VM, `/workspace` holds the same files as your project folder: a change or deletion on either side affects both.

## Stop, start and delete

`stop` shuts the VM down and keeps its disk and home. `start` boots the saved system; it does not read `limanix.toml`. `delete` removes the VM's disk, keeps its home on the Mac and prints the home's path; add `--remove-home` to remove the home too. Your project folder stays where it is.

::: warning
`limanix delete` does not ask for confirmation. Copy what you need from the VM first.
:::

::: code-group

```sh [Mac]
limanix stop dev-box
limanix start dev-box
limanix delete dev-box
```

:::

## Tips

- Run one command in the VM from the Mac: `limanix shell dev-box -- uname -a`. See [Shell and sessions](/vms/shell).
- For Zsh, AstroNvim and tmux, set `preset = "terminal"` in `[shell]`. See [Shell](/config/shell).
- With tmux, `limanix shell dev-box --session work` returns you to the same session after you disconnect. See [Shell and sessions](/vms/shell).
- Add Go, Rust, Python or Node.js in `[toolchains]`. See [Toolchains](/config/toolchains).
- `limanix modules list` shows what your client's catalog offers, such as `lmx:docker`. See [The catalog](/modules/).
- Reach a server in the VM at the VM's address, not at `localhost`. See [Network](/vms/network).
- `pbcopy` and `pbpaste` in the VM use the Mac clipboard. See [Clipboard](/inside/clipboard).
- Try a tool without changing the file: `nix shell nixpkgs#openssl`. See [Packages on the fly](/inside/packages).
- When something looks wrong, run `limanix doctor dev-box`. See [Troubleshooting](/troubleshooting).
