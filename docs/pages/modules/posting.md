---
description: Posting, an HTTP client for the terminal, inside a LimaNix VM.
---

# Posting

The Posting module installs Posting, a terminal client for HTTP APIs, and sets its theme to match the guest's.

## Enable Posting

Add `lmx:posting` to the modules in `limanix.toml`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:posting"]
```

:::

Apply the change from your Mac. The update restarts the VM; see [Changing a VM](/vms/update).

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

## Send requests

Run Posting in the VM to compose HTTP requests and inspect their responses:

::: code-group

```sh [VM]
posting
```

:::

| Key    | Action                                      |
| ------ | ------------------------------------------- |
| Ctrl-J | Send the request                            |
| Ctrl-S | Save the request to the collection          |
| F1     | Show the key bindings of the focused widget |

When an API is unreachable, check its URL from inside the VM: `localhost` there is the VM, not your Mac.

## Keep requests with a project

Save requests in a collection to reuse them. To open a collection that lives with your project:

::: code-group

```sh [VM]
posting --collection ./requests
```

:::

The directory must already exist. `posting locate collection` shows the default collection directory. The [Posting guide](https://posting.sh/guide/) covers collections and request configuration.

## Theme

The module sets `POSTING_THEME` to follow the guest's [theme](/config/environment):

| `[theme]` flavor      | `POSTING_THEME`                                                          |
| --------------------- | ------------------------------------------------------------------------ |
| `system`, the default | `ansi-dark`: Textual's theme in the terminal's own colors and background |
| A Catppuccin flavor   | `catppuccin-<flavor>`, such as `catppuccin-latte`                        |

On a light terminal, add the variable to your `[env]` table:

::: code-group

```toml [limanix.toml]
[env]
POSTING_THEME = "ansi-light"
```

:::

Posting keeps personal settings in `~/.config/posting/config.yaml`, following `XDG_CONFIG_HOME`; `posting locate config` shows the file. A `theme` set there overrides `POSTING_THEME`.

## Versions

Posting comes from the catalog's NixOS package set. The module has no version lines and no settings of its own.
