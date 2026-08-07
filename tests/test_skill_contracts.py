from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "spec-workflow": ROOT / "skills" / "spec-workflow",
    "drive-large-project": ROOT / "skills" / "drive-large-project",
    "organize-ai-project-files": ROOT / "skills" / "organize-ai-project-files",
}


def read_skill(name: str) -> str:
    return (SKILLS[name] / "SKILL.md").read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    try:
        raw = text.split("\n---\n", 1)[0][4:]
    except IndexError as exc:
        raise AssertionError("SKILL.md frontmatter is not closed") from exc
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


class SkillContractTests(unittest.TestCase):
    def test_exact_skill_set(self) -> None:
        actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(set(SKILLS), actual)

    def test_frontmatter_name_and_description(self) -> None:
        for name in SKILLS:
            with self.subTest(skill=name):
                values = frontmatter(read_skill(name))
                self.assertEqual(name, values.get("name"))
                self.assertGreater(len(values.get("description", "")), 80)
                self.assertEqual({"name", "description"}, set(values))

    def test_skills_stay_concise(self) -> None:
        for name in SKILLS:
            with self.subTest(skill=name):
                text = read_skill(name)
                self.assertLessEqual(len(text.splitlines()), 120)
                self.assertLessEqual(len(text.split()), 1_300)

    def test_no_heavy_process_markers(self) -> None:
        banned = (
            "<hard-gate>",
            "<extremely-important>",
            "1% chance",
            "you do not have a choice",
            "every project goes through this process",
            "ask questions one at a time",
        )
        for name in SKILLS:
            lowered = read_skill(name).casefold()
            with self.subTest(skill=name):
                for phrase in banned:
                    self.assertNotIn(phrase, lowered)

    def test_local_markdown_references_exist(self) -> None:
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for name, skill_dir in SKILLS.items():
            text = read_skill(name)
            for target in pattern.findall(text):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(skill=name, target=target):
                    self.assertTrue((skill_dir / target).is_file())

    def test_runtime_metadata_exists(self) -> None:
        for name, skill_dir in SKILLS.items():
            metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertIn("display_name:", metadata)
                self.assertIn("short_description:", metadata)
                self.assertIn("default_prompt:", metadata)

    def test_skill_folders_contain_no_repository_docs(self) -> None:
        banned_names = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md"}
        for name, skill_dir in SKILLS.items():
            actual = {path.name for path in skill_dir.iterdir() if path.is_file()}
            with self.subTest(skill=name):
                self.assertFalse(actual & banned_names)

    def test_matrix_handoffs_are_explicit(self) -> None:
        spec = read_skill("spec-workflow")
        drive = read_skill("drive-large-project")
        organize = read_skill("organize-ai-project-files")
        self.assertIn("drive-large-project", spec)
        self.assertIn("organize-ai-project-files", spec)
        self.assertIn("spec-workflow", drive)
        self.assertIn("organize-ai-project-files", drive)
        self.assertIn("spec-workflow", organize)
        self.assertIn("drive-large-project", organize)

    def test_small_tasks_remain_direct(self) -> None:
        self.assertIn("Skip for small", frontmatter(read_skill("spec-workflow"))["description"])
        self.assertIn("Skip for small", frontmatter(read_skill("drive-large-project"))["description"])
        self.assertIn("Simple placement", read_skill("organize-ai-project-files"))


if __name__ == "__main__":
    unittest.main()
