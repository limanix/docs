---
description: Run Claude Code, Anthropic's coding agent for the terminal, inside a LimaNix VM.
---

# Claude Code

The Claude Code module installs `claude`, Anthropic's coding agent for the terminal, and turns off its self-updates. Claude Code can read and edit files and run commands in the VM.

## Enable Claude Code

Add `lmx:claude` to the modules in `limanix.toml`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:claude"]
```

:::

Apply the change from your Mac. The update restarts the VM; see [Changing a VM](/vms/update).

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

## Start a session

Run `claude` from your project's directory in the VM:

::: code-group

```sh [VM]
claude
```

:::

Sign in through the prompts on first launch, or with `/login` inside a session. Anthropic's [authentication guide](https://code.claude.com/docs/en/authentication) covers account and provider options. The module does not copy the sign-in from your Mac.

`claude --continue` and `claude --resume` return to earlier sessions, and `claude doctor` runs diagnostics; `lmx help claude` lists them. Claude Code needs internet access from the VM; see its [system requirements](https://code.claude.com/docs/en/setup#system-requirements).

## Versions and updates

Claude Code comes from the catalog's nixos-unstable package set, and the module has no version lines. A newer version arrives with a newer catalog. `claude --version` shows the installed one.

The module sets `DISABLE_UPDATES=1` in every session, which turns off background and manual updates. `claude update` and `claude install` are refused: a separate copy under `~/.local` would bypass the catalog's version and update itself.

Claude Code is unfree software, and the NixOS binary cache does not carry it. The module allows the package, and the VM builds it when the module is applied, by wrapping and patching Anthropic's downloaded binary.

## Keep state across VMs

Claude Code keeps its sign-in, settings, session transcripts, prompt history and memory in `~/.claude/` and `~/.claude.json`. Your home keeps them while the VM exists, but a recreated VM gets a new home and starts without them.

To keep them on your Mac, share a Mac directory with the VM and point `CLAUDE_CONFIG_DIR` at it. Claude Code then also stores `.claude.json` there, and one mount holds all of its state:

::: code-group

```toml [limanix.toml]
[env]
CLAUDE_CONFIG_DIR = "/home/dev/.claude"

[[mounts]]
source = "~/.limanix/agents/dev-box/claude"
target = "/home/dev/.claude"
mode = "rw"
```

:::

Use your `user.home` in place of `/home/dev`, and add the variable to your existing `[env]` table. Create the Mac directory before you run `limanix create` or `limanix update`; see [Shared folders](/config/mounts).

- Give each VM a directory of its own. Two VMs that write the same directory at once can overwrite each other's `.claude.json`.
- Don't mount your Mac's `~/.claude`. macOS keeps the Claude Code sign-in in the Keychain, and Mac hooks and plugins may not run in Linux.
- Transcripts belong to the project's path in the VM. To resume a project's sessions in a new VM, share the project at the same path.

::: warning
The directory holds the sign-in in `.credentials.json` and plaintext transcripts that can contain file contents and command output. Keep it out of repositories and synced folders.
:::

## Settings

The module sets no model, permission or sandbox preferences: Claude Code uses its own configuration. A project can share settings in `.claude/settings.json` and keep personal ones in `.claude/settings.local.json`; see Anthropic's [settings files](https://code.claude.com/docs/en/settings#settings-files-and-who-they-affect).

Claude Code does not install your project's toolchain. When a project command is missing, choose the language in [Toolchains](/config/toolchains) or add a module that provides the tool.
