# Repository instructions

These instructions apply to work on this repository. They are not the global
routing instructions installed into a user's Codex configuration.

- Treat `docs/ARCHITECTURE.md` as the canonical policy and
  `templates/AGENTS-routing.md` as its installable summary. Tutorials, examples,
  and the README must link to that policy rather than silently redefining it.
- Keep the source hierarchy explicit: official OpenAI documentation, exact
  runtime evidence, dated attributed product-team explanations, then this
  repository's policy. A lower layer never overrides a higher layer.
- Attribute Eric Provencher's dated public posts with direct links and short,
  copyright-safe excerpts only. Never imply that he or OpenAI reviewed,
  sponsored, endorsed, or is affiliated with this community repository.
- Never copy a user's complete `~/.codex/config.toml`, model cache, model
  catalog, credentials, project trust entries, connector identifiers, local
  paths, environment fingerprints, or private instructions into this repo.
- Keep the default installation merge-based. Never tell Codex to overwrite an
  existing global configuration wholesale.
- Keep every verification script read-only by default.
- Preserve exactly one ordered start/end marker pair in the routing template:
  `<!-- codex-sol-luna-terra-orchestration:v3 -->` and
  `<!-- /codex-sol-luna-terra-orchestration:v3 -->`. Require idempotent
  update-in-place installation behavior.
- Keep `python3 -m unittest discover -s tests -v` passing whenever templates or
  verification scripts change.
- Prefer runtime evidence from `turn_context` over claims inferred from a
  requested model, a role name, or a configuration file.
- Preserve the core topology: Sol Ultra owns the parent thread; native Luna Max
  leaf subagents handle independent, bounded work; Terra High is selected only
  for a collaborative branch that needs proactive inter-agent communication,
  recursive delegation, or materially deeper intermediate reasoning.
- Keep Luna leaf prompts self-contained and focused. Prefer no inherited turns,
  or a small positive fork when recent decisions are essential; do not fork the
  entire parent history by default.
- Preserve the optional separate user-owned Luna Max task for exceptionally
  large autonomous batches, created only after explicit approval. Keep it
  distinct from native Luna leaf delegation.
- Require the stable native `features.multi_agent_v2` switch for the current
  leaf-model route. Do not add unknown/unsupported feature flags, a custom
  agent profile, compatibility override, or model-catalog patch.
