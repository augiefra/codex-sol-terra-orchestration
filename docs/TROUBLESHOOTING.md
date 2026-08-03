# Troubleshooting

## `luna_worker` is missing from the delegation tool

1. Confirm the file is named exactly `luna_worker.toml` in the active global or
   trusted project agent directory.
2. Parse the TOML and confirm `name = "luna_worker"`.
3. Open a new task or fully restart Codex.
4. Test native multi-agent support before using a custom catalog.
5. If the model is still filtered, inspect the active model metadata. Do not
   assume the catalog workaround is required without evidence.

## Custom agent and full history are rejected

Use:

```text
agent_type = "luna_worker"
fork_turns = "none"
```

Send a self-contained packet. Do not ask the custom agent to inherit the full
parent history.

## Final response says `Model : non exposed by the runtime`

The model may exist in the rollout even when it is not directly injected into
the conversation context.

Check that:

- `CODEX_THREAD_ID` exists in the task process;
- the task can read its local Codex sessions directory;
- it validates `session_meta.payload.id` exactly;
- it reads the latest `turn_context` from that exact rollout;
- it does not reuse the parent's thread ID for a child.

Use `scripts/inspect_runtime_model.py` inside the affected process. Do not solve
the problem by hard-coding the expected model as if it were runtime proof.

## The parent runs Luna instead of Sol

This repository intentionally sets Luna Max as the global default. Architecture
threads must be explicitly created or switched to Sol High. Verify the current
turn's runtime rather than reading only the global default.

Project-local `.codex/config.toml`, CLI flags, profiles, or task settings may
also override the user configuration.

## The worker runs the wrong model or effort

Check the following in order:

1. explicit spawn-time overrides;
2. the custom `luna_worker.toml` model and effort;
3. `[agents]` defaults;
4. parent inheritance behavior;
5. the actual child `turn_context`.

Do not stop at the configuration layer.

## TOML parser reports duplicate keys or tables

The public config is a fragment. Merge its keys into existing tables. Do not
append a second `[features]`, `[features.multi_agent_v2]`, or `[agents]` table.

Restore the backup, perform a key-level merge, parse again, and inspect the
diff before restarting.

## Luna works until Codex is updated

If a custom `model_catalog_json` is active, it may now be stale because the
setting replaces the loaded catalog rather than overlaying only one entry.

1. Remove or disable the override temporarily.
2. Restart Codex.
3. Test native Luna support first.
4. If native support works, permanently remove the override.
5. If the same verified mismatch remains, rebuild from the new local cache and
   change only the documented field.

Never reuse an old public or machine-generated catalog snapshot.

## Too many agents are spawned

`max_concurrent_threads_per_session = 10` is only a ceiling. The routing policy
requires the minimum useful number, normally one worker. Parallelize only
independent packets with disjoint file ownership and independent validation.

## The worker starts making architecture decisions

Stop the worker and return the evidence to the parent. Tighten the packet's
out-of-scope list and escalation conditions. Sol owns architecture-thread
decisions and final acceptance.
