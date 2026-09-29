"""Checks for prepared documentation inputs and the assembled site tree."""

from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_docs


class BuildDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.root = self.base / "site"
        self.client = self.base / "prepared-client"
        self.modules = self.base / "prepared-modules"
        self.pages = self.root / "build" / "docs-pages"
        self.enterContext(patch.object(build_docs, "ROOT", self.root))
        self.enterContext(patch.object(build_docs, "PAGES", self.pages))

        files = {
            self.root
            / "docs/pages/index.md": "# Site\n\n```{toctree}\n:glob:\n\n**/index\n```\n",
            self.root / "docs/pages/releases/index.md": "# Releases\n",
            self.client / "index.md": (
                "# Client\n\n"
                "[Catalog](https://limanix.dev/categories/nixos/catalog.html#available-modules)\n"
                "[Catalog page](https://limanix.dev/categories/nixos/catalog.html)\n"
            ),
            self.client / "examples/minimal.toml": 'name = "example"\n',
            self.client
            / "reference/cli.md": "# CLI\n\n```{include} ../generated/cli.md\n```\n",
            self.client / "generated/cli.md": "## limanix create\n",
            self.client / "generated/metadata.json": '{"version": "dev"}\n',
            self.modules
            / "index.md": "# NixOS\n\n```{toctree}\n:hidden:\n\ncatalog\n```\n",
            self.modules / "catalog.md": (
                "# Module catalog\n\n"
                "[Go](modules/go/README.md)\n"
                "[Source](https://github.com/limanix/modules/blob/v4/catalog/go/releases.nix)\n"
                "[Registry](https://limanix.dev/categories/client/index.html#registry)\n"
                "[External](https://example.com/categories/client/index.html)\n"
                "[Release](https://limanix.dev/releases/index.html)\n"
                "[Query](https://limanix.dev/categories/client/index.html?view=all#registry)\n\n"
                "```{toctree}\n:hidden:\n:glob:\n\nmodules/*/README\n```\n"
            ),
            self.modules / "modules/go/README.md": (
                "# Go\n\n[Guide](../../catalog.md)\n"
                "[Registry](https://limanix.dev/categories/client/index.html#registry)\n"
                "[Example](assets/example.dat)\n"
            ),
        }
        for path, content in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        asset = self.modules / "modules/go/assets/example.dat"
        asset.parent.mkdir()
        asset.write_bytes(b"\x00\x01\xff")

    @staticmethod
    def snapshot(directory: Path) -> dict[str, bytes]:
        return {
            path.relative_to(directory).as_posix(): path.read_bytes()
            for path in directory.rglob("*")
            if path.is_file()
        }

    def archive(self, source: Path) -> Path:
        archive = self.base / f"{source.name}.tar.gz"
        with tarfile.open(archive, "w:gz") as output:
            output.add(source, arcname=".")
        return archive

    def test_directory_and_archive_produce_the_same_complete_site(self) -> None:
        client_archive = self.archive(self.client)
        modules_archive = self.archive(self.modules)
        archives = {
            source: source.read_bytes() for source in (client_archive, modules_archive)
        }
        inputs = (self.root / "docs/pages", self.client, self.modules)
        originals = {source: self.snapshot(source) for source in inputs}
        results = []

        for client in (self.client, client_archive):
            for modules in (self.modules, modules_archive):
                with self.subTest(client=client.name, modules=modules.name):
                    build_docs.prepare(client, modules)
                    results.append(self.snapshot(self.pages))

        for result in results[1:]:
            self.assertEqual(results[0], result)
        expected_paths = set(originals[inputs[0]])
        expected_paths.update(
            f"categories/client/{path}" for path in originals[inputs[1]]
        )
        expected_paths.update(
            f"categories/nixos/{path}" for path in originals[inputs[2]]
        )
        self.assertEqual(set(results[0]), expected_paths)

        nixos = self.pages / "categories/nixos"
        self.assertEqual(
            (nixos / "index.md").read_bytes(), (self.modules / "index.md").read_bytes()
        )
        self.assertEqual(
            (nixos / "catalog.md").read_text(),
            (self.modules / "catalog.md")
            .read_text()
            .replace(
                "https://limanix.dev/categories/client/index.html#registry",
                "../client/index.md#registry",
            ),
        )
        self.assertEqual(
            (nixos / "modules/go/README.md").read_text(),
            (self.modules / "modules/go/README.md")
            .read_text()
            .replace(
                "https://limanix.dev/categories/client/index.html#registry",
                "../../../client/index.md#registry",
            ),
        )
        self.assertEqual(
            (nixos / "modules/go/assets/example.dat").read_bytes(), b"\x00\x01\xff"
        )
        self.assertEqual(
            (self.pages / "categories/client/index.md").read_text(),
            (self.client / "index.md")
            .read_text()
            .replace(
                "https://limanix.dev/categories/nixos/catalog.html",
                "../nixos/catalog.md",
            ),
        )
        for reference in (
            "reference/cli.md",
            "generated/cli.md",
            "generated/metadata.json",
        ):
            self.assertEqual(
                (self.pages / "categories/client" / reference).read_bytes(),
                (self.client / reference).read_bytes(),
            )
        self.assertEqual(
            (self.pages / "index.md").read_text(),
            (self.root / "docs/pages/index.md").read_text(),
        )
        for source, original in originals.items():
            self.assertEqual(self.snapshot(source), original)
        for archive, original in archives.items():
            self.assertEqual(archive.read_bytes(), original)

    def test_repeated_preparation_removes_stale_files(self) -> None:
        build_docs.prepare(self.client, self.modules)
        (self.pages / "stale.md").write_text("old output\n")
        (self.modules / "modules/go/assets/example.dat").unlink()
        (self.modules / "index.md").write_text("# Updated NixOS\n")

        build_docs.prepare(self.client, self.modules)
        self.assertFalse((self.pages / "stale.md").exists())
        self.assertFalse(
            (self.pages / "categories/nixos/modules/go/assets/example.dat").exists()
        )
        self.assertEqual(
            (self.pages / "categories/nixos/index.md").read_text(), "# Updated NixOS\n"
        )

        build_docs.prepare(None, None)
        self.assertEqual(
            self.snapshot(self.pages), self.snapshot(self.root / "docs/pages")
        )

    def test_composite_requires_both_inputs_before_changing_staging(self) -> None:
        self.pages.mkdir(parents=True)
        marker = self.pages / "existing.md"
        marker.write_text("keep\n")
        for client, modules in ((self.client, None), (None, self.modules)):
            with self.subTest(client=client, modules=modules):
                with self.assertRaisesRegex(ValueError, "provided together"):
                    build_docs.prepare(client, modules)
                self.assertEqual(marker.read_text(), "keep\n")

    def test_prepared_directory_and_archive_require_a_root_index(self) -> None:
        for name, section in (("client", self.client), ("module", self.modules)):
            index = section / "index.md"
            original = index.read_bytes()
            index.unlink()
            for source in (section, self.archive(section)):
                with self.subTest(section=name, source=source.name):
                    client = source if section == self.client else self.client
                    modules = source if section == self.modules else self.modules
                    with self.assertRaisesRegex(
                        ValueError,
                        f"prepared {name} documentation must contain index.md",
                    ):
                        build_docs.prepare(client, modules)
            index.write_bytes(original)

    def test_archive_rejects_paths_and_symlinks_outside_its_destination(self) -> None:
        for kind in ("traversal", "symlink"):
            with self.subTest(kind=kind):
                archive = self.base / f"{kind}.tar.gz"
                member = tarfile.TarInfo(
                    "../../../../../escaped.md" if kind == "traversal" else "escape"
                )
                if kind == "symlink":
                    member.type = tarfile.SYMTYPE
                    member.linkname = "../../../../../escaped.md"
                else:
                    member.size = len(b"escaped\n")
                with tarfile.open(archive, "w:gz") as output:
                    output.addfile(
                        member,
                        io.BytesIO(b"escaped\n") if kind == "traversal" else None,
                    )

                for client, modules in (
                    (archive, self.modules),
                    (self.client, archive),
                ):
                    with self.subTest(client=client.name, modules=modules.name):
                        with self.assertRaises(tarfile.FilterError):
                            build_docs.prepare(client, modules)
                        self.assertFalse((self.base / "escaped.md").exists())
                        self.assertFalse(
                            (self.pages / "categories/client/escape").is_symlink()
                        )
                        self.assertFalse(
                            (self.pages / "categories/nixos/escape").is_symlink()
                        )

    def test_staging_must_not_be_a_symlink(self) -> None:
        self.pages.parent.mkdir(parents=True)
        self.pages.symlink_to(self.modules, target_is_directory=True)
        original = self.snapshot(self.modules)
        with self.assertRaisesRegex(
            ValueError, "staging directory must not be a symlink"
        ):
            build_docs.prepare(self.client, self.modules)
        self.assertEqual(self.snapshot(self.modules), original)

    def test_output_must_stay_under_build_and_outside_staging(self) -> None:
        for output in ("docs", "build", "build/docs-pages", "build/docs-pages/html"):
            with (
                self.subTest(output=output),
                self.assertRaisesRegex(ValueError, "output must"),
            ):
                build_docs.clean_output(output)
        output = self.root / "build/docs"
        output.mkdir(parents=True)
        (output / "stale.html").write_text("old page")
        build_docs.clean_output("build/docs")
        self.assertFalse(output.exists())

    def test_output_must_not_overlap_directory_or_archive_inputs(self) -> None:
        for argument, source in (
            ("client", "build/inputs/client"),
            ("client", "build/inputs/client/docs.tar.gz"),
            ("modules", "build/inputs/modules"),
            ("modules", "build/inputs/modules/docs.tar.gz"),
        ):
            for output in (source, str(Path(source).parent), f"{source}/html"):
                with (
                    self.subTest(source=source, output=output),
                    self.assertRaisesRegex(ValueError, "overlaps"),
                ):
                    build_docs.clean_output(output, **{argument: self.root / source})


if __name__ == "__main__":
    unittest.main()
