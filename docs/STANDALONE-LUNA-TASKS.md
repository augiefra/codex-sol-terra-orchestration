# Standalone Luna Max tasks

This is an optional execution shape for workloads that are exceptionally
expensive in context but simple in coordination. It supplements native
Sol–Luna–Terra orchestration; it does not replace native Luna leaf agents.

```text
Sol Ultra parent
├── native Luna Max leaf            bounded terminal work
├── Terra High branch lead          collaborative bounded work
└── separate Luna Max user task     exceptional batch, after approval
```

## What it is

A standalone Luna Max task is a **separate user-owned Codex task** whose effective
model is `gpt-5.6-luna` and whose reasoning effort is `max`. The Sol parent
commissions the work, sends a self-contained packet, tracks the task when the
client supports task coordination, reviews the deliverable, and remains the
owner of decisions and final acceptance.

This document is not describing an ordinary native Luna leaf. The separate
task is created through the client's user-task workflow, not `spawn_agent`.
Do not use a custom agent profile, internal feature flag, compatibility patch,
or model catalog override for either execution shape. Max gives Luna more
reasoning budget; it does not turn a terminal worker into a collaborative
branch coordinator.

## Admission gate

Use this lane only when every required condition is true:

| Required condition | Question |
|---|---|
| Material volume | Is the batch large enough that a second task saves meaningful parent context or cost? |
| Autonomous packet | Can the work proceed from one stable, self-contained handoff? |
| Stable scope | Are the sources, boundaries, and expected output already clear? |
| Objective validation | Can Sol verify completeness or correctness from evidence, tests, counts, hashes, or a defined schema? |
| Low coordination | Can the task finish without proactive Multi-Agent V2 communication or frequent steering? |
| Safe boundary | Does it avoid unresolved architecture, security, authorization, data-integrity, destructive, production, and public-contract decisions? |

If the work is bounded and should remain integrated with the current parent,
use a native Luna leaf. Use Terra only when the branch itself needs
coordination. Lower price alone is not an admission criterion for creating a
new user task.

Good candidates include exceptionally large read-only repository inventories,
systematic web or Browser inspections, document extraction, SEO matrices, log
classification, repeatable comparisons, and deterministic batch analysis
whose volume materially justifies another user task instead of one or several
native Luna leaves.

Poor candidates include authentication changes, migrations, payment logic,
production configuration, public API contracts, architecture decisions, and
code changes that require frequent review or shared file ownership.

## Explicit approval boundary

Sol must explain the proposed split and wait for an explicit user instruction
to create the separate task. A global preference for this workflow does not
authorize every future task creation.

The approval request should be concise:

```text
This phase is large, autonomous, and objectively verifiable. I recommend a
separate Luna Max task to preserve the Sol thread's context and reduce cost.
It will be read-only and return <deliverable>. May I create it now?
```

After approval, use the current client's user-owned task creation capability
with model `gpt-5.6-luna` and effort `max`. Select the saved project for
repository work and a projectless task for general analysis. If the capability
is absent or rejects that combination, return the complete packet for manual
creation and report the limitation. Do not silently substitute a different
execution shape or patch a model catalog; let the parent decide whether to use
native Luna leaves after reporting the blocker.

## Autonomous handoff packet

Do not copy or fork the full Sol history by default. Send only what Luna needs:

```text
ROLE
You are a separate Luna Max execution task commissioned by a Sol parent.
You are not the architecture owner and you must not expand this mission.

OBJECTIVE
<one verifiable outcome>

SOURCE OF TRUTH
<exact repositories, files, URLs, documents, or systems>

IN SCOPE
<bounded work>

OUT OF SCOPE
<adjacent work and protected decisions>

AUTHORIZED ACTIONS
<read-only by default; list every allowed mutation if any>

INVARIANTS
<rules that must remain true>

FILE OWNERSHIP
<exact writable files, each owned only by this task, or "none">

DELIVERABLE
<report, table, artifact, patch, or structured output>

VALIDATION
<tests, counts, hashes, evidence, schema, or acceptance criteria>

STOP AND RETURN TO SOL WHEN
- material ambiguity or an unresolved decision appears;
- the requested scope would expand;
- security, authentication, authorization, data integrity, destructive
  migration, production, or a public/cross-system contract is involved;
- two distinct evidence-based attempts fail;
- new user authority is required.

RETURN FORMAT
- result;
- evidence and validation;
- changes, if explicitly authorized;
- limitations and remaining risks;
- exact next action for Sol;
- final runtime line: Model : <Modèle> <effort>.
```

## Parent review

Creating the task does not transfer ownership. Sol must:

1. track the task without flooding the parent context with intermediate logs;
2. respond to attention requests without broadening user authority;
3. inspect the final evidence and validation;
4. reject or correct unsupported conclusions;
5. integrate only accepted output;
6. produce the user-facing conclusion.

The Luna footer is a runtime claim, not proof by itself. Verify model and effort
from the task's exact runtime metadata or canonical rollout when available. If
they cannot be established, use `Model : non exposé par le runtime`.

## Why this remains optional

A separate task has coordination cost: it needs a handoff, monitoring, result
retrieval, and parent review. It is powerful only when the batch is large
enough to outperform native Luna leaves after that overhead. It is wasteful
for a small fix or a task that needs continuous parent interaction.
