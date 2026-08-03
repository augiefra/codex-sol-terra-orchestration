# Troubleshooting

## Native subagents are unavailable

1. Parse `~/.codex/config.toml` and check `[features].multi_agent = true` and
   `[agents].enabled = true`.
2. Check that no project-local configuration or managed policy overrides the
   user configuration.
3. Open a fresh task or fully restart Codex if the installed client requires
   it to discover a configuration change.
4. Verify the active client supports multi-agent workflows before changing any
   unrelated setting.

Do not create a custom profile or add a model catalog override as a fallback.

## A child uses a different model or effort

Check, in order:

1. an explicit user selection for the thread;
2. an explicit spawn model or reasoning override;
3. `[agents]` defaults;
4. the actual child `turn_context`.

The official configuration reference says an explicit spawn model or effort
takes precedence over the defaults. Do not stop at the configuration layer.

## The parent is not Sol High

An explicit user choice, project-local configuration, CLI flag, profile, or
managed policy may override this repository's parent default. Verify the
current runtime rather than guessing from the configuration, then preserve the
user's explicit choice unless they ask to change it.

## Final response says `Model : non exposé par le runtime`

Check that `CODEX_THREAD_ID` is available, the process can read its sessions,
the rollout matches `session_meta.payload.id` exactly, and the latest
`turn_context` contains model and effort. Use
`scripts/inspect_runtime_model.py` in the affected process. Never substitute a
requested label for runtime proof.

## TOML reports duplicate keys or tables

The public file is a fragment. Merge each value into the existing top-level,
`[features]`, or `[agents]` table. Restore the targeted backup, do a key-level
merge, parse again, and inspect the diff before restarting.

## Too many agents are spawned

`max_concurrent_threads_per_session = 10` is a ceiling, not a target. Use the
minimum useful number. Parallelize only independent packets with disjoint file
ownership and independent validation.

## A child starts making an architecture decision

Stop the child and return its evidence to Sol. Tighten the packet's
out-of-scope list and escalation condition. Sol owns framing, authorization,
architecture and protected-boundary decisions, review, and final acceptance.

## Sol never proposes a standalone Luna Max task

Confirm the global `AGENTS.md` contains the standalone-task admission gate.
The route should remain rare: all required conditions must hold, and small or
integrated work should stay with Sol or a native Terra subagent. Open a fresh
task after changing global instructions if the active client does not reload
them dynamically.

## The client cannot create a Luna Max task

Do not use `spawn_agent`, a custom agent, an internal feature flag, or a model
catalog override. Ask Sol to return the complete autonomous handoff, create a
normal user-owned task manually with Luna Max if the client offers that choice,
and paste the packet there. Report the capability limitation explicitly.

## Luna was created without approval

Stop or archive the task and tighten the global rule. A separate user-owned
task is created only after explicit approval for that occurrence. A general
preference for low-cost routing is not standing authorization to create every
future task.
