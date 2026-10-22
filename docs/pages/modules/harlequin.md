---
description: Harlequin, a SQL IDE for the terminal, inside a LimaNix VM.
---

# Harlequin

The Harlequin module installs Harlequin, a SQL IDE for the terminal, with its PostgreSQL adapter. Harlequin's own DuckDB and SQLite adapters are included. The BigQuery adapter is not, and installing the [Google Cloud CLI](/modules/gcloud) does not add it.

## Enable Harlequin

Add `lmx:harlequin` to the modules in `limanix.toml`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:harlequin"]
```

:::

Apply the change from your Mac. The update restarts the VM; see [Changing a VM](/vms/update).

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

## Open a database

Connect to an existing PostgreSQL database, or open a SQLite file:

::: code-group

```sh [VM]
harlequin --adapter postgres "postgresql://user@localhost:5432/database"
harlequin --adapter sqlite ./database.sqlite
```

:::

You can browse the database catalog, edit SQL and inspect query results. For PostgreSQL connection settings, Harlequin also reads the standard `PG*` environment variables. `lmx help harlequin` lists these commands in the VM.

The module installs the client only. For a PostgreSQL server in the VM, see [PostgreSQL](/modules/postgres). When a connection fails, check the host, port, database, credentials and running server as the VM sees them.

## Save connection profiles

Create a personal connection profile:

::: code-group

```sh [VM]
harlequin --config
```

:::

Harlequin reads profiles from project TOML files, `~/.config/harlequin/config.toml` and TOML files in your home. The user configuration directory follows `XDG_CONFIG_HOME`. The [Harlequin configuration guide](https://harlequin.sh/docs/config-file/) explains which profile wins.

## Theme

The default theme is Catppuccin in the guest's [theme](/config/environment) flavor. With the default `system` flavor, Harlequin stays Catppuccin Mocha with its own background, because it refuses Textual's terminal theme.

To choose another theme, set `theme` in a profile or pass `--theme`. The command-line option wins over the profile.

## Versions

Harlequin and its PostgreSQL adapter come from the catalog's NixOS package set. The module has no version lines and no settings of its own. `harlequin --version` shows the installed application and adapters.
