# Repository instructions

These instructions apply to work on this repository. They are not the global
routing instructions installed into a user's Codex configuration.

- Treat `README.md`, `docs/`, and `templates/` as the public source of truth.
- Never copy a user's complete `~/.codex/config.toml`, model cache, model
  catalog, credentials, project trust entries, connector identifiers, local
  paths, environment fingerprints, or private instructions into this repo.
- Keep the default installation merge-based. Never tell Codex to overwrite an
  existing global configuration wholesale.
- Label undocumented flags and the model-catalog workaround as observed,
  version-dependent behavior rather than official OpenAI API guarantees.
- Keep every verification script read-only by default. Any script that writes
  a workaround must require an explicit command and refuse unsafe ambiguity.
- Prefer runtime evidence from `turn_context` over claims inferred from a
  requested model, a role name, or a configuration file.
- Preserve the core topology: Luna Max is the economical default for routine
  work; architecture threads are explicitly run with Sol High; Sol delegates
  independent bounded work back to a single Luna Max custom agent.
- Do not add more custom agent profiles unless a proven technical constraint
  requires them.
