#!/usr/bin/env python3
"""Optionally check paths declared by an existing project layout contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROLE_KEYS = (
    "developmentRoots",
    "outputRoots",
    "referenceRoots",
    "userAssetRoots",
    "ephemeralRoots",
)


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

    entry_files = contract.get("entryFiles", [])
    if not isinstance(entry_files, list) or not all(isinstance(item, str) for item in entry_files):
        errors.append("entryFiles must be an array of strings")
    else:
        for relative in entry_files:
            try:
                path = within(root, relative)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if not path.is_file():
                errors.append(f"declared entry file does not exist: {relative}")

    actual_root_entries = sorted(item.name for item in root.iterdir())
    unclassified: list[str] = []
    if "allowedRootEntries" in contract:
        allowed = contract["allowedRootEntries"]
        if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
            errors.append("allowedRootEntries must be an array of strings")
        else:
            unclassified = sorted(set(actual_root_entries) - set(allowed))
            for name in unclassified:
                warnings.append(f"unclassified root entry: {name}")

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
