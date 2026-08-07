# Examples

## Route by material risk, not repository size

| Request | Route | Why |
|---|---|---|
| “Fix this explicit typo and run the focused test.” | Direct execution | Small, reversible, and observable in one turn |
| “Improve onboarding so new-user retention increases.” | `spec-workflow` | Target behavior and success measure are material choices |
| “Resume the project; the handoff says complete but the acceptance ledger disagrees.” | `drive-large-project` | Live state, evidence, and recovery must survive across turns |
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
│   ├── alignment/
│   ├── continuity/
│   ├── acceptance/
│   └── evidence/
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
└── 02-project-control/  # alignment, continuity, acceptance, and evidence
```

Do not move framework-required roots into `03-project-workspace` merely to make the tree visually uniform. Compatibility is part of correctness.
