from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvalCatalogTests(unittest.TestCase):
    def test_catalog_shape_and_coverage(self) -> None:
        payload = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual("1.0", payload.get("schemaVersion"))
        cases = payload.get("cases")
        self.assertIsInstance(cases, list)
        self.assertGreaterEqual(len(cases), 18)

        ids = [case.get("id") for case in cases]
        self.assertEqual(len(ids), len(set(ids)))

        target_counts = Counter(case.get("target") for case in cases)
        self.assertEqual(
            {"spec-workflow", "drive-large-project", "organize-ai-project-files"},
            set(target_counts),
        )
        for target, count in target_counts.items():
            with self.subTest(target=target):
                self.assertGreaterEqual(count, 6)

        kind_counts = Counter(case.get("kind") for case in cases)
        for kind in ("positive", "negative", "pressure"):
            self.assertGreaterEqual(kind_counts[kind], 3)

        for case in cases:
            with self.subTest(case=case.get("id")):
                self.assertIsInstance(case.get("prompt"), str)
                self.assertGreater(len(case["prompt"]), 20)
                self.assertIsInstance(case.get("success"), list)
                self.assertGreaterEqual(len(case["success"]), 2)
                self.assertIsInstance(case.get("failure"), list)
                self.assertGreaterEqual(len(case["failure"]), 1)


if __name__ == "__main__":
    unittest.main()
