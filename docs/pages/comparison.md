# How LimaNix compares

LimaNix gives each project its own Linux virtual machine. A TOML file in the
project describes the VM, and NixOS modules from the catalog install its tools
and services. Several other tools cover part of this ground. Compare their
workflows and trade-offs to choose a setup for your project.

```{note}
Reviewed in September 2026.
The other projects change quickly; check their documentation for current details.
```

## At a glance

| Tool | Where your tools run | How you describe the environment | Nix on the Mac | License |
| -- | -- | -- | -- | -- |
| LimaNix | A separate NixOS VM for each environment | A TOML file with modules from the catalog | Not needed | Apache-2.0 |
| [OrbStack](https://orbstack.dev) | Linux machines that share one lightweight VM and kernel | A distribution image, then setup scripts or [cloud-init](https://docs.orbstack.dev/machines/cloud-init) | Not needed | [Proprietary; free for personal use, paid for commercial use](https://docs.orbstack.dev/licensing) |
| [Colima](https://github.com/abiosoft/colima) | In Linux containers or directly in the Lima VM | Command-line flags or YAML with optional provisioning scripts | Not needed | MIT |
| [Devbox](https://www.jetify.com/devbox) | A native project shell on macOS | `devbox.json` with Nixpkgs packages | Installed automatically when missing | Apache-2.0 |
| [devenv](https://devenv.sh) | A native project shell on macOS | `devenv.nix`, written in the Nix language | Required | Apache-2.0 |
| [Lima](https://lima-vm.io) | A Linux VM of any supported distribution | A YAML template with shell provisioning scripts | Not needed | Apache-2.0 |

## OrbStack

OrbStack is a macOS app for Docker, Kubernetes, and Linux machines, including
[NixOS](https://docs.orbstack.dev/machines/distros). Its machines
[share one lightweight VM and kernel](https://docs.orbstack.dev/architecture).
They do not have
[the same isolation boundary as separate VMs](https://docs.orbstack.dev/machines/isolated#security-model).
A NixOS machine starts from the stock image, and you configure it inside the
machine with your own Nix code.

Choose OrbStack when you mainly need Docker or quick Linux machines, and its
license fits your use. Choose LimaNix when you want a separate NixOS VM
configured from project TOML and the module catalog. The
[catalog is bundled with the client](https://limanix.dev/categories/client/modules.html);
sharing TOML alone does not lock its version. Use the same LimaNix build across
Macs and import the same sources for any custom modules.

## Colima

Colima starts a Lima VM with Docker, containerd, or Incus and connects the
container tools on your Mac to it. Development tools can run in its containers
or be installed directly in the VM using
[provisioning scripts](https://github.com/abiosoft/colima/blob/main/embedded/defaults/colima.yaml).

Choose Colima when your workflow is built around containers. Choose LimaNix when
you want to select development tools and system services from a NixOS module
catalog. The `lmx:docker` module adds Docker to the same environment.

## Devbox and devenv

Devbox and devenv use Nix to install pinned tools into a project shell. Their
native macOS workflow runs directly on the Mac, without a VM. Both can also run
services, such as PostgreSQL, beside the project. Devbox describes environments
in JSON and
[installs Nix for you](https://www.jetify.com/docs/devbox/installing-devbox);
devenv uses the Nix language and
[requires Nix](https://devenv.sh/getting-started/).

When run natively on macOS, the tools they install are macOS builds, and
Linux-only packages cannot run directly. When a project targets Linux, their
behavior can differ from CI and production. For container workflows, see
[Devbox Dev Containers](https://www.jetify.com/docs/devbox/cli-reference/devbox-generate-devcontainer)
and [devenv containers](https://devenv.sh/containers/). LimaNix runs Linux
builds of your tools in a NixOS VM, and the Mac does not need Nix.

Choose Devbox or devenv when your tools work well on macOS and you want the
lightest setup. Choose LimaNix when you want tools and system services
configured together inside a separate NixOS VM.

## Lima

LimaNix embeds Lima. You do not install Lima separately. Lima runs many
distributions from [YAML templates](https://lima-vm.io/docs/config/) and
provisions them with shell scripts. LimaNix fixes the guest to NixOS and
replaces those scripts with modules. `limanix update` rebuilds the guest from
the configuration instead of running setup commands again. LimaNix also sets up
shared networking and a managed home directory that is preserved when you delete
the VM.

Choose Lima when you need another distribution or full control over the VM
template.

## Trade-offs

- A full VM for each environment uses more memory and disk than a shell or a
  shared-kernel machine.
- `limanix update` restarts the VM to apply the new configuration.
- The current client requires macOS 26 or newer; see
  [Getting started](https://limanix.dev/categories/client/getting-started.html#install-the-client).
- The [catalog](https://limanix.dev/categories/nixos/catalog.html) covers common
  toolchains; for other software,
  [write a module](https://limanix.dev/categories/nixos/writing-modules.html).
- LimaNix is a young project, and early releases can change behavior between
  versions.
