# Routing recipes

These recipes turn the architecture into concrete behavior. They are examples,
not permission grants: every agent remains limited by the user's actual request,
sandbox, approvals, and tool permissions.

## Thirty-second decision rule

Ask these questions in order:

1. Is there an unresolved architecture, product, security, authorization,
   production, data-integrity, destructive, or public-contract decision?
   Keep it with the parent.
2. Can one process finish the assignment directly from a self-contained packet
   and objective validation? Use Luna Max.
3. Must the delegated branch itself message, steer, or recursively delegate to
   agents and integrate dependent results? Select Terra High explicitly.
4. Is the work too small to justify handoff and review overhead? Keep it with
   the parent.

Task size is deliberately absent from the first three questions.

## Common scenarios

| Scenario | Route | Why |
|---|---|---|
| Search a repository for every use of an API and return file references | One Luna Max leaf | Clear, read-heavy, terminal, objectively checkable |
| Inspect two independent sites or repositories | Two Luna Max leaves owned directly by Sol | Independent scopes; no coordinator needed |
| Review logs, screenshots, or web pages and summarize evidence | Luna Max leaf | No cross-agent negotiation |
| Apply a decided mechanical rename to disjoint files | One or more Luna Max leaves | Bounded implementation with explicit ownership |
| Plan a migration with API, database, client, and test dependencies | Sol, optionally with a Terra High branch | Coordination and intermediate integration are material |
| Coordinate several reviewers and steer follow-up checks | Terra High branch | Proactive inter-agent communication is the work |
| Change authentication, payments, permissions, or production data | Parent | Protected boundary; delegation cannot own the decision |
| Make one high-impact one-line public contract change | Parent | Small size does not reduce risk |
| Classify thousands of stable records | Luna Max leaf or approved separate Luna task | High volume, low coordination, objective validation |

## Recipe 1 — one repository explorer

Use when one terminal read-only assignment can answer the question.

```text
OBJECTIVE
Find every call site of <API> and report which ones violate <rule>.

SOURCE OF TRUTH
<repository path>, <contract/document path>

IN SCOPE
Read-only search and targeted file inspection.

OUT OF SCOPE
No fixes, architecture changes, dependency updates, or external access.

AUTHORIZED ACTIONS
rg, file reads, and read-only local inspection.

DELIVERABLE
A deduplicated table: file, symbol, current behavior, evidence, confidence.

VALIDATION
Report the search patterns and reconcile the final count against raw matches.

STOP
Return on material ambiguity, a protected boundary, or two failed evidence-
based approaches. Do not spawn another agent.
```

Recommended execution: one native Luna Max leaf with `fork_turns="none"`.

## Recipe 2 — parallel independent leaves

Use when assignments do not share write ownership or depend on each other's
intermediate conclusions.

```text
Sol Max parent
├── Luna A: audit repository A, read-only
└── Luna B: audit repository B, read-only
```

The parent gives each leaf a complete packet, waits for both, independently
checks their evidence, reconciles disagreements, and concludes. Do not insert
Terra merely to collect two independent reports.

For write work, assign disjoint files explicitly:

```text
Luna A owns: src/importer/**
Luna B owns: tests/importer/**
No other writable paths are authorized.
```

If both need the same file, do not parallelize the writes.

## Recipe 3 — collaborative Terra branch

Use only when the branch's purpose includes coordination.

```text
OBJECTIVE
Coordinate a bounded migration audit across API, persistence, and tests.

WHY TERRA
The branch must delegate three dependent checks, steer follow-ups when their
results conflict, and integrate one intermediate migration recommendation.

AUTHORITY
Read-only. No architecture decision, migration execution, or production write.

CHILD OWNERSHIP
- Luna API leaf: API surface and contract evidence
- Luna data leaf: schema and integrity evidence
- Luna test leaf: coverage and reproducibility evidence

DELIVERABLE
One integrated report that preserves each leaf's evidence and identifies every
decision that belongs to the Sol parent.

STOP
Return immediately on a protected decision or when the branch would need new
user authority.
```

Recommended execution: explicitly select Terra High for this branch. Its
terminal children use the configured Luna Max default.

## Recipe 4 — Browser or web evidence

Luna is appropriate when navigation is evidence collection, not an external
business decision.

```text
OBJECTIVE
Inspect <pages> and report <observable behavior>.

AUTHORIZED
Open, navigate, read, screenshot, and collect console or network evidence.

PROHIBITED
No Save, Publish, Delete, purchase, message, account change, production setting,
or consent action.

VALIDATION
URL, timestamp, screenshot or exact visible evidence, and reproduction steps.
```

If the workflow requires deciding what to publish or changing a production
setting, the leaf returns the evidence and the parent requests or confirms
authority before mutation.

## Recipe 5 — a small implementation already decided

Luna can implement a small change when the decision is already made and the
acceptance test is objective.

```text
OBJECTIVE
Implement <exact behavior>.

OWNED FILES
- path/to/file-a
- path/to/file-b

INVARIANTS
- preserve <public behavior>
- no dependency changes
- no edits outside owned files

VALIDATION
Run <targeted command>; expected result <exact result>.

STOP
Return rather than redesigning if the stated implementation conflicts with the
code, tests, security, or a public contract.
```

Sol reviews the diff and validation before accepting it.

## Recipe 6 — exceptionally large autonomous batch

A separate user-owned Luna Max task is not a native subagent. Consider it only
when the batch is large enough to justify another user task, has stable sources,
needs little coordination, and has objective acceptance criteria.

The parent explains the split and waits for explicit user approval before
creating that task. See
[STANDALONE-LUNA-TASKS.md](STANDALONE-LUNA-TASKS.md).

## Anti-patterns

### “Use Terra because the task is big”

Wrong dimension. A large mechanical scan can be ideal for Luna. A tiny security
change can belong to Sol.

### “Use Luna because it is cheaper”

Cost is a benefit after admission, not the admission test. A cheap model on an
ambiguous or protected assignment is not a saving.

### “Always spawn the maximum number of agents”

Eight is a ceiling. Every child adds context, tool work, review cost, and
potential write conflicts.

### “Make Luna a peer by patching the catalog”

Do not do this. Current native delegation already exposes Luna as a leaf, and
the collaboration boundary remains meaningful.

### “Copy the entire parent history to be safe”

Long history can bury the actual contract. Send the smallest self-contained
packet that preserves objective, authority, invariants, ownership, validation,
and stop conditions.

### “The footer proves the model”

A footer is a reporting convention. Runtime metadata or the exact canonical
rollout is the proof. Follow [VERIFICATION.md](VERIFICATION.md).

## Parent acceptance checklist

Before presenting delegated work as complete, the parent checks:

- the child stayed inside its packet;
- every writable file had one owner;
- the evidence supports the conclusion;
- validation was actually executed;
- no protected decision was silently made;
- failures and limitations are disclosed;
- model and effort are proven when runtime identity matters;
- the final answer reflects parent judgment, not an unreviewed child summary.
