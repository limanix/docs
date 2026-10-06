# Terminal and clipboard

You work in a LimaNix guest through a terminal on your Mac, and that terminal
carries the clipboard. The VM has no direct access to the Mac clipboard:
programs in the guest copy and paste with OSC 52 escape sequences that travel
through `limanix shell`. Set up the terminal once on the **Mac**; every VM uses
the same behavior with or without tmux.

## How copy and paste work

```{mermaid}
flowchart LR
    guest["Guest program: pbcopy, tmux, Neovim, Lazygit"] -->|"OSC 52 write"| terminal["Terminal on the Mac"]
    terminal --> clipboard["Mac clipboard"]
    clipboard -->|"Cmd+V: typed input"| focused["Focused guest program"]
    clipboard -->|"OSC 52 read, when allowed"| reader["pbpaste"]
```

| Direction | How | What the terminal must allow |
| -- | -- | -- |
| VM to Mac | `pbcopy`, tmux copy mode, a Neovim yank, Lazygit copy | OSC 52 writes |
| Mac to the focused guest program | Cmd+V | Nothing; every terminal pastes typed input |
| Mac to a guest command | `pbpaste` | OSC 52 reads, usually after asking you |

Every guest provides `pbcopy` and `pbpaste`, with any module selection. Inside
tmux they go through tmux to the attached terminal; outside tmux they talk to
the terminal directly. Inside the **VM**:

```console
git diff | pbcopy
pbpaste > notes.txt
```

## Enable the clipboard in your terminal

| Terminal | Copy from the VM | `pbpaste` | Setting |
| -- | -- | -- | -- |
| iTerm2 3.5 or later | After you enable the setting | Asks for permission | Settings → General → Selection → **Applications in terminal may access clipboard** |
| Ghostty | By default | Asks for permission by default | `clipboard-write = allow` and `clipboard-read = ask` in the Ghostty configuration |
| kitty | By default | Asks for permission by default | The default `clipboard_control` |
| Alacritty | By default | Only with `osc52 = "CopyPaste"`, without asking | `osc52` in the `[terminal]` table of `alacritty.toml` |
| WezTerm | By default | Not supported; use Cmd+V | None |
| Terminal.app | Not supported | Not supported | Use another terminal, or copy a mouse selection with Cmd+C |

A terminal that allows reads without asking lets any program in the VM read your
Mac clipboard, including passwords you copied. Keep the confirmation where the
terminal offers one. In Alacritty, keep the default `osc52 = "OnlyCopy"` and
paste with Cmd+V unless you need `pbpaste`.

When a terminal does not answer a read, `pbpaste` waits up to 10 seconds and
then reports that the terminal did not share its clipboard.

To check the setup, run `printf 'LimaNix\n' | pbcopy` in the VM and paste with
Cmd+V in a Mac application.

## Copy and paste in the workspace tools

| Tool | Copy to the Mac | Paste from the Mac |
| -- | -- | -- |
| Shell | `command \| pbcopy` | Cmd+V, or `pbpaste` in a command |
| tmux | Select with the mouse, or `v` and `y` in copy mode | Cmd+V; `Ctrl-b ]` pastes the last tmux copy |
| AstroNvim | Yank: `y`, `yy` | Cmd+V in insert mode, or `:r !pbpaste`; `p` puts the last yank |
| Lazygit | Its copy commands | Cmd+V |
| Claude Code, Codex | Select the output with the mouse | Cmd+V |

With tmux, a mouse selection belongs to tmux and is copied through OSC 52 when
you release the button. Hold Shift, or Option in iTerm2, to select with the
terminal instead.

Images do not travel through OSC 52 text. To give a guest program an image or
another file, save it in a directory shared with the VM and use its guest path.

## When copying does not work

| Symptom | Check |
| -- | -- |
| Nothing reaches the Mac clipboard | The terminal setting above; Terminal.app cannot receive OSC 52 |
| Copying works outside tmux but not inside | The tmux client must be attached in this terminal; tmux run inside another tmux needs the outer one to forward OSC 52 |
| `pbpaste` waits, then fails | The terminal does not answer clipboard reads, or the permission prompt was declined; paste with Cmd+V |
| `pbcopy` or `pbpaste` reports that it needs a terminal | Run it from a `limanix shell` session, not from a background service |
| A large copy is cut off or ignored | Terminals limit the size of OSC 52 data; copy a file through a shared directory instead |

The [tmux module](https://limanix.dev/categories/nixos/modules/tmux/README.html)
and
[AstroNvim module](https://limanix.dev/categories/nixos/modules/astronvim/README.html)
describe their clipboard behavior.
