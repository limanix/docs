# From pull request to release

Open your PR against `main` in the repository that owns the change.
Update its guides when behavior changes.

(pull-request-checks)=
## Before merge

| Repository | What `gate` includes |
|------------|----------------------|
| `client` | Shared Go checks and native builds for Intel and Apple Silicon |
| `modules` | Shared Nix checks and NixOS configuration evaluation for both architectures |
| `docs` | Python formatting, lint, tests, and a strict Sphinx build of the shared pages |

Label validation runs separately from `gate` in each repository.
The modules workflow also reports available Nixpkgs updates; that report is outside `gate`.

<details>
<summary>Run client checks locally</summary>

From `client`, with Task and Docker available:

```bash
task --yes ci/fmt ci/lint ci/test ci/vuln modules_version=v4
```

Replace `v4` with the published module catalog tag you want to test.
Tests and native builds require an explicit `modules_version`.

The native build also needs macOS, Go, and the Xcode command-line tools:

```bash
task --yes ci/build modules_version=v4
```

It builds and ad hoc signs both macOS binaries.

</details>

<details>
<summary>Run module checks locally</summary>

From `modules`, with Task and Docker available:

```bash
task --yes ci/fmt ci/lint ci/test
```

The checks validate catalog metadata and evaluate NixOS configurations.
Evaluation does not build packages or boot a VM.

</details>

(check-documentation-changes)=
<details>
<summary>Build and preview documentation locally</summary>

From `docs`, with Task and Docker available:

```bash
task --yes ci/fmt ci/lint ci/test
task --yes ci/static-build
```

`ci/static-build` builds the shared pages, matching the docs PR check.
To include the product guides, point to the sibling repositories:

```bash
task --yes ci/static-build CLIENT_ROOT=../client MODULES_ROOT=../modules
task --yes docs/serve CLIENT_ROOT=../client MODULES_ROOT=../modules
```

Open <http://127.0.0.1:8040> for the preview.
The preview rebuilds when shared pages or product sources change.
Client preparation includes the generated CLI and configuration references.

To use prepared pages, replace either root input with `CLIENT_DOCS` or `MODULES_DOCS`, pointing to a directory or `docs.tar.gz`.
Pass one client input together with one module input.
Release builds use the documentation archives published with those products.

</details>

New commits rerun PR checks; changing labels reruns label validation.
Client and modules PR workflows do not run the combined Sphinx build.

(release-paths)=
## After merge

| Change | Release trigger | Result |
|--------|-----------------|--------|
| Client code | Client tag such as `v1.3.0` | A client release using the selected published catalog |
| Module code or metadata | Modules tag such as `v7` | A catalog release, then rebuilds of selected client versions |
| Shared documentation | Docs tag such as `v1.0.0` | Updated site infrastructure and current documentation |

<details>
<summary>Follow a client code release</summary>

1. `release.yml` selects the latest published module tag matching `vN`.
2. `_publish.yml` builds the client at the tagged commit, prepares its documentation, and publishes the binaries and `docs.tar.gz` in a GitHub Release.
3. `_notify.yml` sends the client and modules tags to docs after publication succeeds.

Other client versions are not rebuilt by this path.
Tags containing `+` do not trigger another client code release.

</details>

<details>
<summary>Follow a module catalog release</summary>

1. The modules workflow validates the `vN` tag and checks that its commit belongs to `main`.
2. It prepares the documentation and publishes `docs.tar.gz` in the catalog's GitHub Release.
3. It sends a `modules-release` event to `client`, with the modules tag in `client_payload.tag`.
4. The client's `events.yml` validates that tag's format and selects [the configured number of client versions](supported-client-versions).
5. Each selected client is rebuilt at its existing commit with the new catalog and the next `+N` suffix.

For example, with `RELEASE_COUNT=3`, a `v7` catalog release can produce:

| Selected client | New client release | Included modules |
|-----------------|--------------------|------------------|
| `v1.3.0` | `v1.3.0+1` | `v7` |
| `v1.2.4+10` | `v1.2.4+11` | `v7` |
| `v1.2.3+4` | `v1.2.3+5` | `v7` |

The builds run in parallel.
If one fails, the other builds continue; docs notification runs only after the complete matrix succeeds.
Sending the same modules event again selects clients again and increments their rebuild counters.

</details>

<details>
<summary>Follow a shared documentation release</summary>

1. The docs workflow validates its tag and checks that its commit belongs to `main`.
2. It combines the tagged shared pages and theme with the highest completed client documentation version and its modules tag.
3. It applies the site infrastructure and publishes the current site at `/`.

If no product documentation has been published yet, the release builds shared pages only.
Existing client archives stay unchanged.

</details>

(notify-docs)=
## What happens after the client builds?

Each client GitHub Release records its source commit and a **Module catalog** link identifying the bundled catalog.
After a successful single release or complete rebuild matrix, `_notify.yml` sends the published pairs to `docs` in one `client-release` event.

<details>
<summary>See an event for two client releases</summary>

```json
{
  "event_type": "client-release",
  "client_payload": {
    "releases": [
      {"client_tag": "v1.3.0+1", "modules_tag": "v7"},
      {"client_tag": "v1.2.4+11", "modules_tag": "v7"}
    ]
  }
}
```

</details>

(published-documentation)=
## When does your documentation appear?

The docs workflow combines each client's `docs.tar.gz` with the documentation archive from its paired modules release.
Shared pages and the theme come from the deployed docs release.
Client events therefore need an initial docs release.

| Address | Content |
|---------|---------|
| `/` | Current complete site, updated by docs tags and client events |
| `/client/` | Redirect to `/` |
| `/client/v1.3.0+1/` | Saved site for that client release and its catalog |

The current site uses the highest client version among completed archives and the incoming pairs.
Each site includes shared pages, client guides, module guides, and generated references in one navigation and search.

The version switcher shows both tags, for example **v1.3.0+1 · modules v7**.
Its current entry opens `/`; older entries open their archives.
Existing archives retain the shared pages, theme, and product versions they were built with.
The client rebuild limit does not remove older documentation.

Merging a docs PR does not change the shared pages used by client events.
A docs release makes those changes available to the current site and later archives.

## Follow the result

For missing product changes, check the matching client or modules release first, then the docs workflow run.
A successful notification confirms that the event was sent; it does not prove that documentation was published.

| What failed | What to check |
|-------------|---------------|
| Client selection | The `clients` job in the client's event workflow |
| A client build or publication | The failed matrix job; other client releases may have completed |
| Docs notification | The client's `notify` job; published releases remain available |
| A docs build | The failed build job; publication waits for all builds |
| Documentation publication | The docs publication job; earlier uploads may remain |

Include the repository, run link, tag, and failed job when reporting a problem.

<details>
<summary>Find the workflow</summary>

All files are under `.github/workflows/` in the corresponding repository.

| Repository | Files | Purpose |
|------------|-------|---------|
| All three | `pr.yml`, `labels.yml` | PR checks and label validation |
| `client` | `release.yml`, `events.yml` | Client tags and module events |
| `client` | `_build.yml`, `_publish.yml`, `_notify.yml` | Build clients, publish releases, and notify docs |
| `modules` | `release.yml` | Publish the catalog and notify client |
| `docs` | `release.yml`, `events.yml` | Docs tags and client events |
| `docs` | `_select.yml`, `_build.yml`, `_publish.yml` | Select sources, build the site, and publish it |

</details>
