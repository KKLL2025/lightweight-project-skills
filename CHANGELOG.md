# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Separated the durable Goal contract and Project Route from the current-milestone Turn Plan, with an explicit verify, report, and end-of-Turn boundary.
- Allowed evidence-driven Turn Plan revisions inside the active milestone while preventing plan churn from silently crossing into later milestones.
- Distinguished host-native Goal pause, blocked, and complete states when human direction or external authority is required.

### Added

- Added contract checks and behavior cases for planning ownership, adaptive Turn Plan revisions, milestone boundaries, and Goal-state integrity.

### Planned

- Broader repeated behavior evaluations across more than one model/runtime.
- More complete real-project fixtures and installation verification.

## [0.6.0-preview] - 2026-08-11

### Added

- Added an adaptive execution-control reference covering macro routing, rolling execution horizons, evidence-based cross-module switching, validation escalation, delegated reporting, and heavy-work budgeting.
- Added conservative handoff-hygiene warnings for duplicate canonical current/next-action sections and explicit closed-history sections, with strict-mode promotion and no semantic guessing from custom prose.
- Added focused behavior cases for adaptive execution boundaries, planned module switching, trust-boundary validation, delegated progress, handoff hygiene, and layout non-triggers.
- Added three public, reproducible worked scenarios that expose the intended boundary of each skill without presenting them as benchmark results.
- Added a tiered behavior-evaluation protocol that separates worked examples, exploratory pairs, repeated comparisons, and cross-runtime benchmarks.
- Added a local-first GitHub integration guide and a redacted real-project case-report issue form.

### Changed

- Extended requirements alignment with optional first-outcome, sequencing, reorder, excluded-review, trust-boundary, and external-gate handoff fields without making them mandatory for direct tasks.
- Replaced unconditional milestone continuation with proportional execution batches that preserve autonomous low-risk progress without hiding substantial stateful work.
- Tightened folder-governance triggering so ordinary code, content, business, and security audits do not activate layout migration when paths and folder roles are unchanged.
- Kept the former alignment-skill name as a compact upgrade compatibility note instead of a prominent README callout.
- Reframed the README around the project's evidence boundary instead of a generic list of marketing pain points.
- Added a behavior-change gate that requires an observed failure and a non-trigger boundary before a general skill rule can grow.

### Preserved

- Kept all three runtime `SKILL.md` files unchanged in this documentation-and-evidence iteration. Candidate terminology, ticket-dependency, and handoff-redaction rules did not yet demonstrate a general gap that justified expanding the core instructions.

## [0.5.0-preview] - 2026-08-08

### Changed

- Tightened the English and Chinese README first screen around the lightweight, proportional-governance value proposition.
- Added a tested one-command discovery and project-scoped Codex installation path through the open-source `skills` CLI, while retaining manual installation fallbacks.
- Added non-blocking milestone updates and lightweight direction re-anchoring to `drive-large-project`, using observable recovery events instead of self-imposed timers or hidden context-compaction counters while preserving host-required progress heartbeats.
- Renamed `spec-workflow` to `align-project-requirements` and its evaluation IDs from `S-*` to `A-*` so the public name matches its lightweight requirements-alignment behavior and no longer reuses the CloudBase skill name. Existing preview users must remove only the old copy installed from this repository before reinstalling to avoid duplicate routing; unrelated provider or plugin skills with the same old name must not be removed.

### Known limitations

- Behavior evidence remains a small Codex sample rather than a statistically meaningful multi-model benchmark.
- Real symlink tests require platform permission; policy tests provide a permission-independent fallback.
- This preview is not a production or safety certification.

## [0.4.0-preview] - 2026-08-08

### Added

- `spec-workflow` for proportional requirements alignment.
- `drive-large-project` for evidence-backed multi-turn project delivery.
- `organize-ai-project-files` for safe topology and path migration.
- Python checks for continuity ledgers, layout contracts, content-preserving moves, path boundaries, and repository contracts.
- Eighteen positive, negative, and pressure evaluation cases.
- Windows/Linux GitHub Actions matrix and public repository health files.

### Known limitations

- Behavior evidence is a small Codex sample, not a multi-model statistical benchmark.
- Real symlink tests require platform permission; policy tests provide a permission-independent fallback.
- This preview is not a production or safety certification.

### Fixed

- Windows hosted-runner UTF-8 output and equivalent long/8.3 symlink target spellings.

[Unreleased]: https://github.com/KKLL2025/lightweight-project-skills/compare/v0.6.0-preview...HEAD
[0.6.0-preview]: https://github.com/KKLL2025/lightweight-project-skills/releases/tag/v0.6.0-preview
[0.5.0-preview]: https://github.com/KKLL2025/lightweight-project-skills/releases/tag/v0.5.0-preview
[0.4.0-preview]: https://github.com/KKLL2025/lightweight-project-skills/releases/tag/v0.4.0-preview
