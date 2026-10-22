---
description: Set environment variables, the colors and your account in a VM.
---

# Environment and theme

Three small tables shape the VM around you. `[env]` sets environment variables, `[theme]` picks the colors, and `[user]` sets up the account you work in.

## Set environment variables

::: code-group

```toml [limanix.toml]
[env]
APP_ENV = "development"
APP_PORT = "8080"
OPTIONAL_SETTING = ""
```

:::

The variables apply to the whole VM: login sessions and system and user services. Apply a change with `limanix update --config limanix.toml`; see [Changing a VM](/vms/update).

| Rule                                                                          | Example                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------- |
| Every value is a string, numbers included                                     | `APP_PORT = "8080"`                       |
| An empty string is a value                                                    | `OPTIONAL_SETTING = ""`                   |
| Names use ASCII letters, digits and `_`, and do not start with a digit        | `APP_ENV`                                 |
| Values are literal text: they do not read the Mac's variables or run commands | `TOKEN = "$TOKEN"` sets the text `$TOKEN` |

Without an `[env]` table, the VM gets `APP_ENV = "development"` and `APP_LOG_LEVEL = "debug"`. A table with entries sets exactly those entries. For no variables, write an empty `[env]` table, or `env = {}` before the first table.

::: warning
`[env]` is plain text, not secret storage. The values are written to files under `/etc/limanix` in the VM, readable by root and your account's group.
:::

## Choose a theme

::: code-group

```toml [limanix.toml]
[theme]
flavor = "system"
```

:::

| Flavor                | Colors                                               |
| --------------------- | ---------------------------------------------------- |
| `system`, the default | Your terminal's own 16 colors and its background     |
| `latte`               | [Catppuccin](https://catppuccin.com/palette/), light |
| `frappe`              | Catppuccin, dark                                     |
| `macchiato`           | Catppuccin, darker                                   |
| `mocha`               | Catppuccin, darkest                                  |

`lmx` and the catalog tools with colors share the theme, among them the Zsh prompt, tmux, AstroNvim, Yazi, Lazygit, Posting and Harlequin.

With `system`, the VM draws in the colors of your terminal's theme on the Mac, on its background. When you change that theme, or the terminal switches between light and dark, the VM follows at once; there is nothing to apply. A few tools keep colors of their own:

| Tool      | With `system`                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------- |
| AstroNvim | Catppuccin text colors on a transparent background: Latte on a light terminal background, Mocha on a dark one |
| Harlequin | Catppuccin Mocha                                                                                              |

A Catppuccin flavor sets its colors in every tool, and several tools also paint its background: choose the flavor that matches your terminal. Apply it with `limanix update --config limanix.toml`; the VM restarts with the new colors. Settings you make in a tool itself still take precedence. `NO_COLOR` or `TERM=dumb` turn the colors of `lmx` off.

## Set up your account

::: code-group

```toml [limanix.toml]
[user]
name = "dev"
home = "/home/dev"
sudo = true
```

:::

| Key    | Default     | What it sets                                                   |
| ------ | ----------- | -------------------------------------------------------------- |
| `name` | `dev`       | The account `limanix shell` logs you in as                     |
| `home` | `/home/dev` | Your home folder in the VM, kept on the Mac under `~/.limanix` |
| `sudo` | `true`      | Passwordless `sudo` in the VM; `false` leaves it out           |

A name starts with a lowercase letter or `_`, followed by lowercase letters, digits, `_` or `-`, up to 32 characters. `root` and `limanix-admin` are reserved. The name can differ from your Mac account's name; the account uses your Mac account's numeric user ID for the ownership of shared files. LimaNix creates a group for it.

`home` follows the rules of [paths in the VM](/config/mounts#paths-in-the-vm), and [Files and storage](/vms/storage) explains where it lives on the Mac. `sudo` applies only in the VM and grants no administrator rights on the Mac.

`name` and `home` are fixed when you create the VM; changing them needs a new VM. `sudo` changes with `limanix update`.
