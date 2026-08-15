# Architecture and routing policy

## Objective

Keep authority and cross-cutting judgment in a Sol Max parent while moving
independent, noisy, or high-volume execution into native Luna Max leaves.
Select Terra High only when a bounded branch must itself coordinate agents,
communicate proactively, delegate recursively, or integrate dependent
intermediate results.

This uses Codex's documented `features.multi_agent` and `[agents]` settings.
There is no custom role to install, compatibility layer to force, model cache
to patch, or catalog to override.

## Topology

```text
Sol Max parent
├── Luna Max leaf                 independent terminal assignment
├── Luna Max leaf                 independent terminal assignment
└── Terra High branch lead        collaborative bounded subproject
    ├── Luna Max leaf
    └── Luna Max leaf
```

Sol may coordinate several Luna leaves directly. Terra is not a mandatory
middle layer.

## Responsibilities

### Sol Max — parent owner

Sol frames the objective and invariants, owns user authorization, decides
architecture/product/security/production questions, chooses the execution
shape, reviews evidence, integrates accepted work, and concludes.

### Luna Max — default native leaf

Luna completes one self-contained assignment with objective validation. It is
well suited to repository and document scans, web or Browser evidence,
console inspection, tests, deterministic transformations, high-volume
classification, and small implementation already decided by the parent.

A Luna leaf may use its tools and edit only explicitly owned files when the
user authorized implementation. It does not coordinate peers, steer another
agent, recursively delegate, modify the global objective, or decide a
protected boundary.

### Terra High — collaborative branch lead

Terra owns a bounded subproject only when that branch needs proactive
inter-agent communication, recursive delegation, steering, or materially
deeper intermediate reasoning. Terra may delegate terminal packets to Luna
leaves, combine their evidence, and return one result to the parent.

Terra still cannot broaden authority or take architecture, security,
production, product, or public-contract decisions away from the parent.

### Luna Max — optional separate user task

A separate user-owned Luna Max task remains available for an exceptionally
large autonomous batch. Creating that new task is different from spawning a
native Luna leaf and requires explicit user approval for that occurrence.
See [Standalone Luna Max tasks](STANDALONE-LUNA-TASKS.md).

## Routing gate

| Dimension | Luna Max leaf | Terra High branch | Keep with parent |
|---|---|---|---|
| Work shape | Independent terminal assignment | Dependent subproject requiring coordination | Tightly coupled or cross-cutting |
| Ambiguity | Clear interpretation | Several bounded intermediate choices | Material unresolved decision |
| Communication | Return once or request parent attention | Proactive agent messaging or steering | User/product/architecture arbitration |
| Delegation | No recursive delegation | May delegate bounded leaves | Owns the overall tree |
| Validation | Objective and available | Several objective results to integrate | Subjective, missing, or high-stakes |
| Security/data | No protected boundary | No protected decision delegated | Auth, permissions, secrets, payments, integrity |
| Ownership | Explicit sole owner per writable file | Disjoint owners across its branch | Shared or conflicting ownership |

Task size never decides the route by itself. A large mechanical inventory may
fit Luna, while a one-line authorization change belongs to the parent.

## Delegation packet

Every child receives:

1. objective;
2. minimal context and exact sources of truth;
3. in-scope and out-of-scope boundaries;
4. authorized and prohibited actions;
5. invariants;
6. exact writable files, each with one owner, or `none`;
7. expected deliverable;
8. objective validation;
9. stop and return conditions;
10. runtime-model footer rule.

Start read-only unless implementation or mutation was explicitly authorized.
Parent instructions never broaden the user's authority.

## Context policy

For Luna leaves, prefer a self-contained packet with no inherited parent
turns. Use a small positive fork, normally one to three recent turns, only
when those turns contain an essential decision. Do not fork the complete
parent history by default.

This is a context-quality rule, not a claim that Luna cannot inherit context.
Luna can receive focused context; the goal is to avoid sending years of
architecture discussion, unrelated logs, or duplicated instructions to a
terminal worker.

Terra may receive more context when it must coordinate a branch, but the same
minimal-context principle applies.

## Stop and escalation rules

A child stops immediately and returns the exact issue when:

- ambiguity becomes material;
- an unmade decision is required;
- the assignment would expand beyond its packet;
- security, authentication, authorization, data integrity, destructive
  migration, production, or a public/cross-system contract is involved;
- new user authority is required.

After two distinct evidence-based attempts fail, the child stops retrying and
returns the evidence, remaining plausible hypotheses, and exact blocker.

External publication, production mutation, commit, push, deployment, purchase,
or destructive action still requires explicit user authorization and a
bounded parent instruction.

## Concurrency and ownership

`max_concurrent_threads_per_session = 8` is a ceiling, not a target. Use one
agent when one agent is sufficient. Parallelize only independent assignments
with independent validation and disjoint writable ownership. Two agents never
edit the same file in one batch.

## Model and effort precedence

An explicit user selection in the app, extension, CLI, or thread settings wins
over this default policy for the process where the selection was made. A
parent-thread choice controls the parent but does not implicitly pin every
child. Unless the user scopes the choice to child work too, an unpinned child
still resolves through `[agents]`; an explicit child spawn model or effort wins
over that default. Never silently replace a manual choice to recreate the
preferred topology.

Ultra may delegate more proactively, but it is not required for this workflow.
Sol Max follows applicable `AGENTS.md` routing instructions while avoiding the
default latency and token overhead of Ultra.

## Runtime identity

Requested settings and `config.toml` prove intent only. When available, prove
the current runtime from the exact rollout:

```text
CODEX_THREAD_ID
  -> exact match with the first session_meta.payload.id
  -> latest turn_context
  -> model + effort
```

Only the first `session_meta` establishes rollout ownership. A child rollout
may contain its parent's history later. If runtime identity cannot be proven,
the footer says `Model : non exposé par le runtime`.
