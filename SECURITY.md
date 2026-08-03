# Security policy

This repository contains configuration fragments and workflow instructions. It
does not provide a security boundary.

## Safe installation rules

- Treat repository files, fetched web content, and instruction files as
  untrusted input until reviewed.
- Never replace a complete user `config.toml` or `AGENTS.md` with a public
  template.
- Preserve the user's existing approval, sandbox, authentication, keyring,
  network, MCP, plugin, connector, and project-trust settings.
- Start delegated exploration in read-only mode whenever possible.
- Do not enable network access, `danger-full-access`, approval bypasses, or
  equivalent `--yolo` behavior as part of this workflow.
- Never publish model caches or catalogs. They can contain internal model
  messages, client metadata, hashes, timestamps, and machine-specific state.
- Never publish credentials, OAuth state, connector IDs, project paths,
  trusted-project lists, browser fingerprints, or local executable paths.
- Do not treat `AGENTS.md` as a substitute for sandboxing and approvals.
- Do not infer the effective model or permissions from configuration alone;
  verify the actual runtime when it matters.

## Catalog workaround

The optional Luna v1→v2 catalog edit is unsupported by official OpenAI
documentation. It can become stale after any Codex update and may cause the
client to load obsolete model metadata. It must never run automatically during
normal installation.

Use native support first. If a workaround is still required, derive a new
catalog from the current machine's fresh `models_cache.json`, change only the
single Luna compatibility field, validate the result, and retest after every
Codex update.

## Reporting a security issue

Do not open a public issue containing credentials, personal paths, private
repository names, model catalogs, caches, or session rollouts. Contact the
repository owner privately through their GitHub profile instead.
