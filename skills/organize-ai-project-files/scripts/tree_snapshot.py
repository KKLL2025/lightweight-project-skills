#!/usr/bin/env python3
"""Create or compare snapshots for high-risk moves that need preservation evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_EXCLUDES = (".git", ".codex-tmp", "node_modules")
CRITICAL_EXTENSIONS = {
    ".7z",
    ".dll",
    ".exe",
    ".go",
    ".gz",
    ".ini",
    ".js",
    ".json",
    ".lock",
    ".md",
    ".msi",
    ".ps1",
    ".py",
    ".rar",
    ".sha256",
    ".tar",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
    ".zip",
}


def common_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", required=True, help="Tree root")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Relative path prefix to exclude; compare also retains all baseline exclusions",
    )
    parser.add_argument(
        "--hash-mode",
        choices=("none", "critical", "all"),
        default=None,
        help=(
            "Hash no files, critical files, or all files; create defaults to none, "
            "compare inherits the before snapshot"
        ),
    )
    parser.add_argument(
        "--critical-max-mib",
        type=int,
        default=512,
        help="Maximum size hashed in critical mode",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="Create a snapshot")
    common_parser(create)
    create.add_argument("--output", required=True, help="Snapshot JSON path")

    compare = commands.add_parser("compare", help="Compare a snapshot with a tree")
    common_parser(compare)
    compare.add_argument("--before", required=True, help="Before snapshot JSON")
    compare.add_argument(
        "--path-mode",
        choices=("exact", "content"),
        default="content",
        help="Require exact paths or compare content identities",
    )
    compare.add_argument("--json", action="store_true", help="Emit JSON only")
    return parser.parse_args()


def normalize_prefix(value: str) -> str:
    # Accept either separator regardless of the host running the audit.
    return value.replace("\\", "/").strip("/")


def excluded(relative: str, prefixes: Iterable[str]) -> bool:
    normalized_path = Path(relative)
    normalized = normalized_path.as_posix()
    parts = set(normalized_path.parts)
    for prefix in prefixes:
        if "/" not in prefix and prefix in parts:
            return True
        if normalized == prefix or normalized.startswith(prefix + "/"):
            return True
    return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def relative_to_root(path: Path, root: Path) -> Path | None:
    """Return a contained relative path, including Windows alias spellings."""
    try:
        return path.relative_to(root)
    except ValueError:
        pass

    # Windows can expose the same directory through a long path and an 8.3 or
    # ``\\?\`` spelling. Walk existing ancestors and compare file identity so
    # an alias does not turn an in-root link into a false path-escape report.
    parts: list[str] = []
    candidate = path
    while True:
        try:
            if os.path.samefile(candidate, root):
                return Path(*reversed(parts))
        except OSError:
            # Broken leaf targets are allowed when an existing parent can
            # still establish containment.
            pass
        parent = candidate.parent
        if parent == candidate:
            return None
        parts.append(candidate.name)
        candidate = parent


def safe_symlink_target(path: Path, root: Path) -> tuple[str, str]:
    """Return raw and root-relative targets without opening target content."""
    raw_target = os.readlink(path)
    target_path = Path(raw_target)
    if not target_path.is_absolute():
        target_path = path.parent / target_path
    try:
        resolved_target = target_path.resolve(strict=False)
    except RuntimeError as exc:
        raise ValueError(f"cannot resolve symlink safely: {path}: {exc}") from exc
    relative_target = relative_to_root(resolved_target, root)
    if relative_target is None:
        link_relative = relative_to_root(path, root)
        relative = link_relative.as_posix() if link_relative is not None else path.name
        raise ValueError(
            f"symlink points outside tree root: {relative} -> {raw_target}"
        )
    return raw_target, relative_target.as_posix()


def iter_tree(root: Path, prefixes: list[str]) -> Iterable[tuple[Path, str]]:
    """Yield regular files and safe in-root links without following symlinks."""

    def walk(directory: Path) -> Iterable[tuple[Path, str]]:
        with os.scandir(directory) as entries:
            ordered = sorted(
                entries, key=lambda entry: (entry.name.casefold(), entry.name)
            )
        for entry in ordered:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if excluded(relative, prefixes):
                continue
            if entry.is_symlink():
                # The caller records the link itself and never traverses it.
                yield path, "symlink"
                continue
            entry_stat = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(entry_stat.st_mode):
                yield from walk(path)
            elif stat.S_ISREG(entry_stat.st_mode):
                yield path, "file"
            else:
                raise ValueError(f"unsupported filesystem entry: {relative}")

    yield from walk(root)


def should_hash(path: Path, size: int, mode: str, critical_max: int) -> bool:
    if mode == "all":
        return True
    if mode == "none":
        return False
    return path.suffix.casefold() in CRITICAL_EXTENSIONS and size <= critical_max


def build_snapshot(
    root: Path,
    excludes: list[str],
    hash_mode: str,
    critical_max_mib: int,
) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"tree root does not exist: {root}")
    if type(critical_max_mib) is not int or critical_max_mib <= 0:
        raise ValueError("critical-max-mib must be a positive integer")
    prefixes = list(dict.fromkeys(normalize_prefix(value) for value in (*DEFAULT_EXCLUDES, *excludes)))
    critical_max = critical_max_mib * 1024 * 1024
    files: list[dict[str, Any]] = []
    total_bytes = 0

    for path, kind in iter_tree(root, prefixes):
        relative = path.relative_to(root).as_posix()
        if kind == "symlink":
            link_target, resolved_target = safe_symlink_target(path, root)
            encoded_target = os.fsencode(link_target)
            files.append(
                {
                    "path": relative,
                    "name": path.name,
                    "kind": "symlink",
                    "bytes": len(encoded_target),
                    "target": resolved_target,
                }
            )
            total_bytes += len(encoded_target)
            continue

        path_stat = os.stat(path, follow_symlinks=False)
        item: dict[str, Any] = {
            "path": relative,
            "name": path.name,
            "kind": "file",
            "bytes": path_stat.st_size,
            "mtimeNs": path_stat.st_mtime_ns,
        }
        if should_hash(path, path_stat.st_size, hash_mode, critical_max):
            item["sha256"] = sha256(path)
        files.append(item)
        total_bytes += path_stat.st_size

    return {
        "schemaVersion": "1.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "hashMode": hash_mode,
        "criticalMaxMiB": critical_max_mib,
        "excludes": prefixes,
        "snapshotOutputPath": None,
        "fileCount": len(files),
        "totalBytes": total_bytes,
        "files": files,
    }


def load_snapshot(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict) or value.get("schemaVersion") != "1.0":
        raise ValueError("unsupported snapshot schema")
    if not isinstance(value.get("files"), list):
        raise ValueError("snapshot files must be an array")
    excludes = value.get("excludes", [])
    if not isinstance(excludes, list) or not all(isinstance(item, str) for item in excludes):
        raise ValueError("snapshot excludes must be an array of strings")
    if value.get("hashMode", "none") not in ("none", "critical", "all"):
        raise ValueError("snapshot hashMode must be none, critical, or all")
    critical_max = value.get("criticalMaxMiB", 512)
    if type(critical_max) is not int or critical_max <= 0:
        raise ValueError("snapshot criticalMaxMiB must be a positive integer")
    output_path = value.get("snapshotOutputPath")
    if output_path is not None and (not isinstance(output_path, str) or not output_path.strip()):
        raise ValueError("snapshotOutputPath must be a non-empty string or null")
    seen_paths: set[str] = set()
    for item in value["files"]:
        if not isinstance(item, dict):
            raise ValueError("snapshot file entries must be objects")
        if not isinstance(item.get("path"), str) or not item["path"]:
            raise ValueError("snapshot file paths must be non-empty strings")
        if item["path"] in seen_paths:
            raise ValueError(f"duplicate snapshot path: {item['path']}")
        seen_paths.add(item["path"])
        if item.get("kind", "file") not in ("file", "symlink"):
            raise ValueError("snapshot entry kind must be file or symlink")
        if type(item.get("bytes")) is not int or item["bytes"] < 0:
            raise ValueError("snapshot entry bytes must be a non-negative integer")
        if item.get("kind") == "symlink":
            if not isinstance(item.get("target"), str) or not item["target"]:
                raise ValueError("snapshot symlink targets must be non-empty strings")
        elif "sha256" in item:
            digest = item["sha256"]
            if not isinstance(digest, str) or len(digest) != 64 or any(
                char not in "0123456789abcdefABCDEF" for char in digest
            ):
                raise ValueError("snapshot sha256 must be a 64-character hexadecimal string")
            item["sha256"] = digest.upper()
        elif type(item.get("mtimeNs")) is not int:
            raise ValueError("unhashed snapshot entries require integer mtimeNs")
    if type(value.get("fileCount")) is not int or value["fileCount"] != len(value["files"]):
        raise ValueError("snapshot fileCount must match its file entries")
    if type(value.get("totalBytes")) is not int or value["totalBytes"] != sum(
        item["bytes"] for item in value["files"]
    ):
        raise ValueError("snapshot totalBytes must match its file entries")
    return value


def comparison_exclusions(
    before: dict[str, Any], before_path: Path, root: Path, extra: list[str]
) -> list[str]:
    """Retain user exclusions; ignore an automatic output only while it is the snapshot."""
    root = root.resolve()
    baseline = list(before.get("excludes", []))
    output_relative = before.get("snapshotOutputPath")
    if "snapshotOutputPath" not in before:
        # Legacy files mixed the output path into their exclusion list.
        old_root = before.get("root")
        try:
            inferred = before_path.relative_to(Path(old_root).resolve()).as_posix() if isinstance(old_root, str) else None
        except (OSError, RuntimeError, ValueError):
            inferred = None
        if inferred in baseline:
            baseline.remove(inferred)
            output_relative = inferred
    exclusions = [*baseline, *extra]
    candidates = [before_path]
    if output_relative is not None:
        candidates.append(root / output_relative)
    for candidate in candidates:
        if candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve()
            relative = resolved.relative_to(root).as_posix()
        except ValueError:
            continue
        if excluded(relative, exclusions) or not resolved.is_file():
            continue
        if os.path.samefile(resolved, before_path) or (
            resolved.stat().st_size == before_path.stat().st_size
            and sha256(resolved) == sha256(before_path)
        ):
            exclusions.append(relative)
    return exclusions


def fingerprint(item: dict[str, Any], path_mode: str) -> tuple[Any, ...]:
    kind = item.get("kind", "file")
    if kind == "symlink":
        content = ("symlink", item.get("target"))
    elif item.get("sha256"):
        content = ("file", item.get("bytes"), item.get("sha256"))
    else:
        # Metadata is useful for a diagnostic diff, but is not proof of content.
        content = ("unhashed-file", item.get("bytes"), item.get("mtimeNs"))
    if path_mode == "exact":
        return (item.get("path"),) + content
    return content


def unhashed_file_count(snapshot: dict[str, Any]) -> int:
    return sum(
        1
        for item in snapshot["files"]
        if item.get("kind", "file") == "file" and not item.get("sha256")
    )


def summarize_counter(counter: Counter[tuple[Any, ...]]) -> list[dict[str, Any]]:
    result = []
    for key, count in counter.most_common(25):
        result.append({"fingerprint": list(key), "count": count})
    return result


def main() -> int:
    args = parse_args()
    try:
        if args.command == "create":
            output = Path(args.output).resolve()
            excludes = list(args.exclude)
            root = Path(args.root).resolve()
            output_relative = None
            try:
                output_relative = output.relative_to(root).as_posix()
                excludes.append(output_relative)
            except ValueError:
                pass
            snapshot = build_snapshot(
                root,
                excludes,
                args.hash_mode or "none",
                args.critical_max_mib,
            )
            # Automatic snapshot output exclusion must not reserve this filename forever.
            snapshot["excludes"] = list(dict.fromkeys(
                normalize_prefix(value) for value in (*DEFAULT_EXCLUDES, *args.exclude)
            ))
            snapshot["snapshotOutputPath"] = output_relative
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("w", encoding="utf-8", newline="\n") as handle:
                json.dump(snapshot, handle, ensure_ascii=True, indent=2)
                handle.write("\n")
            print(
                f"Snapshot created: {snapshot['fileCount']} file(s), "
                f"{snapshot['totalBytes']} bytes -> {output}"
            )
            return 0

        before_path = Path(args.before).resolve()
        before = load_snapshot(before_path)
        effective_hash_mode = args.hash_mode
        if effective_hash_mode is None and before.get("hashMode") in {
            "none",
            "critical",
            "all",
        }:
            effective_hash_mode = before["hashMode"]
        if effective_hash_mode is None:
            effective_hash_mode = "none"
        after = build_snapshot(
            Path(args.root),
            comparison_exclusions(before, before_path, Path(args.root), list(args.exclude)),
            effective_hash_mode,
            int(before.get("criticalMaxMiB", args.critical_max_mib)),
        )
        before_counter = Counter(
            fingerprint(item, args.path_mode) for item in before["files"]
        )
        after_counter = Counter(
            fingerprint(item, args.path_mode) for item in after["files"]
        )
        missing = before_counter - after_counter
        added = after_counter - before_counter
        structural_equal = (
            before.get("fileCount") == after.get("fileCount")
            and before.get("totalBytes") == after.get("totalBytes")
            and not missing
            and not added
        )
        before_unhashed = unhashed_file_count(before)
        after_unhashed = unhashed_file_count(after)
        content_verified = before_unhashed == 0 and after_unhashed == 0
        # A metadata-only snapshot cannot prove preservation. Fail closed instead
        # of presenting same-name, same-size files as reliably equal.
        equal = structural_equal and content_verified
        result = {
            "equal": equal,
            "structuralEqual": structural_equal,
            "contentVerified": content_verified,
            "unhashedFiles": {
                "before": before_unhashed,
                "after": after_unhashed,
            },
            "pathMode": args.path_mode,
            "excludes": after["excludes"],
            "before": {
                "fileCount": before.get("fileCount"),
                "totalBytes": before.get("totalBytes"),
            },
            "after": {
                "fileCount": after.get("fileCount"),
                "totalBytes": after.get("totalBytes"),
            },
            "missing": summarize_counter(missing),
            "added": summarize_counter(added),
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=True, indent=2))
        else:
            if equal:
                status = "PASS"
            elif structural_equal and not content_verified:
                status = "UNVERIFIED (unhashed files)"
            else:
                status = "FAIL"
            print(f"Snapshot compare: {status}")
            print(
                f"Before: {result['before']['fileCount']} file(s), "
                f"{result['before']['totalBytes']} bytes"
            )
            print(
                f"After:  {result['after']['fileCount']} file(s), "
                f"{result['after']['totalBytes']} bytes"
            )
            if missing:
                print(f"Missing identities: {sum(missing.values())}")
            if added:
                print(f"Added identities: {sum(added.values())}")
        return 0 if equal else 1
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
