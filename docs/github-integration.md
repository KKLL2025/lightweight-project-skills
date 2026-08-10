# GitHub Integration Without Making GitHub Mandatory

The three skills remain useful in a non-Git project. GitHub adds a delivery and feedback surface; it does not become a second owner for requirements, task state, acceptance state, or layout roles.

## Local work and external actions

Local inspection, edits, tests, builds, commits, and evidence preparation can proceed when they are already in scope. Pushing a branch, opening or merging a pull request, publishing a release, changing repository settings, and posting public messages are external actions and require the user's authorization.

## Recommended delivery path

1. Read repository instructions and inspect the live worktree before trusting a handoff.
2. Pin the comparison base and keep the branch focused on one declared outcome.
3. Run validation proportional to the claim and record remaining gaps.
4. Review the diff against both the intended outcome and repository standards.
5. Commit only the intended files with a description of the delivered outcome.
6. Push and open a pull request only when externally authorized.
7. Treat merge and release as separate evidence boundaries. A merged commit is not automatically a published release, and a release is not external acceptance.

## Mapping to the core skills

- `align-project-requirements` supplies the desired outcome, non-goals, acceptance boundary, and external-authority limits.
- `drive-large-project` owns the current execution state, validation evidence, resumable boundary, and release gap.
- `organize-ai-project-files` applies when a change moves referenced paths, repository roots, outputs, or protected assets.

GitHub Issues or pull requests may point to these owners, but should not silently maintain competing copies of changing project facts.

## Why this is a guide, not a fourth core skill

Branch names, review rules, merge queues, release permissions, and issue conventions vary by repository. Keeping the integration here preserves the local-first core. If repeated case reports reveal one stable, reusable GitHub workflow that is not already covered by existing tools, it can be evaluated later as an optional companion skill.
