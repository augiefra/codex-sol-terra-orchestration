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
- Preserve the core topology: Sol Max owns the parent thread; native Luna Max
  leaf subagents handle independent, bounded work; Terra High is selected only
  for a collaborative branch that needs proactive inter-agent communication,
  recursive delegation, or materially deeper intermediate reasoning.
- Keep Luna leaf prompts self-contained and focused. Prefer no inherited turns,
  or a small positive fork when recent decisions are essential; do not fork the
  entire parent history by default.
- Preserve the optional separate user-owned Luna Max task for exceptionally
  large autonomous batches, created only after explicit approval. Keep it
  distinct from native Luna leaf delegation.
- Do not add a custom agent profile, internal feature flag, compatibility
  override, or model-catalog patch for routing already exposed natively.
