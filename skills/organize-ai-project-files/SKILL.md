---
name: organize-ai-project-files
description: Design, establish, audit, and safely migrate clean project-folder structures for AI-assisted development. Use when creating a project tree, grouping AI runtime files, project-control documents, and actual product files; cleaning a cluttered root; separating assets and outputs; repairing layout drift; or moving referenced paths without losing Git history, user assets, commands, evidence, or release truth.
---

# Organize AI Project Files

Make the project easy for a person and a fresh AI agent to navigate. Treat structural moves as compatibility changes; treat ordinary file placement as a lightweight housekeeping decision.

## Decide the topology

Read [layout-standard.md](references/layout-standard.md) when creating a tree or choosing between layouts.

- Use the **three-zone shell** for new AI-led projects, mixed project containers, or when the user wants a clean main view with AI runtime, project control, and actual project files separated.
- Use the **compatible repository layout** when an existing framework, CI system, package manager, or monorepo expects files at the repository root. Preserve those conventions and introduce only the missing control/output boundaries.
- Never reorganize solely to make names visually uniform. The new structure must improve retrieval, ownership, output clarity, or safe continuation enough to justify path churn.

For the three-zone shell, keep only discovery files and these main categories at the root:

```text
project/
├── AGENTS.md
├── README.md
├── 01-ai-runtime/
├── 02-project-control/
└── 03-project-workspace/
```

Root adapters such as `CLAUDE.md`, `.gitignore`, and tool manifests may remain when required. Do not scatter specifications, logs, installers, drafts, exports, and source folders beside the three zones.

## Classify before placing

- `01-ai-runtime/`: project-specific AI instructions, reusable skills, prompts, AI tool helpers, and AI configuration. Do not put product source or project status here.
- `02-project-control/`: alignment, architecture, plans, continuity, acceptance, evidence, research, and history used to guide and resume the project.
- `03-project-workspace/`: actual product/repository files, user assets, input data, outputs, exports, and temporary working data.

Within the product workspace, preserve framework-native module and test structure. Do not force every technology into a generic `src/` shape.

## Apply proportional safety

### Simple placement or local cleanup

Inspect the relevant files, Git state, and path references. Move or create the item in the obvious role, update affected links/configuration, and run the cheapest check that proves consumers still work. Do not demand a full-project snapshot for an independent draft or generated file with no consumers.

### Structural migration

Use the full migration path when changing roots, moving multiple/referenced paths, relocating large or valuable untracked assets, or changing build/run/release locations:

1. Discover the actual Git and working roots plus repository instructions.
2. Inventory tracked, modified, ignored, and untracked files; protected assets; key sizes/counts; manifests; commands; and path consumers.
3. Run `scripts/tree_snapshot.py create`. Use `--hash-mode all` when paths may be renamed or content preservation must be proved; a partial or unhashed snapshot is diagnostic evidence, not integrity proof.
4. Produce an explicit source-to-destination map with role, consumers, rollback, and stop conditions.
5. Resolve absolute source/destination paths and verify they remain inside the authorized workspace.
6. Move explicit paths with one filesystem API, then update commands, manifests, ignores, indexes, evidence links, CI, and agent entry files.
7. Compare renamed or moved trees with `--path-mode content`; use `exact` when paths must stay unchanged. Then run `scripts/audit_layout.py`, search stale paths, parse manifests, run focused build/test/smoke checks, and inspect Git state. Stop if a symlink resolves outside the authorized root rather than reading through it.

Do not delete unknown files, caches, duplicates, historical candidates, or user assets merely because they appear untidy. Classification comes before deletion; deletion requires its own authority.

## Keep a layout contract only when useful

Adapt `assets/project-layout.json` into the project when the layout will be maintained across sessions, contains protected paths, or has output/release boundaries worth auditing. Reuse an equivalent existing contract instead of adding another one.

The contract should identify development, control/reference, output, protected-asset, ephemeral, entry, and hot-continuity paths. Treat unclassified root entries as review items, not automatic failures to delete.

Use output states only when the project produces deliverables:

- **engineering output:** built or generated and checked locally;
- **delivery candidate:** packaged for further verification;
- **formal release:** fixed revision plus required release evidence and no open release gate.

A copy, rename, hash, local build, mock, or folder label cannot upgrade an artifact's state.

## Coordinate with the other two skills

- `align-project-requirements` owns the desired outcome, non-goals, and acceptance boundaries. Store its durable artifacts under the control/alignment role.
- `drive-large-project` owns execution continuity and keeps ordinary new files in their correct roles during development.
- This skill owns topology, placement rules, structural migration, asset preservation, and path-consumer verification. It does not redefine product scope or claim acceptance.

## Finish with evidence

Report the resulting root map, important subfolders, what moved or stayed, path consumers updated, preservation checks, commands run, Git state, and any unresolved item. For a simple placement task, keep the report proportionate; for a structural migration, include the full mapping and integrity evidence.
