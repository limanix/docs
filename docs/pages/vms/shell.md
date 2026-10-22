---
description: Open a shell in a VM, keep named sessions and run single commands from the Mac.
---

# Shell and sessions

`limanix shell` connects your terminal on the Mac to a VM. Use it for an interactive shell, a named
session that outlives your terminal, or a single command.

## Open a shell

::: code-group

```sh [Mac]
limanix shell dev-box
```

:::

You log in as the user from `[user]` in `limanix.toml`, in that user's home: `dev` in `/home/dev`
with the defaults. The login shell is Zsh with the `terminal` shell preset and Bash with `minimal`;
see [Shell](/config/shell). The welcome summary appears when you enter, and `lmx welcome` shows it
again.

The VM must be running: start a stopped one with `limanix start dev-box`. Your home is the managed
home shared with the Mac, and a shared project folder is at its target, such as `/workspace`. See
[Files and storage](/vms/storage).

## Leave the shell

Type `exit` to return to the Mac. The VM keeps running until you stop it with
`limanix stop dev-box`.

## Run one command

Put the command after `--`:

::: code-group

```sh [Mac]
limanix shell dev-box -- id
```

:::

The command runs as the same user and starts in the home. `limanix shell` exits with the command's
exit status, which makes it usable in scripts: `limanix shell dev-box -- true` succeeds when you can
reach the VM as that user.

LimaNix passes the arguments to the VM unchanged. For `cd`, pipelines or variables, run a shell in
the VM:

::: code-group

```sh [Mac]
limanix shell dev-box -- bash -lc 'cd /workspace && pwd'
limanix shell dev-box -- bash -lc 'printf "%s\n" "$HOME"'
```

:::

The single quotes keep the Mac's shell from expanding `$HOME` before the command reaches the VM.

## Use a named session

A named session keeps your terminal work running in the VM when the connection closes. Open the
session `work`, or return to it:

::: code-group

```sh [Mac]
limanix shell dev-box --session work
```

:::

The first call creates the session; later calls attach to it. `--session` also works before the VM
name, as in `limanix shell --session work dev-box`. It needs a nonempty name and cannot be combined
with a command after `--`. Inside the VM, `limanix-session work` opens the same session.

### Choose a session provider

A provider in the VM runs the sessions. The catalog's provider is tmux: the `terminal` preset
includes it, and `multiplexer` adds it to the `minimal` preset:

::: code-group

```toml [limanix.toml]
[shell]
preset = "minimal"
multiplexer = "tmux"
```

:::

Apply the change with `limanix update --config limanix.toml`. A module of your own can provide the
sessions instead; see [Your own modules](/modules/custom). Without a provider, `--session` prints
the `limanix.toml` setting that adds one and exits with status 127.

### Name sessions for tmux

The tmux provider rejects a name that contains `.` or `:`, because tmux would change it, and exits
with status 64. Use names such as `work` or `project-api`.

### Detach and return

In tmux, press Ctrl-B, then `d`, to detach. The session keeps running in the VM; run
`limanix shell dev-box --session work` again to return to it. [The terminal](/inside/terminal)
covers windows, panes and the other tmux keys.

### Sessions and restarts

A session outlives a closed terminal, not a VM restart: `limanix stop` and `limanix update` end the
processes running in it. Before an update, save the tmux layout with Ctrl-B, Ctrl-S and wait for the
save to finish; tmux restores the layout the next time it starts. Running processes and unsaved
editor buffers are not restored.
