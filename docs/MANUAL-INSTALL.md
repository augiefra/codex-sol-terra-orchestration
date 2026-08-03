# Manual installation

Use this path only if you understand TOML merging and can inspect diffs. The
Codex-assisted flow is safer for configurations that already contain several
tables, MCP servers, plugins, projects, or managed settings.

## 1. Back up the target files

Create recoverable timestamped copies of only the files that already exist and
will be changed:

```text
~/.codex/config.toml
~/.codex/AGENTS.md
~/.codex/agents/luna_worker.toml
```

Do not include credentials, caches, catalogs, or session rollouts in a public
bug report or commit.

## 2. Merge the configuration fragment

Open [`../templates/config.fragment.toml`](../templates/config.fragment.toml).
Merge its top-level `model` values and the individual keys from `[features]`,
`[features.multi_agent_v2]`, and `[agents]` into existing tables.

Do not paste the fragment at the end if those tables already exist. Duplicate
TOML keys or tables are invalid.

## 3. Install the custom agent

Copy [`../templates/luna_worker.toml`](../templates/luna_worker.toml) to:

```text
~/.codex/agents/luna_worker.toml
```

Review the developer instructions before installing them globally.

## 4. Merge the global routing rules

Merge [`../templates/AGENTS-routing.md`](../templates/AGENTS-routing.md) into
`~/.codex/AGENTS.md`. Preserve every unrelated user instruction.

## 5. Validate statically

Run:

```bash
python3 scripts/verify_install.py
```

The verifier is read-only. Resolve every error before restarting Codex.

## 6. Restart and smoke-test

Fully restart Codex Desktop or open a fresh task, then follow
[`VERIFICATION.md`](VERIFICATION.md).

## 7. Use Sol High intentionally

The global default is Luna Max. For an architecture or high-impact thread,
select Sol High explicitly in the UI, CLI, thread settings, or thread-creation
call. That explicit selection must remain the primary model for that thread.
