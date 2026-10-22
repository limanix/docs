---
description: Install PostgreSQL in a LimaNix VM, run a server and connect to it from the VM or your Mac.
---

# PostgreSQL

The PostgreSQL module installs the PostgreSQL server and its command-line tools. It creates no database and starts no service: you choose where the data lives and when the server runs.

## Enable PostgreSQL

Add `lmx:postgres` to the modules in `limanix.toml`, then apply the change from your Mac. The update restarts the VM.

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:postgres"]
```

:::

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

`lmx help postgres` in the VM lists the installed commands and common tasks.

## Versions

| Selector                          | PostgreSQL | Notes   |
| --------------------------------- | ---------- | ------- |
| `lmx:postgres`, `lmx:postgres-18` | 18.x       | Default |
| `lmx:postgres-17`                 | 17.x       |         |
| `lmx:postgres-16`                 | 16.x       |         |

Each line adds its commands with the version as a suffix, such as `initdb-18`, `pg_ctl-18`, `psql-18`, `createdb-18`, `pg_dump-18` and `pg_config-18`. Commands without a suffix, such as `psql`, come from the newest selected line. Support dates are in the [PostgreSQL versioning policy](https://www.postgresql.org/support/versioning/).

To install several lines side by side, select each of them, for example `modules = ["lmx:postgres-16", "lmx:postgres-18"]`. Give each running server its own data directory, socket directory and, with TCP, port.

## Run a server

In the VM, choose a data directory and a socket directory, then create the instance. Run `initdb` only once per instance.

::: code-group

```sh [VM]
pg_root="$HOME/.local/share/postgresql/18"
pg_socket="$XDG_RUNTIME_DIR/postgresql-18"
mkdir -p "$pg_root"
initdb-18 -D "$pg_root/data" --auth-local=peer --auth-host=scram-sha-256
```

:::

`initdb` creates a database superuser with your VM user's name and a database named `postgres`. The data lives in your home, which LimaNix keeps on the Mac.

Before the first start, open `$pg_root/data/postgresql.conf` and replace the line `#listen_addresses = 'localhost'` with `listen_addresses = ''`. This turns off TCP connections. Keep this single active `listen_addresses` line: PostgreSQL uses the last one, and the steps below edit it.

Start the server and connect through its Unix socket:

::: code-group

```sh [VM]
mkdir -p "$pg_socket"
pg_ctl-18 -D "$pg_root/data" -l "$pg_root/server.log" -o "-k '$pg_socket'" start
psql-18 -h "$pg_socket" -d postgres
```

:::

`psql` signs you in as your Linux user through the socket, without a password or `sudo`. Type `\q` to leave it. To create a database for your app, run `createdb-18 -h "$pg_socket" app`.

Stop the server when you are done; the data stays:

::: code-group

```sh [VM]
pg_ctl-18 -D "$pg_root/data" stop
```

:::

In a new shell, set `pg_root` and `pg_socket` again. After the VM restarts, run `mkdir -p "$pg_socket"` and the start command again.

Server settings, such as `listen_addresses`, `port` and memory limits, live in `postgresql.conf`. `pg_hba.conf`, in the same directory, decides which connections are allowed and how they authenticate. After changing authentication rules, run `pg_ctl-18 -D "$pg_root/data" reload`. A change to `listen_addresses`, `port` or the socket directory needs a stop and a start.

## Connect from your Mac

`localhost:5432` on the Mac does not reach PostgreSQL in the VM. Connect to the VM's address instead:

1. In `postgresql.conf`, set the active line to `listen_addresses = '*'` and set `port = 5432`, removing the leading `#` if needed.
2. In `limanix.toml`, add `5432` to `tcp` under `[network.ports]`, keeping the ports you already list. Run `limanix update --config limanix.toml`.
3. After the VM restarts, start the server again. Connect through the socket and run `\password` to give your role a password.
4. Add the line `host all all MAC_IP/32 scram-sha-256` to `pg_hba.conf`, keeping the existing rules, and reload the server.

`MAC_IP` is the Mac's address as the VM sees it, not the VM's address. If you don't know it, run the connection command below once without `-W`: the error `no pg_hba.conf entry for host "..."` names it. Update the rule if that address changes.

On the Mac, read the VM's address in the `ADDRESS` column of `limanix list`. Connect with `psql` installed on the Mac and the VM user's name, which can differ from your Mac username:

::: code-group

```sh [Mac]
psql -h <guest-ip> -p 5432 -U <vm-user> -d postgres -W
```

:::

A graphical client uses the same host, port, user, database and password. If the connection fails, run `limanix network check dev-box 5432`; see [Network](/vms/network).

## Run as a system service

To have NixOS create the database and start PostgreSQL at boot, enable the service in [a module of your own](/modules/custom). Save this one on the Mac. It creates a database and a role named after your VM user, and accepts connections only from inside the VM:

::: code-group

```nix [modules/postgres-service/default.nix]
{ config, pkgs, ... }:
{
  services.postgresql = {
    enable = true;
    package = pkgs.postgresql_18;
    ensureDatabases = [ config.limanix.user.name ];
    ensureUsers = [
      {
        name = config.limanix.user.name;
        ensureDBOwnership = true;
      }
    ];
  };
}
```

:::

Import it with `limanix modules add postgres-service ./modules/postgres-service`, add `third-party:postgres-service` to `[nixos] modules` and update the VM. Then check the service and connect:

::: code-group

```sh [VM]
systemctl status postgresql
psql -h /run/postgresql -d "$(id -un)"
```

:::

The service keeps its data in `/var/lib/postgresql/<major>` on the guest disk, separate from a manual instance; `limanix delete` removes it with the disk. For another major version, change `pkgs.postgresql_18` to `pkgs.postgresql_17` or `pkgs.postgresql_16`. The service installs its own PostgreSQL: select `lmx:postgres` as well only for the versioned commands. Commands without a suffix then come from the newest selected line, whatever version the service runs.

For access from the Mac, add these lines to `services.postgresql` and [import the module again](/modules/custom#change-an-imported-module). Then open the port as in step 2, set a password as in step 3, and connect with your VM user's name as the database.

::: code-group

```nix [modules/postgres-service/default.nix]
enableTCPIP = true;
authentication = ''
  host all all MAC_IP/32 scram-sha-256
'';
```

:::

## Limits

- The module itself has no settings. A service takes the standard `services.postgresql.*` options, such as `dataDir`, `settings` and `authentication`.
- Run a data directory with the major version that created it. Selecting another line does not migrate data; moving it needs a [PostgreSQL upgrade](https://www.postgresql.org/docs/18/upgrading.html). Changing the service's major version starts a new instance and does not migrate the old databases.
- To build client bindings, `pg_config-18 --includedir` and `pg_config-18 --libdir` show the line's paths. Choose your compiler or SDK separately.
