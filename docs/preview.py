"""Assemble local project documentation for the shared Sphinx preview."""

import argparse
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SITE = Path(__file__).resolve().parent
MARKER = ".limanix-docs-preview"


def project_sources(projects):
    """Validate mounted projects and give each one a distinct URL namespace."""
    sources = {}
    for name, directory in projects:
        slug = re.sub(r"[^a-z0-9_-]+", "-", name.lower()).strip("-")
        if not slug:
            raise ValueError(f"Cannot derive a documentation name from {name!r}")
        if slug in sources:
            raise ValueError(f"Projects must have distinct directory names: {name!r}")
        source = Path(directory).resolve() / "docs"
        if not (source / "index.md").is_file():
            raise ValueError(f"Project {name!r} must contain docs/index.md: {source}")
        sources[slug] = source
    return sources


def prepare(workspace, projects):
    """Refresh only the temporary source tree owned by this preview process."""
    if not (workspace / MARKER).is_file():
        raise ValueError(f"Not a preview workspace: {workspace}")
    sources = project_sources(projects)
    if sources and (SITE / "pages" / "projects").exists():
        raise ValueError("docs/pages/projects is reserved for local project previews")

    source = workspace / "source"
    previous = {path.relative_to(source) for path in source.rglob("*.md")}
    if source.exists():
        shutil.rmtree(source)
    shutil.copytree(SITE / "pages", source)

    for slug, directory in sources.items():
        shutil.copytree(directory, source / "projects" / slug)

    if sources:
        entries = "\n".join(f"projects/{slug}/index" for slug in sources)
        with (source / "index.md").open("a", encoding="utf-8") as homepage:
            homepage.write(
                "\n\n```{toctree}\n:caption: Local projects\n"
                ":maxdepth: 1\n:titlesonly:\n\n" + entries + "\n```\n"
            )

    # Sphinx does not remove HTML for deleted source pages by itself.
    current = {path.relative_to(source) for path in source.rglob("*.md")}
    for removed in previous - current:
        (workspace / "html" / removed.with_suffix(".html")).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8070)
    parser.add_argument(
        "--project", nargs=2, action="append", default=[], metavar=("NAME", "DIRECTORY")
    )
    parser.add_argument("--prepare", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        sources = project_sources(args.project)
        if args.prepare is not None:
            prepare(args.prepare, args.project)
            return 0

        with tempfile.TemporaryDirectory(prefix="limanix-docs-") as directory:
            workspace = Path(directory)
            (workspace / MARKER).touch()
            prepare(workspace, args.project)

            refresh = [sys.executable, str(Path(__file__).resolve()), "--prepare", directory]
            for name, path in args.project:
                refresh.extend(["--project", name, path])

            command = [
                sys.executable, "-m", "sphinx_autobuild",
                "--host", "0.0.0.0", "--port", str(args.port),
                "--pre-build", shlex.join(refresh),
                "--ignore", str(workspace / "source"),
                "--watch", str(SITE),
            ]
            for source in sources.values():
                command.extend(["--watch", str(source)])
            command.extend([
                "-E", "-a", "-W", "--keep-going", "-c", str(SITE),
                str(workspace / "source"), str(workspace / "html"),
            ])
            return subprocess.call(command)
    except (OSError, ValueError) as error:
        parser.exit(2, f"docs preview: {error}\n")
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
