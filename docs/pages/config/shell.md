---
description: Choose the shell preset, prompt, editor and multiplexer of a VM.
---

# Shell

The `[shell]` table chooses what you work in when you open a shell in the VM: the login shell and its tools, the prompt, the editor and the terminal multiplexer.

::: code-group

```toml [limanix.toml]
[shell]
preset = "terminal"   # terminal or minimal
prompt = "pure"       # pure, starship or none
editor = "astronvim"  # astronvim, neovim or none
multiplexer = "tmux"  # tmux or none
```

:::

These are the defaults: a file without a `[shell]` table gets the same shell. Apply a change with `limanix update --config limanix.toml`; see [Changing a VM](/vms/update).

## Choose a preset

| Preset                  | Login shell        | Always included                                      |
| ----------------------- | ------------------ | ---------------------------------------------------- |
| `terminal`, the default | Zsh with Oh My Zsh | Git, the CLI tools, Lazygit, Yazi and the GitHub CLI |
| `minimal`               | Bash               | Git and the CLI tools                                |

The CLI tools are `rg`, `fd`, `fzf`, `bat`, `eza`, `delta`, `jq`, `yq`, `xh`, `btop`, `dust`, `duf` and `tldr`. Zsh adds command suggestions, syntax highlighting, completion search with Tab, history search with Ctrl-R, `z` to return to visited directories and direnv for project environments. [The terminal](/inside/terminal) shows how to use them.

The preset also sets the defaults of the other settings:

| Setting       | Choices                       | `terminal` default | `minimal` default |
| ------------- | ----------------------------- | ------------------ | ----------------- |
| `prompt`      | `pure`, `starship`, `none`    | `pure`             | `none`            |
| `editor`      | `astronvim`, `neovim`, `none` | `astronvim`        | `none`            |
| `multiplexer` | `tmux`, `none`                | `tmux`             | `none`            |

`none` leaves the component out of the VM. With `minimal`, name an editor or a multiplexer to add it:

::: code-group

```toml [limanix.toml]
[shell]
preset = "minimal"
editor = "neovim"
```

:::

The minimal preset has no GitHub CLI: add it with `packages = ["gh"]` in [`[nixos]`](/config/modules). To keep the terminal preset with another login shell, set `limanix.user.shell` in [your own module](/modules/custom).

## Choose a prompt

The prompt belongs to Zsh and needs the terminal preset.

| `prompt`            | What you get                                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `pure`, the default | Pure on two lines: the directory, the Git state, how long a command took and a different color after a failed command |
| `starship`          | Starship, which also shows the hostname, the language versions it detects and the exit status                         |
| `none`              | No managed prompt: set `PROMPT` in your `~/.zshrc`                                                                    |

Both prompts use the colors of the [theme](/config/environment#choose-a-theme). Outside tmux, they show the words of `lmx status --short` that need attention, such as `restart`; inside tmux, the status line shows them. A personal `~/.config/starship.toml` takes precedence over the managed Starship settings.

With `preset = "minimal"`, leave `prompt` out or set it to `none`: `limanix create` and `limanix update` reject a prompt there. Bash then shows your account, the VM's hostname and the directory in the theme's accent colors.

## Choose an editor

| `editor`                 | What you get                                                                                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `astronvim`, the default | Neovim set up as AstroNvim: file explorer, fuzzy search, completion, Git UI, diagnostics and the language servers of your [toolchains](/config/toolchains). Neovim becomes the default `EDITOR`. |
| `neovim`                 | Plain Neovim. `vi` and `vim` start it too; `EDITOR` stays `nano`, and you configure language servers yourself.                                                                                   |
| `none`                   | No editor                                                                                                                                                                                        |

Open files with `nvim`. Your own `~/.config/nvim/init.lua` or `init.vim`, for example from your [dotfiles](/config/dotfiles), replaces the bundled AstroNvim setup. To extend AstroNvim instead, add plugin specifications under `~/.config/nvim/lua/plugins/`.

## Choose a multiplexer

`multiplexer = "tmux"` adds tmux: windows, split panes, mouse support, copying to the Mac clipboard and saved layouts that tmux restores after a restart. It also provides named sessions. From the Mac, `--session` opens a tmux session in the VM, or attaches to it when it exists:

::: code-group

```sh [Mac]
limanix shell dev-box --session work
```

:::

Run the same command to return after you detach with Ctrl-B d. Session names cannot contain `.` or `:`. Without tmux or a session provider from your own module, `limanix shell --session` names the setting that adds one and exits.

[Shell and sessions](/vms/shell) covers sessions, and [The terminal](/inside/terminal) covers the tmux keys.

## Your own startup files

Your startup files, such as `~/.zshrc`, load after the catalog's configuration. Keep them in your [dotfiles](/config/dotfiles) to share them between VMs.
