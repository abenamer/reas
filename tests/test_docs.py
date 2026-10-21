"""Unit tests for the REAS documentation checker."""
from pathlib import Path
import tempfile
import unittest
from scripts.check_docs import split_frontmatter, outside_fences, validate

class CheckDocsTests(unittest.TestCase):
    def test_valid_frontmatter(self):
        metadata, body, err = split_frontmatter("---\ntype: Rule\n---\nText")
        self.assertIsNone(err)
        self.assertEqual(metadata["type"], "Rule")
        self.assertEqual(body, "Text")
    def test_missing_frontmatter(self):
        metadata, body, err = split_frontmatter("Text")
        self.assertIsNone(metadata)
        self.assertEqual(body, "Text")
        self.assertIsNone(err)
    def test_invalid_yaml(self):
        _, _, err = split_frontmatter("---\ntype: [unclosed\n---\nBody")
        self.assertIsNotNone(err)
    def test_code_fence_filter(self):
        self.assertNotIn("bad link", outside_fences("```md\nbad link\n```"))
    def test_real_repository(self):
        self.assertEqual(validate(Path(__file__).resolve().parents[1]), [])
    def test_missing_index(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "standard").mkdir()
            (root / "standard" / "rule.md").write_text("---\ntype: Rule\n---\n# REAS-RUST-001\n")
            self.assertEqual(validate(root), [])
    def test_broken_link(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bundle = root / "standard"
            bundle.mkdir()
            (bundle / "index.md").write_text("---\nokf_version: '0.2'\n---\n# Index\n")
            (bundle / "rule.md").write_text("---\ntype: Rule\n---\n# REAS-RUST-001\n[missing](absent.md)\n")
            self.assertTrue(any("Broken local link" in x for x in validate(root)))

if __name__ == "__main__":
    unittest.main()
