# Contributing

Thanks for helping improve Lightweight Project Skills. Contributions should preserve the project's core idea: use deterministic checks for fragile facts while leaving ordinary engineering judgment to the model.

## Start here

1. Search existing issues and discussions.
2. For a behavior change, describe the failure mode and the smallest useful change before editing a skill.
3. Fork the repository, create a focused branch, and keep unrelated changes out of the pull request.
4. Run the validation commands below.

Questions and early design ideas are welcome in [Discussions](https://github.com/KKLL2025/lightweight-project-skills/discussions). Reproducible defects and scoped feature requests belong in the issue forms.

## Local validation

The runtime scripts use only the Python standard library. From the repository root, run:

```sh
python -m unittest discover -s tests -v
```

If you have the Agent Skills structure validator installed, also run it once for every changed skill. The repository CI repeats the unit suite on Windows and Linux with Python 3.11 and 3.13.

## Changing a skill

- Preserve public entry paths under `skills/` unless an intentional rename is fully migrated across runtime references, documentation, tests, evaluations, community forms, and release notes.
- Prefer a narrow rule over a mandatory phase, artifact, or tool.
- Do not require a PRD, subagent, issue tracker, shell, or test method for every task.
- Add or update a focused test when a deterministic contract changes.
- Add an evaluation case when the intended difference is behavioral.
- Distinguish structural checks from model-behavior evidence.
- Never include credentials, private project material, internal reports, or machine-specific absolute paths.

### Behavior-change gate

Do not append a rule merely because it sounds safer or more professional. Before changing a `SKILL.md` behavior:

1. Capture an observable failure, recurring friction, or missing decision boundary.
2. Check whether the existing skill already covers it and the failure came from triggering, stale installation, or runtime behavior instead.
3. Prefer clarifying, replacing, or narrowing an existing rule over adding a parallel rule.
4. State when the new rule stays inactive so small and unrelated work does not inherit more ceremony.
5. Add a focused catalog case and any deterministic regression test the change permits.
6. Re-read all three ownership boundaries and remove wording that duplicates another skill.

If the evidence supports only a project-specific convention, document it in that project rather than promoting it into this general repository.

## Documentation and positioning

- Lead from the project's actual mechanism and verified boundary, not a generic problem/solution template.
- Do not turn familiar AI copy patterns, extra headings, repeated triads, or added detail into a substitute for evidence.
- Preserve useful structure when revising. Rewrite only the surface whose purpose, reader, or evidence has changed.
- Keep claims traceable to a test, reproducible scenario, case report, or explicitly labelled design intent.

## Pull request checklist

- [ ] The change has one clear purpose.
- [ ] Existing skill ownership boundaries remain understandable.
- [ ] Tests pass locally.
- [ ] Local Markdown links resolve.
- [ ] Documentation and `CHANGELOG.md` are updated when users would notice the change.
- [ ] Behavior claims include reproducible prompts, runtime identity, repeated runs, and a baseline where practical.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
