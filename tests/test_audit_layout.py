from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "organize-ai-project-files" / "scripts" / "audit_layout.py"


def make_project(base: Path) -> tuple[Path, Path, dict]:
    project = base / "项目"
    for relative in ("src", "outputs", "docs", "assets", "temp"):
        (project / relative).mkdir(parents=True, exist_ok=True)
    (project / "README.md").write_text("project entry", encoding="utf-8")

    contract = {
        "schemaVersion": "1.0",
        "topology": "single-repository",
        "roles": {
            "developmentRoots": ["src"],
            "outputRoots": ["outputs"],
            "referenceRoots": ["docs"],
            "userAssetRoots": ["assets"],
            "ephemeralRoots": ["temp"],
        },
        "entryFiles": ["README.md"],
        "allowedRootEntries": ["README.md", "assets", "docs", "outputs", "src", "temp"],
    }
    config = base / "PROJECT_LAYOUT.json"
    config.write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")
    return project, config, contract


def run_audit(project: Path, config: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(project), "--config", str(config), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


class AuditLayoutTests(unittest.TestCase):
    def test_valid_chinese_path_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, _ = make_project(Path(tmp))
            result = run_audit(project, config)
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["passed"])
            self.assertEqual([], payload["unclassifiedRootEntries"])

    def test_declared_path_cannot_escape_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, contract = make_project(Path(tmp))
            contract["roles"]["referenceRoots"] = ["../outside"]
            config.write_text(json.dumps(contract), encoding="utf-8")
            result = run_audit(project, config)
            self.assertEqual(1, result.returncode)
            self.assertIn("path escapes project root", result.stdout)

    def test_release_metadata_is_outside_layout_audit_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, contract = make_project(Path(tmp))
            contract["roles"]["formalReleases"] = ["outputs/releases/v1"]
            contract["releaseEvidence"] = "owned by another project mechanism"
            config.write_text(json.dumps(contract), encoding="utf-8")
            result = run_audit(project, config)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("formal release", result.stdout.casefold())

    def test_unclassified_root_entry_is_review_warning_when_allowlist_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, _ = make_project(Path(tmp))
            (project / "mystery.bin").write_bytes(b"unknown")
            result = run_audit(project, config)
            self.assertEqual(0, result.returncode)
            payload = json.loads(result.stdout)
            self.assertIn("mystery.bin", payload["unclassifiedRootEntries"])
            self.assertTrue(any("unclassified root entry" in item for item in payload["warnings"]))

    def test_root_is_not_inventoried_without_explicit_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, contract = make_project(Path(tmp))
            contract.pop("allowedRootEntries")
            config.write_text(json.dumps(contract), encoding="utf-8")
            (project / "mystery.bin").write_bytes(b"unknown")
            result = run_audit(project, config)
            self.assertEqual(0, result.returncode)
            payload = json.loads(result.stdout)
            self.assertEqual([], payload["unclassifiedRootEntries"])
            self.assertFalse(any("unclassified root entry" in item for item in payload["warnings"]))


if __name__ == "__main__":
    unittest.main()
