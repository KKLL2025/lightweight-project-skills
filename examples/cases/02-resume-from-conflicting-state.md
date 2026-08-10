# Recover from Conflicting Project State

## Situation

A multi-turn project has a handoff that says a CSV feature is complete, while the task owner still marks it unfinished. The source tree and checks are available.

## Prompt

> Continue this project. The handoff says CSV is complete, but the task ledger is not checked off. Resume from the current real state.

## Failure this scenario exposes

Treating the handoff as an authority can skip unfinished work or preserve a stale completion claim.

## Expected skill decision

`drive-large-project` should inspect the live source, Git state, task owner, acceptance owner when present, and relevant checks. It should repair the stale summary and resume at the first unfinished, unblocked outcome.

## Observable checks

- The agent does not infer completion from the handoff alone.
- Conflicting sources are resolved using the repository's authority order and live evidence.
- The updated handoff contains one current next action rather than copied history.

## Evidence boundary

This is a reproducible behavior scenario mapped to `D-01` in [`evals/cases.json`](../../evals/cases.json). A completed run must retain the raw prompt, runtime identity, output, scoring, and relevant fixture state before it can support a behavior claim.
