---
description: Write a NixOS module of your own, import it with limanix modules add and select it in limanix.toml.
---

# Your own modules

A module of your own adds what the catalog and `[nixos] packages` do not cover, such as a service with your settings. You write it in Nix, import it on your Mac and select it in `limanix.toml` like a catalog module.

## When to write a module

A package works on its own once installed: list it in `[nixos] packages`, as [Modules and packages](/config/modules) shows. Write a module when you need more than a package: to start a service, such as [PostgreSQL with a database for your user](/modules/postgres#run-as-a-system-service), to create a user or a group, to write configuration you would otherwise write by hand, or to change system settings such as your login shell.

## Write the module

Keep each module in a directory of its own, such as `modules/dev-tools/` in your project. The directory needs a `default.nix` at its root:

::: code-group

```nix [modules/dev-tools/default.nix]
{ pkgs, ... }:
{
  environment.systemPackages = [
    pkgs.jq
    pkgs.ripgrep
  ];
}
```

:::

The file is a function that receives `pkgs`, the package set, and returns settings. This one sets `environment.systemPackages`, the NixOS option that installs packages for all users, to `jq` and `ripgrep`; `ripgrep` provides the `rg` command. List entries are separated by spaces, and each assignment ends with a semicolon.

Look up package names in [NixOS packages](https://search.nixos.org/packages) and option names in [NixOS options](https://search.nixos.org/options), in the channel of your VM's NixOS release. To split a module into files, add `imports = [ ./tools.nix ./editor.nix ];` to `default.nix`.

## Import and select it

On your Mac, import the directory under a name:

::: code-group

```sh [Mac]
limanix modules add dev-tools ./modules/dev-tools
```

:::

Select it as `third-party:dev-tools`, then apply the change with `limanix update --config limanix.toml`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["third-party:dev-tools"]
```

:::

Importing checks the directory and copies it, but it does not evaluate the Nix code. Syntax errors, missing packages and conflicting options show up when the VM builds, in the output of `limanix update`. `limanix modules list` shows imported modules next to the catalog.

A name uses lowercase letters, digits and single hyphens, up to 63 characters, and each part between hyphens starts with a letter: `my-tools` and `tools2` work, `2tools` and `my_tools` don't. Use the name without `third-party:` with `add` and `remove`.

LimaNix copies the whole directory, hidden files such as `.git` included. Keep every file the module imports inside the directory, and import the module's own directory rather than a whole checkout. Symlinks inside the tree, including a symlinked `default.nix`, are rejected.

## Change an imported module

LimaNix works from its copy: editing your files changes nothing until you import them again. `add` refuses a name that exists. Remove the old copy first, then import and update:

::: code-group

```sh [Mac]
limanix modules remove dev-tools
limanix modules add dev-tools ./modules/dev-tools
limanix update --config limanix.toml
```

:::

Reimporting rebuilds no VM: update each VM that should get the change. To try a revision without replacing the current copy, import it as `dev-tools-next` and select `third-party:dev-tools-next` in a test VM.

To take a module out of a VM, remove its selector and update the VM. `limanix modules remove` deletes only the imported copy and changes no VM's selection or applied system. A configuration that still selects the module can't be created or updated until you import it again.

## What a module can use

A module can use standard NixOS options and the public interface that LimaNix supplies to every VM:

| Interface                                              | Use                                                                                                                  |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `config.limanix.user.name`, `config.limanix.user.home` | Read the development account's name and home; both are read-only                                                     |
| `limanix.user.shell`                                   | Choose the account's login shell: Bash by default, Zsh with the `terminal` preset                                    |
| `limanix.help.<topic>`                                 | Add a help card for `lmx help TOPIC`                                                                                 |
| `limanix.session.command`                              | Provide named sessions for `limanix shell --session`: an executable's absolute path, which receives the session name |
| `lmx.capabilities.languageSupport`                     | Offer language servers and parsers to editors; AstroNvim configures the declared servers                             |
| `lmx.capabilities.theme`                               | Read the guest's colors: `flavor`, which `[theme]` chooses, and the read-only `palette` and `ansi`                   |
| Documented `lmx.<module>.*` options                    | Change a setting that a catalog module documents, such as `lmx.tmux.navigation.enable`                               |
| Standard NixOS options                                 | Packages, services, firewall rules and other system settings                                                         |

Read the account through `config` instead of hard-coding a name such as `dev`:

::: code-group

```nix [module.nix]
{ config, pkgs, ... }:
{
  users.users.${config.limanix.user.name}.packages = [ pkgs.jq ];
}
```

:::

To change the login shell, set `limanix.user.shell` rather than the account's `users.users.<name>.shell`:

::: code-group

```nix [module.nix]
{ pkgs, ... }:
{
  programs.fish.enable = true;
  limanix.user.shell = pkgs.fish;
}
```

:::

Everything else is private and can change between releases: the catalog's files, `lmx.internal.*` options, generated files and directory layouts. Don't import catalog files into your module.

::: details Modules written for older releases

The `runtime` and `inputs` module arguments no longer exist, and a module that reads them fails to build. Remove them from the function's arguments and replace their uses:

| Before                                           | Now                                                                                                 |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `runtime.name`                                   | `config.networking.hostName`                                                                        |
| `runtime.arch`                                   | `pkgs.stdenv.hostPlatform`, an attribute set; its `system` is `"aarch64-linux"` or `"x86_64-linux"` |
| `runtime.user.name`, `runtime.user.home`         | `config.limanix.user.name`, `config.limanix.user.home`                                              |
| `runtime.user.uid`                               | `config.users.users.${config.limanix.user.name}.uid`                                                |
| `runtime.ports.tcp`, `runtime.ports.udp`         | `config.networking.firewall.allowedTCPPorts`, `config.networking.firewall.allowedUDPPorts`          |
| `runtime.user.sudo`, `runtime.modules`, `inputs` | No replacement                                                                                      |

:::

## Show help in lmx

Give your module a help card for `lmx help`. Save it next to `default.nix`:

::: code-group

```nix [modules/dev-tools/help.nix]
{
  limanix.help.dev-tools = {
    title = "Dev tools";
    summary = "jq and ripgrep for inspecting project data.";
    commands = [ "jq" "rg" ];
    tips = [
      {
        label = "Pretty";
        text = "jq . data.json";
      }
    ];
  };
}
```

:::

Add `imports = [ ./help.nix ];` to the settings in `default.nix`, import the module again and update the VM. `lmx help dev-tools` then shows the card.

| Field      | Content                                                                                            |
| ---------- | -------------------------------------------------------------------------------------------------- |
| `title`    | The card's heading, such as the tool's name; the topic by default                                  |
| `summary`  | One sentence about what the module gives you                                                       |
| `commands` | Commands the module puts on `PATH`, most used first                                                |
| `tips`     | Up to four common tasks, each a `label` of at most 10 characters and a command or a short sentence |
| `guide`    | Address of a full guide; optional                                                                  |

## Trust and secrets

A module can install software, run services as root and read the folders shared with the VM. Use modules from sources you trust.

::: warning
Files in `/nix/store` are readable by every user in the VM, and module sources can end up there. Keep passwords, tokens and private keys out of modules. For a service that needs a secret, use its secret-file option, if it has one, and create that file inside the VM.
:::
