# From pull request to release

Open your PR against `main` in the repository that owns the change.
Update its guides when behavior changes.

(pull-request-checks)=
## Before merge

| Repository | Automated checks | What `gate` includes |
|------------|------------------|----------------------|
| `client` | Go formatting, lint, race tests, vulnerability scan, then macOS builds for Intel and Apple Silicon | Go checks and both native builds |
| `modules` | Nix formatting, lint, catalog validation, and NixOS configuration evaluation | Nix checks and the PR label check |
| `docs` | Sphinx build of the shared pages, with warnings treated as errors | Documentation build |

Every repository checks that the PR has at least one label.
The current check accepts any label; it does not choose the release version.
In `client` and `docs`, labels run separately from `gate`.

<details>
<summary>Run client checks locally</summary>

From the `client` repository, with Task and Docker available:

```bash
task --yes ci/fmt ci/lint ci/test ci/vuln
```

The native build also needs macOS, Go, and the Xcode command-line tools:

```bash
task --yes ci/build
```

It builds and ad hoc signs both macOS binaries.

</details>

<details>
<summary>Run module checks locally</summary>

From the `modules` repository, with Task and Docker available:

```bash
task --yes ci/fmt ci/lint ci/test
```

The checks validate catalog metadata and evaluate NixOS configurations for both supported architectures.
They cover individual modules, module combinations, and declared versions.
Evaluation does not build packages or boot a VM.

</details>

(check-documentation-changes)=
<details>
<summary>Build and preview documentation locally</summary>

Run these commands from the `docs` repository, with Task and Docker available.

**Shared pages only**, matching the docs PR check:

```bash
task --yes ci/docs
```

**Include product guides**, with `client` and `modules` checked out beside `docs`:

```bash
task --yes ci/docs DOCS='../client ../modules'
task --yes docs/serve DOCS='../client ../modules'
```

Open <http://127.0.0.1:8040> for the preview.
The `DOCS` paths point to repository roots; their `docs/` directories are mounted read-only into the build.
No guide files are copied into the docs repository.

This preview includes handwritten guides.
The release build also generates the CLI and configuration references for its exact client and modules versions.
Client and modules PR workflows do not run this Sphinx build.

</details>

A failed, cancelled, or skipped dependency does not pass `gate`.
New commits rerun PR checks; changing labels reruns the label check.
In `modules`, a label change also reruns the Nix checks.

(release-paths)=
## After merge

| Change | Release trigger | Result |
|--------|-----------------|--------|
| Client code | Client tag such as `v1.3.0` | One client release using that commit's catalog pin |
| Module code or metadata | Modules tag such as `v7` | Catalog release, then rebuilds of up to three client base versions |
| Shared documentation | Docs tag such as `v1.0.0` | Updated shared pages and site infrastructure |

<details>
<summary>Follow a client code release</summary>

1. Selection reads `modules_version` from the tagged commit's `Taskfile.yml` and verifies that the catalog has a published stable release.
2. Preparation checks the client tag format and verifies that its commit belongs to `main`.
3. The shared build creates both macOS binaries from that commit and catalog.
4. Publication creates the GitHub Release and records the client and modules tags for documentation.

The tagged commit can be an earlier commit in `main`.
Other client versions are not rebuilt by this path.
Tags containing `+` do not trigger another client code release.

</details>

<details>
<summary>Follow a module catalog release</summary>

1. The modules workflow verifies the `vN` tag and checks that its commit is contained in `main`.
2. It publishes the catalog's GitHub Release.
3. It sends `limanix-modules-release` to `client`, with the modules tag in `client_payload.tag`.
4. The client verifies the catalog release and selects [up to three client base versions](select-up-to-three-versions).
5. Each selected client is rebuilt at its existing commit with the new catalog and the next `+N` suffix.

For example, a `v7` catalog release can produce:

| Selected client | New client release | Included modules |
|-----------------|--------------------|------------------|
| `v1.3.0` | `v1.3.0+1` | `v7` |
| `v1.2.4+10` | `v1.2.4+11` | `v7` |
| `v1.2.3+4` | `v1.2.3+5` | `v7` |

These builds run in parallel.
The tag checks do not rerun the module PR checks.

</details>

<details>
<summary>Follow a shared documentation release</summary>

1. The docs workflow validates a tag such as `v1.0.0`.
2. Sphinx builds the shared pages from the tagged docs source.
3. The deployment workflow applies the site infrastructure and publishes those pages.

Product guides follow the client release event below.

</details>

(notify-docs)=
## What happens after the client builds?

Each published client release records its source commit and a **Module catalog** link.
Use that link to find the included modules version.

After the builds finish, `finalize` marks the highest published client version as GitHub **Latest**.
When this run has publication records, it sends their exact client and modules pairs to `docs` in one `limanix-client-release` event.
Build completion order does not choose Latest.

<details>
<summary>See the event for two published clients</summary>

```json
{
  "event_type": "limanix-client-release",
  "client_payload": {
    "releases": [
      {"client_tag": "v1.3.0+1", "modules_tag": "v7"},
      {"client_tag": "v1.2.4+11", "modules_tag": "v7"}
    ]
  }
}
```

Publication records are uploaded after each GitHub Release.
Without them, finalization skips the event instead of choosing an older release marked Latest.

</details>

(published-documentation)=
## When does your documentation appear?

The docs event checks out each client and catalog at the tags in the event.
It generates the references and builds a complete site for that pair.
Shared pages and theme come from the docs checkout used by that event.

| Address | Content |
|---------|---------|
| `/` | Shared site, updated by a docs tag |
| `/client/` | Redirect to the highest published documentation version |
| `/client/v1.3.0+1/` | Saved site for that client release and its catalog |

The version switcher shows both tags, for example **v1.3.0+1 · modules v7**.
Switching versions changes the whole saved site, including its guides, references, and search.

A client or module guide appears after a release containing it passes the docs workflow.
Existing archives stay unchanged.
The three-version rebuild limit does not remove older documentation.

<details>
<summary>Why can Latest and current documentation differ?</summary>

GitHub Latest is selected from published client releases.
Current documentation is selected from completed documentation snapshots.
A client release can exist before its docs build finishes, or its docs build can fail.

Docs orders snapshots by major, minor, patch, then rebuild number.
It keeps completed archives unchanged when the same event arrives again.
An event that pairs an archived client tag with a different catalog fails publication.

</details>

## Follow the result

If your change is missing, first check whether a release includes its commit.
For missing pages, also check the matching run in the docs repository.
A successful notification means the event was sent; it does not prove the docs were published.

<details>
<summary>Understand a failed or partial run</summary>

| What you see | What it means |
|--------------|---------------|
| Client selection fails or selects nothing | No client build starts |
| One client build fails | Other builds continue and their published releases remain |
| A release exists but its publication record is missing | That pair cannot enter this run's docs event |
| The client run is cancelled | Finalization is skipped; already published releases can remain |
| One docs build fails | Publication of that event's documentation is skipped |
| Documentation publication fails | Earlier uploads can remain; the client releases are unaffected |

Include the repository, run link, tag, and failed job when reporting the problem.

Sending the same modules event again selects versions again and increments their rebuild counters.
Retrying old client publication jobs can reuse an existing tag on the same commit without checking its recorded catalog.

</details>

<details>
<summary>Find the workflow behind a check or release</summary>

All paths below are relative to each repository's `.github/workflows/` directory.

| Repository | File | Role |
|------------|------|------|
| `client` | `pr.yml`, `labels.yml` | PR checks and labels |
| `client` | `release.yml`, `event.yml` | Code tag and modules event entry points |
| `client` | `_release.yml`, `_select.yml` | Select versions, run builds, and finalize |
| `client` | `_deploy.yml`, `__build.yml` | Prepare, build, and publish each client |
| `modules` | `pr.yml`, `release.yml` | PR checks, catalog release, and client notification |
| `docs` | `pr.yml`, `labels.yml` | Shared-page build and labels |
| `docs` | `release.yml` | Shared site release |
| `docs` | `event.yml`, `build-docs.yml`, `publish-client-docs.yml` | Build and publish versioned product docs |

</details>
