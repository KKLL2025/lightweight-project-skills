# Examples

These examples explain expected decisions, not benchmark results. Each reproducible scenario links to the matching catalog case so a reviewer can inspect the prompt and scoring boundary without treating one run as a general performance claim.

## Reproducible scenarios

- [Keep a small task small](cases/01-small-task-without-ceremony.md) — `align-project-requirements` stays out of an explicit, reversible edit.
- [Recover from conflicting project state](cases/02-resume-from-conflicting-state.md) — `drive-large-project` verifies live owners instead of trusting a stale handoff.
- [Move referenced paths without losing assets](cases/03-safe-structural-migration.md) — `organize-ai-project-files` treats a directory move as a compatibility change.

## Route by material risk, not repository size

| Request | Route | Why |
|---|---|---|
| “Fix this explicit typo and run the focused test.” | Direct execution | Small, reversible, and observable in one turn |
| “Improve onboarding so new-user retention increases.” | `align-project-requirements` | Target behavior and success measure are material choices |
| “Resume the project; the handoff says complete but the authoritative project state record disagrees.” | `drive-large-project` | Live state, evidence, and recovery must survive across turns |
| “Move several referenced asset and output directories without breaking CI.” | `organize-ai-project-files` | Structural migration has path consumers and preservation risk |

## New AI-led project container

```text
project/
├── AGENTS.md
├── README.md
├── 01-ai-runtime/
│   ├── instructions/
│   ├── prompts/
│   └── tools/
├── 02-project-control/
│   ├── alignment/       # only when durable alignment is genuinely needed
│   └── continuity/      # only when resumable working memory is genuinely needed
└── 03-project-workspace/
    ├── product/
    ├── assets/
    ├── data/
    ├── outputs/
    └── temp/
```

Create only folders the project actually needs. This is a role map, not a requirement to generate empty directory trees.

## Existing framework repository

```text
existing-repo/
├── package.json
├── src/
├── tests/
├── .github/
├── 01-ai-runtime/       # only when project-specific AI resources exist
└── 02-project-control/  # alignment, continuity, and project-specific records when needed
```

Do not move framework-required roots into `03-project-workspace` merely to make the tree visually uniform. Compatibility is part of correctness.
