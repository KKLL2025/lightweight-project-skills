---
name: drive-large-project
description: Drive medium-to-large projects across turns or days while preserving scope, truthful state, evidence-backed acceptance, and resumable handoffs. Use when the user asks Codex to continue autonomously, resume staged work, coordinate milestones or long-running checks, or deliver an aligned specification. Skip for small fixes and one-turn changes.
---

# Drive Large Projects

Keep long work truthful and resumable without repeated confirmation.

## Start from reality

1. At the start of each Turn inside a long-running Goal, re-anchor to its contract and the smallest current authority set the host exposes; do not assume an automatic re-read.
2. Inspect repository instructions, live Git, relevant files, and the smallest current index/handoff before trusting status claims.
3. Reuse existing alignment, route, acceptance, execution, evidence, and layout owners. Do not create a second source of truth.
4. If the desired outcome or material boundary is unclear, use `align-project-requirements`. Otherwise resume the first unfinished, unblocked milestone without replaying completed work.

Use this authority order when sources conflict: latest user decision, repository rules, approved alignment/design, task and acceptance owners, current handoff, then history. Repair stale summaries after verifying the live state.

## Exercise judgment without ceremony

- Proceed through reversible in-scope analysis, code, tests, builds, documentation, and ordinary refactors. Decide routine technical details from project conventions and the aligned outcome.
- Ask only when a choice materially changes product direction, privacy/legal posture, irreversible production data or permissions, spending, public release, external communication, or authority beyond the user's delegation.
- Batch genuinely blocking questions. Continue other independent in-scope work when possible.
- Add process only in response to actual project complexity or observed failure risk.

## Keep the root and project tree clean during development

Follow `PROJECT_LAYOUT.json` or repository conventions. In the three-zone layout, use `01-ai-runtime/` for AI instructions and configuration, `02-project-control/` for governance and evidence, and `03-project-workspace/` for product work, assets, and outputs. Classify new root entries first and preserve framework-native structure.

Correct simple placement drift when the move is local, reversible, and has no path consumers. Use `organize-ai-project-files` for new structures, root changes, multiple or referenced moves, output separation, or protected assets. Folder governance is continuous; structural migration is specialized.

## Use only the durable state the project needs

- A one-turn task needs no new management documents.
- A multi-turn project normally needs a short document router/index and a current-only handoff.
- Add a durable task owner when several milestones must preserve execution state across Turns. Keep the current Turn Plan in the host unless persistence is needed for recovery.
- Add an acceptance ledger only when multiple criteria, external validation, or evidence gaps must survive across sessions.
- Store raw logs, screenshots, manifests, and old milestone details outside the default read set.

Read [artifact-templates.md](references/artifact-templates.md) for templates, [context-lifecycle.md](references/context-lifecycle.md) for growing, duplicated, or uncertain recovery context, and [execution-control.md](references/execution-control.md) for ordered outcomes, expensive validation, or delegated work.

Give each changing fact one owner: alignment owns the Goal contract, desired behavior, and Project Route; tasks own milestone state; the host Turn Plan owns the current Turn; the acceptance ledger owns evidence; the handoff owns the current summary and next action; the layout contract owns folder roles. References may point to these facts but must not maintain competing copies.

## Work in outcome-sized milestones

For the active milestone:

1. State the observable outcome and relevant boundary or acceptance IDs.
2. Write a Turn Plan for this milestone only; its final item must verify, record evidence, report milestone state, and end the Turn.
3. Inspect or reproduce current behavior.
4. Implement the smallest coherent vertical slice.
5. Run focused checks, then broader checks proportional to risk.
6. Exercise the real user/runtime path when practical.
7. Record evidence and gaps honestly; update the task, acceptance owner when present, and concise handoff.
8. At milestone completion, re-anchor against the Goal contract, Project Route, non-goals, authority, evidence, live state, and next unblocked result.
9. Send a brief user-visible update with the verified result, evidence, material gaps, and next milestone.
10. End the Turn at the resumable boundary declared by the final plan item.

Revise the Turn Plan when evidence changes an assumption, dependency, validation path, or safe slice, but keep revisions inside the current milestone. Do not use repeated updates to cross into the next milestone or execute the whole project in one Turn.

Complete small, clear work directly. For stateful, resource-heavy, cross-module, or multi-agent work, default to one current milestone per Turn; the milestone may continue in a later Turn if it cannot finish safely. Related outcomes may share a Turn only for small work or explicitly continuous low-risk work when evidence and recovery remain intact. "Do everything" or "do not stop" does not make substantial work low-risk or authorize silent milestone crossings. Monitoring does not conceal new development.

Cross modules only for the active outcome, dependency, vertical path, blocker bypass, or high-risk seam. Record a short reason in the existing plan when evidence materially reorders work; do not opportunistically rescan or recreate the roadmap.

Do not claim more than the evidence establishes. Code written, locally checked, packaged candidate, externally accepted, and formally released are different states. Reopen an acceptance item when later changes invalidate its evidence.

Use the runtime's progress channel or the next user-visible boundary. Update canonical owners first. Delegated-agent messages are internal evidence; the coordinator summarizes them. Do not split milestones merely to create updates, invent a time-based reporting cadence when the host does not require one, repeat unchanged status, or turn updates into a permission gate. Treat any host-required progress heartbeat separately.

Report when evidence overturns the plan, a material boundary changes, a blocker appears, or before stopping, handoff, release, or completion. Announce expensive work only for useful control or recovery. Ask only when authority requires a decision; otherwise adjust without creating an approval step.

Keep Goal state honest: routine discoveries do not rewrite it, milestone completion does not complete it, and human direction ends the Turn through the host's pause mechanism when available. Follow host semantics for `blocked`; never misuse blocked or complete to stop execution. Read [execution-control.md](references/execution-control.md) for the planning and Goal-state rules.

## Refresh context on observable events

Do not estimate, persist, or act on hidden runtime compaction counts. After a context boundary, cross-day gap, handoff, or from explicit summarized, materially incomplete, or conflicting context, load active instructions and the smallest current authority set. Re-read this `SKILL.md` directly when the host exposes it.

Load `align-project-requirements` only for renewed material alignment and `organize-ai-project-files` only for structural work. Before release or completion, re-check evidence and completion boundaries. If nothing material changed, continue without creating an approval step.

## Handle long-running and release work

- Record a long-running command, code identity, start time, process/job identifier, progress location, and terminal condition. Resume monitoring instead of starting duplicates.
- Preserve useful failure evidence and diagnose before restarting a costly run.
- Treat release as a separate evidence boundary: fixed revision, declared worktree state, appropriate tests/builds, artifact manifest/hashes, known gaps, and required external acceptance.
- Never promote an artifact through a folder name, copied file, mock result, or unverified status flag.

Run `scripts/validate_continuity.py` only when the project already uses its compatible JSON acceptance ledger; pass project-relative paths only. When the handoff consistently cites acceptance IDs, add `--handoff-ledger-check warn` during recovery or `error` in an established CI gate. This check compares explicit IDs and status words, not arbitrary prose, and never replaces comparison with live project state.

## Leave a resumable boundary

At a durable stopping point, keep the handoff current and compact: objective/stage, verified results, unfinished or blocked work, live Git/worktree state, recent checks, risks, and one exact next action. Move closed chronology to linked history instead of appending indefinitely.

Declare completion only when the aligned definition of done is met and no required work remains. Report engineering completion and outstanding external acceptance separately.
