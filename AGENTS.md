# Repository instructions

These instructions apply to work on this repository. They are not the global
routing instructions installed into a user's Codex configuration.

- Treat `README.md`, `docs/`, and `templates/` as the public source of truth.
- Never copy a user's complete `~/.codex/config.toml`, model cache, model
  catalog, credentials, project trust entries, connector identifiers, local
  paths, environment fingerprints, or private instructions into this repo.
- Keep the default installation merge-based. Never tell Codex to overwrite an
  existing global configuration wholesale.
- Keep every verification script read-only by default.
- Prefer runtime evidence from `turn_context` over claims inferred from a
  requested model, a role name, or a configuration file.
- Preserve the core topology: Sol High owns the parent thread; native Terra
  High subagents handle independent, bounded work through Codex multi-agent
  communication. Do not add a custom agent profile unless a proven technical
  constraint requires it; stop and raise that constraint before doing so.
