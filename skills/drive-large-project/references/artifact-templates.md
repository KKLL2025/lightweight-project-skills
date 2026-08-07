# Durable Project Artifact Templates

Use only the smallest artifacts the project lacks. Reuse project-native formats and keep one owner per changing fact.

## Three-zone default locations

| Concern | Default path |
|---|---|
| Alignment and scope | `02-project-control/alignment/` |
| Architecture and decisions | `02-project-control/architecture/` |
| Plans and tasks | `02-project-control/planning/` |
| Document router | `02-project-control/continuity/PROJECT_INDEX.md` |
| Current handoff | `02-project-control/continuity/PROJECT_HANDOFF.md` |
| Acceptance ledger | `02-project-control/acceptance/ledger.json` |
| Raw evidence | `02-project-control/evidence/` |
| Closed history | `02-project-control/history/` |

Adapt these paths for a compatible existing repository. Do not create a second control tree.

## Minimal document router

```markdown
# Project Index

## Always read
- `AGENTS.md` — stable rules and navigation.
- `PROJECT_HANDOFF.md` — current stage and next action.

## Read for the active work
- `<path>` — owns <concern>; read when <condition>.

## Historical or evidentiary
- `<path>` — read only for <audit, regression, or acceptance ID>.
```

Keep progress counts and chronology out of the router.

## Current-only handoff

```markdown
# Project Handoff

## Current outcome and stage
## Verified results
## In progress
## Unfinished, blocked, or externally pending
## Risks and invariants
## Git/worktree and recent checks
## Exact next action
```

Reference task and acceptance IDs. Replace stale current-state text; move closed chronology to history.

## Acceptance ledger

Create only when acceptance state must survive several tasks, agents, or external checks.

```json
{
  "schemaVersion": 1,
  "scope": "path/to/alignment-or-spec",
  "updatedAt": "YYYY-MM-DD",
  "items": [
    {
      "id": "A-01",
      "title": "Observable outcome",
      "status": "not_started",
      "evidence": [],
      "gaps": ["Exact missing work or proof"]
    }
  ]
}
```

Compatible states: `not_started`, `in_progress`, `blocked`, `implemented_pending`, `verified`, `abandoned`.

## Milestone capsule

```markdown
### <Outcome>
- Acceptance: <IDs or observable boundary>
- Likely modules: <paths/components>
- Verification: <focused and proportional checks>
- External dependency: <if any>
- Recovery rule: <only when material>
```

## Closed-history capsule

```markdown
### YYYY-MM-DD: <milestone>
- Outcome: <delivered result>
- Decision: <durable choice and rationale>
- Invariant: <what future work must preserve>
- Evidence: <path, revision, or command>
- Reopen when: <condition that invalidates the result>
```

## Exact next action

```text
Implement <bounded outcome> in <module>, preserving <invariant>.
First verify with <command or observation>.
```
