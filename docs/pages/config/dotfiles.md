---
description: Link your dotfiles from a folder on the Mac into the home of every VM.
---

# Dotfiles

Keep your shell, editor and Git settings in one folder on your Mac. Name the folder in `[shell]`, and each VM links its files into your home.

## Name your dotfiles folder

::: code-group

```toml [limanix.toml]
[shell]
dotfiles = "~/dotfiles"
```

:::

The folder is shaped like a home: `.zshrc`, `.tmux.conf`, `.gitconfig`, `.config/nvim` and so on. One folder can serve every VM.

The folder must exist when you create or update the VM. A relative path resolves from the folder that holds `limanix.toml`. Without `dotfiles`, the VM gets no dotfiles. Apply a change with `limanix update --config limanix.toml`; see [Changing a VM](/vms/update).

## What gets linked

The VM mounts the folder read-write at `/mnt/dotfiles`. Every new shell you open links its entries into your home before it reads your startup files, such as `~/.zshenv` or `~/.bash_profile`:

| In the folder                                                        | In your home in the VM                                                |
| -------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `.zshrc`, `.tmux.conf` and every other name that starts with `.`     | A link of the same name, such as `~/.zshrc` to `/mnt/dotfiles/.zshrc` |
| `.config/nvim` and every other entry of `.config`                    | A link in `~/.config`, such as `~/.config/nvim`                       |
| `.git`, `.github`, `.gitignore`, `.gitmodules` and `.DS_Store`       | Nothing                                                               |
| `README.md`, `install.sh` and every other name without a leading `.` | Nothing                                                               |

`~/.config` stays a folder of the VM, where tools keep their own files beside your links. Inside `.config`, the names `.git`, `.github`, `.gitignore`, `.gitmodules` and `.DS_Store` are skipped too.

Your startup files, such as `.zshrc`, load after the catalog's shell configuration. A `.config/nvim` with an `init.lua` replaces the bundled AstroNvim setup; see [Shell](/config/shell#choose-an-editor).

## Edit on the Mac

An edit on the Mac is live in every VM at once: the links point to your files, and there is nothing to copy. The next shell links a new entry and removes the link of an entry you deleted. For settings that differ between VMs, test the hostname in your startup files, such as `$HOST` in Zsh.

## Files in the way

A file or folder that already exists in your home is never replaced, and neither is a link that points outside the dotfiles folder. `lmx dotfiles` lists such a path as a conflict, and `lmx doctor` warns about it. Move it aside, then open a new shell:

::: code-group

```sh [VM]
mv ~/.gitconfig ~/.gitconfig.guest
```

:::

## Check the links

`lmx dotfiles` shows the state of each link and changes nothing:

::: code-group

```console [VM]
$ lmx dotfiles
Dotfiles  /mnt/dotfiles
Home      /home/dev

linked    ~/.tmux.conf
linked    ~/.config/nvim
missing   ~/.zshrc
conflict  ~/.gitconfig is a file

Open a new shell, or run lmx dotfiles link, to update the links.
Move the conflicting paths aside, then open a new shell.
```

:::

`lmx dotfiles link` makes the links now and prints each change. It runs as your account and refuses `sudo`: every link in your home belongs to you. [The lmx command](/inside/lmx) covers the other `lmx` commands.

## When the folder is missing

While the VM does not see the folder, nothing is linked or removed, and each new shell says so. Your links stay until the folder is back. This happens when the mount fails, or when the folder moved or was deleted on the Mac. Fix the path in `limanix.toml` if it changed, then run `limanix update --config limanix.toml`; it mounts the folder again.
