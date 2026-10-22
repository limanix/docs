---
description: Add catalog modules and packages from nixpkgs to a VM.
---

# Modules and packages

The `[nixos]` table adds software to the VM. `modules` selects modules from the LimaNix catalog or your own, and `packages` installs commands from nixpkgs, the Nix package collection.

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:docker"]
packages = ["kubectl", "k9s", "unstable:kubernetes-helm"]
```

:::

Apply a change with `limanix update --config limanix.toml`; see [Changing a VM](/vms/update).

## Package or module

A package installs a tool that works on its own. Choose a module when a tool needs more than its package:

| A module                                                | For example                                  |
| ------------------------------------------------------- | -------------------------------------------- |
| Starts a service, or creates a user or a group          | `lmx:docker` runs Docker Engine as a service |
| Writes configuration you would otherwise write yourself | `lmx:posting` in the VM's theme              |
| Keeps several versions side by side                     | `lmx:postgres-16` with `lmx:postgres-18`     |
| Changes a tool's own behavior                           | `lmx:claude` turns off its self-updates      |

[The catalog](/modules/) describes each module.

## Select modules

| Selector           | Selects                                                 | Example                |
| ------------------ | ------------------------------------------------------- | ---------------------- |
| `lmx:NAME`         | A catalog module, at its default line when it has lines | `lmx:docker`           |
| `lmx:NAME-VERSION` | A specific line of a catalog module                     | `lmx:postgres-16`      |
| `third-party:NAME` | Your own module, imported with `limanix modules add`    | `third-party:my-tools` |

The catalog comes with your `limanix` client. List what it has on the Mac:

::: code-group

```sh [Mac]
limanix modules list
```

:::

Each row shows a selector, its kind and a description. `modules` takes the selectors of kind `modules`. The [shell](/config/shell) and [toolchains](/config/toolchains) tables choose the other kinds, and a selector of theirs in `modules` fails with a message that names the table:

::: code-group

```text [Mac]
nixos.modules[0]: lmx:go is a toolchain; choose its version in [toolchains], such as go = "1.27"
```

:::

An explicit line replaces the module's default line. Several lines of one module work where the module supports them, as PostgreSQL does:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:postgres-16", "lmx:postgres-18"]
```

:::

Modules that allow one line, such as Docker, stop the build when you select two. `modules = []` selects no optional modules; the shell, the toolchains and the LimaNix base system remain.

## Use your own module

Import a folder that has a `default.nix` at its root, under a name of your choice:

::: code-group

```sh [Mac]
limanix modules add my-tools ./my-tools
```

:::

Then select it with `third-party:`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:docker", "third-party:my-tools"]
```

:::

The import is a copy. After you change the module, remove it and add it again, then update each VM that uses it. [Your own modules](/modules/custom) shows how to write and replace one.

## Install packages

List packages by their attribute path in nixpkgs, such as `kubectl` or `python3Packages.ipython`. Find names on [search.nixos.org](https://search.nixos.org/packages), in the channel of the VM's NixOS release; `nixos-version` in the VM shows it.

| Rule                    | What it means                                                                                                                                                                                                                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unstable:`             | `unstable:NAME` takes the package from the catalog's nixos-unstable revision instead, for tools whose release in the VM's NixOS is too old, such as `unstable:kubernetes-helm` or `unstable:codex`. Search them in the `unstable` channel. The revision moves with each catalog release. |
| Commands, not libraries | List packages that bring their own commands. A library such as `python3Packages.requests` installs but cannot be imported: use the project's environment, such as a venv, or a module.                                                                                                   |
| Licenses                | Naming a package accepts its license, even an unfree one. The acceptance uses the last part of the name. When the package's own name differs, the build error names it, and your own module can allow it with `nixpkgs.config.allowUnfreePackages`.                                      |
| Conflicts               | When a listed package provides a command that another package of the VM also provides, the build fails and names both. The same package is no conflict: `jq` beside the CLI tools, which install it, is fine.                                                                            |
| Versions                | One version of a tool per list. Choose language versions in [`[toolchains]`](/config/toolchains), and several versions of a service with module lines.                                                                                                                                   |

With the terminal preset, listing `gh` or `unstable:gh` replaces the preset's GitHub CLI.

A name that is not a package, or a conflict, fails `limanix create` or `limanix update` before the VM restarts. The output gives the reason, and the VM keeps its current system. Fix the file and run the update again.

To try a tool in one VM without editing the file, see [Packages on the fly](/inside/packages).
