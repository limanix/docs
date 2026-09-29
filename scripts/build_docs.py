"""Prepare the source tree consumed by Sphinx."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tarfile
from os.path import relpath
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "build" / "docs-pages"
SITE_GUIDE_LINK = re.compile(
    r"\]\(https://limanix\.dev/categories/(client|nixos)/([\w/-]+)\.html(#[^\s)]*)?\)"
)


def copy_prepared(source: Path, destination: Path, name: str) -> None:
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        with tarfile.open(source, "r:gz") as archive:
            archive.extractall(destination, filter="data")
    if not (destination / "index.md").is_file():
        raise ValueError(
            f"prepared {name} documentation must contain index.md: {source}"
        )


def rewrite_site_guide_links(content: str, page: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        target = PAGES / "categories" / match[1] / f"{match[2]}.md"
        relative = Path(relpath(target, page.parent)).as_posix()
        return f"]({relative}{match[3] or ''})"

    return SITE_GUIDE_LINK.sub(replace, content)


def prepare(client: Path | None, modules: Path | None) -> None:
    if (client is None) != (modules is None):
        raise ValueError(
            "prepared client and module documentation must be provided together"
        )

    if PAGES.is_symlink():
        raise ValueError(f"staging directory must not be a symlink: {PAGES}")
    shutil.rmtree(PAGES, ignore_errors=True)
    shutil.copytree(ROOT / "docs" / "pages", PAGES)

    if client is None:
        return

    categories = PAGES / "categories"
    copy_prepared(client, categories / "client", "client")
    copy_prepared(modules, categories / "nixos", "module")

    for page in categories.rglob("*.md"):
        original = page.read_text(encoding="utf-8")
        updated = rewrite_site_guide_links(original, page)
        if updated != original:
            page.write_text(updated, encoding="utf-8")


def clean_output(
    value: str, client: Path | None = None, modules: Path | None = None
) -> None:
    output = (ROOT / value).resolve()
    build = (ROOT / "build").resolve()
    if (
        not output.is_relative_to(build)
        or output == build
        or output.is_relative_to(PAGES.resolve())
    ):
        raise ValueError(f"output must be a directory under {build}, excluding {PAGES}")
    for source in (client, modules):
        if source is not None:
            resolved_source = source.resolve()
            if output.is_relative_to(resolved_source) or resolved_source.is_relative_to(
                output
            ):
                raise ValueError(
                    f"output overlaps a documentation input: {resolved_source}"
                )
    if output.exists():
        shutil.rmtree(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--client-docs", type=Path, help="Prepared directory or docs.tar.gz"
    )
    parser.add_argument(
        "--modules-docs", type=Path, help="Prepared directory or docs.tar.gz"
    )
    parser.add_argument(
        "--clean-output", help="Remove an HTML output directory under build/"
    )
    args = parser.parse_args()

    try:
        if args.clean_output:
            clean_output(args.clean_output, args.client_docs, args.modules_docs)
        prepare(args.client_docs, args.modules_docs)
    except (OSError, ValueError, tarfile.TarError) as error:
        print(f"build_docs: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
