# LimaNix documentation

The LimaNix documentation website.

## Local preview

Requires [Task](https://taskfile.dev/) 3.53.1 or newer and Docker.
Python and uv run in the pinned shared container; documentation dependencies are installed from `uv.lock`.

```console
task --yes docs/serve
```

Open <http://127.0.0.1:8070/>. 
Changes to the pages or Sphinx configuration rebuild the site automatically. 
Stop the preview with `Ctrl+C`.

To use another port:

```console
task --yes docs/serve DOCS_PORT=8071
```

### Include local projects

Pass project directories in `DOCS`:

```console
task --yes docs/serve DOCS='../modules'
```

For several projects:

```console
task --yes docs/serve DOCS='../modules ../client'
```

Each directory must contain `docs/index.md`. Relative paths are resolved from
this repository. Use absolute paths for projects elsewhere; quote a path inside
the list when it contains spaces:

```console
task --yes docs/serve DOCS='../modules "/path/to/my client"'
```

The homepage and sidebar gain a **Local projects** section. Each project uses
its directory name for a separate URL, such as `/projects/modules/index.html`.
Names are lowercased; letters, digits, underscores, and hyphens are kept. Other
characters become hyphens. Project names must remain distinct after this conversion.

The preview uses this site's Sphinx configuration. It copies each complete
`docs/` tree, including images and downloadable examples, into a temporary
directory. Keep relative links and included files inside that tree. A project's
own `conf.py`, theme, or dependencies are not loaded.

Edits, new pages, and deleted pages trigger a rebuild. Site configuration and
static assets are watched too. Project directories are mounted read-only; the
preview does not modify their documentation. Restart the command to change the
project list. `DOCS_PORT` works with `DOCS`.

## Build

```console
task --yes ci/docs
```
