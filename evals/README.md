# Behavior Evaluation

[`cases.json`](cases.json) is a catalog of positive, negative, and pressure prompts. Its repository test validates catalog shape and coverage; it does not execute a model or prove behavior improvement.

## Evidence levels

- **Worked scenario:** explains the expected boundary and how to inspect it. It makes no runtime claim.
- **Exploratory pair:** one run without the target skill and one run with it, using the same prompt, fixture, model, and runtime. It may reveal a failure but cannot support a general performance claim.
- **Repeated comparison:** multiple isolated pairs with raw outputs and a predeclared rubric. Use this before describing a repeatable behavior difference.
- **Cross-runtime benchmark:** repeated comparisons across more than one model/runtime. This remains a pre-`v1.0.0` goal.

## Minimal exploratory protocol

1. Pin the repository commit and record the model, runtime, date, operating system, and available tools.
2. Prepare two isolated copies of the same safe fixture.
3. Run the raw prompt once without the target skill and once with the target skill loaded from the pinned commit.
4. Do not show the catalog's `success` or `failure` fields to the evaluated agent.
5. Preserve the complete redacted outputs and material file diffs.
6. Score each output against the pre-existing catalog criteria. Record ambiguity instead of forcing a pass or fail.
7. Publish the result as exploratory unless repeated runs justify a stronger claim.

## Suggested result record

```json
{
  "caseId": "D-01",
  "repositoryCommit": "<commit>",
  "condition": "baseline-or-with-skill",
  "model": "<model>",
  "runtime": "<runtime and version>",
  "date": "YYYY-MM-DD",
  "fixture": "<public path or redacted description>",
  "rawOutput": "<path>",
  "materialDiff": "<path or none>",
  "criterionResults": [],
  "notes": "<ambiguity, interruption, or environment limits>"
}
```

Never publish credentials, private project data, machine-specific absolute paths, or outputs whose redistribution is unauthorized.
