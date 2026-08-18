---
name: drive-large-project
description: "Sustain projects that genuinely benefit from persistent planning and resumable context across multiple execution batches or Sessions. Use when the agreed scope, delivery depth, dependencies, duration, or recovery needs make it likely that progress would otherwise be lost, duplicated, or difficult to resume. Focus on continuity, practical coordination, bounded Turns, and compact handoffs rather than repeated verification, evidence collection, or heavy governance. Skip when normal Agent execution is sufficient."
---

# Drive Large Projects

Keep substantial work moving across Turns and Sessions without losing direction, overloading context, or allowing project management to displace the actual work.

The Agent's primary job is to advance the project.

Use additional process only when it materially improves continuity, recovery, coordination, or a level of rigor the project actually requires.

## Enter only when persistent coordination is useful

Do not classify work as a large project from the task label alone.

The same request may need a quick implementation or a long multi-stage effort depending on the agreed delivery depth.

Use this skill when persistent project state would materially improve execution, such as when:

- meaningful work will span multiple bounded execution batches;
- several stages, dependencies, or workstreams must remain coordinated;
- progress would be costly or difficult to reconstruct later;
- the project is expected to continue across Sessions;
- losing the current route or working state would cause substantial repeated work.

When `align-project-requirements` has established the project framework, use that understanding to decide whether this mode is actually needed.

Do not force a clear project through alignment merely to activate this skill.

## Recover only the context needed to continue

When resuming work, establish enough context to understand:

- the intended outcome and agreed delivery depth;
- the current project route;
- where execution currently stands;
- what is active or unfinished;
- what should happen next.

Prefer host-native and repository-native search, indexing, memory, planning, and session mechanisms when they already solve the need.

Use existing project navigation, the current project plan or roadmap, and the current Handoff when available. These are information roles, not mandatory separate files; reuse or combine existing artifacts when that reduces duplication.

If persistent continuity is genuinely needed and no suitable state exists, create only the lightest equivalent required to resume later.

Read deeper project knowledge and implementation files only when the active work requires them.

Do not routinely replay project history, load every control document, inspect the whole repository, or re-establish facts that remain reasonably stable.

A fresh Session should be able to understand the project progressively instead of loading the entire project at once or guessing from filenames.

When a recovery summary is observed to conflict with a newer user decision or the current relevant project state, treat the summary as stale and update it. Do not force reality to match the summary or turn recovery into a full-project audit.

This skill defines what execution context needs to survive and how it is used. `organize-ai-project-files` owns how that information is arranged in the project filesystem.

## Keep project control proportional

Different projects require different levels of rigor.

An internal prototype, ordinary product feature, exploratory experiment, formal benchmark, production release, and high-risk system should not automatically receive the same process.

Increase validation, documentation, coordination, traceability, or formality when the project's actual purpose, risk, observed problems, or user requirements justify it.

Do not reduce rigor when the project genuinely requires strong reproducibility, formal acceptance, irreversible operations, or release controls. But do not impose those standards on ordinary work by default.

Time, tokens, repeated checks, documentation maintenance, and context consumption are project costs.

## Let normal Agent capabilities handle normal work

Do not prescribe ordinary coding, debugging, testing, research, implementation, or routine technical judgment merely because the work belongs to a large project.

Do not turn every local fix, experiment, file change, or implementation decision into a milestone, audit, acceptance event, or evidence record.

This skill does not add a separate verification layer, but it does not waive checks required by the task, project conventions, or normal engineering judgment.

This skill controls the long-running process around the work, not every action inside it.

## Maintain one practical project route

Prefer the project framework produced by `align-project-requirements`, or an existing roadmap or plan.

Do not create another plan merely because this skill became active.

Keep only durable project-level information that future execution needs, such as:

- intended outcome and delivery standard;
- major stages or milestones;
- important dependencies or gates;
- current overall route and meaningful progress;
- unresolved project-level issues that affect later work.

Treat the route as the best current plan, not a frozen implementation contract.

The Agent may reorder stages, change implementation sequence, or choose a better technical route when actual development justifies it.

Do not silently redefine the user's current requirements baseline or intended outcome.

Update the route only when something materially changes for future execution. Do not use it as an activity log.

For each changing project fact, prefer one primary maintained location rather than keeping competing copies in the plan, Handoff, module notes, and other documents.

## Keep the Handoff as current working memory

The Handoff exists so the next Turn or a fresh Session can continue without reconstructing the project.

Keep only information that materially helps continuation, normally:

- current stage or work area;
- recent important results;
- active or unfinished work;
- new findings or problems that still affect upcoming work;
- the most useful next action.

The Handoff is not project history and not a second knowledge base.

Update it at a useful execution boundary when the resumable state has materially changed. A simple current update is sufficient; do not add a separate review cycle merely to maintain it.

The same current facts should normally support both the Handoff update and the concise progress report to the user.

Prefer replacement, compression, and removal of obsolete material over indefinite appending.

When information becomes stable long-term project knowledge, let it live in the project's existing durable knowledge mechanism rather than keeping it permanently in active Handoff context.

Stable knowledge should preserve useful high-level understanding, responsibilities, interfaces, and important decisions rather than duplicate implementation details.

## Work in bounded execution batches

A Turn is an execution batch, not a synonym for a milestone.

At the beginning of a Turn, select a bounded batch in the host's plan or working context. It may contain several closely related small steps or one coherent part of a difficult milestone.

Make meaningful progress within that boundary. Necessary adjustments inside the same outcome are allowed, but do not repeatedly redefine the batch to absorb the next major outcome.

When the batch is completed, materially blocked, or reaches a decision that belongs with the user:

- preserve project state that materially changed;
- update the Handoff when useful;
- give the user a concise report of progress, important issues, and likely next work;
- end the Turn and return control to the user.

Milestones organize the project route. Turn boundaries keep execution manageable. They do not need to coincide.

The Agent keeps the project ready for a fresh Session, but only the user decides whether to start one.

## Trust settled state until reality gives a reason not to

Previously established work and facts should normally remain usable when nothing relevant has changed.

Do not automatically repeat checks because a new Turn began, a milestone ended, a Session resumed, or a report is being written.

Recheck something when the active work depends on a fact that may reasonably have changed, or when implementation changes, observed failure, contradictory information, an invalidated assumption, or project-specific risk gives a concrete reason.

Checks should be triggered by reality, not by workflow position.

## Handle long-running work without duplicating it

When a command, experiment, training run, migration, benchmark, or other task is expensive or difficult to repeat, preserve enough identity and current state to recognize and resume the existing work.

Do not start a duplicate merely because execution moved to another Turn or Session.

Record only the information actually needed to locate, understand, or resume that task. Do not turn this into a general logging requirement for ordinary commands.

## Adapt execution without changing the user's goal

Long projects should evolve as implementation reveals new information.

Resolve ordinary technical discoveries and implementation decisions autonomously. Adjust the practical project route when reality makes another sequence or approach more effective.

When execution exposes a material requirement misunderstanding, important new constraint, major product or business trade-off, or another decision that reasonably belongs with the user, return that issue to focused `align-project-requirements`.

Do not restart the entire alignment process for a local issue. Resolve the relevant question, update the project-level understanding when necessary, and continue.

## Avoid self-auditing workflows

No rule in this skill should become a recurring self-audit loop.

These rules guide execution; they are not checkpoints that must be repeatedly re-verified before the Agent may continue.

Do not repeatedly confirm that every rule was followed, every boundary remains unchanged, every completed step remains valid, or every document is synchronized unless current reality gives a specific reason to doubt it.

Project control exists to make execution more stable, not to make the Agent continuously prove that it is under control.

## Coordinate responsibilities

`align-project-requirements` owns understanding the user's real need, the current requirements baseline, the delivery standard, and requirement-level revision.

`drive-large-project` owns sustained execution, the evolving practical route, active project state, bounded Turn execution, and resumable working context.

`organize-ai-project-files` owns project directory topology, file placement, navigation structure, and structural migrations.

Do not duplicate another skill's responsibility merely for convenience.

## Finish or pause cleanly

Before stopping, preserve only enough current state for later work to continue effectively.

Do not create acceptance ledgers, evidence archives, detailed histories, release manifests, hashes, or additional management artifacts unless the actual project has a concrete need for them.

Do not confuse local progress with completion of the whole project.

Declare completion according to the delivery standard actually agreed for that project, without manufacturing additional work solely to increase certainty.

A successful use of this skill should make the project easier to continue, understand, and finish while keeping most Agent effort focused on the project itself.
