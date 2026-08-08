<div align="center">

# Lightweight Project Skills

**Three lightweight Agent Skills that keep AI projects aligned, resumable, and structurally safe—without turning every task into ceremony.**

[简体中文](README.zh-CN.md)

[![CI](https://github.com/KKLL2025/lightweight-project-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/KKLL2025/lightweight-project-skills/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/KKLL2025/lightweight-project-skills?include_prereleases&label=release)](https://github.com/KKLL2025/lightweight-project-skills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-4b3baf)](https://agentskills.io)

</div>

```bash
npx skills add KKLL2025/lightweight-project-skills
```

One repository, three composable skills: **Align → Drive → Organize.** Align material decisions, resume long-running delivery from evidence, and reorganize project folders without losing files or breaking path consumers. Choose one skill or all three when prompted.

Lightweight Project Skills assumes the model can make ordinary engineering decisions. It adds structure only where ambiguity, continuity, evidence, or filesystem safety makes structure useful. It does **not** require a PRD for every change, fixed phase files, a specific issue tracker, Bash, TDD for every task, or a fresh subagent for every step.

> [!IMPORTANT]
> `0.5.0-preview` is a public preview. The deterministic checks are tested, but behavior evidence is still limited to a small Codex sample. Test these skills in your own runtime before relying on them for critical work.

## Choose the right skill

| Situation | Use | Owns |
|---|---|---|
| The material outcome, user, boundary, or acceptance is unclear | [`align-project-requirements`](skills/align-project-requirements/SKILL.md) | Desired behavior, material decisions, assumptions, observable acceptance |
| Delivery spans turns, milestones, or long-running checks | [`drive-large-project`](skills/drive-large-project/SKILL.md) | Current state, milestones, evidence, resumable handoff, ordinary file placement |
| The project tree or referenced paths need structural change | [`organize-ai-project-files`](skills/organize-ai-project-files/SKILL.md) | Topology, safe migration, protected assets, path consumers, output boundaries |
| The task is small, explicit, reversible, and verifiable now | Execute directly | No management artifact is required |

```text
unclear material outcome -> align-project-requirements
multi-turn delivery      -> drive-large-project
structural path change   -> organize-ai-project-files
small explicit task      -> execute directly
```

The skills coordinate without duplicating ownership. Requirements do not maintain execution status, handoffs do not become acceptance ledgers, and folder names do not prove release state.

During long delivery, `drive-large-project` reports completed outcome-sized milestones, re-anchors to the aligned outcome, boundaries, evidence, and live state, then continues unless a material blocker requires input. It does not invent timer-based interruptions or pretend to know a host's hidden context-compaction count; host-required progress heartbeats still apply.

## 30-second install

> [!NOTE]
> Upgrading from `v0.4.0-preview`? `spec-workflow` was renamed to `align-project-requirements`. Before reinstalling, remove only the old `spec-workflow` copy that came from this repository; verify its source first and do not delete an unrelated provider or plugin skill with the same name. Keeping this repository's old and new copies active can produce duplicate routing.

### One command (recommended)

With Node.js and npm available, let the open-source [`skills` CLI](https://github.com/vercel-labs/skills) discover the three skills and choose the target agent and installation scope:

```bash
npx skills add KKLL2025/lightweight-project-skills
```

To copy all three into the current project's Codex-compatible skill directory without prompts:

```bash
npx skills add KKLL2025/lightweight-project-skills --skill '*' --agent codex --yes --copy
```

The repository has been smoke-tested for remote discovery and a project-scoped copy install of all three skills. Review skills before installing them; installed skills run with the permissions of your agent.

### Manual fallback

Copy one or all folders under `skills/` into the Agent Skills directory used by your harness.

### Codex on Windows PowerShell

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills'
Copy-Item -Recurse -Force skills\align-project-requirements $target
Copy-Item -Recurse -Force skills\drive-large-project $target
Copy-Item -Recurse -Force skills\organize-ai-project-files $target
```

### POSIX-style environment

```sh
mkdir -p ~/.codex/skills
cp -R skills/align-project-requirements ~/.codex/skills/
cp -R skills/drive-large-project ~/.codex/skills/
cp -R skills/organize-ai-project-files ~/.codex/skills/
```

Restart or refresh the harness after installation. For other Agent Skills-compatible runtimes, use that runtime's documented skill directory rather than assuming the Codex path.

## Example prompts

```text
Use $align-project-requirements to align this product change, then continue if no material decision blocks implementation.

Use $drive-large-project to resume from the live project state and complete the next unblocked outcome.

Use $organize-ai-project-files to clean this project root without breaking framework-native paths or losing user assets.
```

See [examples](examples/README.md) for routing examples and the three-zone versus compatible-repository layouts.

## Folder governance

New AI-led or mixed project containers can use a clean three-zone shell:

```text
project/
├── AGENTS.md
├── README.md
├── 01-ai-runtime/
├── 02-project-control/
└── 03-project-workspace/
```

Existing framework repositories use compatibility mode. Required files such as `package.json`, `src/`, `app/`, CI configuration, or monorepo manifests stay where their tools expect them.

## Verification

The runtime skills have no third-party Python dependency. Run the repository suite with:

```sh
python -m unittest discover -s tests -v
```

CI runs the suite on Windows and Linux with Python 3.11 and 3.13. It covers skill contracts, layout boundaries, content-preserving moves, duplicate files, path escape, symlink policy, continuity-ledger validation, UTF-8 paths, repository links, and public-repository hygiene.

The catalog in [`evals/cases.json`](evals/cases.json) contains positive, negative, and pressure prompts. It separates raw prompts from expected behavior so evaluators can run blind forward tests.

Passing structural tests does not prove that every model follows a skill. Publish behavior claims only with the raw prompt, output, model/runtime identity, repeated runs, and a baseline without the skill.

## Verified and not yet verified

Verified for this preview:

- all three skills pass the local skill structure validator;
- the Python unit suite passes locally on Windows;
- small-task non-interference, stale-handoff recovery, compatible repository layout, and routing boundaries received limited Codex forward tests;
- runtime scripts use the Python standard library only.

Not yet established:

- statistically meaningful multi-model behavior improvements;
- long-term operation across many independent public projects;
- full installation testing across every Agent Skills-compatible runtime;
- production or safety certification.

See the [roadmap](ROADMAP.md) for the evidence required before a stable `v1.0.0` claim.

## Design references

This project learned from the engineering discipline and discoverability of [Superpowers](https://github.com/obra/superpowers), [GSD Core](https://github.com/open-gsd/gsd-core), [CCPM](https://github.com/automazeio/ccpm), and the [Agent Skills specification](https://agentskills.io). Its deliberate difference is proportional governance: deterministic checks for fragile facts, broad model judgment for ordinary work.

No benchmark badge or superiority claim is published without reproducible evidence.

## Contributing and support

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill or evaluation.
- Use [GitHub Discussions](https://github.com/KKLL2025/lightweight-project-skills/discussions) for questions.
- Use an issue form for reproducible bugs or feature proposals.
- Report security problems privately as described in [SECURITY.md](SECURITY.md).

Project conduct is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE). Attribution for incorporated upstream work is preserved in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
