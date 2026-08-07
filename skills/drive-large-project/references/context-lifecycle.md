# Context and Document Lifecycle

Use this reference when project Markdown grows enough to make routine resume reads expensive or when reorganizing project documentation.

## Core rule

Optimize the default read set, not merely the number of files. Splitting one large document into many files provides no benefit if every file remains mandatory.

## Classify documents

### Hot

Read on every project resume. Keep this set small:

- repository rules and hard constraints;
- document router/index;
- current-only handoff;
- compact current acceptance summary when needed.

Hot documents should answer what is authoritative, what is happening now, what can break, and what to do next. Move architecture catalogs, complete command lists, long completion inventories, and chronology out of the hot set.

### Warm

Read only when selected by the active task:

- current requirements, design, and tasks;
- module architecture and data contracts;
- deployment, migration, security, and recovery guides;
- relevant acceptance criteria and known limitations.

Inspect headings, search terms, or stable IDs first. Load only relevant sections unless the task changes the whole document's authority or structure.

### Cold

Do not read by default:

- completed milestones and superseded plans;
- full command transcripts and old verification snapshots;
- raw logs, screenshots, recordings, manifests, and evidence collections;
- closed investigations and previous release details.

Keep cold material discoverable through the index, acceptance ledger, milestone capsules, and Git history.

## Give dynamic state one owner

Context control fails if several short files disagree. Use one canonical writer for each changing concern:

- repository instructions own stable policy and hard constraints;
- the document index owns routing and authority relationships, not phase progress;
- the task plan owns per-task execution state;
- the acceptance ledger owns per-criterion evidence state and counts;
- the handoff owns a replaceable summary of current stage, external state, risks, and exact next action.

Other files may reference stable IDs and authority paths, but should not independently maintain temporary phrases such as "not created", "currently running", or copied completion counts. When a task changes, update its owner first and then refresh the handoff summary.

## Trigger compaction

Compact or archive when any of these become true:

- the handoff exceeds roughly 240 lines or 20,000 characters;
- closed chronology or repeated verification occupies more than half of the handoff;
- the same current status or decision is maintained in more than one authority file;
- a resume requires reading completed phase specifications or full evidence directories;
- an exact next action is difficult to locate quickly;
- current facts and historical facts are interleaved.

Treat these as defaults, not immutable product limits. Lower them for context-sensitive environments and raise them only with a documented reason.

## Compact semantically

For closed work, retain:

1. outcome;
2. decision and durable rationale;
3. invariant future work must preserve;
4. evidence or revision pointer;
5. condition that requires reopening or revalidation.

Remove from the hot copy:

- chronological narration with no current consequence;
- repeated test totals superseded by a newer baseline;
- raw command output already stored as evidence;
- obsolete next steps and historical worktree snapshots;
- duplicated architecture or command catalogs available elsewhere.

## Preserve exact material

Do not use lossy compression for:

- active acceptance criteria and approved requirements;
- security, privacy, legal, licensing, migration, or data-loss constraints;
- unresolved risks and user decisions;
- raw evidence required for audit;
- a failure record that explains a still-relevant defect;
- an interface or schema contract currently being implemented.

Move exact material to a stable warm or cold file and link it. Do not silently rewrite its meaning.

## Resume in two stages

### Stage 1: orient

Read repository rules, the project index, the current handoff, `git status`, and recent history. Determine the active phase, exact next action, relevant acceptance IDs, and dirty-worktree ownership. Check that artifacts named as missing or complete actually exist and that the handoff's next task agrees with the task plan and acceptance ledger.

### Stage 2: retrieve

Use the index and stable IDs to load only the required scope sections, current spec/design/task sections, module documentation, and evidence. If documents conflict, prefer live state and the defined authority order, then repair the stale document.

## Rotate safely

1. Identify the exact closed range and verify it has no current-only facts.
2. Preserve it verbatim in a dated or versioned archive when audit value exists.
3. Add a semantic milestone capsule and links from the current handoff or index.
4. Replace duplicated completion lists with acceptance-ledger counts and the most recent baseline.
5. Re-run link, acceptance, and continuity validation.
6. Forward-test resume behavior from a fresh context.
