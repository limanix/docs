---
description: Copy to and paste from the Mac clipboard inside a VM with pbcopy and pbpaste.
---

# Clipboard

Inside the VM, `pbcopy` and `pbpaste` work like on your Mac: they copy to and paste from the Mac clipboard. Every VM has them. The terminal on your Mac must support OSC 52 and allow it.

## Copy and paste

::: code-group

```sh [VM]
pbcopy < notes.txt
git diff | pbcopy
pbpaste > snippet.txt
```

:::

`pbcopy` copies its standard input to the Mac clipboard, and `pbpaste` prints the Mac clipboard. Neither takes options. They are other names of `lmx clipboard copy` and `lmx clipboard paste`.

## How they reach the Mac

`pbcopy` and `pbpaste` work through the terminal you opened the shell in. They send it OSC 52 escape sequences, and the terminal on your Mac writes or reads its clipboard. Inside tmux, they hand over to tmux, which passes the clipboard on through the terminal it is attached to.

## Allow clipboard access in your terminal

Clipboard access is a setting of the terminal on your Mac. Allow OSC 52 in it; reading the clipboard usually needs one more permission than writing it. The terminal may ask for permission first: `pbpaste` waits up to 10 seconds for its answer.

::: tip
When the terminal does not let the VM read the clipboard, paste with Cmd+V, the terminal's own paste shortcut.
:::

## In tmux, AstroNvim and Lazygit

| Where     | Copy to the Mac                                    | Paste from the Mac                     |
| --------- | -------------------------------------------------- | -------------------------------------- |
| tmux      | Ctrl-B, `[` for copy mode; `v` selects, `y` copies | Cmd+V                                  |
| AstroNvim | Yank as usual: yanks go to the Mac clipboard       | Cmd+V in insert mode, or `:r !pbpaste` |
| Lazygit   | Its copy commands                                  | Cmd+V                                  |

In AstroNvim, `p` puts the last yank without asking the terminal, and never waits for a clipboard read. tmux turns on clipboard support for terminal types that start with `xterm`, such as Ghostty's `xterm-ghostty`; for other types, it relies on its own detection.

## When it does not work

| What you see                                                                   | What to do                                                                                                                                    |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `pbpaste` prints nothing and says `The terminal did not share its clipboard.`  | The terminal refused to share its clipboard, or did not answer within 10 seconds. Allow clipboard reads in its settings, or paste with Cmd+V. |
| `pbcopy` or `pbpaste` says it `needs the terminal of a limanix shell session.` | The command has no terminal to talk to. Run it in an interactive shell that you opened with `limanix shell`.                                  |
| A copy does not reach the Mac                                                  | Check that the terminal on your Mac supports OSC 52 and allows it.                                                                            |
