#!/usr/bin/env python3
"""Read-only audit for an AI-collaboration project layout contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROLE_KEYS = (
    "developmentRoots",
    "outputRoots",
    "engineeringOutputs",
    "candidateOutputs",
    "formalReleases",
    "referenceRoots",
    "userAssetRoots",
    "ephemeralRoots",
)
CANDIDATE_MARKERS = ("candidate", "pending", "unverified", "候选", "待验收", "未验收")
SOURCE_MARKERS = {".git", "src", "specs", "acceptance", "tests", "node_modules"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Project root")
    parser.add_argument("--config", required=True, help="PROJECT_LAYOUT.json path")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("layout contract must be a JSON object")
    return value


def within(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("layout paths must be non-empty strings")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes project root: {relative}") from exc
    return candidate


def is_under(path: Path, parents: list[Path]) -> bool:
    for parent in parents:
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            continue
    return False


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    config_path = Path(args.config).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"error: project root does not exist: {root}", file=sys.stderr)
        return 2

    try:
        contract = load_json(config_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: cannot load layout contract: {exc}", file=sys.stderr)
        return 2

    if contract.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be 1.0")
    if contract.get("topology") not in {"single-repository", "shell-root"}:
        errors.append("topology must be single-repository or shell-root")

    roles = contract.get("roles")
    if not isinstance(roles, dict):
        errors.append("roles must be an object")
        roles = {}

    resolved_roles: dict[str, list[Path]] = {}
    relative_roles: dict[str, list[str]] = {}
    for key in ROLE_KEYS:
        raw = roles.get(key, [])
        if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
            errors.append(f"roles.{key} must be an array of strings")
            raw = []
        relative_roles[key] = raw
        paths: list[Path] = []
        for item in raw:
            try:
                path = within(root, item)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            paths.append(path)
            if key != "ephemeralRoots" and not path.exists():
                errors.append(f"declared path does not exist: {item}")
            elif key == "ephemeralRoots" and not path.exists():
                warnings.append(f"ephemeral path is currently absent: {item}")
        resolved_roles[key] = paths

    development = resolved_roles.get("developmentRoots", [])
    outputs = resolved_roles.get("outputRoots", [])
    for dev_path in development:
        for output_path in outputs:
            if is_under(dev_path, [output_path]) or is_under(output_path, [dev_path]):
                errors.append(
                    f"development and output roots overlap: "
                    f"{dev_path.relative_to(root)} / {output_path.relative_to(root)}"
                )

    for key in ("engineeringOutputs", "candidateOutputs", "formalReleases"):
        for path in resolved_roles.get(key, []):
            if outputs and not is_under(path, outputs):
                errors.append(f"{key} path is outside outputRoots: {path.relative_to(root)}")

    for relative in relative_roles.get("candidateOutputs", []):
        lowered = relative.casefold()
        if not any(marker in lowered for marker in CANDIDATE_MARKERS):
            warnings.append(f"candidate output lacks explicit candidate wording: {relative}")

    entry_files = contract.get("entryFiles", [])
    hot_files = contract.get("hotFiles", [])
    for label, values in (("entryFiles", entry_files), ("hotFiles", hot_files)):
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            errors.append(f"{label} must be an array of strings")
            continue
        for relative in values:
            try:
                path = within(root, relative)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if not path.is_file():
                errors.append(f"required {label} file does not exist: {relative}")

    allowed = contract.get("allowedRootEntries", [])
    if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
        errors.append("allowedRootEntries must be an array of strings")
        allowed = []
    actual_root_entries = sorted(item.name for item in root.iterdir())
    unclassified = sorted(set(actual_root_entries) - set(allowed))
    for name in unclassified:
        warnings.append(f"unclassified root entry: {name}")

    evidence = contract.get("releaseEvidence", {})
    if not isinstance(evidence, dict):
        errors.append("releaseEvidence must be an object")
        evidence = {}
    for release in relative_roles.get("formalReleases", []):
        items = evidence.get(release)
        if not isinstance(items, list) or not items:
            errors.append(f"formal release has no declared evidence: {release}")
            continue
        for relative in items:
            if not isinstance(relative, str):
                errors.append(f"release evidence must be a string: {release}")
                continue
            try:
                path = within(root, relative)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if not path.is_file():
                errors.append(f"formal release evidence does not exist: {relative}")

    for release_path in resolved_roles.get("formalReleases", []):
        if not release_path.is_dir():
            continue
        for child in release_path.rglob("*"):
            if child.name in SOURCE_MARKERS:
                warnings.append(
                    f"formal release contains source/control marker: "
                    f"{child.relative_to(root)}"
                )

    result = {
        "root": str(root),
        "config": str(config_path),
        "topology": contract.get("topology"),
        "errors": errors,
        "warnings": warnings,
        "unclassifiedRootEntries": unclassified,
        "rootEntryCount": len(actual_root_entries),
        "roleCounts": {key: len(relative_roles.get(key, [])) for key in ROLE_KEYS},
        "passed": not errors,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Layout audit: {'PASS' if not errors else 'FAIL'}")
        print(f"Root: {root}")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARNING: {message}")
        print(
            f"Summary: {len(errors)} error(s), {len(warnings)} warning(s), "
            f"{len(unclassified)} unclassified root entrie(s)"
        )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
