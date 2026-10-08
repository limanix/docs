# LimaNix documentation

[![License: Apache-2.0](https://img.shields.io/github/license/limanix/docs?label=license)](LICENSE)

<p align="center">
  <img src=".github/assets/readme-header.png"
       alt="LimaNix documentation"
       width="100%">
</p>

The documentation site for [LimaNix](https://github.com/limanix/client), which
runs Linux development environments on macOS. This repository builds and
publishes [limanix.dev](https://limanix.dev) using Sphinx.

It owns the shared pages, theme, navigation and publication infrastructure.
Client and module guides live in their own repositories; this repository
assembles them with the shared pages into one site.

[Documentation](https://limanix.dev) |
[Release process](docs/pages/releases/index.md) |
[Releases](https://github.com/limanix/docs/releases)

## Get started

Local builds require [Task](https://taskfile.dev) 3.53.1 or newer and Docker
with a running engine. Keep the `client`, `modules`, `lmx` and `docs` checkouts
side by side. From the `docs` checkout, build and preview the complete site:

```console
task --yes ci/static/build CLIENT_ROOT=../client MODULES_ROOT=../modules LMX_ROOT=../lmx
task --yes docs/serve CLIENT_ROOT=../client MODULES_ROOT=../modules LMX_ROOT=../lmx
```

The build writes HTML to `build/docs`. Open <http://127.0.0.1:8040> for the
preview, which rebuilds when shared pages or product sources change. Omit all
product inputs to build or preview only the shared pages. See
[Build and preview documentation locally](docs/pages/releases/workflow.md) for
prepared documentation inputs and local checks.

## Documentation

| Guide | Contents |
| -- | -- |
| [Overview](docs/pages/index.md) | Product introduction and routes into the client and module guides. |
| [Comparison](docs/pages/comparison.md) | Development workflows and trade-offs compared with other tools. |
| [Release process](docs/pages/releases/index.md) | Repository responsibilities and the path from a contribution to publication. |
| [Release workflow](docs/pages/releases/workflow.md) | Local checks, release paths and documentation publication. |
| [Versioning](docs/pages/releases/versioning.md) | Client versions, catalog rebuilds and docs tags. |

The assembled site includes the
[client guides](https://limanix.dev/categories/client/index.html) and
[module documentation](https://limanix.dev/categories/nixos/index.html).

## Contributing

Follow the
[contribution guide](https://github.com/limanix/.github/blob/main/CONTRIBUTING.md)
when changing the documentation. Edit client guides and reference definitions in
[client](https://github.com/limanix/client), and module guides and references in
[modules](https://github.com/limanix/modules).

Shared pages live in [docs/pages/](docs/pages/), Sphinx configuration in
[docs/conf.py](docs/conf.py), and styles and page scripts in
[docs/\_static/](docs/_static/). See [Taskfile.yml](Taskfile.yml) for local
checks, build inputs and preview settings. Use
[Issues](https://github.com/limanix/docs/issues) for questions, bug reports and
feature requests.

<details>
<summary>Code walkthroughs</summary>

For Nix and TOML line-by-line examples, use a MyST `code-block` or
`literalinclude` with `:linenos:`, a unique `:name:`, and
`:class: code-example`. Link table cells to line ranges with
`[2–5](#example-name.2-5){.external .code-lines}` and use `Code` as the column
heading. The bundled Prism plugins highlight the linked range; the `external`
class preserves the fragment for the browser.

</details>

Licensed under [Apache 2.0](LICENSE).
