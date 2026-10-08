"""Check product-page assembly and internal navigation across site versions."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "site_docs", Path(__file__).parents[1] / "build_docs.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BuildDocsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.pages = self.root / "build/docs-pages"
        (self.root / "docs/pages").mkdir(parents=True)
        self.link = "[Workspace](https://limanix.dev/categories/client/workspace.html#create-the-workbench)"
        (self.root / "docs/pages/index.md").write_text(self.link)
        self.client = self.root / "inputs/client"
        self.modules = self.root / "inputs/modules"
        self.lmx = self.root / "inputs/lmx"
        for directory in (self.client, self.modules, self.lmx):
            directory.mkdir(parents=True)
            (directory / "index.md").write_text("# Product\n")
        (self.client / "workspace.md").write_text("# Workspace\n")
        (self.modules / "catalog.md").write_text(self.link)
        (self.lmx / "updates.md").write_text(self.link)
        for name, value in (("ROOT", self.root), ("PAGES", self.pages)):
            patcher = patch.object(MODULE, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_shared_and_product_links_stay_inside_assembled_site(self):
        MODULE.prepare(self.client, self.modules, self.lmx)
        self.assertEqual(
            (self.pages / "index.md").read_text(),
            "[Workspace](categories/client/workspace.md#create-the-workbench)",
        )
        self.assertEqual(
            (self.pages / "categories/nixos/catalog.md").read_text(),
            "[Workspace](../client/workspace.md#create-the-workbench)",
        )
        self.assertEqual(
            (self.pages / "categories/lmx/updates.md").read_text(),
            "[Workspace](../client/workspace.md#create-the-workbench)",
        )
        self.assertTrue((self.pages / "categories/client/workspace.md").is_file())

    def test_shared_only_build_keeps_published_product_links(self):
        MODULE.prepare(None, None, None)
        self.assertEqual((self.pages / "index.md").read_text(), self.link)
        self.assertFalse((self.pages / "categories").exists())

    def test_partial_pair_is_rejected_before_cleaning_staged_pages(self):
        self.pages.mkdir(parents=True)
        sentinel = self.pages / "index.md"
        sentinel.write_text("previous successful build")
        with self.assertRaisesRegex(ValueError, "provided together"):
            MODULE.prepare(self.client, self.modules, None)
        self.assertEqual(sentinel.read_text(), "previous successful build")

    def test_cleanup_refuses_to_overlap_prepared_input(self):
        with self.assertRaisesRegex(ValueError, "overlaps"):
            MODULE.clean_output("build/site", self.root / "build/site/client")


if __name__ == "__main__":
    unittest.main()
