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
- Never publish model caches. They can contain internal model messages, client
  metadata, hashes, timestamps, and machine-specific state.
- Never publish credentials, OAuth state, connector IDs, project paths,
  trusted-project lists, browser fingerprints, or local executable paths.
- Do not treat `AGENTS.md` as a substitute for sandboxing and approvals.
- Do not infer the effective model or permissions from configuration alone;
  verify the actual runtime when it matters.
- Treat a standalone Luna Max task as a new user-owned task, not as a native
  subagent. Require explicit approval before creation, send minimal context,
  and preserve the same authorization and protected-boundary rules.

## Native configuration only

This workflow intentionally uses documented native multi-agent settings. Do
not add an internal feature flag, model catalog override, or custom agent as a
fallback. If native support is unavailable, preserve the current configuration
and investigate the client version, managed policy, and documented settings.
The optional standalone Luna Max lane does not alter this rule.

## Reporting a security issue

Do not open a public issue containing credentials, personal paths, private
repository names, model catalogs, caches, or session rollouts. Contact the
repository owner privately through their GitHub profile instead.
