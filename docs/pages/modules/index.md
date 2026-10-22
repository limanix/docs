---
description: What the LimaNix catalog contains and how to choose shell components, toolchains and modules from it.
---

# The catalog

The catalog is the set of NixOS modules that LimaNix can add to a VM: a shell, language toolchains, services and tools. You choose from it in `limanix.toml` without writing Nix.

## Where the catalog comes from

Each `limanix` binary embeds one catalog release and is tested with it. To see what your client bundles, run:

::: code-group

```sh [Mac]
limanix modules list
```

:::

Each row shows a selector, its kind and its description. The list reads the embedded catalog and the modules you imported; it downloads nothing. A newer client can bring new modules, version lines and defaults. Installing it does not change an existing VM until you run `limanix update`.

## Three kinds

The catalog has three kinds of entries, and `limanix.toml` chooses each kind in its own table:

| Kind             | Chosen in                                                  | Example                    | Page                                    |
| ---------------- | ---------------------------------------------------------- | -------------------------- | --------------------------------------- |
| Shell components | `[shell]`: a preset and its prompt, editor and multiplexer | `editor = "astronvim"`     | [Shell](/config/shell)                  |
| Toolchains       | `[toolchains]`: one version per language                   | `go = "1.27"`              | [Toolchains](/config/toolchains)        |
| Modules          | `[nixos] modules`, by selector                             | `modules = ["lmx:docker"]` | [Modules and packages](/config/modules) |

One file can use all three:

::: code-group

```toml [limanix.toml]
[shell]
preset = "terminal"

[toolchains]
go = "1.27"

[nixos]
modules = ["lmx:docker"]
```

:::

Without these tables the VM gets the `terminal` preset, no toolchain and no other module. A shell component or a toolchain in `[nixos] modules` fails and names the table that chooses it, for example `lmx:go is a toolchain; choose its version in [toolchains], such as go = "1.27"`.

## Modules

| Module                              | Selector        | Adds                                                                         |
| ----------------------------------- | --------------- | ---------------------------------------------------------------------------- |
| [Docker](/modules/docker)           | `lmx:docker`    | Docker Engine, the Docker CLI, Compose and Lazydocker                        |
| [PostgreSQL](/modules/postgres)     | `lmx:postgres`  | The PostgreSQL server and its tools, for manual use                          |
| [Google Cloud CLI](/modules/gcloud) | `lmx:gcloud`    | The Google Cloud CLI                                                         |
| [Claude Code](/modules/claude-code) | `lmx:claude`    | Anthropic's coding agent for the terminal, without self-updates              |
| [Posting](/modules/posting)         | `lmx:posting`   | An HTTP client for the terminal, in the guest's theme                        |
| [Harlequin](/modules/harlequin)     | `lmx:harlequin` | A SQL IDE for the terminal with the PostgreSQL adapter, in the guest's theme |

Software that needs no configuration is a package, not a module: list it in `[nixos] packages`, as [Modules and packages](/config/modules) shows. For settings or services of your own, [write a module](/modules/custom) and select it as `third-party:NAME`.

## Versions

Some modules offer version lines. `lmx:NAME` selects the module's default line. `lmx:NAME-LINE` selects a line explicitly and replaces the default.

| Module     | Lines            | Default |
| ---------- | ---------------- | ------- |
| Docker     | `28`, `29`       | `29`    |
| PostgreSQL | `16`, `17`, `18` | `18`    |

The other modules have no lines and only the `lmx:NAME` selector. A future catalog release may change a default; to stay on a line, select it explicitly.

Select several lines of one module only when its page allows it. PostgreSQL installs `lmx:postgres-16` and `lmx:postgres-18` side by side. Docker takes one line, and two lines stop the build with `docker: select one line`. Each module page lists the package versions of its lines and their support status. An end-of-life line prints a warning when the VM builds.

## Help inside the VM

Every module explains itself in the VM:

::: code-group

```sh [VM]
lmx help docker
```

:::

The card shows the installed versions, the commands the module adds, common tasks and a link to its guide. `lmx help` lists the topics; `lmx help docker-29` and `lmx help lmx:docker` work too. See [The lmx command](/inside/lmx).

::: details Selectors from earlier catalogs

Earlier catalogs had modules that only installed a package, and aggregates that the shell presets replace. Replace them as follows:

| Former selector                                                                                  | Now                                                                                 |
| ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| `lmx:cozy`, `lmx:console`                                                                        | The `terminal` preset, with `[toolchains]` and modules for the rest                 |
| `lmx:zsh`, `lmx:tmux`, `lmx:astronvim`, `lmx:neovim`, `lmx:yazi`, `lmx:lazygit`, `lmx:cli-tools` | `[shell]`                                                                           |
| `lmx:go`, `lmx:python`, `lmx:nodejs`, `lmx:rust`                                                 | `[toolchains]`                                                                      |
| `lmx:git`                                                                                        | Part of the CLI tools                                                               |
| `lmx:gh`                                                                                         | Part of the `terminal` preset; `packages = ["gh"]` with `minimal`                   |
| `lmx:lazydocker`                                                                                 | Part of `lmx:docker`                                                                |
| `lmx:k9s`, `lmx:minikube`                                                                        | `packages = ["k9s", "minikube"]`                                                    |
| `lmx:helm`, `lmx:terraform`, `lmx:taskfile`                                                      | `packages = ["unstable:kubernetes-helm", "unstable:terraform", "unstable:go-task"]` |
| `lmx:codex`, `lmx:aws`                                                                           | `packages = ["unstable:codex", "unstable:awscli2"]`                                 |

:::
