from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).parents[1]
    / "skills"
    / "drive-large-project"
    / "scripts"
    / "validate_continuity.py"
)


class ValidateContinuityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "项目"
        (self.root / "control").mkdir(parents=True)
        (self.root / "evidence").mkdir()
        (self.root / "evidence" / "验证.txt").write_text("passed", encoding="utf-8")
        self.write_ledger()
        self.write_handoff(
            "# 当前交接\n\n"
            "目标是继续可靠地完成当前项目，并保留可核验的进展。\n\n"
            "- AC-1：已验证，证据见验收账本。\n"
            "- AC-2：进行中，仍需完成真实运行路径。\n\n"
            "下一步：完成 AC-2 的运行验证并更新证据。\n"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_ledger(self, *, second_status: str = "in_progress") -> None:
        payload = {
            "items": [
                {
                    "id": "AC-1",
                    "title": "中文验证项",
                    "status": "verified",
                    "evidence": ["evidence/验证.txt"],
                    "gaps": [],
                },
                {
                    "id": "AC-2",
                    "title": "运行验证",
                    "status": second_status,
                    "evidence": [],
                    "gaps": ["需要真实运行"],
                },
            ]
        }
        (self.root / "control" / "acceptance.json").write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )

    def write_handoff(self, text: str) -> None:
        (self.root / "control" / "handoff.md").write_text(text, encoding="utf-8")

    def run_validator(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(self.root),
                "--formal-acceptance",
                "--acceptance",
                "control/acceptance.json",
                *extra,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def test_valid_ledger_and_chinese_paths_pass(self) -> None:
        result = self.run_validator(
            "--handoff",
            "control/handoff.md",
            "--handoff-ledger-check",
            "error",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Formal acceptance validation passed", result.stdout)

    def test_requires_explicit_formal_acceptance_mode(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(self.root),
                "--acceptance",
                "control/acceptance.json",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires --formal-acceptance", result.stderr)

    def test_invalid_status_fails(self) -> None:
        self.write_ledger(second_status="almost_done")
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid status", result.stderr)

    def test_missing_evidence_fails(self) -> None:
        (self.root / "evidence" / "验证.txt").unlink()
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("evidence file does not exist", result.stderr)

    def test_project_paths_reject_absolute_and_escape(self) -> None:
        outside = Path(self.temp_dir.name) / "outside.md"
        outside.write_text("outside " * 20, encoding="utf-8")

        cases = {
            "acceptance absolute": ["--acceptance", str(self.root / "control" / "acceptance.json")],
            "handoff absolute": ["--handoff", str(self.root / "control" / "handoff.md")],
            "index escape": ["--index", "../outside.md"],
        }
        for label, extra in cases.items():
            with self.subTest(label=label):
                base = [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(self.root),
                    "--formal-acceptance",
                    "--acceptance",
                    "control/acceptance.json",
                ]
                if label == "acceptance absolute":
                    base = base[:-2]
                result = subprocess.run(
                    [*base, *extra], capture_output=True, text=True, encoding="utf-8", check=False
                )
                self.assertEqual(result.returncode, 1)
                self.assertRegex(result.stderr, r"must be relative|escapes project root")

    def test_evidence_paths_reject_absolute_and_escape(self) -> None:
        cases = (
            (str(self.root / "evidence" / "验证.txt"), "must be relative"),
            ("../../outside.txt", "escapes project root"),
        )
        for evidence_value, expected in cases:
            with self.subTest(evidence=evidence_value):
                self.write_ledger()
                ledger_path = self.root / "control" / "acceptance.json"
                payload = json.loads(ledger_path.read_text(encoding="utf-8"))
                payload["items"][0]["evidence"] = [evidence_value]
                ledger_path.write_text(json.dumps(payload), encoding="utf-8")
                result = self.run_validator()
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)

    def test_stale_handoff_warns_or_fails_by_selected_mode(self) -> None:
        self.write_handoff(
            "# Current handoff\n\n"
            "This handoff preserves enough current project context for a reliable resume.\n\n"
            "- AC-2: complete\n\n"
            "Next action: publish the already completed work after one final review.\n"
        )
        warned = self.run_validator(
            "--handoff", "control/handoff.md", "--handoff-ledger-check", "warn"
        )
        self.assertEqual(warned.returncode, 0, warned.stderr)
        self.assertIn("AC-2: unfinished item is explicitly presented as complete", warned.stdout)

        failed = self.run_validator(
            "--handoff", "control/handoff.md", "--handoff-ledger-check", "error"
        )
        self.assertEqual(failed.returncode, 1)
        self.assertIn("handoff ledger: AC-2", failed.stderr)

    def test_verified_item_explicitly_presented_as_pending_fails(self) -> None:
        self.write_handoff(
            "# Current handoff\n\n"
            "This handoff preserves enough current project context for a reliable resume.\n\n"
            "- AC-1: pending and not verified.\n"
            "- AC-2: in progress with runtime evidence still missing.\n\n"
            "Next action: reconcile acceptance state against the evidence ledger.\n"
        )
        result = self.run_validator(
            "--handoff", "control/handoff.md", "--handoff-ledger-check", "error"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("AC-1: verified item is explicitly presented as unfinished", result.stderr)

    def test_negated_completion_does_not_trigger_false_positive(self) -> None:
        self.write_handoff(
            "# Current handoff\n\n"
            "This handoff preserves enough current project context for a reliable resume.\n\n"
            "- AC-1: verified with evidence.\n"
            "- AC-2: not complete; runtime evidence remains pending.\n\n"
            "Next action: run AC-2 through the real user path and capture evidence.\n"
        )
        result = self.run_validator(
            "--handoff", "control/handoff.md", "--handoff-ledger-check", "error"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_semantic_check_requires_handoff(self) -> None:
        result = self.run_validator("--handoff-ledger-check", "warn")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires --handoff", result.stderr)

    def test_short_native_handoff_and_index_are_allowed(self) -> None:
        self.write_handoff("# Now\n\nContinue A.")
        (self.root / "control" / "index.md").write_text("# Map\n", encoding="utf-8")
        result = self.run_validator(
            "--handoff",
            "control/handoff.md",
            "--index",
            "control/index.md",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("too short", result.stdout + result.stderr)

    def test_canonical_handoff_hygiene_warns_or_fails_in_strict_mode(self) -> None:
        self.write_handoff(
            "# Project handoff\n\n"
            "## Current state\nEnough current detail exists to resume the active project safely.\n\n"
            "## Current outcome and stage\nThe same current state is duplicated here.\n\n"
            "## Exact next action\nRun the focused verification.\n\n"
            "## Next action\nPublish after verification.\n\n"
            "## Closed history\nOld test runs and completed tasks remain in the hot handoff.\n"
        )
        warned = self.run_validator("--handoff", "control/handoff.md")
        self.assertEqual(warned.returncode, 0, warned.stderr)
        self.assertIn("canonical current-state sections", warned.stdout)
        self.assertIn("canonical next-action sections", warned.stdout)
        self.assertIn("explicit closed-history section", warned.stdout)

        failed = self.run_validator(
            "--handoff", "control/handoff.md", "--strict-context"
        )
        self.assertEqual(failed.returncode, 1)
        self.assertIn("context budget: handoff has 2 canonical next-action sections", failed.stderr)

    def test_custom_handoff_does_not_trigger_semantic_guessing(self) -> None:
        self.write_handoff(
            "# 恢复入口\n\n"
            "## 工作焦点\n当前证据足以继续这个项目。\n\n"
            "## 候选动作\n先验证接口，再根据结果选择后续动作。\n\n"
            "历史基线只是普通正文中的说明，不应被猜测成独立章节。\n"
        )
        result = self.run_validator(
            "--handoff", "control/handoff.md", "--strict-context"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("canonical", result.stdout + result.stderr)

    def test_template_headings_inside_fence_are_not_handoff_sections(self) -> None:
        self.write_handoff(
            "# Current handoff\n\n"
            "The active project state is described here with enough detail to resume safely.\n\n"
            "```markdown\n## Exact next action\n## Next action\n## Closed history\n```\n\n"
            "The fenced headings are a documentation example, not active handoff sections.\n"
        )
        result = self.run_validator(
            "--handoff", "control/handoff.md", "--strict-context"
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
