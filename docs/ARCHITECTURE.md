# Architecture and routing policy

## Objective

Keep authority and cross-cutting judgment in a Sol High parent thread, while
using native Terra High subagents for work that is independently executable
and objectively checkable. This uses Codex's built-in multi-agent workflow and
the documented `[agents]` defaults; there is no profile to install or catalog
to patch.

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

## Runtime identity

The requested model and `config.toml` prove intent only. When available, prove
the current runtime from the exact rollout:

```text
CODEX_THREAD_ID
  -> exact session_meta.payload.id match
  -> latest turn_context
  -> model + effort
```

The response footer is always the final line and reports the proven runtime;
otherwise it says `Model : non exposé par le runtime`.
