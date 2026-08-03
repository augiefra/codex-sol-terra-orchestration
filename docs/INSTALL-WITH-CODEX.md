# Guarded installation with Codex

This document is written for the most common sharing flow: a person gives this
repository URL to Codex and asks Codex to install it.

## Installer contract

Codex must treat the target machine's existing configuration as user-owned
state. The public repository provides an overlay, not a replacement.

Before changing anything, Codex should identify:

- the active Codex home directory;
- the existing user `config.toml` and global `AGENTS.md`;
- existing custom-agent files;
- the installed Codex version and current model support;
- whether a project-local configuration will override the user configuration;
- whether the files contain unrelated, private, or machine-specific settings.

It must not print credentials, OAuth state, environment values, full model
catalogs, or private project paths in its response.

## Copy/paste installation prompt

```text
Install the workflow from:
https://github.com/augiefra/codex-sol-luna-orchestration

Read the repository's README.md, SECURITY.md,
docs/INSTALL-WITH-CODEX.md, templates/config.fragment.toml,
templates/luna_worker.toml, and templates/AGENTS-routing.md completely before
taking action.

Objective:
- global routine-work default: gpt-5.6-luna with effort max;
- architecture/high-impact threads: explicitly selected gpt-5.6-sol with
  effort high;
- one global custom subagent: luna_worker on gpt-5.6-luna with effort max;
- custom-agent spawns use agent_type="luna_worker" and fork_turns="none";
- final responses report the actual runtime model and effort from the exact
  rollout whenever CODEX_THREAD_ID is available.

Safety boundaries:
1. Audit first and preserve all existing unrelated settings.
2. Never replace my complete config.toml or AGENTS.md.
3. Never copy another user's paths, catalogs, caches, credentials, project
   trust entries, connector IDs, fingerprints, plugins, MCP servers, sandbox,
   approval, authentication, keyring, or network settings.
4. Merge only the required keys into existing TOML tables; do not create
   duplicate tables or duplicate keys.
5. Back up only the files you will change, with a timestamped recoverable copy.
6. Show the proposed diff before any unsupported workaround.
7. Try current native Luna multi-agent support first.
8. If Luna is filtered out, show runtime evidence and ask my approval before
   using docs/MODEL-CATALOG-WORKAROUND.md. Never apply it silently.
9. Do not commit, push, deploy, publish, enable full access, or mutate an
   external system.

Implementation:
- merge templates/config.fragment.toml into my user config;
- install templates/luna_worker.toml at the exact global custom-agent path
  using the filename luna_worker.toml;
- merge templates/AGENTS-routing.md into my existing global AGENTS.md without
  deleting my collaboration style or repository-specific rules;
- keep the number of custom agents at one;
- preserve any explicit model selection I make in a thread.

Validation:
- parse all changed TOML files;
- run scripts/verify_install.py against my Codex home;
- restart Codex fully if the installed build requires it;
- create a clean projectless Sol High smoke-test thread;
- delegate one bounded read-only task to luna_worker with fork_turns="none";
- make parent and child independently validate their own exact rollout using
  CODEX_THREAD_ID == session_meta.payload.id;
- require parent gpt-5.6-sol/high and child gpt-5.6-luna/max;
- show the final diff, test evidence, rollback paths, and any remaining caveat.
```

## Required merge behavior

### `config.toml`

TOML tables may appear only once. If `[features]`,
`[features.multi_agent_v2]`, or `[agents]` already exists, merge individual
keys into that table. Do not append a second table with the same name.

Keep unrelated keys exactly as they were. In particular, do not import this
repository's opinions into:

- `approval_policy`;
- `sandbox_mode`;
- network access;
- credential stores;
- MCP servers;
- plugins and apps;
- project trust;
- notification commands;
- service tier or account settings.

### Global `AGENTS.md`

Merge the routing sections. Do not delete the user's collaboration style,
language, repository-reading rules, safety constraints, or durable project
conventions.

If an existing rule conflicts with the new block, report the conflict and ask
before choosing a materially different policy.

### Custom agent

Use the exact filename:

```text
~/.codex/agents/luna_worker.toml
```

An underscore and a hyphen are not interchangeable when a tool expects the
custom agent name.

## Reload behavior

After installation, open a new Codex task or fully restart Codex Desktop before
testing agent discovery. Existing tasks may keep instruction or catalog state
loaded earlier.

## Completion criteria

Installation is complete only when:

- all TOML parses successfully;
- the custom agent is discoverable as `luna_worker`;
- a clean Sol High parent can spawn it with `fork_turns="none"`;
- the child actually runs as Luna Max;
- parent and child runtime identities are proven independently;
- no unrelated user configuration was overwritten;
- rollback copies are identified;
- any catalog workaround is clearly reported as active or absent.
