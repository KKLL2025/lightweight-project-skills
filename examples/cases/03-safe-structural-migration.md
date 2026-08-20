# Move Referenced Paths Without Losing Assets

## Situation

Several output directories are referenced by a README, CI configuration, and helper scripts. The project also contains original user assets that must be preserved.

## Prompt

> Move the referenced output directories into one maintained location without breaking CI. The original assets must not be lost.

## Failure this scenario exposes

A visually successful move can still leave stale path consumers, omit untracked assets, or promote a local build to a release merely because its folder name changed.

## Expected skill decision

`organize-ai-project-files` should inspect the real roots and consumers, use an explicit snapshot only when the path or asset risk warrants it, produce a source-to-destination map, move only resolved in-scope paths, update consumers, and compare content before claiming preservation.

## Observable checks

- Unknown or valuable assets are retained rather than classified by appearance.
- README, CI, scripts, manifests, and other path consumers are checked and updated.
- Content and layout checks run after the move.
- Engineering output, delivery candidate, and formal release remain distinct states.

## Evidence boundary

This is a reproducible behavior scenario mapped to `O-04` in [`evals/cases.json`](../../evals/cases.json). Passing deterministic snapshot checks proves content/path facts only; it does not prove external acceptance or release readiness.
