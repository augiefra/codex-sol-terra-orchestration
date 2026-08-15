# Troubleshooting

## Native subagents are unavailable

1. Parse `~/.codex/config.toml` and check `[features].multi_agent = true` and
   `[agents].enabled = true`.
2. Check that no project-local configuration or managed policy overrides the
   user configuration.
3. Open a fresh task or fully restart Codex if the active client does not
   reload global settings dynamically.
4. Verify the active client exposes native multi-agent workflows and Luna in
   the spawn model surface.

Do not create a custom profile, enable an undocumented internal feature, patch
a model cache, or add a model-catalog override as a fallback. Report the exact
capability blocker.

## A child uses a different model or effort

Check, in order:

1. a user selection explicitly applied to that process;
2. an explicit child-spawn model or effort;
3. a custom role file, if the user intentionally selected one;
4. `[agents].default_subagent_model` and
   `[agents].default_subagent_reasoning_effort`;
5. the parent's model and effort fallback;
6. the actual child `turn_context`.

The expected unpinned child for this workflow is Luna Max. An explicitly
selected collaborative branch is Terra High. Configuration is intent; runtime
metadata is the proof.

A manual parent-thread model selection controls the parent. It does not by
itself pin an unpinned child, which still resolves through `[agents]`, unless
the user explicitly applied the manual choice to child work as well. An
explicit child spawn selection always wins for that child.

## The parent is not Sol Max

An explicit user choice, project-local configuration, CLI flag, profile, or
managed policy may override the global parent default. Verify the current
runtime, then preserve the user's explicit choice unless they ask to change
it.

## Terra High was selected for a terminal assignment

Terra should have a concrete reason: proactive inter-agent communication,
steering, recursive delegation, integration of dependent intermediate
results, or materially deeper bounded reasoning. If none applies, return the
assignment to a Luna leaf or let the parent complete it directly. Do not keep
Terra merely because the task is large.

## A Luna leaf tries to coordinate or delegate

Luna is a terminal worker in this topology. Tighten the packet with:

```text
Complete this assignment directly. Do not spawn, steer, or coordinate other
agents. Return evidence and validation to the parent.
```

If the active runtime exposes an unexpected capability surface, stop and
report the observed tool/model metadata rather than modifying the catalog.

## Final response says `Model : non exposé par le runtime`

Check that `CODEX_THREAD_ID` is available, the process can read its sessions,
the owning rollout's **first** `session_meta.payload.id` matches exactly, and
the latest `turn_context` contains model and effort. Use
`scripts/inspect_runtime_model.py` in the affected process. Never substitute a
requested label for runtime proof.

Use `--explain` to see the relative rollout, exact owner, context count, and
latest runtime, or `--json` to capture the same evidence mechanically. The
default output remains the exact footer only.

## TOML reports duplicate keys or tables

The public file is a fragment. Merge each value into the existing top-level,
`[features]`, or `[agents]` table. Restore the targeted backup, do a key-level
merge, parse again, and inspect the diff before restarting.

## The verifier reports missing, reversed, or duplicate routing markers

The installed policy must contain exactly one ordered v3 start/end pair, as
shown in the routing template. If the pair is missing from an otherwise
equivalent older install, enclose only that workflow section. If several copies
exist, compare them, preserve unrelated custom instructions, and consolidate
only the duplicated managed block. Re-run the verifier before restarting.

## Too many agents are spawned

`max_concurrent_threads_per_session = 8` is a ceiling, not a target. Use the
minimum useful number. Parallelize only independent packets with disjoint file
ownership and independent validation. Close completed or stale agent threads
through the parent when the client exposes that control.

## A child starts making a protected decision

Stop the child and return its evidence to the parent. Tighten the packet's
out-of-scope list and escalation condition. The parent owns framing,
authorization, architecture, protected-boundary decisions, review, and final
acceptance.

## A separate Luna task was created without approval

This rule concerns a new **user-owned task**, not a native Luna leaf. Stop or
archive the separate task and tighten the global rule. Creating another user
task requires explicit approval for that occurrence; a preference for Luna
subagents is not standing authorization for new user threads.

## The client cannot create an optional separate Luna task

Return the complete autonomous handoff and report the limitation. Do not patch
a catalog or silently replace the requested execution shape. The parent may
then ask whether to use one or several native Luna leaves instead.
