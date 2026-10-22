---
description: Zsh, the prompt, AstroNvim, tmux and the other tools of the terminal preset, and how to start each one.
---

# The terminal

The `terminal` shell preset, the default, sets up the VM for development in the terminal. This page shows what each of its tools is for and how to start it. To switch a tool off or choose another prompt or editor, see [Shell](/config/shell).

## What you get

| Tool               | Use it for                                                     | Start it with                      |
| ------------------ | -------------------------------------------------------------- | ---------------------------------- |
| Zsh with Oh My Zsh | Your shell, with completion, suggestions and history search    | `limanix shell dev-box` on the Mac |
| Pure prompt        | Directory, Git state and how long a command took               | Every shell                        |
| CLI tools          | Searching, reading files, querying data, sending HTTP requests | `rg`, `fd`, `bat`, `jq` and more   |
| Lazygit            | Git in a terminal interface                                    | `lazygit`                          |
| Yazi               | Browsing files                                                 | `y`                                |
| GitHub CLI         | Working with GitHub from the terminal                          | `gh`                               |
| AstroNvim          | Editing code, with language servers                            | `nvim`                             |
| tmux               | Windows, panes and sessions that outlive a closed terminal     | `tmux`                             |

The `minimal` preset has Bash, Git and the CLI tools, plus an editor or tmux when you choose them.

## Welcome and help

Each new shell session starts with the welcome: the state of the VM, its resources, network, shared folders and selected modules. When something needs attention, the welcome names it, with the command that helps. Run `lmx welcome` to show it again; [The lmx command](/inside/lmx#the-welcome) explains what it shows.

`lmx help` shows the commands of the VM and the help topics. `lmx help TOPIC`, such as `lmx help tmux`, shows what a tool gives you: its commands, common tasks and a link to its guide. The terminal tools have the topics `zsh`, `cli-tools`, `lazygit`, `yazi`, `astronvim` and `tmux`.

## Zsh and the prompt

Zsh, with the Oh My Zsh framework, is your login shell: `limanix shell dev-box` on the Mac opens it.

| Keys or command  | What it does                                                                 |
| ---------------- | ---------------------------------------------------------------------------- |
| Tab              | Search the completion candidates                                             |
| Right arrow      | Accept the suggestion from your history                                      |
| Ctrl-R           | Search the commands you ran, with Atuin                                      |
| Ctrl-T           | Insert selected paths, with fzf                                              |
| Alt-C            | Change directory, with fzf                                                   |
| `z NAME` or `zi` | Return to a directory you visited, with zoxide                               |
| `direnv allow`   | Approve a project's `.envrc`; it then loads whenever you enter the directory |

Atuin keeps your history in the VM; it does not sync and needs no account. Run `direnv allow` again after `.envrc` changes. Personal settings go in `~/.zshrc`, which Zsh reads after the managed setup. Keep it in your [dotfiles](/config/dotfiles) to share it between VMs.

Pure, the default prompt, takes two lines. It shows the directory, the Git state and how long a command took, and its color tells you when the last command failed. Outside tmux, its right side shows a word when the VM needs attention, such as `restart`; [status words](/inside/lmx#status-words-in-tmux-and-the-prompt) lists them. Pure reads its settings, such as `zstyle ':prompt:pure:path' color cyan`, from `~/.zshrc`. With `prompt = "starship"`, Starship also shows the hostname, the versions of the languages it detects and the exit status.

## CLI tools

Both presets include these commands:

| Command       | Use it to                                             |
| ------------- | ----------------------------------------------------- |
| `rg`          | Search file contents                                  |
| `fd`          | Find files by name                                    |
| `fzf`         | Pick from a list with fuzzy search                    |
| `bat`         | Read files with syntax highlighting                   |
| `eza`         | List directory contents                               |
| `jq`, `yq`    | Query JSON and YAML                                   |
| `xh`          | Send HTTP requests                                    |
| `btop`        | Watch the VM's CPU, memory and processes              |
| `dust`, `duf` | See directory sizes and free file system space        |
| `tldr`        | Read command examples; run `tldr --update` once first |

`git diff` and `git log -p` show changes through `delta`.

## Git and Lazygit

The VM does not copy your Git identity from the Mac. Set it once:

::: code-group

```sh [VM]
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

:::

For private repositories, the VM account needs its own access, such as an SSH key mounted into the VM or a credential helper.

Run `lazygit` inside a repository to stage, commit, push and pull. Press Space on a file to stage it, `c` to commit, `P` to push, `p` to pull and `?` for all keys. The GitHub CLI, `gh`, works from the same shell.

## Yazi

Run `y` to browse files and their previews, starting from the current directory. Press `q` to leave and move your shell to the directory Yazi was in, or `Q` to leave without moving it. F1 or `~` shows the keys. A file you change or delete in a shared folder changes on the Mac too.

## AstroNvim

AstroNvim is Neovim with a file explorer, fuzzy search, completion, a Git interface and diagnostics. Run `nvim .` in a project, such as `/workspace`, to open it. Space is the leader key: press it and pause for hints.

| Keys            | Action                                    |
| --------------- | ----------------------------------------- |
| Space, `e`      | Open the file explorer                    |
| Space, `f`, `f` | Find files                                |
| Space, `g`, `g` | Open Lazygit                              |
| Ctrl-H/J/K/L    | Move between editor splits and tmux panes |
| Alt-H/J/K/L     | Resize them                               |

AstroNvim is also the VM's `EDITOR`, which programs such as `git commit` open. To return to your last session after you quit, start `nvim` and run `:lua require("resession").load("Last Session", { reset = true })`. It restores the files, splits and cursor positions, not unsaved changes.

Customize it with Lazy plugin specifications in `~/.config/nvim/lua/plugins/`. An `init.lua` or `init.vim` of your own in `~/.config/nvim` replaces the bundled setup. [Languages](/inside/languages) covers the language servers. With `editor = "neovim"`, you get plain Neovim instead: `nvim`, `vi` and `vim`, with no language servers set up.

## tmux

tmux starts only when you run it. Start a named session, or return to it:

::: code-group

```sh [VM]
tmux new-session -A -s work
```

:::

`limanix-session work` does the same, as does `limanix shell dev-box --session work` on the Mac; see [Shell and sessions](/vms/shell). Session names cannot contain `.` or `:`. The prefix is Ctrl-B: press it, release it, then press the second key.

| Keys               | Action                                                  |
| ------------------ | ------------------------------------------------------- |
| Ctrl-B, `c`        | New window                                              |
| Ctrl-B, `n` or `p` | Next or previous window                                 |
| Ctrl-B, `w`        | Choose a window                                         |
| Ctrl-B, `%` or `"` | Split left and right, or top and bottom                 |
| Ctrl-H/J/K/L       | Move between panes                                      |
| Alt-H/J/K/L        | Resize a pane                                           |
| Ctrl-B, `[`        | Copy mode: `v` selects, `y` copies to the Mac clipboard |
| Ctrl-B, `d`        | Detach; the session keeps running                       |
| Ctrl-B, Ctrl-S     | Save the layout                                         |
| Ctrl-B, `?`        | Show all key bindings                                   |

The mouse works too. In tmux, Ctrl-L moves to the pane on the right instead of clearing the screen; press Ctrl-B, Ctrl-L to clear it. The right side of the status line shows a word when the VM needs attention.

tmux saves the layout every 15 minutes. Before `limanix update`, save it with Ctrl-B, Ctrl-S and wait for the save to finish. After the restart, start tmux: sessions, windows, panes and their directories come back, while running programs such as development servers and unsaved editor changes do not.

## A typical workflow

Open a session from the Mac:

::: code-group

```sh [Mac]
limanix shell dev-box --session work
```

:::

In the VM, run `cd /workspace` and `nvim .` to open the project in the editor. Press Ctrl-B, `c` for a new window and run `lazygit` there to review your changes. Open one more window for the project's build and test commands. Switch windows with Ctrl-B, `n` and Ctrl-B, `p`. Detach with Ctrl-B, `d`, and run the same `limanix shell` command to return.

## Set up the terminal on your Mac

Fonts, colors and the clipboard belong to the terminal on your Mac, not to the VM:

- Choose a Nerd Font and turn on true color.
- Allow OSC 52 clipboard access; see [Clipboard](/inside/clipboard).
- Send Option as Alt, for Alt keys such as Alt-H/J/K/L.

The VM knows Ghostty's terminal type, `xterm-ghostty`. By default, the tools draw in the colors and on the background of your terminal's theme; [Environment and theme](/config/environment) has the other choices.
