"""Select and publish documentation versions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

CLIENT_TAG = re.compile(
    r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(\+[1-9][0-9]*)?"
)
MODULES_TAG = re.compile(r"v[1-9][0-9]*")


@dataclass(frozen=True)
class Release:
    """A client release and the module release bundled with it."""

    client_tag: str
    modules_tag: str

    @classmethod
    def from_json(cls, data: object) -> Release:
        if isinstance(data, dict):
            client_tag = data.get("client_tag")
            modules_tag = data.get("modules_tag")
            if isinstance(client_tag, str) and isinstance(modules_tag, str):
                return cls(client_tag, modules_tag)
        raise TypeError(f"expected a client and modules tag pair: {data!r}")

    def to_json(self) -> dict[str, str]:
        return {"client_tag": self.client_tag, "modules_tag": self.modules_tag}

    @property
    def version(self) -> tuple[int, ...]:
        """Numeric parts of the client tag; v1.10.0 follows v1.9.0."""
        return tuple(int(part) for part in re.findall(r"[0-9]+", self.client_tag))


def by_version(releases: Iterable[Release]) -> list[Release]:
    """Newest release first."""
    return sorted(releases, key=lambda release: release.version, reverse=True)


def combine(
    archives: dict[str, Release], incoming: Iterable[Release]
) -> dict[str, Release]:
    """Add releases by client tag; a client release bundles one module release."""
    releases = dict(archives)
    for release in incoming:
        known = releases.setdefault(release.client_tag, release)
        if known != release:
            raise ValueError(
                f"conflicting modules tags for client {release.client_tag}: "
                f"{known.modules_tag} and {release.modules_tag}"
            )
    return releases


def read_object(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"expected a JSON object: {path}")
    return data


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


@dataclass(frozen=True)
class Deployment:
    """Receipts downloaded from the site bucket."""

    docs_sha: str | None
    archives: dict[str, Release]


def read_deployment(root: Path) -> Deployment:
    """Read downloaded receipts; missing ones have not been published yet."""
    current = root / "release.json"
    docs_sha = read_object(current).get("docs_sha") if current.is_file() else None

    archives = {}
    for receipt in sorted(root.glob("client/*/release.json")):
        release = Release.from_json(read_object(receipt))
        if release.client_tag != receipt.parent.name:
            raise ValueError(f"receipt records client {release.client_tag}: {receipt}")
        archives[release.client_tag] = release
    return Deployment(docs_sha if isinstance(docs_sha, str) else None, archives)


def parse_incoming(text: str) -> set[Release]:
    """Parse the client and modules tag pairs of a release event."""
    data = json.loads(text)
    if not isinstance(data, list):
        raise TypeError(f"expected a JSON list of client and modules tag pairs: {text}")

    releases = set()
    for item in data:
        release = Release.from_json(item)
        if not CLIENT_TAG.fullmatch(release.client_tag):
            raise ValueError(f"invalid client tag: {release.client_tag!r}")
        if not MODULES_TAG.fullmatch(release.modules_tag):
            raise ValueError(f"invalid modules tag: {release.modules_tag!r}")
        releases.add(release)
    return releases


def read_site(site: Path) -> Release:
    """Return the release a built site records."""
    if not (site / "index.html").is_file():
        raise ValueError(f"built site is missing: {site}")
    return Release.from_json(read_object(site / "release.json"))


def json_list(releases: Iterable[Release]) -> str:
    return json.dumps(
        [release.to_json() for release in by_version(releases)], separators=(",", ":")
    )


def catalog_entry(release: Release, current: bool) -> dict[str, object]:
    """Version switcher entry; the current release is served at the site root."""
    entry: dict[str, object] = {
        "name": f"{release.client_tag} · modules {release.modules_tag}",
        "version": release.client_tag,
        "url": "/" if current else f"/client/{quote(release.client_tag, safe='')}/",
    }
    if current:
        entry["preferred"] = True
    return entry


@dataclass(frozen=True)
class Selection:
    """The docs commit and the sites to build for the next publication."""

    docs_ref: str
    current: Release | None
    incoming: set[Release]
    builds: set[Release]

    def outputs(self) -> dict[str, str]:
        current = self.current or Release("", "")
        return {
            "docs-ref": self.docs_ref,
            "client-tag": current.client_tag,
            "modules-tag": current.modules_tag,
            "releases": json_list(self.incoming),
            "builds": json_list(self.builds),
        }


def select(deployment: Deployment, incoming: set[Release], docs_ref: str) -> Selection:
    """Choose the docs commit and the client releases to build."""
    if not docs_ref:
        if not incoming:
            raise ValueError("the release event contains no releases")
        if not deployment.docs_sha:
            raise ValueError("no deployed docs commit is recorded")
        docs_ref = deployment.docs_sha

    releases = combine(deployment.archives, incoming)
    current = max(releases.values(), key=lambda release: release.version, default=None)
    builds = (incoming | {current}) if current else incoming
    return Selection(docs_ref, current, incoming, builds)


@dataclass(frozen=True)
class Publication:
    """New archived sites with their receipts, and the version catalog."""

    archives: list[Release]
    catalog: list[dict[str, object]]

    def write(self, output: Path) -> None:
        write_json(output / "versions.json", self.catalog)
        for release in self.archives:
            receipt = output / "client" / release.client_tag / "release.json"
            write_json(receipt, release.to_json())

    def outputs(self) -> dict[str, str]:
        return {"archives": " ".join(release.client_tag for release in self.archives)}


def publish(
    deployment: Deployment,
    incoming: set[Release],
    docs_ref: str,
    client_tag: str,
    sites: Path,
) -> Publication:
    """Check the built sites against the deployment and plan the upload."""
    current_site = sites / f"docs-{client_tag or 'current'}"
    if read_site(current_site).client_tag != client_tag:
        raise ValueError(f"site is not built for client {client_tag}: {current_site}")
    if incoming and deployment.docs_sha != docs_ref:
        raise ValueError(
            f"deployed docs commit changed from {docs_ref} "
            f"to {deployment.docs_sha or 'none'}; rerun all jobs"
        )

    archives = []
    for release in by_version(incoming):
        site = sites / f"docs-{release.client_tag}"
        if read_site(site) != release:
            raise ValueError(
                f"site is not built for client {release.client_tag} with modules "
                f"{release.modules_tag}: {site}"
            )
        archived = deployment.archives.get(release.client_tag)
        if archived is None:
            archives.append(release)
        elif archived != release:
            raise ValueError(
                f"client {release.client_tag} is archived with modules "
                f"{archived.modules_tag}, not {release.modules_tag}"
            )

    releases = by_version(combine(deployment.archives, archives).values())
    newest = releases[0].client_tag if releases else ""
    if newest != client_tag:
        raise ValueError(
            f"newest client release changed from {client_tag or 'none'} to {newest}; "
            "rerun all jobs"
        )
    catalog = [
        catalog_entry(release, current=index == 0)
        for index, release in enumerate(releases)
    ]
    return Publication(archives, catalog)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)

    select_command = commands.add_parser(
        "select", help="choose the docs commit and the client releases to build"
    )
    select_command.add_argument(
        "--docs-ref", default="", help="docs commit; empty keeps the deployed one"
    )

    publish_command = commands.add_parser(
        "publish", help="check built sites and write receipts and the catalog"
    )
    publish_command.add_argument(
        "--docs-ref", required=True, help="docs commit the sites were built from"
    )
    publish_command.add_argument(
        "--client-tag", default="", help="client release served at the site root"
    )
    publish_command.add_argument(
        "--sites", type=Path, required=True, help="built sites, one docs-<tag> each"
    )
    publish_command.add_argument(
        "--output", type=Path, required=True, help="directory for files to upload"
    )

    for command in (select_command, publish_command):
        command.add_argument(
            "--deployed", type=Path, required=True, help="downloaded bucket receipts"
        )
        command.add_argument(
            "--incoming", default="[]", help="JSON list of client and modules tags"
        )

    args = parser.parse_args()
    try:
        deployment = read_deployment(args.deployed)
        incoming = parse_incoming(args.incoming)
        if args.command == "select":
            outputs = select(deployment, incoming, args.docs_ref).outputs()
        else:
            publication = publish(
                deployment, incoming, args.docs_ref, args.client_tag, args.sites
            )
            publication.write(args.output)
            outputs = publication.outputs()
    except (OSError, TypeError, ValueError) as error:
        print(f"releases: {error}", file=sys.stderr)
        return 1

    for name, value in outputs.items():
        print(f"{name}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
