# Keep a Small Task Small

## Situation

An existing interface has one explicit text change and an established focused test. The user has already fixed the desired outcome; no product boundary is open.

## Prompt

> Change the login page submit button text to "Continue" and run the existing frontend test.

## Failure this scenario exposes

A project-management workflow can add more cost than the edit by demanding a PRD, a design document, or approval of routine implementation details.

## Expected skill decision

`align-project-requirements` should not activate a durable alignment workflow. The agent should inspect the current implementation, make the reversible edit, and run the smallest relevant check.

## Observable checks

- No new requirements, design, task, or handoff document is created.
- The existing code convention is used rather than re-designed.
- The focused frontend check runs and its actual result is reported.

## Evidence boundary

This is a reproducible behavior scenario mapped to `A-01` in [`evals/cases.json`](../../evals/cases.json). It documents the intended boundary; it is not evidence that every model will follow it.
