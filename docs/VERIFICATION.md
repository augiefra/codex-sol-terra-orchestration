# Verification

Static configuration is not proof of runtime execution. Verification has three
levels: syntax, agent discovery, and actual parent/child rollouts.

## 1. Static verification

From the repository root:

```bash
python3 scripts/verify_install.py
```

Expected checks:

- user `config.toml` parses;
- top-level default is Luna with effort Max;
- multi-agent and agent tables are enabled;
- the default subagent is Luna Max;
- `luna_worker.toml` exists under the exact filename and parses;
- the worker pins Luna Max;
- the global `AGENTS.md` contains the core routing, `fork_turns="none"`,
  two-failure, one-owner, and runtime-identification rules;
- any configured model catalog exists and reports its Luna compatibility value.

## 2. Clean runtime smoke test

Create a new projectless task explicitly in Sol High and use this prompt:

```text
ROUTING SMOKE TEST ONLY. Do not modify files or external systems.

Remain the Sol High parent. Spawn exactly one custom agent with
agent_type="luna_worker" and fork_turns="none".

Give the child this bounded read-only packet:
- compute the SHA-256 of the ASCII string SOL-LUNA-ROUTING-2026 without a
  trailing newline using one local command;
- return the command and hash;
- independently identify its actual model and effort from its own exact
  runtime rollout using its own CODEX_THREAD_ID;
- end with Model : <Model> <effort>.

After the child returns, verify the hash with a different local command.
Independently identify the parent's actual model and effort from the parent's
own exact rollout. Report parent identity, child identity, matching hash, and
whether routing succeeded.
```

Expected hash:

```text
af690a40d33623049c759135ca4dcbc0fc48c0c4a2d0f2e08ef90ac7e83567aa
```

Expected runtime:

```text
Parent: gpt-5.6-sol / high
Child:  gpt-5.6-luna / max
```

## 3. Existing-thread smoke test

Repeat a bounded read-only task in an existing architecture thread with a long
history. The spawn must explicitly use `fork_turns="none"`.

Example packet:

```text
Objective: report the current repository path and minimal Git status.
Authorized commands: pwd, git rev-parse --is-inside-work-tree,
git status --short --branch.
Mutations: none.
Validation: the parent repeats all three commands independently.
Return conditions: any error or ambiguity.
```

This test catches the common failure where a custom agent is accidentally
combined with a full-history fork.

## 4. Exact runtime identity

For the current process only:

```bash
python3 scripts/inspect_runtime_model.py
```

The helper requires `CODEX_THREAD_ID`, finds candidates by filename, validates
the exact `session_meta.payload.id`, and reads the latest `turn_context`.

It must fail closed if:

- the environment variable is absent;
- no exact session match exists;
- more than one exact session match exists;
- the rollout has no `turn_context`;
- the model or effort is missing.

## Evidence standard

The following are not sufficient proof by themselves:

- `model = ...` in `config.toml`;
- model settings in a custom-agent TOML;
- an agent role named `luna_worker`;
- a prompt asking for Sol or Luna;
- a hard-coded footer;
- the `/root` role name.

The validated current process rollout is the source of truth for this workflow.
