import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.7.0"


class RepositoryHealthTests(unittest.TestCase):
    def test_required_community_files_exist(self):
        required = [
            "README.md",
            "README.zh-CN.md",
            "LICENSE",
            "THIRD_PARTY_NOTICES.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SUPPORT.md",
            ".github/CODEOWNERS",
            ".github/dependabot.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/case_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            ".github/workflows/ci.yml",
        ]
        missing = [name for name in required if not (ROOT / name).is_file()]
        self.assertEqual(missing, [])

    def test_upstream_attribution_is_preserved(self):
        notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("align-project-requirements", notices)
        self.assertIn("TencentCloudBase/CloudBase-AI-Toolkit", notices)
        self.assertIn("Copyright (c) 2025 Tencent CloudBase", notices)
        self.assertIn("MIT License", notices)

    def test_version_is_consistent(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, EXPECTED_VERSION)
        for name in ("README.md", "README.zh-CN.md", "CHANGELOG.md"):
            content = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn(EXPECTED_VERSION, content, name)

    def test_public_skill_entries_are_documented(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in (
            "align-project-requirements",
            "drive-large-project",
            "organize-ai-project-files",
        ):
            skill = ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(skill.is_file(), str(skill))
            self.assertIn("skills/{}/SKILL.md".format(name), readme)

    def test_retired_skill_name_is_not_an_active_entry(self):
        self.assertFalse((ROOT / "skills" / "spec-workflow").exists())
        active_surfaces = [
            "README.md",
            "README.zh-CN.md",
            "examples/README.md",
            "evals/cases.json",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/case_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
        ]
        for name in active_surfaces:
            content = (ROOT / name).read_text(encoding="utf-8")
            if name.startswith("README"):
                content = "\n".join(
                    line
                    for line in content.splitlines()
                    if not (
                        "v0.4.0-preview" in line
                        and "spec-workflow" in line
                        and "align-project-requirements" in line
                    )
                )
            self.assertNotIn("spec-workflow", content, name)

    def test_local_markdown_links_resolve(self):
        link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
        missing = []
        for document in ROOT.rglob("*.md"):
            text = document.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(text):
                target = raw_target.strip().split(" ", 1)[0].strip("<>")
                if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                local_part = unquote(target.split("#", 1)[0])
                if not local_part:
                    continue
                resolved = (document.parent / local_part).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    missing.append("{} -> {} (outside repository)".format(document.relative_to(ROOT), target))
                    continue
                if not resolved.exists():
                    missing.append("{} -> {}".format(document.relative_to(ROOT), target))
        self.assertEqual(missing, [])

    def test_text_files_are_utf8_and_do_not_leak_private_material(self):
        text_suffixes = {".md", ".py", ".json", ".yml", ".yaml", ".txt"}
        forbidden = [
            "C:" + "\\Users\\",
            "Documents" + "\\Codex",
            "internal" + "-audit-report",
            "backup" + "-before-install",
            "work" + "/fixtures",
        ]
        findings = []
        candidates = [path for path in ROOT.rglob("*") if path.is_file()]
        for path in candidates:
            if path.suffix.lower() not in text_suffixes and path.name != "VERSION":
                continue
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                if marker.lower() in text.lower():
                    findings.append("{}: {}".format(path.relative_to(ROOT), marker))
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
