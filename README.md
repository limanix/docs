# LimaNix documentation

[![License: Apache-2.0](https://img.shields.io/github/license/limanix/docs?label=license)](LICENSE)

<p align="center">
  <img src=".github/assets/readme-header.png"
       alt="LimaNix documentation"
       width="800">
</p>

This repository builds and publishes [limanix.dev](https://limanix.dev).
It owns the shared pages, theme, navigation, and publication infrastructure.
Client and module guides live in their own repositories.
This repository assembles them with the shared pages.

[Site](https://limanix.dev) ·
[Release process](https://limanix.dev/releases/index.html) ·
[Client](https://github.com/limanix/client) ·
[Modules](https://github.com/limanix/modules)

## Where to edit

| Content                                         | Edit in                                                                              |
|-------------------------------------------------|--------------------------------------------------------------------------------------|
| Client guides, CLI and configuration references | [`client`](https://github.com/limanix/client): `guides/` and the source definitions  |
| Module guides and module pages                  | [`modules`](https://github.com/limanix/modules): `guides/` and `catalog/*/README.md` |
| Home page, release process, theme, navigation   | This repository: `docs/pages/`, `docs/conf.py`, and `docs/_static/`                  |

Client and module pages reach the site with the next release of their repository.
Changes in this repository reach the site with the next docs tag.

## Repository layout

| Path                            | Contents                                                       |
|---------------------------------|----------------------------------------------------------------|
| `docs/pages/`                   | Shared pages: the home page and the release process            |
| `docs/conf.py`, `docs/_static/` | Sphinx configuration, styles, and page scripts                 |
| `scripts/build_docs.py`         | Combines the shared pages with prepared client and module docs |
| `scripts/releases.py`           | Selects the versions to build and the files to upload          |
| `tf/`                           | The S3 bucket and CloudFront distribution that serve the site  |
| `.github/workflows/`            | PR checks, docs releases, and client release events            |

## Build and preview

Run from this repository with [Task](https://taskfile.dev) and Docker available:

```bash
task --yes ci/static-build
task --yes ci/static-build CLIENT_ROOT=../client MODULES_ROOT=../modules
task --yes docs/serve CLIENT_ROOT=../client MODULES_ROOT=../modules
```

`ci/static-build` without product inputs builds the shared pages, as in the docs PR workflow.
With both products, it includes client guides, generated CLI and configuration references, module guides, and module READMEs.
`docs/serve` rebuilds when the shared pages or product sources change.
Open <http://127.0.0.1:8040>, or set `DOCS_PORT` to use another port.

Choose one input for each product:

| Input          | Accepted value                                 |
|----------------|------------------------------------------------|
| `CLIENT_ROOT`  | Client checkout; runs its `docs/prepare` task  |
| `CLIENT_DOCS`  | Prepared client directory or `docs.tar.gz`     |
| `MODULES_ROOT` | Modules checkout; runs its `docs/prepare` task |
| `MODULES_DOCS` | Prepared modules directory or `docs.tar.gz`    |

Prepared inputs must contain `index.md` at their root.
For example:

```bash
task --yes ci/static-build CLIENT_ROOT=../client MODULES_DOCS=../modules/build/docs
task --yes ci/static-build CLIENT_DOCS=build/inputs/client/docs.tar.gz MODULES_DOCS=build/inputs/modules/docs.tar.gz
```

`DOCS_OUTPUT` defaults to `build/docs`.
Other output directories must also be under `build/`.
With `MODULES_ROOT`, source links use the modules checkout's commit SHA.
Set `MODULES_REF=v2` to point them at a published tag instead.
Uncommitted documentation edits still appear in the local build.

Client pages appear under `/categories/client/`.
NixOS guides appear under `/categories/nixos/`.
Module READMEs appear under `/categories/nixos/modules/`.
Links between those guides stay within the selected site version.

## Checks

```bash
task --yes ci/terraform-fmt ci/terraform-validate ci/static-test ci/static-audit
```

See [Taskfile.yml](Taskfile.yml) for the complete task list.
The PR workflow runs the Terraform and static checks through reusable workflows.
It also builds the site and combines the results in `gate`.
The Terraform plan uses the repository's AWS role and configured state variables.

## Publication

| Trigger              | Sources                                                              | Published result                            |
|----------------------|----------------------------------------------------------------------|---------------------------------------------|
| Docs PR              | Current shared pages                                                 | Build check only                            |
| Docs tag             | Tagged docs commit and highest completed client/modules pair, if any | Site infrastructure and current site at `/` |
| Client release event | Deployed docs commit and the published client/modules pairs          | Client archives and updated current site    |

`release.yml` and `events.yml` use `_select.yml`, `_build.yml`, and `_publish.yml`.
These workflows select sources, build the site, and publish it.
`scripts/releases.py` decides which versions to build and which archives and catalog to upload.
The workflows transfer the selected files.
Release builds download the products' prepared documentation from GitHub Releases.
The version switcher links the current site and saved client versions under `/client/<tag>/`.
Existing archives stay unchanged.

See the [release guide](docs/pages/releases/index.md) for the path from product changes to published documentation.

## Code walkthroughs

For line-by-line examples, use a standard MyST `code-block` or `literalinclude` with `:linenos:`, a unique `:name:`, and `:class: code-example`.
Nix and TOML walkthroughs use the bundled Prism 1.30.0 Line Numbers and Line Highlight plugins.
Link a table cell to a range with `[2–5](#example-name.2-5){.external .code-lines}`.
Use `Code` as the column heading.
The site displays each link as a code icon with its line range in a tooltip and an accessible label.
The Markdown source keeps the line numbers.
The `external` class tells MyST to leave the fragment for Prism to resolve in the browser.
The fragment still links within the current page.
Clicking the link highlights the entire range.
The fragment preserves the highlight when the URL is reopened.
Ordinary code blocks retain the site's standard rendering.

Licensed under [Apache 2.0](LICENSE).
