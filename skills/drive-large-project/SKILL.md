---
name: drive-large-project
description: Drive medium-to-large projects across turns or days while preserving scope, truthful state, evidence-backed acceptance, and resumable handoffs. Use when the user asks Codex to continue autonomously, resume staged work, coordinate milestones or long-running checks, or deliver an aligned specification. Skip for small fixes and one-turn changes.
---

# Drive Large Projects

Keep long work truthful and resumable without repeated confirmation.

## Start from reality

1. Read repository instructions and the smallest existing project index/handoff needed to orient.
2. Inspect live Git and relevant files before trusting a previous status claim.
3. Reuse existing scope, plan, acceptance, evidence, and layout artifacts. Do not create a second source of truth.
4. If the desired outcome or material product boundary is unclear, use `align-project-requirements`. Otherwise continue directly.
5. Resume at the first unfinished, unblocked outcome; do not replay completed work merely because conversation context was lost.

Use this authority order when sources conflict: latest user decision, repository rules, approved alignment/design, task and acceptance owners, current handoff, then history. Repair stale summaries after verifying the live state.

## Exercise judgment without ceremony

- Proceed through reversible local analysis, code, tests, builds, documentation, and ordinary refactors that are already in scope.
- Decide routine technical details from project conventions, maintainability, and the aligned outcome.
- Ask only when a choice materially changes product direction, privacy/legal posture, irreversible production data or permissions, spending, public release, external communication, or authority beyond the user's delegation.
- Batch genuinely blocking questions. Continue other independent in-scope work when possible.
- Add process only in response to actual project complexity or observed failure risk.

## Keep the root and project tree clean during development

Follow the existing `PROJECT_LAYOUT.json` or repository conventions. When the project uses the three-zone layout, place new material under:

- `01-ai-runtime/` for project-specific AI instructions, skills, prompts, tool helpers, and AI configuration;
- `02-project-control/` for alignment, architecture, plans, continuity, acceptance, evidence, research, and history;
- `03-project-workspace/` for product files, assets, data, scripts, outputs, and temporary work.

Do not place a new root entry merely because it is convenient. Classify it first, then use the narrowest fitting subfolder. Preserve framework-native structure inside the product workspace rather than inventing a new source tree.

During each milestone, correct simple placement drift as part of the work when the move is local, obvious, reversible, and has no meaningful path consumers. Use `organize-ai-project-files` when creating the project structure, changing roots, moving multiple or referenced paths, separating outputs/releases, or protecting valuable user assets. Folder governance remains a continuous concern; structural migration remains a specialized operation.

## Use only the durable state the project needs

- A one-turn task needs no new management documents.
- A multi-turn project normally needs a short document router/index and a current-only handoff.
- Add a task plan when several executable outcomes must be sequenced.
- Add an acceptance ledger only when multiple criteria, external validation, or evidence gaps must survive across sessions.
- Store raw logs, screenshots, manifests, and old milestone details outside the default read set.

When templates are needed, read [artifact-templates.md](references/artifact-templates.md). When project documents are growing or duplicated, or recovery context is summarized or uncertain, read [context-lifecycle.md](references/context-lifecycle.md). When several outcomes or modules must be ordered, validation may become expensive, or delegated work needs coordination, read [execution-control.md](references/execution-control.md).

Give each changing fact one owner: alignment owns desired behavior; tasks own execution state; the acceptance ledger owns evidence state; the handoff summarizes the current stage and next action; the layout contract owns folder roles. References may point to these facts but must not independently maintain competing copies.

## Work in outcome-sized milestones

For the active milestone:

1. State the observable outcome and relevant boundary or acceptance IDs.
2. Inspect or reproduce current behavior.
3. Implement the smallest coherent vertical slice.
4. Run focused checks, then broader checks proportional to risk.
5. Exercise the real user/runtime path when practical.
6. Record evidence and gaps honestly.
7. Update the task owner, acceptance owner when present, and concise handoff.
8. At the completion of each outcome-sized milestone, re-anchor against the aligned outcome, relevant non-goals and authority boundaries, acceptance evidence, live project state, and the next unblocked result.
9. Send a brief user-visible milestone update with the verified result and evidence, material gaps or risks, and the next milestone.
10. Select the next execution boundary proportionally instead of continuing or stopping mechanically.

Complete small, clear work directly. For stateful, resource-heavy, cross-module, or multi-agent work, default to one major outcome per user-visible execution batch. Related outcomes may share a batch for small or explicitly continuous low-risk work when evidence and recovery remain intact. "Do everything" or "do not stop" does not make substantial work low-risk or authorize silent major-outcome crossings. Monitoring does not conceal new development.

Cross modules only for the active outcome, dependency, vertical path, blocker bypass, or high-risk seam. Record a short reason in the existing plan when evidence materially reorders work; do not opportunistically rescan or recreate the roadmap.

Do not claim more than the evidence establishes. Code written, locally checked, packaged candidate, externally accepted, and formally released are different states. Reopen an acceptance item when later changes invalidate its evidence.

Use the runtime's progress channel when available; otherwise report at the next user-visible output boundary. Update canonical owners first. Delegated-agent messages are internal evidence, not user-visible progress; the coordinating agent summarizes results. Do not split milestones merely to create updates, invent a time-based reporting cadence when the host does not require one, repeat unchanged status, or turn an update into a permission gate. Treat any host-required progress heartbeat separately.

Report immediately when evidence overturns the plan, a material scope, order, assumption, or authority boundary changes, a real blocker appears, or before stopping, handoff, release, or completion. Announce expensive or long work only when useful for control or recovery. Ask only when authority requires a user decision; otherwise adjust and continue without creating an approval step.

## Refresh context on observable events

Do not estimate, persist, or act on hidden runtime compaction counts. When resuming an existing project across a thread or context boundary, after a cross-day gap or handoff, or from explicit summarized, materially incomplete, or conflicting context, ensure the active instructions are loaded and re-read the smallest current authority set. Re-read this `SKILL.md` directly when the host exposes it.

Load `align-project-requirements` only when desired behavior or another material boundary needs renewed alignment. Load `organize-ai-project-files` only when topology, multiple referenced paths, or protected assets require structural work. Before release or a completion claim, re-check this skill's evidence and completion boundaries. If re-anchoring finds no material deviation, continue without creating an approval step.

## Handle long-running and release work

- Record a long-running command, code identity, start time, process/job identifier, progress location, and terminal condition. Resume monitoring instead of starting duplicates.
- Preserve useful failure evidence and diagnose before restarting a costly run.
- Treat release as a separate evidence boundary: fixed revision, declared worktree state, appropriate tests/builds, artifact manifest/hashes, known gaps, and required external acceptance.
- Never promote an artifact through a folder name, copied file, mock result, or unverified status flag.

Run `scripts/validate_continuity.py` only when the project already uses its compatible JSON acceptance ledger; pass project-relative paths only. When the handoff consistently cites acceptance IDs, add `--handoff-ledger-check warn` during recovery or `error` in an established CI gate. This check compares explicit IDs and status words, not arbitrary prose, and never replaces comparison with live project state.

## Leave a resumable boundary

At a durable stopping point, keep the handoff current and compact: objective/stage, verified results, unfinished or blocked work, live Git/worktree state, recent checks, risks, and one exact next action. Move closed chronology to linked history instead of appending indefinitely.

Declare completion only when the aligned definition of done is met and no required work remains. Report engineering completion and outstanding external acceptance separately.
