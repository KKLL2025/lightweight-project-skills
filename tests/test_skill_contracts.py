from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "align-project-requirements": ROOT / "skills" / "align-project-requirements",
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
                self.assertLessEqual(len(text.splitlines()), 220)
                self.assertLessEqual(len(text.split()), 1_800)

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
                self.assertIn("$" + name, metadata)

    def test_skill_folders_contain_no_repository_docs(self) -> None:
        banned_names = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md"}
        for name, skill_dir in SKILLS.items():
            actual = {path.name for path in skill_dir.iterdir() if path.is_file()}
            with self.subTest(skill=name):
                self.assertFalse(actual & banned_names)

    def test_matrix_handoffs_are_explicit(self) -> None:
        spec = read_skill("align-project-requirements")
        drive = read_skill("drive-large-project")
        organize = read_skill("organize-ai-project-files")
        self.assertIn("drive-large-project", spec)
        self.assertIn("organize-ai-project-files", spec)
        self.assertIn("align-project-requirements", drive)
        self.assertIn("organize-ai-project-files", drive)
        self.assertIn("align-project-requirements", organize)
        self.assertIn("drive-large-project", organize)

    def test_small_tasks_remain_direct(self) -> None:
        self.assertIn(
            "Skip when the goal and expected result are already clear enough for direct execution",
            frontmatter(read_skill("align-project-requirements"))["description"],
        )
        self.assertIn(
            "Skip when normal Agent execution is sufficient",
            frontmatter(read_skill("drive-large-project"))["description"],
        )
        self.assertIn("Do not use for ordinary implementation", frontmatter(read_skill("organize-ai-project-files"))["description"])

    def test_bounded_turns_preserve_progress_without_extra_gates(self) -> None:
        drive = read_skill("drive-large-project")
        required = (
            "At the beginning of a Turn, select a bounded batch",
            "Necessary adjustments inside the same outcome are allowed",
            "do not repeatedly redefine the batch to absorb the next major outcome",
            "update the Handoff when useful",
            "end the Turn and return control to the user",
            "Checks should be triggered by reality, not by workflow position",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, drive)

        self.assertIn("`drive-large-project` owns the mutable execution route", read_skill("align-project-requirements"))

    def test_alignment_hands_off_execution_and_trust_boundaries(self) -> None:
        alignment = read_skill("align-project-requirements")
        for phrase in (
            "underlying problem and intended result",
            "Ask when a reasonable difference in the answer would materially change the project direction or result",
            "Batch related questions when practical",
            "This is a working baseline, not a frozen contract",
            "use `drive-large-project`",
            "use `organize-ai-project-files`",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, alignment)

    def test_layout_trigger_rejects_unrelated_audits(self) -> None:
        organize = read_skill("organize-ai-project-files")
        description = frontmatter(read_skill("organize-ai-project-files"))["description"]
        self.assertIn("Do not use for ordinary implementation", description)
        self.assertIn("Do not reorganize by guesswork", organize)
        self.assertIn("Do not turn cleanup into a full-project inventory or audit", organize)
        self.assertIn("Do not reorganize stable areas simply because another naming scheme looks better", organize)

    def test_execution_reference_preserves_adaptive_routing_and_validation(self) -> None:
        reference = (
            SKILLS["drive-large-project"] / "references" / "execution-control.md"
        ).read_text(encoding="utf-8").casefold()
        for phrase in (
            "maintain two planning levels",
            "switch modules for a reason",
            "derive security validation from the active threat model",
            "do not prescribe a fixed candidate count",
            "do not repeat an unchanged full test suite",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, reference)

    def test_ownership_and_handoffs_are_explicit(self) -> None:
        alignment = read_skill("align-project-requirements")
        drive = read_skill("drive-large-project")
        organize = read_skill("organize-ai-project-files")

        self.assertIn("`drive-large-project` owns the mutable execution route", alignment)
        self.assertIn("`align-project-requirements` owns understanding the user's real need", drive)
        self.assertIn("`organize-ai-project-files` owns project directory topology", drive)
        self.assertIn("`align-project-requirements` decides what the project should become", organize)
        self.assertIn("`drive-large-project` decides what execution context needs to survive", organize)

    def test_bounded_batches_allow_small_related_steps(self) -> None:
        drive = read_skill("drive-large-project")
        self.assertIn("A Turn is an execution batch, not a synonym for a milestone", drive)
        self.assertIn("several closely related small steps", drive)
        self.assertIn("one coherent part of a difficult milestone", drive)
        self.assertIn("Necessary adjustments inside the same outcome are allowed", drive)
        self.assertIn("do not repeatedly redefine the batch to absorb the next major outcome", drive)

    def test_progress_refresh_uses_observable_events_not_timers_or_counts(self) -> None:
        drive = read_skill("drive-large-project").casefold()
        self.assertIn("do not automatically repeat checks", drive)
        self.assertIn("recheck something when the active work depends on a fact that may reasonably have changed", drive)
        self.assertIn("checks should be triggered by reality, not by workflow position", drive)
        self.assertIn("do not add a separate review cycle merely to maintain it", drive)
        for banned in ("30-minute", "30 minutes", "every 30", "after five compactions", "compaction_count"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, drive)


if __name__ == "__main__":
    unittest.main()
