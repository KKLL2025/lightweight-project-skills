# Durable Project Artifact Templates

Use only the smallest durable artifact the project actually lacks. These are optional shapes, not required schemas. Reuse the project's existing README, roadmap, plan, issue, design document, or handoff when it already serves the information role.

Keep one primary owner for each changing fact and do not create a second control tree merely because a three-zone layout is available.

## Example locations by information role

| Role | Example location | Use only when |
|---|---|---|
| Canonical project map | Existing `README.md` or project index | The project has a real navigation problem |
| Alignment baseline | Project-native specification or `02-project-control/alignment/` | Later review or coordination needs durable alignment |
| Project route | Existing roadmap or plan | Stages, dependencies, or recovery need persistence |
| Current Handoff | Existing continuity area or `02-project-control/continuity/PROJECT_HANDOFF.md` | A later Turn or Session needs resumable working memory |
| Project-specific acceptance or evidence | Existing project-native location | Formal acceptance, reproducibility, or external checks genuinely require it |

Adapt paths for a compatible existing repository. Do not wrap a mature repository or create folders for visual neatness.

## Minimal project map

```markdown
# Project Map

## Start here
- `AGENTS.md` — stable rules, if present.
- `README.md` — project purpose and entry points.

## Read for the active work
- `<path>` — owns <concern>; read when <condition>.

## Deeper sources
- `<path>` — read only when the active task needs it.
```

Keep progress counts, activity logs, and copied document contents out of the map.

## Current Handoff

```markdown
# Project Handoff

## Current work area or stage
## Important recent results
## Active or unfinished work
## New issues, constraints, or external dependencies
## Most useful next action
```

Replace obsolete current-state text instead of appending an indefinite history. Add repository or worktree details only when they materially help the next resume.

## Bounded outcome note

```markdown
### <Bounded outcome>
- Result: <what changed or was learned>
- Remaining: <unfinished or externally pending work>
- Check: <focused validation when useful>
- Next action: <the most useful continuation>
```

Use a separate acceptance record, evidence archive, release manifest, or detailed history only when the project has a concrete need for it. Those artifacts are not defaults of this skill.
