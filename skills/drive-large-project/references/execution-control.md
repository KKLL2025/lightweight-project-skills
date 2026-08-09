# Adaptive Execution Control

Read this reference when several outcomes or modules must be sequenced, work may consume substantial time or resources, or delegated work needs coordination. Keep simple tasks direct.

## Maintain two planning levels

Use a macro route only when the project has meaningful staging or dependencies. Capture the current product stage, dependency or vertical-delivery order, external gates, contracts that must stabilize first, work that can proceed independently, acceptance order, and deliberately deferred areas.

Under that route, keep a rolling execution horizon containing only:

- the current stage outcome and active milestone;
- the next useful outcome candidates and their entry conditions;
- dependencies or external gates;
- evidence that would justify changing the order.

Do not prescribe a fixed candidate count or turn distant guesses into commitments. Give changing execution state one existing owner, such as the project task plan; summarize only the current entry in the handoff.

## Switch modules for a reason

Cross-module work is appropriate when it completes a vertical user path, follows a dependency, bypasses a real blocker with independent work, stabilizes a high-risk seam, or serves one observable outcome. Avoid repeated whole-project rescans and unrelated opportunistic work.

When new evidence materially reorders the route, update the plan owner and record one short reason. Reordering is not a reason to rewrite stable alignment or recreate the roadmap.

## Select a user-visible execution batch

- Complete small, explicit, reversible, cheaply verified work in one batch.
- For stateful, resource-heavy, cross-module, or delegated work, prefer one major outcome before the next user-visible boundary.
- Continue through closely related outcomes when the user requested continuous execution, risk and cost remain controlled, and every outcome retains separate evidence.
- Keep monitoring and waiting attached to the recorded job. Do not use monitoring time to start unrelated development.

A milestone update is not a request for routine permission. Stop only for a real authority boundary, material decision, unsafe or irreversible action, exhausted useful work, or an explicit user stopping condition.

## Report observable events

Always summarize a completed outcome-sized milestone. Also report when evidence changes the plan, scope/order/assumptions/authority materially change, a real blocker appears, or work is stopping, handing off, releasing, or claiming completion.

Report the start of a long or expensive operation only when it gives the user useful control or recovery information. A delegated agent's message is not user-visible progress; the coordinating agent owns a concise summary of material results.

Use the host's progress channel when available and otherwise use the next output boundary. Do not invent a timer, duplicate an unchanged status, or split work only to generate updates.

## Escalate validation from evidence

Choose the cheapest level that can establish the claim, then broaden only when risk or evidence requires it:

1. Focused checks for the changed unit, file, or behavior.
2. Integration checks when contracts, modules, persistence, configuration, or consumers interact.
3. End-to-end, real-runtime, or external checks when the acceptance claim depends on them.

Derive security validation from the active threat model and changed trust boundaries. Escalate when work changes untrusted input handling, instruction or code execution, identity, permissions, secrets, private data, external communication, or production control. Do not introduce generic security, network, privacy, abuse, or adversarial testing merely because a request says audit, risk, robustness, or validation.

## Budget delegated and heavy work

- Delegate or parallelize only independent work with a clear expected time, coverage, or review benefit.
- Give delegated work a bounded outcome and require evidence; the coordinating agent integrates and reports it.
- Do not repeat an unchanged full test suite, scan, build, or research pass without new code, new evidence, or a specific unresolved failure.
- Preserve identifiers and logs for costly jobs so monitoring resumes the same work instead of starting duplicates.
- If cost or duration becomes materially different from the authorized plan, report and reselect the execution boundary.
