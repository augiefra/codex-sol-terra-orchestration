# Manual installation

Use this path only if you can merge TOML and inspect a diff. The Codex-assisted
flow is safer when the configuration already includes several tables, MCP
servers, plugins, projects, or managed settings.

Prerequisites: a current client exposing Sol, Terra, and Luna; Python 3.11+;
and `openssl` or `shasum -a 256` for smoke testing. Resolve the active Codex
home from `CODEX_HOME` when set, otherwise use `~/.codex`. Check managed and
project-local overrides before assuming the user config is effective.

## 1. Back up only the target files

Create timestamped, recoverable copies of existing files only when you will
change them:

```text
~/.codex/config.toml
~/.codex/AGENTS.md
```

Never include credentials, caches, catalogs, or session rollouts in a public
report or commit.

## 2. Merge the configuration fragment

Open [templates/config.fragment.toml](../templates/config.fragment.toml) and
merge its top-level values plus the values in `[features]` and `[agents]` into
matching existing tables. Do not paste the fragment at the end when the table
is already present: duplicate TOML keys or tables are invalid.

The fragment sets Sol Max as the parent default, enables native multi-agent
tools, caps child concurrency at eight, and sets Luna Max as the native leaf
default. It adds no custom agent, catalog override, compatibility patch, or
internal feature flag.

Terra High is selected explicitly by the parent only for a collaborative
branch that needs proactive communication, recursive delegation, or materially
deeper intermediate reasoning. It is not the ordinary child default.

## 3. Merge routing rules

Merge [templates/AGENTS-routing.md](../templates/AGENTS-routing.md) into
`~/.codex/AGENTS.md`, preserving unrelated user instructions.

The block is enclosed by the v3 start/end HTML comments in the template. Keep
exactly one ordered marker pair. On an upgrade, replace only the content and
markers of the existing managed block rather than appending another.

The merged policy does not require additional user approval for a native Luna
leaf operating within the current authorized workflow. It still requires Sol
to explain the benefit and wait for explicit approval before creating a
separate user-owned Luna Max task. Read
[STANDALONE-LUNA-TASKS.md](STANDALONE-LUNA-TASKS.md) before changing that
boundary.

## 4. Validate and smoke-test

From this repository root:

```bash
python3 scripts/verify_install.py
```

Resolve all errors, open a fresh task, and restart Codex only if that fresh
task still sees stale settings. Then follow
[VERIFICATION.md](VERIFICATION.md). An explicit model selection by the user
still takes precedence for the process where it was made. A parent-thread
selection does not implicitly pin unpinned children unless the user scopes the
choice to child work too.
