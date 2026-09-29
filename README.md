# LimaNix documentation

This repository builds and publishes the combined Sphinx site.
It owns the shared pages, theme, navigation, and S3 publication.
The client and modules repositories prepare their own documentation and publish it as `docs.tar.gz` release assets.

## Build and preview

Run from this repository with Task and Docker available:

```bash
task --yes ci/fmt ci/lint ci/test
task --yes ci/static-build
task --yes ci/static-build CLIENT_ROOT=../client MODULES_ROOT=../modules
task --yes docs/serve CLIENT_ROOT=../client MODULES_ROOT=../modules
```

`ci/static-build` without product inputs builds the shared pages, as in the docs PR workflow.
With both products, it also includes client guides, generated CLI and configuration references, module guides, and module READMEs.
`docs/serve` rebuilds when the shared pages or product sources change.
Open <http://127.0.0.1:8040>, or set `DOCS_PORT` to use another port.

Choose one input for each product:

| Input | Accepted value |
|-------|----------------|
| `CLIENT_ROOT` | Client checkout; runs its `docs/prepare` task |
| `CLIENT_DOCS` | Prepared client directory or `docs.tar.gz` |
| `MODULES_ROOT` | Modules checkout; runs its `docs/prepare` task |
| `MODULES_DOCS` | Prepared modules directory or `docs.tar.gz` |

Prepared inputs must contain `index.md` at their root.
For example:

```bash
task --yes ci/static-build CLIENT_ROOT=../client MODULES_DOCS=../modules/build/docs
task --yes ci/static-build CLIENT_DOCS=build/inputs/client/docs.tar.gz MODULES_DOCS=build/inputs/modules/docs.tar.gz
```

`DOCS_OUTPUT` defaults to `build/docs`; other output directories must also be under `build/`.
With `MODULES_ROOT`, source links use the modules checkout's commit SHA; set `MODULES_REF=v3` to point them at a published tag instead.
Uncommitted documentation edits still appear in the local build.

Client pages appear under `/categories/client/`, NixOS guides under `/categories/nixos/`, and module READMEs under `/categories/nixos/modules/`.
Links between those guides stay within the selected site version.

## Publication

| Trigger | Sources | Published result |
|---------|---------|------------------|
| Docs PR | Current shared pages | Build check only |
| Docs tag | Tagged docs commit and highest completed client/modules pair, if any | Site infrastructure and current site at `/` |
| Client release event | Deployed docs commit and the published client/modules pairs | Client archives and updated current site |

`release.yml` and `events.yml` use `_select.yml`, `_build.yml`, and `_publish.yml` to select sources, build the site, and publish it.
`scripts/releases.py` decides which versions to build and which archives and catalog to upload; the workflows only transfer files.
Release builds download the products' prepared documentation from GitHub Releases.
The version switcher links the current site and saved client versions under `/client/<tag>/`.
Existing archives stay unchanged.

See the [release guide](docs/pages/releases/index.md) for the paths from product changes to published documentation.

## Code walkthroughs

For examples explained line by line, use a standard MyST `code-block` or `literalinclude` with `:linenos:`, a unique `:name:`, and `:class: code-example`.
Nix and TOML walkthroughs use the bundled Prism 1.30.0 Line Numbers and Line Highlight plugins.
Link a table cell to a range with `[2–5](#example-name.2-5){.external .code-lines}`.
Use `Code` as the column heading.
The site displays each link as a code icon, with its line range in a tooltip and an accessible label; the Markdown source keeps the numbers.
The `external` class tells MyST to leave the fragment for Prism to resolve in the browser; it still links within the current page.
Clicking the link highlights the entire range, and the fragment preserves it when the URL is reopened.
Ordinary code blocks retain the site's standard rendering.
