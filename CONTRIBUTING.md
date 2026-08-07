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

- Preserve the public entry paths under `skills/`.
- Prefer a narrow rule over a mandatory phase, artifact, or tool.
- Do not require a PRD, subagent, issue tracker, shell, or test method for every task.
- Add or update a focused test when a deterministic contract changes.
- Add an evaluation case when the intended difference is behavioral.
- Distinguish structural checks from model-behavior evidence.
- Never include credentials, private project material, internal reports, or machine-specific absolute paths.

## Pull request checklist

- [ ] The change has one clear purpose.
- [ ] Existing skill ownership boundaries remain understandable.
- [ ] Tests pass locally.
- [ ] Local Markdown links resolve.
- [ ] Documentation and `CHANGELOG.md` are updated when users would notice the change.
- [ ] Behavior claims include reproducible prompts, runtime identity, repeated runs, and a baseline where practical.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
