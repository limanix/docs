# Versions and rebuilds

Keep three numbers separate: the **client code version**, its **rebuild counter**, and the **module catalog version**.

## Read a tag

| Tag | Meaning |
|-----|---------|
| Modules `v7` | Catalog revision 7 |
| Client `v1.2.3` | Client code version 1.2.3, built with its Taskfile catalog pin |
| Client `v1.2.3+4` | The fourth catalog rebuild of client version 1.2.3 |

The client tags `v1.2.3`, `v1.2.3+1`, and `v1.2.3+4` point to the **same client commit**. Each rebuild has its own binaries and GitHub Release.

```{important}
`+4` is a rebuild counter. It does not mean modules `v4`.
Client `v1.2.3+4` can contain modules `v7`. Read the **Module catalog** link in its GitHub Release to find the included version.
```

### Accepted formats

| Item | Format | Valid examples | Rejected examples |
|------|--------|----------------|-------------------|
| Modules | `vN`, starting at 1 | `v1`, `v7`, `v123` | `v0`, `v01`, `v1.2.3` |
| Client code | `vMAJOR.MINOR.PATCH` | `v0.1.0`, `v1.2.3` | `v1.2`, `v01.2.3`, `v1.2.3-rc.1` |
| Client rebuild | Code tag followed by `+N`, starting at 1 | `v1.2.3+1`, `v1.2.3+12` | `v1.2.3+0`, `v1.2.3+01`, `v1.2.3+abc` |

Code version components can be zero; leading zeros are rejected. These workflows publish stable releases and use a numeric rebuild suffix.

## Choose the next client version

The code version follows the [SemVer components](https://semver.org/#summary):

| Change from `v1.2.3+4` | Next tag |
|------------------------|----------|
| Rebuild the same code with another catalog | `v1.2.3+5` |
| Compatible bug fix | `v1.2.4` |
| Compatible feature | `v1.3.0` |
| Incompatible client change | `v2.0.0` |

A new code version starts without a suffix. Its first catalog rebuild adds `+1`; the previous code version's counter does not carry over.

In SemVer, the suffix after `+` is [build metadata](https://semver.org/#spec-item-10). SemVer ignores it when comparing precedence. LimaNix uses **Git version sorting** to choose between rebuilds, including their numeric counters.

## Keep the catalog and source commit separate

| Build path | Where the modules tag comes from | What changes in Git |
|------------|---------------------------------|---------------------|
| New client code tag | `modules_version` in that commit's `Taskfile.yml` | The code tag identifies the selected `main` commit |
| Catalog event | `client_payload.tag`, such as `v7` | A new `+N` tag points to the selected client's existing commit |

For example, the source for `v1.2.3+4` may still contain `modules_version: 'v1'`. The release build can pass `modules_version=v7` and record `v7` in its GitHub Release. The unchanged Taskfile is the default for that source, not a record of every later rebuild.

Keep published tags on their original commits. A new code change gets a new base version; a new catalog build gets a new counter.

(select-up-to-three-versions)=
## Select up to three versions

The active unit is the **full base version**, including `PATCH`. `v1.2.4` and `v1.2.3` count as two versions.

For catalog rebuilds, `get-tags`:

1. Matches the client tag glob and requires a published GitHub Release.
2. Sorts the matching tags by Git version order, highest first.
3. Groups tags by the text before `+` and keeps the first tag in each group.
4. Returns up to three groups as `{tag, commit_sha}` entries.

| Published tags | Selected for the active set |
|----------------|-----------------------------|
| `v1.3.0` | `v1.3.0` |
| `v1.2.4+10`, `v1.2.4+2`, `v1.2.4` | `v1.2.4+10` |
| `v1.2.3+4`, `v1.2.3+1`, `v1.2.3` | `v1.2.3+4` |
| `v1.2.2+5`, `v1.2.2` | Outside the active set |

With fewer than three base versions, all available groups are selected. A tag without a published GitHub Release does not enter this set.

Leaving the active set stops automatic catalog rebuilds. Existing releases remain available.

```{note}
The shared selector checks publication and a tag glob; it does not exclude GitHub prereleases or apply the client's full format check. An unsupported tag can occupy a selection slot before later validation rejects it. The examples above use the stable tag formats accepted by this release process.
```
