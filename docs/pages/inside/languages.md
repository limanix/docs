---
description: Build, test and edit Go, Rust, Python and Node.js projects inside a VM.
---

# Languages

Each toolchain you choose in the `[toolchains]` table of `limanix.toml` installs a language with its build tools and its language server. This page shows how to use them inside the VM. To choose a language or its version, see [Toolchains](/config/toolchains).

## See what a toolchain installed

::: code-group

```sh [VM]
lmx help go
```

:::

The card shows the installed version, the commands on your `PATH` and common tasks. The topics are `go`, `rust`, `python` and `nodejs`.

| Toolchain | Installs                                                                                  |
| --------- | ----------------------------------------------------------------------------------------- |
| Go        | Go, the gopls language server, the Delve debugger and GCC for cgo                         |
| Rust      | rustup with Cargo, rustc, rustfmt, Clippy and rust-analyzer, plus GCC, pkg-config and GDB |
| Python    | Python with venv, virtualenv and the Pyright language server                              |
| Node.js   | Node.js with npm and npx, and the TypeScript language server                              |

## Go

Run these from a directory that contains `go.mod`:

::: code-group

```sh [VM]
go build ./...
go test ./...
go test -race ./...
```

:::

GCC enables cgo and the race detector. The Delve debugger runs as `dlv`.

When a project's `go.mod` or `go.work` requires a newer Go, Go can download that toolchain and run it instead. To use only the installed Go, set `GOTOOLCHAIN` in `limanix.toml` and apply it with `limanix update`; a project that requires a newer Go then fails to build:

::: code-group

```toml [limanix.toml]
[env]
GOTOOLCHAIN = "local"
```

:::

## Rust

Rust comes from rustup. When the VM starts after you choose or change the toolchain in `limanix.toml`, it downloads that toolchain, which needs network access. Until the download finishes, Cargo reports that no default toolchain is configured. Follow it with:

::: code-group

```sh [VM]
systemctl --user status rust-toolchain
```

:::

A failed download is tried again; `systemctl --user restart rust-toolchain` starts it at once. Then, from a directory that contains `Cargo.toml`:

::: code-group

```sh [VM]
cargo build
cargo test
cargo fmt
cargo clippy
```

:::

| Task                      | Command                                               |
| ------------------------- | ----------------------------------------------------- |
| Show the toolchain in use | `rustup show`                                         |
| Debug a program           | `rust-gdb`                                            |
| List or remove toolchains | `rustup toolchain list`, `rustup toolchain uninstall` |

A channel does not move on its own: `rustup update` fetches its newest release. A default you set with `rustup default` stays until the value in `limanix.toml` changes. A project selects its own toolchain with a `rust-toolchain.toml` file; rustup installs it on first use. Toolchains in `~/.rustup` and crates in `~/.cargo` stay across VM updates. Commands from `cargo install` go to `~/.cargo/bin`, which comes first on your `PATH`.

## Python

Create a virtual environment in the project directory, activate it and install the project's dependencies:

::: code-group

```sh [VM]
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

:::

The environment includes pip, and `virtualenv .venv` creates an equivalent one. Run `deactivate` to leave it. A virtual environment keeps the interpreter that created it: create it again after you change the Python version.

## Node.js

From a directory that contains `package.json`:

::: code-group

```sh [VM]
npm install
npm run build
```

:::

`npm install` installs the project's dependencies, and `npm run build` runs its `build` script. Packages that build native addons with node-gyp also need Python, make and a C/C++ compiler, which the toolchain does not install.

## Language servers in AstroNvim

AstroNvim, the editor of the `terminal` preset, turns on the language server of each toolchain you choose:

| Toolchain | Language server            | Good to know                                                                                                                                    |
| --------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Go        | gopls                      |                                                                                                                                                 |
| Rust      | rust-analyzer              | rustup runs the rust-analyzer of the project's toolchain, which matches the compiler                                                            |
| Python    | Pyright                    | When it cannot find the project's dependencies, configure the environment in `pyrightconfig.json` or under `[tool.pyright]` in `pyproject.toml` |
| Node.js   | typescript-language-server | Uses the project's own TypeScript when the project configures one                                                                               |

Open the project at its path in the VM, such as `/workspace`: the language servers then see its Linux dependencies. The Tree-sitter parsers for these languages come with the toolchains; add one for another language with `:TSInstall LANGUAGE`, which needs network access.

A language server on your `PATH` alone does not start in the editor. To turn on another one, such as a server from a project environment, add it to the `servers` option of AstroLSP in your Neovim configuration. With `editor = "neovim"`, plain Neovim starts no language server until you configure its LSP client.

## Native libraries

GCC comes with the Go and Rust toolchains, and Rust also has pkg-config. Code that links to a C library still needs that library and its headers: a Go package with cgo, a crate such as `openssl-sys`, a Python package with a native extension or a Node.js native addon. Python and Node.js packages that compile code also need build tools, and a virtual environment does not provide system libraries. Add what a project needs with a module of your own; see [Your own modules](/modules/custom).
