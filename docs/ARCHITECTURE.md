# Architecture and routing policy

## Objective

Keep authority and cross-cutting judgment in a Sol High parent thread, while
using native Terra High subagents for work that is independently executable
and objectively checkable. This uses Codex's built-in multi-agent workflow and
the documented `[agents]` defaults; there is no profile to install or catalog
to patch.

For large autonomous batches, the parent may propose a third execution shape:
a separate user-owned Luna Max task. It is created only after explicit user
approval, receives a self-contained handoff, and returns a verifiable
deliverable. It is not a native subagent and does not change the Sol–Terra
configuration.

## Responsibilities

### Sol High — parent orchestrator

Sol frames the objective and invariants, grants in-scope authority only,
decides architecture/product/security/production questions, reviews evidence,
integrates results, and provides the final answer.

### Terra High — native subagent

Terra explores or executes a self-contained task with a clear validation:
read-heavy repository or document scans, supporting research, log and test
analysis, bounded console work, deterministic transformations, or a small
implementation already decided by Sol. It returns evidence and does not alter
the global objective or decide a protected boundary.

### Luna Max — optional standalone batch task

Luna handles a high-volume, repeatable, context-heavy workload that is large
enough to justify a separate user-owned task and can run without proactive
inter-agent communication. Sol explains the split, obtains explicit approval,
creates the task when the client exposes that capability, tracks it, reviews
its deliverable, and keeps every decision and authorization boundary.

The standalone task is not created through native subagent spawning. It does
not inherit the full parent history by default and cannot modify the global
objective, expand authority, or cross a protected boundary.

## Delegation gate

| Dimension | Native Terra subagent | Keep with Sol |
|---|---|---|
| Ambiguity | Clear interpretation | Material contradiction or choice |
| Blast radius | Local and reversible | Cross-system, public, destructive, difficult to reverse |
| Validation | Deterministic and available | Subjective, missing, or expensive |
| Security/data | No protected boundary | Auth, permissions, secrets, payments, integrity |
| Failure state | Fewer than two failed evidence-based attempts | Two distinct attempts already failed |
| Ownership | Explicit sole owner per file | Shared or conflicting write ownership |

Task size never decides routing by itself: a large mechanical change may fit a
bounded Terra task, while a small authorization change belongs to Sol.

## Execution-shape gate

| Shape | Use when | Do not use when |
|---|---|---|
| Sol directly | The task is small, ambiguous, high-risk, decision-heavy, or tightly coupled | The only reason is to avoid a useful bounded delegation |
| Native Terra High subagent | Work is independently bounded but should remain integrated with the parent workflow | It requires an unresolved architecture or protected-boundary decision |
| Standalone Luna Max task | Work is large, autonomous, high-volume, objectively verifiable, and needs no proactive V2 coordination | The user has not explicitly approved creating a task, or coordination overhead exceeds the expected saving |

## Child packet and stop rules

Every delegation states the objective, relevant context, scope, prohibited
actions, authorized actions, invariants, exact owned writable files, expected
result, and validation. Start read-only unless Sol explicitly authorizes a
mutation. Parallel work requires genuinely independent scopes, validation, and
file ownership.

The child stops immediately and returns the exact issue if ambiguity becomes
material, an unmade decision is needed, the scope would expand, or the task
touches security, authentication, authorization, data integrity, destructive
migration, or a public/cross-system contract. After two distinct
evidence-based failures, it stops further attempts and reports the evidence,
remaining plausible hypotheses, and blocker to Sol.

Parent instructions never broaden user authority. External changes,
publication, production mutation, commits, pushes, and deployments still need
explicit user authorization and a bounded instruction from the parent.

## Standalone-task lifecycle

1. Sol classifies the workload and explains why a separate Luna Max task is
   preferable to direct work or a Terra subagent.
2. Sol waits for explicit approval to create the user-owned task.
3. Sol sends a minimal autonomous packet rather than the full parent history.
4. Luna executes within the packet and returns evidence, validation,
   limitations, and the actual runtime footer.
5. Sol verifies the result, resolves ambiguity, and integrates only accepted
   output.

If the current client cannot create a task with an explicit model and effort,
Sol returns the complete handoff for manual creation. It must not fall back to
catalog modification or claim that Luna ran as a native subagent.

## Runtime identity

The requested model and `config.toml` prove intent only. When available, prove
the current runtime from the exact rollout:

```text
CODEX_THREAD_ID
  -> exact match with the first session_meta.payload.id
  -> latest turn_context
  -> model + effort
```

Only the first `session_meta` establishes rollout ownership. A child rollout
can contain the parent's `session_meta` later in inherited history.

The response footer is always the final line and reports the proven runtime;
otherwise it says `Model : non exposé par le runtime`.
