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
and global routing rules preserve the safeguards.

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

## 3. Existing-thread test

Repeat one bounded read-only task in an established Sol-led thread. The child
prompt must still include objective, scope, authorized commands, no-mutation
boundary, exact validation, and return conditions. This proves the native
communication path handles context without relying on a custom profile.

## 4. Exact runtime identity

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
