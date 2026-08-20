---
name: organize-ai-project-files
description: "Use when project-level file or directory organization is itself part of the task or an observed obstacle: establishing a project structure, cleaning a confusing workspace, improving navigation, deciding where major artifacts belong, or making structural moves that affect paths, repositories, assets, or outputs. Skip ordinary implementation, routine file creation, and local placement inside an understandable repository when no project-level organization problem exists."
---

# Organize AI Project Files

Make the project easy to enter, navigate, understand, and continue without forcing a person or Agent to explore the whole workspace.

Organize for progressive discovery and maintainability, not for control, security, or proof.

## Keep the responsibility narrow

This skill owns:

- project-level directory topology;
- top-level organization and navigation;
- placement of project-level artifacts;
- structural cleanup and migration;
- keeping major project areas understandable as the project grows.

It does not own requirements, Project Plan or Handoff content, execution sequencing, acceptance, release state, code-quality review, or unrelated security and operational audits.

`align-project-requirements` decides what the project should become.

`drive-large-project` decides what execution context needs to survive.

This skill decides how project information and project areas are arranged so they can be found efficiently.

## Prefer a recognizable project entrance

Use one concise project map as the canonical navigation source, preferably by reusing an existing README, host-native Agent entry, or established project index.

Host-specific instruction files and human-facing documentation may both exist, but they should divide roles or link to the same map rather than maintain competing copies of the project structure.

For a new multi-repository, mixed-asset, or AI-led project container, a consistent outer shell is useful:

```text
project/
├── AGENTS.md
├── README.md
├── 01-ai-runtime/
├── 02-project-control/
└── 03-project-workspace/
```

Broadly:

- `01-ai-runtime/` contains project-specific Agent instructions, skills, prompts, helpers, and AI configuration;
- `02-project-control/` contains project-level alignment, plans, continuity material, architecture, research, decisions, and other durable references;
- `03-project-workspace/` contains product repositories, source projects, assets, data, outputs, and working material.

The value of the common shell is a predictable entrance, not visual uniformity.

For a standard single repository whose framework, package manager, monorepo, CI, build, or deployment tooling expects files at the root, keep the product repository at that root. Add only the smallest compatible Agent entry, project map, or control area needed; do not wrap the repository inside `03-project-workspace/` solely to fit the template.

Standardize the project entrance, not every internal structure.

## Preserve mature structures as coherent units

Treat established repositories, framework projects, packages, monorepos, third-party components, datasets, or other mature subsystems as coherent units unless restructuring them is itself the task.

Do not reorganize their internal source, tests, packages, configuration, or build structure merely to fit the outer project scheme.

Ordinary file placement inside a mature subsystem follows that subsystem's conventions and normal Agent engineering judgment. This skill does not need to intervene.

## Design for progressive discovery

A fresh Agent should be able to move from broad context to detailed implementation only as needed:

```text
project entry
    ↓
major project area
    ↓
relevant subsystem or knowledge area
    ↓
local context when necessary
    ↓
actual files and implementation
```

Navigation should help answer:

- what major areas exist;
- what each area is for;
- where a particular kind of information belongs;
- where to look next.

Keep navigation concise and point toward deeper sources instead of copying their contents.

Do not create a README, index, or summary at every directory level. Add another navigation layer only when a real branching or discovery problem makes it useful. A clear mature directory may need no additional explanation.

Do not require an Agent to scan the entire project tree merely to discover where relevant information lives, but also do not encourage guessing implementation from filenames or shallow summaries.

## Place project-level material by role

Use the narrowest existing location that matches the material's actual role.

Prefer an existing suitable location over creating another category.

Separate source, durable project references, generated outputs, temporary work, and Agent configuration when mixing them would make navigation meaningfully harder.

Do not create folders merely for visual neatness. A structural distinction should improve navigation, retrieval, ownership, or maintainability enough to justify its existence.

## Treat new and existing projects differently

### New or clean projects

Establish a simple compatible shell and useful entry points early when appropriate.

Avoid elaborate indexes, registries, manifests, or control structures before the project has a reason to need them.

### Existing or confusing projects

Do not reorganize by guesswork.

Start from the top level and the areas relevant to the requested cleanup. Understand deeper contents only when their role, dependencies, or destination cannot otherwise be determined.

Identify mature subsystems that should stay intact, obviously misplaced or mixed material, relevant path consumers, and valuable or difficult-to-recover assets when they matter.

Then make the smallest structural changes that materially improve the project.

Do not turn cleanup into a full-project inventory or audit.

Organization does not imply deletion. Do not delete or discard unknown, user-owned, or difficult-to-recover material merely because it appears redundant, temporary, or untidy. Deletion requires explicit authority or a clearly safe project-native cleanup rule.

## Apply migration care proportionally

Use normal engineering judgment for simple, reversible moves.

When moving referenced files, update affected consumers and perform a reasonable check that the affected paths still work.

Increase protection only when the actual migration warrants it, such as when:

- many referenced paths are changing;
- valuable or difficult-to-recreate assets are involved;
- build, deployment, automation, or external systems depend heavily on paths;
- a large migration would be expensive to undo.

Use backups, inventories, mappings, integrity checks, or broader verification when those measures solve a real migration risk.

Do not require universal snapshots, hashing, rollback maps, exhaustive repository audits, or full test suites for ordinary organization work.

## Correct structural drift when it becomes a real problem

As projects grow, structure may gradually become harder to navigate.

Correct it when actual work reveals problems such as:

- a cluttered project root;
- temporary and durable material becoming mixed;
- related project-level information being scattered;
- navigation no longer representing the real project;
- a new major subsystem having no understandable place.

Do not periodically scan the project merely to prove that the structure is still clean.

Do not reorganize stable areas simply because another naming scheme looks better.

Structure maintenance should be triggered by observed friction or an explicit organization task, not by a recurring housekeeping ritual.

## Coordinate without duplicating content

This skill may create or maintain navigation that points toward plans, handoffs, stable knowledge, repositories, assets, and other project areas.

It does not decide what those artifacts should contain.

Do not duplicate their contents into navigation files.

When another skill determines that information should exist, place it appropriately within the established structure and keep the navigation sufficient to find it.

## Finish proportionally

Report only the structural changes and unresolved issues that matter to the user or the next Agent.

Keep simple placement or cleanup reports brief.

For meaningful migrations, explain the resulting structure, important moves, and any unresolved path or asset issue.

Do not create evidence packages or additional management documents merely to prove that organization occurred.

A successful structure lets a fresh Agent reach the information needed for its current task with little unnecessary reading while leaving mature project internals intact.
