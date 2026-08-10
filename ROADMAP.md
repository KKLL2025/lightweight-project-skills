# Roadmap

The project stays lightweight unless evidence shows that more machinery is necessary.

## Evidence grows in stages

Worked scenarios make the intended boundary reviewable. A single with-skill/without-skill pair is exploratory. Repeated isolated comparisons can support a narrow behavior claim. Cross-runtime comparisons and independent real-project reports are required before stable performance claims.

These stages are cumulative evidence levels, not one large test project that every preview must finish. See [`evals/README.md`](evals/README.md) for the minimal protocol.

## Before `v1.0.0`

- Expand the evaluation catalog to at least 12 scenarios per skill.
- Repeat blind with-skill and without-skill runs across at least two model/runtime combinations.
- Publish raw prompts, environment identities, scoring rules, repeated-run results, and variance.
- Verify installation and triggering in at least two Agent Skills-compatible harnesses.
- Run real internal and external symlink tests on Linux and an appropriately privileged Windows environment.
- Add complete fixtures for a mature frontend repository, a monorepo, a data/content project, and a Windows non-Git project.
- Accumulate independent real-project reports before making stable performance claims.

## Possible later work

- A read-only project doctor that reports conflicting owners, stale handoffs, layout drift, and missing release evidence.
- Optional installation helpers only if manual copying becomes a demonstrated source of errors.

## Explicit non-goals

- A mandatory PRD-to-epic-to-issue pipeline.
- A fixed project phase operating system.
- Requiring Bash, GitHub Issues, TDD, or subagents for every task.
- Replacing live repository and runtime evidence with generated status documents.
