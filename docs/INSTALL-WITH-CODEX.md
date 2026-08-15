# Guarded installation with Codex

This is the assisted path for a person who gives this repository to Codex.
The repository supplies a small overlay; the existing machine configuration is
user-owned state and must not be replaced.

## Copy/paste installation prompt

```text
Install the workflow from:
https://github.com/augiefra/codex-sol-terra-orchestration

Read README.md, SECURITY.md, this document,
docs/STANDALONE-LUNA-TASKS.md,
templates/config.fragment.toml, and templates/AGENTS-routing.md completely
before making changes.

Audit my active Codex home, existing config.toml, and global AGENTS.md first.
Merge only the documented keys and rules. Do not replace either complete file,
create a custom agent, add a model catalog override, or use internal feature
flags.

Target topology:
- parent default: gpt-5.6-sol with max reasoning;
- native leaf default: gpt-5.6-luna with max reasoning;
- explicit collaborative branch lead: gpt-5.6-terra with high reasoning;
- features.multi_agent and agents.enabled enabled;
- max_concurrent_threads_per_session set to 8.

Merge the native routing policy from AGENTS-routing.md: Luna is a terminal
leaf, Sol may coordinate several Luna leaves directly, and Terra is chosen
only when a branch needs proactive inter-agent coordination, recursive
delegation, or materially deeper intermediate reasoning.

Also merge the optional separate-task policy. Sol may propose a new
user-owned gpt-5.6-luna/max task for an exceptionally large autonomous batch,
but only after explicit user approval. This separate task is distinct from a
native Luna leaf. Do not create a separate Luna task during installation.

Preserve every unrelated setting, including approval, sandbox, authentication,
network, MCP, plugin, connector, project-trust, service-tier, and any explicit
model selection I make in the process where I make it. A parent-thread choice
controls the parent; it does not implicitly pin unpinned children unless I
explicitly scope it to child work too. Back up only a file that you will
change, using a timestamped recoverable copy. Show the proposed diff before
writing.

Validate changed TOML, run scripts/verify_install.py, and run the read-only
smoke tests in docs/VERIFICATION.md. Prove every process's runtime identity
from their own exact rollout when available; otherwise report that it is not
exposed. Do not commit, push, deploy, publish, or mutate an external system.
```

## Required merge behavior

### `config.toml`

Merge individual values from
[templates/config.fragment.toml](../templates/config.fragment.toml) into the
existing top level, `[features]`, and `[agents]` tables. A TOML table may occur
only once, so never append a duplicate table or duplicate key. Keep all
unrelated keys unchanged.

In particular, this workflow must not import opinions about `approval_policy`,
sandbox mode, network access, credentials, MCP servers, plugins, connectors,
project trust, notifications, or account and service-tier settings.

### Global `AGENTS.md`

Merge [templates/AGENTS-routing.md](../templates/AGENTS-routing.md) into the
existing global instructions. Keep the user's collaboration style, repository
rules, safety constraints, and existing footer rules. Do not add a custom
agent profile: native Luna leaves use the `[agents]` defaults and a
collaborative Terra branch is selected explicitly. The optional separate-task
lane is represented only by routing instructions.

## Validation and rollback

1. Parse every changed TOML file.
2. Run `python3 scripts/verify_install.py` against the target Codex home.
3. Fully restart Codex only if the active client does not discover the merged
   configuration in a fresh task.
4. Run the read-only native smoke tests in [VERIFICATION.md](VERIFICATION.md):
   Sol-to-Luna, parallel Luna leaves, and Sol-to-Terra-to-Luna.
5. Retain the timestamped copies until the smoke test is accepted.

To roll back, restore only the specific backups created before this install;
do not overwrite unrelated state created later.
