# Five-minute quickstart

This is the shortest safe path from a neutral Codex installation to the
workflow documented in this repository.

## Result

```text
Sol Ultra parent
├── unpinned native child -> Luna Max leaf
└── explicitly selected collaborative branch -> Terra High
```

You do not need a custom agent, model-catalog override, cache patch, or
`multi_agent_v2` setting.

## Prerequisites

- a current Codex client whose model picker exposes Sol, Terra, and Luna;
- Python 3.11 or newer for the read-only verifier;
- `openssl` or `shasum -a 256` for the smoke-test hash;
- permission to edit the active Codex home, normally `~/.codex` but possibly
  the path in `CODEX_HOME`;
- a fresh task after configuration changes. If a fresh task still sees stale
  settings, fully quit and restart the Codex client, then create another task.

Managed workspace policy, project-local configuration, or a manual model
selection can override user defaults. The installer must report those layers
rather than trying to bypass them.

## 1. Give the repository to Codex

Open a fresh Codex task and paste:

```text
Install the workflow from:
https://github.com/augiefra/codex-sol-terra-orchestration

Read README.md, SECURITY.md, docs/QUICKSTART.md,
docs/INSTALL-WITH-CODEX.md,
templates/config.fragment.toml, and templates/AGENTS-routing.md completely.

Resolve my active Codex home first: use CODEX_HOME when it is set, otherwise
use ~/.codex. Read-only audit the active config.toml, global AGENTS.md, managed
policy, and project-local overrides before proposing any mutation. If a target
file is absent, say that explicitly; do not treat an absent file as an empty
configuration that already passed validation.

Merge only the documented keys and routing section. Never replace either
complete file. Preserve unrelated approvals, sandbox, authentication, network,
MCP, plugin, connector, project, notification, and manual model settings.

Before writing, report the source repository commit inspected, show the exact
proposed changes, identify any effective override, and ask for confirmation.
After confirmation, back up only existing files that will change, apply an
idempotent merge, show the diff, parse the final TOML, run
scripts/verify_install.py against the resolved Codex home, and stop before any
unrelated cleanup or external mutation. Never execute a remote script that you
have not inspected.
```

For the complete guarded prompt, use
[INSTALL-WITH-CODEX.md](INSTALL-WITH-CODEX.md).

## 2. Expected configuration

Codex should merge these values into existing tables:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "ultra"

[features]
multi_agent = true

[agents]
enabled = true
max_concurrent_threads_per_session = 8
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "max"
```

`multi_agent` and `agents.enabled` are explicit here for auditability even when
the current client already enables them by default.

Do not paste a second `[features]` or `[agents]` table into a file that already
has one. Merge keys into the existing table instead.

The installed routing block is enclosed by a unique ordered start/end marker
pair containing `codex-sol-luna-terra-orchestration:v3`. Update that managed
block in place on a later install; do not append a second copy.

## 3. Expected routing policy

Codex should merge [AGENTS-routing.md](../templates/AGENTS-routing.md) into the
existing global instructions. The important rules are:

- keep the main owner on Sol Ultra unless the user manually selected another
  parent model;
- route independent, bounded, terminal work to Luna Max;
- select Terra High explicitly only when that branch must communicate with or
  recursively delegate to other agents;
- keep architecture, authorization, protected decisions, evidence review, and
  the final answer with the parent;
- prefer self-contained Luna packets with no inherited turns;
- stop children on protected boundaries or after two evidence-based failures;
- verify the actual model from runtime metadata.

## 4. Restart and verify

After the files are merged, run the verifier from the checked-out repository:

```bash
python3 scripts/verify_install.py --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

Then open a new projectless task and run the first smoke test in
[VERIFICATION.md](VERIFICATION.md). If that fresh task still uses pre-install
settings, fully quit and restart Codex, create a second fresh task, and repeat
the test. Editing a file does not retroactively change a process already
running.

Expected result:

```text
Parent: gpt-5.6-sol / ultra
Child:  gpt-5.6-luna / max
```

If the child remains Terra after editing the file, do not patch the catalog.
Check explicit spawn overrides, custom roles, project and managed policy, and
the actual child runtime. Then follow
[TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 5. Use it naturally

You should not need to remember an agent profile name. Ask for the outcome:

```text
Inspect this repository for stale API calls and give me a verified report.
```

The parent decides whether the work is small enough to keep, suitable for one
Luna leaf, worth parallel Luna leaves, or genuinely collaborative enough for a
Terra branch.

## Before and after

| Old workaround | Current native workflow |
|---|---|
| Copy and patch a model catalog | Use documented `[agents]` defaults |
| Force Luna into a V2 peer slot | Use Luna as a terminal leaf |
| Remember custom `luna_worker` profiles | Describe the objective; let routing rules choose |
| Treat every large task as Terra | Route by coordination and risk, not size |
| Trust the requested model label | Verify the actual rollout |

The dated explanation is in
[EVOLUTION-AND-EVIDENCE.md](EVOLUTION-AND-EVIDENCE.md).
