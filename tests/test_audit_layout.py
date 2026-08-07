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
    paths = (
        "03-project-workspace/product",
        "03-project-workspace/outputs/engineering",
        "03-project-workspace/outputs/candidates",
        "02-project-control/research",
        "02-project-control/history",
        "03-project-workspace/assets/source",
        "03-project-workspace/data/input",
        "03-project-workspace/temp",
        "02-project-control/continuity",
        "02-project-control/layout",
    )
    for relative in paths:
        (project / relative).mkdir(parents=True, exist_ok=True)
    for relative in (
        "AGENTS.md",
        "README.md",
        "02-project-control/continuity/PROJECT_INDEX.md",
        "02-project-control/continuity/PROJECT_HANDOFF.md",
    ):
        (project / relative).write_text("x" * 100, encoding="utf-8")

    contract = {
        "schemaVersion": "1.0",
        "topology": "shell-root",
        "roles": {
            "developmentRoots": ["03-project-workspace/product"],
            "outputRoots": ["03-project-workspace/outputs"],
            "engineeringOutputs": ["03-project-workspace/outputs/engineering"],
            "candidateOutputs": ["03-project-workspace/outputs/candidates"],
            "formalReleases": [],
            "referenceRoots": ["02-project-control/research", "02-project-control/history"],
            "userAssetRoots": ["03-project-workspace/assets/source", "03-project-workspace/data/input"],
            "ephemeralRoots": ["03-project-workspace/temp"],
        },
        "entryFiles": ["AGENTS.md", "README.md"],
        "hotFiles": [
            "02-project-control/continuity/PROJECT_INDEX.md",
            "02-project-control/continuity/PROJECT_HANDOFF.md",
        ],
        "allowedRootEntries": [
            "AGENTS.md",
            "README.md",
            "02-project-control",
            "03-project-workspace",
        ],
        "releaseEvidence": {},
    }
    config = project / "02-project-control" / "layout" / "PROJECT_LAYOUT.json"
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

    def test_formal_release_requires_declared_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, contract = make_project(Path(tmp))
            release = project / "03-project-workspace" / "outputs" / "releases" / "v1"
            release.mkdir(parents=True)
            contract["roles"]["formalReleases"] = [
                "03-project-workspace/outputs/releases/v1"
            ]
            config.write_text(json.dumps(contract), encoding="utf-8")
            result = run_audit(project, config)
            self.assertEqual(1, result.returncode)
            self.assertIn("formal release has no declared evidence", result.stdout)

    def test_unclassified_root_entry_is_review_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project, config, _ = make_project(Path(tmp))
            (project / "mystery.bin").write_bytes(b"unknown")
            result = run_audit(project, config)
            self.assertEqual(0, result.returncode)
            payload = json.loads(result.stdout)
            self.assertIn("mystery.bin", payload["unclassifiedRootEntries"])
            self.assertTrue(any("unclassified root entry" in item for item in payload["warnings"]))


if __name__ == "__main__":
    unittest.main()
