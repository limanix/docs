---
description: Install the Google Cloud CLI in a LimaNix VM and sign in from inside the VM.
---

# Google Cloud CLI

The Google Cloud CLI module installs `gcloud`, together with `gsutil`, `bq` and `gke-gcloud-auth-plugin`.

## Enable the CLI

Add `lmx:gcloud` to the modules in `limanix.toml`:

::: code-group

```toml [limanix.toml]
[nixos]
modules = ["lmx:gcloud"]
```

:::

Apply the change from your Mac. The update restarts the VM; see [Changing a VM](/vms/update).

::: code-group

```sh [Mac]
limanix update --config limanix.toml
```

:::

## Sign in and choose a project

Credentials on your Mac are not copied into the VM. Sign in inside the VM with your organization's approved method, such as `gcloud auth login`, then set the project:

::: code-group

```sh [VM]
gcloud auth login
gcloud config set project PROJECT_ID
```

:::

Check the active account and project before you run project commands:

::: code-group

```sh [VM]
gcloud config list
gcloud auth list
```

:::

Application Default Credentials are separate from the CLI's own sign-in. Set them up when your application needs them:

::: code-group

```sh [VM]
gcloud auth application-default login
```

:::

If the CLI works but an application fails, check how that application gets its credentials, such as through ADC. `lmx help gcloud` shows these commands in the VM.

## Configuration and credentials

The CLI keeps its configuration and credentials in `~/.config/gcloud/`, in your home. The home is stored on the Mac and survives `limanix delete`; `limanix delete --remove-home` removes the credentials with it. See [Files and storage](/vms/storage).

`CLOUDSDK_CONFIG` selects another configuration directory. To use one from your Mac, [share it with the VM](/config/mounts) and set `CLOUDSDK_CONFIG` to its path in [`[env]`](/config/environment). Keep the credentials themselves out of `[env]` and out of Nix modules.

## Versions

The CLI comes from the catalog's nixos-unstable package set, which carries the newest releases. The module has no version lines: a newer CLI arrives with a newer catalog. Check the installed version:

::: code-group

```sh [VM]
gcloud version
```

:::

## Limits

- Nix manages the CLI and its components. Add a missing component through [a module of your own](/modules/custom); the files of installed packages are read-only.
- The module has no settings of its own. Use the CLI's own configurations.
- The module adds no services and creates no cloud resources.
