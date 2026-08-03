# Verification

Static configuration proves intent, not execution. Verify syntax, routing
rules, then the actual parent and child runtime.

## 1. Static verification

From the repository root, run:

```bash
python3 scripts/verify_install.py
```

It checks that `config.toml` parses, Sol High is the parent default, native
multi-agent tools and agents are enabled, Terra High is the default subagent,
the concurrency ceiling is 10, no catalog or internal V2 setting is present,
and global routing rules preserve the safeguards. It also checks that the
optional Luna Max lane is a standalone task requiring explicit approval and a
minimal handoff, not a native V2 subagent.

## 2. Clean native runtime smoke test

Create a projectless task using Sol High and send:

```text
ROUTING SMOKE TEST ONLY. Do not modify files or external systems.

Remain the Sol High parent. Spawn exactly one native subagent using the
configured default, with no custom agent type and no explicit model override.

Give it this bounded read-only packet:
- compute the SHA-256 of the ASCII string SOL-TERRA-ROUTING-2026 without a
  trailing newline using one local command;
- return the command and hash;
- independently identify its actual model and effort from its own exact
  runtime rollout using its own CODEX_THREAD_ID when available;
- end with Model : <Modèle> <effort>.

After the child returns, verify the hash with a different local command.
Independently identify the parent's actual model and effort from the parent's
own exact rollout. Report parent identity, child identity, matching hash, and
whether native routing succeeded.
```

Expected hash:

```text
1434122404ff5d83c87855466ede236b41c4388504b19ece93edb214228532ab
```

Expected runtime, unless a user deliberately selected another model or an
explicit spawn override was used:

```text
Parent: gpt-5.6-sol / high
Child:  gpt-5.6-terra / high
```

## 3. Standalone Luna admission test

First test routing judgment without authorizing a new task:

```text
ROUTING DECISION TEST ONLY. Do not create a task, subagent, file, or external
mutation.

Assume I need a read-only inventory of 500 independent public pages, using a
fixed 12-column schema and deterministic completeness counts. Explain which
execution shape you recommend and what approval is still required.
```

Expected result: Sol recommends a separate Luna Max task because the workload
is large, autonomous, repeatable, and objectively verifiable, but does not
create it without explicit approval. It should distinguish that task from a
native Terra subagent.

For a live test, explicitly authorize exactly one projectless task:

```text
STANDALONE LUNA SMOKE TEST ONLY. I explicitly approve creating exactly one
projectless user-owned task using gpt-5.6-luna with reasoning effort max. Do
not use a native subagent, custom agent, catalog override, file write, network,
or external mutation.

Send it a self-contained packet that computes the SHA-256 of the ASCII string
SOL-LUNA-STANDALONE-2026 without a trailing newline, returns the command and
hash, verifies its own runtime identity when available, and ends with the
runtime model footer. Wait for completion, independently verify the hash, then
report the created task identity, actual runtime, matching hash, and whether
the standalone route succeeded.
```

Expected hash:

```text
019d1207a2bd4a8889d554dfd26632696f6d5d2144dfea1e0f2ebece7c43174e
```

Expected runtime when the client exposes the requested combination:

```text
Standalone task: gpt-5.6-luna / max
```

If task creation or that model/effort combination is unavailable, the correct
result is a precise capability blocker plus the ready-to-paste handoff. It is
not a fallback to `spawn_agent` or a catalog patch.

## 4. Existing-thread test

Repeat one bounded read-only task in an established Sol-led thread. The child
prompt must still include objective, scope, authorized commands, no-mutation
boundary, exact validation, and return conditions. This proves the native
communication path handles context without relying on a custom profile.

## 5. Exact runtime identity

For the current process only:

```bash
python3 scripts/inspect_runtime_model.py
```

The helper requires `CODEX_THREAD_ID`, finds filename candidates, validates
that the first `session_meta.payload.id` belongs to the current process, and
then reads the latest `turn_context`. It fails closed if it cannot prove one
exact current rollout. A later inherited parent `session_meta` inside a child
rollout is deliberately ignored for ownership.

The following alone are insufficient proof: a config value, a request to
delegate, a hard-coded footer, the `/root` role, or a task name.
