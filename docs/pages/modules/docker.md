---
description: Run Docker Engine, Compose and Lazydocker inside a LimaNix VM.
---

# Docker

The Docker module runs Docker Engine as a system service in the VM. It adds the Docker CLI, the Compose plugin and Lazydocker, and lets your VM user run Docker without `sudo`.

## Enable Docker

Add `lmx:docker` to the modules in `limanix.toml`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:docker"]
```

:::

Apply the change from your Mac. The update restarts the VM; see [Changing a VM](/vms/update).

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

## Run containers

Check that Docker Engine runs:

::: code-group

```sh [VM]
docker ps
```

:::

The command lists running containers. An empty list is normal before you start any.

Run `lazydocker` for a terminal interface to containers, logs, images and volumes. `lmx help docker` lists the module's commands and common tasks.

## Run a Compose project

[Share the project's directory](/config/mounts) with the VM. Then run this in the VM, from the directory that contains the Compose file:

::: code-group

```sh [VM]
docker compose up -d
```

:::

## Reach a container from your Mac

`docker run -p 8080:80 IMAGE` publishes the container's port 80 on port 8080 of the VM. From your Mac, connect to the VM's address and that port. [Network](/vms/network) shows how to find the address.

Docker manages the firewall rules for published ports itself:

- A published port is reachable without adding it to `network.ports` in `limanix.toml`.
- Removing a port from `network.ports` does not close a published port.
- To keep a port inside the VM, publish it on the loopback address: `docker run -p 127.0.0.1:8080:80 IMAGE`.

Compose `ports:` entries behave the same way. A container started with `--network host` uses the VM's network directly, and `network.ports` applies to it as to any other service in the VM. Docker's guides cover [port publishing](https://docs.docker.com/engine/network/port-publishing/) and [firewall rules](https://docs.docker.com/engine/network/firewall-iptables/).

## Permissions

The module adds your VM user to the `docker` group. Docker commands then work without `sudo`.

::: warning
Membership in the `docker` group is equivalent to root access in the VM.
:::

## Versions

| Selector                      | Docker Engine and CLI | Notes       |
| ----------------------------- | --------------------- | ----------- |
| `lmx:docker`, `lmx:docker-29` | 29.x                  | Default     |
| `lmx:docker-28`               | 28.5.2                | End of life |

Lines marked `.x` come from the catalog's NixOS package set and get its patch releases with each catalog release. Support status follows [Moby's branch maintenance table](https://github.com/moby/moby/blob/master/project/BRANCHES-AND-TAGS.md). The end-of-life line prints a warning when the VM builds: `Docker Engine 28.5.2 no longer receives upstream security updates.`

Select one line per VM. Two lines stop the build with `docker: select one line`. Both lines keep containers, images and volumes in the same storage; switching lines does not create a separate Docker environment.

## Data and settings

| What                           | Where                                                                                   |
| ------------------------------ | --------------------------------------------------------------------------------------- |
| Images, containers and volumes | `/var/lib/docker` on the guest disk                                                     |
| Service                        | `docker.service`                                                                        |
| Settings                       | Standard `virtualisation.docker.*` NixOS options, in [your own module](/modules/custom) |

The module has no settings of its own. Deleting the VM deletes the guest disk and the Docker volumes on it; see [Files and storage](/vms/storage).
