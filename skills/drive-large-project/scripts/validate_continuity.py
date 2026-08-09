#!/usr/bin/env python3
"""Validate a large-project acceptance ledger and optional handoff file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


ALLOWED_STATUSES = {
    "not_started",
    "in_progress",
    "blocked",
    "implemented_pending",
    "verified",
    "abandoned",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Project root")
    parser.add_argument("--acceptance", type=Path, required=True, help="Acceptance JSON path")
    parser.add_argument("--index", type=Path, help="Optional non-empty project document index")
    parser.add_argument("--handoff", type=Path, help="Optional non-empty handoff Markdown path")
    parser.add_argument("--max-handoff-lines", type=int, default=240)
    parser.add_argument("--max-handoff-chars", type=int, default=20_000)
    parser.add_argument(
        "--strict-context",
        action="store_true",
        help="Treat context-size and canonical handoff-hygiene warnings as errors",
    )
    parser.add_argument(
        "--handoff-ledger-check",
        choices=("off", "warn", "error"),
        default="off",
        help=(
            "Optionally compare acceptance IDs with the handoff: off (default), "
            "warn without failing, or error on findings"
        ),
    )
    return parser.parse_args()


def resolve_project_path(root: Path, value: Path, label: str, errors: list[str]) -> Path | None:
    """Resolve a project-relative path without allowing it to leave root."""
    if value.is_absolute():
        errors.append(f"{label} path must be relative to project root: {value}")
        return None

    try:
        candidate = (root / value).resolve()
    except (OSError, RuntimeError) as exc:
        errors.append(f"cannot resolve {label} path {value}: {exc}")
        return None
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"{label} path escapes project root: {value}")
        return None
    return candidate


def require_string(item: dict, key: str, item_id: str, errors: list[str]) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{item_id}: {key} must be a non-empty string")
        return ""
    return value.strip()


_NEGATED_COMPLETION = re.compile(
    r"\b(?:not|isn['’]?t|is\s+not|never)\s+(?:complete|completed|done|verified|passed|closed)\b"
    r"|\b(?:incomplete|pending|unfinished|unverified|blocked)\b"
    r"|(?:未完成|尚未完成|没有完成|未验证|待验证|进行中|已阻塞|被阻塞)",
    re.IGNORECASE,
)
_COMPLETION_WORD = (
    r"(?:complete|completed|done|verified|passed|closed|"
    r"已完成|完成|已验证|验收通过|已通过|已关闭)"
)

_CURRENT_SECTION_HEADINGS = {
    "current outcome and stage",
    "current state",
    "当前目标和阶段",
    "当前状态",
}
_NEXT_ACTION_HEADINGS = {
    "exact next action",
    "next action",
    "精确下一步",
    "下一步",
}
_CLOSED_HISTORY_HEADINGS = {
    "closed history",
    "closed-history",
    "closed chronology",
    "已关闭历史",
    "历史流水账",
    "完整时间线",
}


def _markdown_h2_headings(text: str) -> list[str]:
    """Return normalized level-two headings outside fenced code blocks."""
    headings: list[str] = []
    fence_marker: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue
        if fence_marker is not None:
            continue
        match = re.fullmatch(r"##\s+(.+?)\s*#*", stripped)
        if match:
            headings.append(re.sub(r"\s+", " ", match.group(1)).strip().casefold())
    return headings


def handoff_hygiene_findings(handoff_text: str) -> list[str]:
    """Check explicit canonical headings without guessing from prose."""
    headings = _markdown_h2_headings(handoff_text)
    findings: list[str] = []
    current_sections = sum(heading in _CURRENT_SECTION_HEADINGS for heading in headings)
    next_sections = sum(heading in _NEXT_ACTION_HEADINGS for heading in headings)
    closed_sections = [heading for heading in headings if heading in _CLOSED_HISTORY_HEADINGS]

    if current_sections > 1:
        findings.append(
            f"handoff has {current_sections} canonical current-state sections; keep one current owner"
        )
    if next_sections > 1:
        findings.append(
            f"handoff has {next_sections} canonical next-action sections; keep one exact next action"
        )
    if closed_sections:
        findings.append(
            "handoff contains an explicit closed-history section; move closed chronology to linked history"
        )
    return findings


def _id_pattern(item_id: str) -> str:
    return rf"(?<![\w.-]){re.escape(item_id)}(?![\w.-])"


def handoff_ledger_findings(items: list[dict], handoff_text: str) -> list[str]:
    """Find only explicit, ID-addressable handoff/ledger contradictions."""
    findings: list[str] = []
    lines = handoff_text.splitlines()

    for item in items:
        item_id = item.get("id")
        status = item.get("status")
        if not isinstance(item_id, str) or not item_id.strip() or status not in ALLOWED_STATUSES:
            continue

        item_id = item_id.strip()
        id_re = re.compile(_id_pattern(item_id), re.IGNORECASE)
        matching_lines = [line for line in lines if id_re.search(line)]

        if not matching_lines or status == "abandoned":
            continue

        if status == "verified":
            for line_number, line in enumerate(lines, start=1):
                if id_re.search(line) and _NEGATED_COMPLETION.search(line):
                    findings.append(
                        f"{item_id}: verified item is explicitly presented as unfinished "
                        f"in handoff line {line_number}"
                    )
                    break
            continue

        after_id = re.compile(
            _id_pattern(item_id)
            + rf"(?:\s*(?:[:：=|\-]|\b(?:is|status|state)\b)\s*|\s+)"
            + _COMPLETION_WORD
            + r"(?![A-Za-z])",
            re.IGNORECASE,
        )
        before_id = re.compile(
            _COMPLETION_WORD
            + rf"\s*(?:[:：=|\-])\s*{_id_pattern(item_id)}",
            re.IGNORECASE,
        )
        for line_number, line in enumerate(lines, start=1):
            if not id_re.search(line) or _NEGATED_COMPLETION.search(line):
                continue
            if after_id.search(line) or before_id.search(line):
                findings.append(
                    f"{item_id}: unfinished item is explicitly presented as complete "
                    f"in handoff line {line_number}"
                )
                break

    return findings


def validate() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    context_warnings: list[str] = []

    if not root.is_dir():
        errors.append(f"project root does not exist: {root}")
    acceptance_path = resolve_project_path(root, args.acceptance, "acceptance", errors)
    if acceptance_path is not None and not acceptance_path.is_file():
        errors.append(f"acceptance ledger does not exist: {acceptance_path}")
    if errors:
        return report(errors, warnings, Counter())

    assert acceptance_path is not None

    try:
        payload = json.loads(acceptance_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return report([f"cannot read acceptance ledger: {exc}"], warnings, Counter())

    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list) or not items:
        return report(["acceptance ledger must contain a non-empty items array"], warnings, Counter())

    seen_ids: set[str] = set()
    counts: Counter[str] = Counter()

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"item #{index}: must be an object")
            continue

        fallback_id = f"item #{index}"
        item_id = require_string(item, "id", fallback_id, errors) or fallback_id
        require_string(item, "title", item_id, errors)

        if item_id in seen_ids:
            errors.append(f"{item_id}: duplicate id")
        seen_ids.add(item_id)

        status = item.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{item_id}: invalid status {status!r}")
        else:
            counts[status] += 1

        evidence = item.get("evidence")
        gaps = item.get("gaps")
        if not isinstance(evidence, list) or not all(isinstance(x, str) and x.strip() for x in evidence):
            errors.append(f"{item_id}: evidence must be an array of non-empty paths")
            evidence = []
        if not isinstance(gaps, list) or not all(isinstance(x, str) and x.strip() for x in gaps):
            errors.append(f"{item_id}: gaps must be an array of non-empty strings")
            gaps = []

        for evidence_value in evidence:
            evidence_path = resolve_project_path(
                root, Path(evidence_value), f"{item_id}: evidence", errors
            )
            if evidence_path is not None and not evidence_path.is_file():
                errors.append(f"{item_id}: evidence file does not exist: {evidence_value}")

        if status == "verified":
            if not evidence:
                errors.append(f"{item_id}: verified items require evidence")
            if gaps:
                errors.append(f"{item_id}: verified items cannot retain gaps")
        elif status not in {"abandoned"} and not gaps:
            errors.append(f"{item_id}: unfinished items must state at least one gap")

    handoff_text: str | None = None
    if args.handoff:
        handoff_path = resolve_project_path(root, args.handoff, "handoff", errors)
        if handoff_path is not None:
            try:
                handoff_text = handoff_path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError) as exc:
                errors.append(f"cannot read handoff: {exc}")
        if handoff_text is not None:
            if len(handoff_text.strip()) < 80:
                errors.append("handoff is missing or too short to preserve project state")
            line_count = len(handoff_text.splitlines())
            if line_count > args.max_handoff_lines:
                context_warnings.append(
                    f"handoff has {line_count} lines; compact or archive closed history "
                    f"(limit {args.max_handoff_lines})"
                )
            if len(handoff_text) > args.max_handoff_chars:
                context_warnings.append(
                    f"handoff has {len(handoff_text)} characters; keep the hot handoff current-only "
                    f"(limit {args.max_handoff_chars})"
                )
            context_warnings.extend(handoff_hygiene_findings(handoff_text))
    elif args.handoff_ledger_check != "off":
        errors.append("--handoff-ledger-check requires --handoff")

    if handoff_text is not None and args.handoff_ledger_check != "off":
        findings = handoff_ledger_findings(items, handoff_text)
        if args.handoff_ledger_check == "error":
            errors.extend(f"handoff ledger: {finding}" for finding in findings)
        else:
            warnings.extend(f"handoff ledger: {finding}" for finding in findings)

    if args.index:
        index_path = resolve_project_path(root, args.index, "index", errors)
        index_text: str | None = None
        if index_path is not None:
            try:
                index_text = index_path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError) as exc:
                errors.append(f"cannot read project document index: {exc}")
        if index_text is not None:
            if len(index_text.strip()) < 80:
                errors.append("project document index is missing or too short to route context")

    if args.strict_context and context_warnings:
        errors.extend(f"context budget: {warning}" for warning in context_warnings)
    else:
        warnings.extend(context_warnings)

    return report(errors, warnings, counts)


def report(errors: list[str], warnings: list[str], counts: Counter[str]) -> int:
    if errors:
        print("Continuity validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        for warning in warnings:
            print(f"- warning: {warning}", file=sys.stderr)
        return 1

    summary = ", ".join(f"{status}={counts[status]}" for status in sorted(counts))
    print(f"Continuity validation passed ({summary})")
    for warning in warnings:
        print(f"Continuity warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
