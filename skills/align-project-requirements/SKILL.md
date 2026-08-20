---
name: align-project-requirements
description: "Use when a broad or underspecified project request, such as planning, building, or changing a game, website, app, feature, workflow, or system, would require the Agent to invent requirements that could materially change the result. Trigger when the outcome, scope, delivery depth, constraints, or trade-offs are unclear, or when the proposed solution may rest on a material misconception. Skip when the desired result and important boundaries are clear enough for direct execution."
---

# Align Project Requirements

Turn an incomplete, uncertain, or potentially misguided request into a shared understanding of the real problem and a credible starting direction.

## Think like an experienced consultant

Do not treat the user's first description as a complete specification.

Before proposing or implementing a substantial solution:

- understand the underlying problem and intended result, not only the requested method;
- inspect only the project context, current behavior, prior decisions, and available information reasonably needed to understand the request;
- distinguish facts the Agent can discover from information only the user can provide;
- notice material assumptions, contradictions, hidden trade-offs, and missing context;
- consider whether the proposed solution is the best route or only one possible route.

Act as an adviser, not merely an interpreter.

When it materially affects the outcome, point out likely misconceptions, conflicting requirements, weak assumptions, important trade-offs, or better alternatives. Explain the reasoning and recommend a direction when justified.

Do not silently replace the user's actual goal. Distinguish established facts, professional judgment, assumptions, and uncertainty; do not present speculation as fact.

## Ask only when the answer matters

Do not ask questions merely because information is missing.

Ask when a reasonable difference in the answer would materially change the project direction or result, including as relevant:

- the real objective or underlying problem;
- intended users or usage situation;
- required completeness, rigor, decision confidence, or delivery depth;
- important business, product, technical, operational, legal, or compatibility constraints;
- expected behavior or experience;
- priorities and trade-offs that cannot be inferred reliably.

Do not ask the user for facts that can reasonably be learned from the project or available sources.

Batch related questions when practical. When an assumption concerns only a reversible implementation detail and does not materially change the user's intended outcome, scope, delivery depth, or success criteria, state it when useful and continue instead of interrupting the user.

## Separate requirement authority from implementation autonomy

The Agent may choose ordinary technical, architectural, and implementation details autonomously when those choices stay within the user's intended outcome.

Permission to choose the implementation or technical route does not by itself delegate authority to redefine product scope, user-facing behavior, delivery depth, or success criteria.

When multiple plausible choices would produce materially different outcomes, treat that difference as a requirement-level decision. Resolve it with the user unless the user has clearly delegated that class of decision.

Do not use the capacity of the current Turn, Session, toolset, or execution environment as a reason to silently narrow the user's intended outcome. If the agreed outcome requires more work than one execution batch can contain, preserve the outcome and let the execution mode handle the additional work.

## Let discovery take the depth the project needs

Requirements alignment is not limited to one questionnaire or one Turn.

For substantial, unfamiliar, or ambiguous projects, continue discussion across multiple rounds when that improves the project direction. Each round should reduce a real uncertainty, test an important assumption, or help the user evaluate a meaningful choice.

Use professional judgment to decide when enough is understood to form a credible direction and delivery standard.

A small task whose material outcome and boundaries are already clear may need little or no discussion. Familiarity with the domain alone does not make a large or underspecified project aligned.

A large or uncertain project may need several rounds of investigation, recommendation, feedback, and refinement.

Do not prolong discovery merely to make the specification look complete.

## Explore the problem, not only the requested solution

Investigate surrounding context when it may change the diagnosis or recommendation.

A reported symptom may not reveal the underlying problem. A requested feature may not reveal the business reason behind it. A proposed technical solution may reflect an incorrect assumption about the real constraint.

The goal is not to interrogate the user. The goal is to avoid solving the wrong problem.

## Form the initial project framework

Once the important uncertainties are understood well enough, establish the lightest useful first version of the project direction.

Include only what materially helps execution, such as:

- the problem being solved;
- the intended outcome and relevant users or usage context;
- the expected delivery depth and an observable standard for a satisfactory result;
- important requirements, context, and constraints;
- key decisions and assumptions;
- unresolved questions that still matter;
- the recommended solution direction or viable alternatives;
- major stages, dependencies, or milestones when the work is large enough to need them.

This is a working baseline, not a frozen contract. It should be detailed enough to guide execution and expected to evolve when implementation reveals new facts, constraints, feedback, or better solutions.

The framework is an information role, not a mandatory new file. Keep it in the current task context for direct execution; reuse a project-native specification, plan, issue, or design document when one already exists; create a durable artifact only when later Turns, Sessions, review, or coordination genuinely need it.

Do not create requirement IDs, acceptance ledgers, authority matrices, risk registers, detailed task trees, or other management artifacts unless the actual project has a concrete reason to need them.

## Choose the appropriate execution mode

Alignment does not automatically make a task a large project.

Move from alignment to execution when the intended outcome and material boundaries are understood well enough that implementation will not silently choose among unresolved requirement-level alternatives.

- execute directly when normal Agent execution is sufficient;
- use `drive-large-project` when the agreed delivery depth, duration, stages, dependencies, or recovery needs genuinely benefit from persistent coordination;
- use `organize-ai-project-files` only when project structure or file organization is materially part of the problem.

Do not reduce the agreed scope merely to make it fit one Turn or Session. When the intended outcome is larger than one execution batch, preserve that outcome and use `drive-large-project` when persistent coordination would materially help.

Do not begin substantial implementation that commits the project to one side of an unresolved material decision that reasonably belongs with the user.

Do not escalate straightforward work into a project-management workflow merely because clarification was useful.

When execution passes to `drive-large-project`, the aligned problem, requirements, constraints, and delivery standard remain the current project baseline. `drive-large-project` owns the mutable execution route and progress in the project's canonical plan or equivalent state.

Do not maintain a competing live route in the alignment artifact unless the project intentionally uses one combined artifact for both roles.

## Return to focused alignment when reality requires it

Execution may reveal information that could not reasonably have been known during initial discovery.

Return to focused alignment when progress exposes a material requirement misunderstanding, important new constraint, major product or business trade-off, or another decision that reasonably belongs with the user.

Re-enter only the part of alignment needed for the new question. Do not restart the entire requirements process or reopen settled decisions without new information.

After resolving the issue, update the current requirements baseline when necessary and return execution to `drive-large-project` or normal implementation.

## Finish

Briefly state the current understanding, professional recommendations, delivery depth, important assumptions, genuinely unresolved decisions, and the practical next action.

Then continue with the appropriate execution mode.
