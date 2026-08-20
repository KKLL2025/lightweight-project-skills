from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = (
    Path(__file__).parents[1]
    / "skills"
    / "organize-ai-project-files"
    / "scripts"
    / "tree_snapshot.py"
)
SPEC = importlib.util.spec_from_file_location("tree_snapshot", SCRIPT)
assert SPEC and SPEC.loader
tree_snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tree_snapshot)


class TreeSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "project"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def snapshot(self, hash_mode: str = "all") -> dict:
        return tree_snapshot.build_snapshot(self.root, [], hash_mode, 512)

    def write_snapshot(self, value: dict) -> Path:
        before = Path(self.temporary.name) / "before.json"
        before.write_text(json.dumps(value), encoding="utf-8")
        return before

    def compare(self, before: dict, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "compare",
                "--root",
                str(self.root),
                "--before",
                str(self.write_snapshot(before)),
                "--json",
                *extra,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_content_mode_accepts_pure_move_and_rename(self) -> None:
        source = self.root / "old" / "原文件.txt"
        source.parent.mkdir()
        source.write_text("same content", encoding="utf-8")
        before = self.snapshot()
        destination = self.root / "new" / "renamed.txt"
        destination.parent.mkdir()
        source.rename(destination)

        result = self.compare(before, "--path-mode", "content")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["equal"])
        self.assertTrue(payload["contentVerified"])

        exact = self.compare(before, "--path-mode", "exact")
        self.assertEqual(exact.returncode, 1)
        self.assertFalse(json.loads(exact.stdout)["equal"])

    def test_duplicate_content_uses_multiset_counts(self) -> None:
        (self.root / "a.bin").write_bytes(b"duplicate")
        (self.root / "b.bin").write_bytes(b"duplicate")
        before = self.snapshot()
        (self.root / "a.bin").unlink()

        result = self.compare(before, "--path-mode", "content")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["equal"])
        self.assertEqual(payload["missing"][0]["count"], 1)

    def test_duplicate_content_allows_renaming_every_copy(self) -> None:
        (self.root / "a.bin").write_bytes(b"duplicate")
        (self.root / "b.bin").write_bytes(b"duplicate")
        before = self.snapshot()
        (self.root / "a.bin").rename(self.root / "x.bin")
        (self.root / "b.bin").rename(self.root / "y.bin")

        result = self.compare(before, "--path-mode", "content")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_empty_and_chinese_paths_are_content_identified(self) -> None:
        nested = self.root / "资料" / "空文件.txt"
        nested.parent.mkdir()
        nested.write_bytes(b"")
        before = self.snapshot()
        moved = self.root / "归档" / "重命名.txt"
        moved.parent.mkdir()
        nested.rename(moved)

        snapshot = self.snapshot()
        self.assertEqual(snapshot["files"][0]["path"], "归档/重命名.txt")
        result = self.compare(before, "--path-mode", "content")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_windows_style_exclude_is_portable(self) -> None:
        excluded = self.root / "资料" / "临时" / "ignore.txt"
        excluded.parent.mkdir(parents=True)
        excluded.write_text("ignored", encoding="utf-8")
        kept = self.root / "资料" / "keep.txt"
        kept.write_text("kept", encoding="utf-8")

        snapshot = tree_snapshot.build_snapshot(
            self.root, [r"资料\临时"], "all", 512
        )
        self.assertEqual([item["path"] for item in snapshot["files"]], ["资料/keep.txt"])

    def test_hash_mode_none_fails_closed_even_when_metadata_matches(self) -> None:
        target = self.root / "same-name.bin"
        target.write_bytes(b"AAAA")
        before = self.snapshot("none")
        original_mtime = before["files"][0]["mtimeNs"]
        target.write_bytes(b"BBBB")
        os.utime(target, ns=(original_mtime, original_mtime))

        result = self.compare(before, "--hash-mode", "none", "--path-mode", "exact")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["equal"])
        self.assertTrue(payload["structuralEqual"])
        self.assertFalse(payload["contentVerified"])
        self.assertEqual(payload["unhashedFiles"], {"before": 1, "after": 1})

    def test_create_defaults_to_metadata_only_snapshot(self) -> None:
        (self.root / "ordinary.bin").write_bytes(b"content")
        output = Path(self.temporary.name) / "snapshot.json"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "create",
                "--root",
                str(self.root),
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        snapshot = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(snapshot["hashMode"], "none")
        self.assertNotIn("sha256", snapshot["files"][0])

    def test_internal_symlink_is_recorded_without_reading_target(self) -> None:
        target = self.root / "target.txt"
        target.write_text("inside", encoding="utf-8")
        link = self.root / "link.txt"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")

        snapshot = self.snapshot()
        link_item = next(item for item in snapshot["files"] if item["path"] == "link.txt")
        self.assertEqual(link_item["kind"], "symlink")
        self.assertEqual(link_item["target"], "target.txt")
        self.assertNotIn("sha256", link_item)

    def test_internal_symlink_policy_runs_without_platform_privilege(self) -> None:
        link = self.root / "nested" / "link.txt"
        link.parent.mkdir()
        with mock.patch.object(tree_snapshot.os, "readlink", return_value="../target.txt"):
            raw, target = tree_snapshot.safe_symlink_target(link, self.root.resolve())
        self.assertEqual(raw, "../target.txt")
        self.assertEqual(target, "target.txt")

    def test_root_relative_path_accepts_equivalent_alias_ancestor(self) -> None:
        root = Path("long-spelling") / "project"
        target = Path("short-spelling") / "project" / "nested" / "target.txt"

        def samefile(left: Path, right: Path) -> bool:
            return Path(left) == target.parents[1] and Path(right) == root

        with mock.patch.object(tree_snapshot.os.path, "samefile", side_effect=samefile):
            relative = tree_snapshot.relative_to_root(target, root)

        self.assertEqual(relative, Path("nested") / "target.txt")

    def test_external_symlink_is_rejected(self) -> None:
        outside = Path(self.temporary.name) / "outside.txt"
        outside.write_text("must not be read", encoding="utf-8")
        link = self.root / "escape.txt"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")

        with self.assertRaisesRegex(ValueError, "outside tree root"):
            self.snapshot()

    def test_external_symlink_policy_runs_without_platform_privilege(self) -> None:
        link = self.root / "escape.txt"
        outside = Path(self.temporary.name) / "outside.txt"
        with mock.patch.object(tree_snapshot.os, "readlink", return_value=str(outside)):
            with self.assertRaisesRegex(ValueError, "outside tree root"):
                tree_snapshot.safe_symlink_target(link, self.root.resolve())


if __name__ == "__main__":
    unittest.main()
