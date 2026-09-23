# Versions and release lines

The client and module catalog have separate versions. 
A client release tag records both, so each published client identifies the catalog it includes.

## Read a release tag

| Item                  | Format                 | Example    |
|-----------------------|------------------------|------------|
| Module release        | `vN`                   | `v7`       |
| Client release branch | `vMAJOR.MINOR`         | `v1.2`     |
| Client release tag    | `vMAJOR.MINOR.PATCH+N` | `v1.2.3+7` |

In `v1.2.3+7`, **`1.2.3` is the client version** and **`7` selects modules `v7`**. 
The `v1.2` branch carries that client's release line.

## Choose the next version

The client code version uses the usual SemVer components: 
`PATCH` for compatible bug fixes, `MINOR` for compatible additions, and `MAJOR` for incompatible changes.
[SemVer defines these rules](https://semver.org/#summary).

For example, starting from client `v1.2.3+7`:

| Change                                                 | Next client tag | Release branch |
|--------------------------------------------------------|-----------------|----------------|
| Update only the catalog to `v8`                        | `v1.2.3+8`      | `v1.2`         |
| Fix a client bug, keep modules `v7`                    | `v1.2.4+7`      | `v1.2`         |
| Add compatible client functionality, keep modules `v7` | `v1.3.0+7`      | New `v1.3`     |
| Make an incompatible client change, keep modules `v7`  | `v2.0.0+7`      | New `v2.0`     |

A new minor or major line starts from the selected code in `main`. 
A patch release stays on its existing release branch.

**Published tags do not move.** Each release gets a new tag; 
an existing tag is never overwritten to point at a newer client or catalog.

## Select the latest release

The `+N` suffix is SemVer build metadata. Standard SemVer comparison ignores it, so `1.2.3+7` and `1.2.3+8` have equal precedence.
[See SemVer's build metadata rule](https://semver.org/#spec-item-10).

LimaNix adds an explicit rule when selecting a published client release:

1. Compare `MAJOR`, `MINOR`, and `PATCH` numerically, in that order.
2. If the client versions match, compare the catalog number `N` numerically.

Under this rule, `v1.2.3+8` follows `v1.2.3+7`. 
This catalog comparison is a **LimaNix release-selection rule**, not part of SemVer precedence.

Use `+` for the catalog suffix: `v1.2.3-7` would mean a prerelease under [SemVer's prerelease rule](https://semver.org/#spec-item-9).

## Support three release lines

Support covers **three `MAJOR.MINOR` lines**, not three individual release tags.
For example, `v1.0`, `v1.1`, and `v1.2` each receive catalog updates and retain their own client version.

The site presents the latest successfully published client release from each supported line. 
See [Documentation builds](documentation.md) for how the client and catalog sources become one version of the documentation.
