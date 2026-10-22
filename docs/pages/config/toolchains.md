---
description: Install Go, Rust, Python and Node.js with their language servers.
---

# Toolchains

The `[toolchains]` table installs one version of each language you need, with its language server and build tools.

::: code-group

```toml [limanix.toml]
[toolchains]
go = "1.27"
rust = "stable"
python = "3.14"
nodejs = "26"
```

:::

Leave a key out, or set it to `""`, to install none of that language. Apply a change with `limanix update --config limanix.toml`; see [Changing a VM](/vms/update).

## What each key installs

| Key      | Value                                    | Installs                                                                                  |
| -------- | ---------------------------------------- | ----------------------------------------------------------------------------------------- |
| `go`     | A line, such as `1.27`                   | Go, the gopls language server, the Delve debugger (`dlv`) and GCC for cgo                 |
| `rust`   | A channel or a version, such as `stable` | rustup with Cargo, rustc, rustfmt, Clippy and rust-analyzer, plus GCC, pkg-config and GDB |
| `python` | A line, such as `3.14`                   | Python with venv, virtualenv and the Pyright language server                              |
| `nodejs` | A line, such as `26`                     | Node.js with npm and npx, and the TypeScript language server                              |

[Languages](/inside/languages) shows how to work with each one in the VM.

## Go, Python and Node.js lines

A line is a release series. `go = "1.27"` installs Go 1.27.x, and each catalog release brings the line's patch releases. The current catalog has these lines:

| Key      | Lines                                              |
| -------- | -------------------------------------------------- |
| `go`     | `1.27` (recommended), `1.26`, `1.25` (end of life) |
| `python` | `3.14` (recommended), `3.13`, `3.12`               |
| `nodejs` | `26` (recommended), `24`, `22`                     |

The catalog comes with your `limanix` client. List the lines it has on the Mac:

::: code-group

```sh [Mac]
limanix modules list
```

:::

Each line appears as a row of kind `toolchains`, such as `lmx:go-1.27`. A line the catalog does not have fails `limanix create` or `limanix update` with the lines it has. An end-of-life line prints a warning when the VM is built.

## Rust channels and versions

`rust` sets the default toolchain of rustup:

| Value                       | Toolchain                                          |
| --------------------------- | -------------------------------------------------- |
| `stable`, `beta`, `nightly` | The newest release of the channel when it installs |
| `nightly-2026-10-01`        | The channel as it was on that date                 |
| `1.90`, `1.90.0`            | A Rust release                                     |

rustup downloads the toolchain when the VM starts after the value changes, from `static.rust-lang.org`. A failed download is tried again. Until the toolchain is installed, Cargo reports that no default toolchain is configured. Follow the download in the VM:

::: code-group

```sh [VM]
systemctl --user status rust-toolchain
```

:::

A channel does not move on its own: run `rustup update` for its newest release. A project's `rust-toolchain.toml` selects its own toolchain, which rustup installs on first use.

## Language servers in the editor

With `editor = "astronvim"`, the default of the terminal preset, AstroNvim turns on the language server of each toolchain: gopls, rust-analyzer, Pyright and the TypeScript language server. Its plugins and syntax parsers come with the VM instead of downloading when the editor first starts.

With `editor = "neovim"` or `"none"`, the language servers are still installed for any editor that speaks the Language Server Protocol. Plain Neovim needs your own LSP configuration; see [Shell](/config/shell#choose-an-editor).

Open the project at its path in the VM, such as `/workspace`, for the language servers to see its Linux dependencies.

## Keep Go on the installed version

When a project's `go.mod` or `go.work` requires a newer Go, Go can download that toolchain. To use only the installed one, set `GOTOOLCHAIN` in [`[env]`](/config/environment#set-environment-variables):

::: code-group

```toml [limanix.toml]
[env]
GOTOOLCHAIN = "local"
```

:::

A project that requires a newer Go then fails to build instead of downloading one.
