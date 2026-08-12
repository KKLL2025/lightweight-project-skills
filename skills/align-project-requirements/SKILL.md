---
name: align-project-requirements
description: Align the goal, current facts, non-goals, material decisions, assumptions, and observable acceptance for a medium-to-large project change before implementation. Use for new features, product or workflow changes, ambiguous requests, cross-module work, architecture choices, or when an existing specification needs correction. Skip for small, explicit, low-risk fixes that can be executed and verified directly. Do not use for routine diagnosis, formatting, dependency maintenance, or one-turn implementation unless it changes product behavior or another material boundary.
---

# Align Project Requirements

Turn intent into a usable decision boundary without turning every request into a documentation ceremony.

## Use autonomous judgment by default

- Inspect the repository, current behavior, existing decisions, and project state before asking the user for facts that can be discovered.
- Execute simple, reversible, in-scope work directly when the goal and observable result are already clear.
- Ask only when a missing choice would materially change the target user, core value, success measure, product behavior, user experience, legal/privacy posture, irreversible data shape, cost, or external commitment.
- When several ordinary implementation choices are valid, choose the one that best fits existing project conventions and record the assumption only if it matters later.
- Batch related blocking questions. Explain the material difference and recommend a reversible default when one exists. Do not interrupt for routine naming, file placement, or technical details the codebase can answer.

## Build the lightest useful alignment

Confirm these concerns, in conversation or in an existing project artifact:

1. **Goal contract:** the bounded final result, observable completion condition, and small set of non-negotiable constraints that must remain stable across the project. Keep routine steps and temporary implementation choices out of it.
2. **Current facts:** what the live project, runtime, or source evidence shows now.
3. **Boundary:** what is in scope, explicitly out of scope, and which reviews are intentionally excluded.
4. **Acceptance:** how a person can tell the change works, including important failure behavior.
5. **Decisions and assumptions:** material choices already made, unresolved choices, and safe defaults selected autonomously.
6. **Project Route:** when the work has meaningful stages, record the major milestones, dependencies or external gates, first executable milestone, and evidence that would justify reordering. This is the project-level route, not a live plan for one Turn.
7. **Authority and trust:** what Codex may do locally, what requires a user or external party, and any threat model or changed trust boundary relevant to validation.

For direct execution, establish only the bounded outcome, observable check, and authority needed to act safely; infer the other concerns from verified project facts unless they change the result. Omit the Project Route, threat-model, and review-exclusion fields when they have no material effect.

Do not mistake a requested implementation detail for the underlying goal. Challenge a proposed solution only when it would materially damage the stated outcome, safety, compatibility, or authority boundary.

## Scale the artifact to the work

- **Direct execution:** keep alignment in the task context when work is small, precise, and finishes in one turn.
- **Alignment card:** create or update one concise artifact only when the change will span turns, needs independent review, or contains an unresolved material choice. In the three-zone layout, use `02-project-control/alignment/<change>.md`.
- **Expanded specification:** split requirements, design, and tasks only when independent review, multiple milestones, or substantial architectural reasoning makes the separation useful.

Read [alignment-card.md](references/alignment-card.md) only when creating or repairing an alignment artifact. Reuse project-native formats instead of creating a parallel specification system.

## Write acceptance for humans and tests

- Prefer concrete scenarios and observable behavior over implementation prose.
- Include boundaries a reasonable human would check: empty input, failure, permissions, persistence, recovery, and compatibility only when relevant.
- Use EARS or stable requirement IDs when traceability helps; do not force them onto a small change.
- Separate verified current facts from forecasts, preferences, and assumptions.

## Hand off cleanly

- If implementation is expected to span multiple Turns, milestones, or external checks, hand `drive-large-project` the Goal contract, observable acceptance, Project Route and first executable milestone, reorder conditions, unresolved decisions, relevant trust boundaries, and authority limits. Let that skill own the live milestone state and Turn Plan.
- If alignment changes project roots, multiple or referenced output paths, protected assets, or a broad directory migration, use `organize-ai-project-files` for layout decisions and move safety.
- This skill owns the Goal contract, desired behavior, Project Route, and decision boundaries. It does not own the live Turn Plan, long-running execution status, acceptance evidence state, or filesystem migration.

## Finish

State the aligned outcome, material assumptions made autonomously, any genuinely unresolved decision, and the next executable action. Continue into implementation when authorized and no material decision blocks it.
