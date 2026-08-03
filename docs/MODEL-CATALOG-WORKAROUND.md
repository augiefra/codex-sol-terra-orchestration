# Optional Luna multi-agent catalog workaround

> [!CAUTION]
> This is an unsupported, version-dependent local workaround. OpenAI documents
> the `model_catalog_json` configuration path, but does not document a public
> model-catalog schema, a Luna v1→v2 migration, or catalog editing as a way to
> add or authorize model support.

## Use it only when all conditions are true

- the current Codex build has been fully restarted;
- native Luna custom-agent support has been tested first;
- Luna is actually missing or rejected by the active multi-agent runtime;
- the current machine's fresh model cache contains exactly one Luna entry;
- that entry is marked `multi_agent_version = "v1"` while the runtime expects
  V2 custom agents;
- the user explicitly approves the workaround and its maintenance burden.

Do not use the workaround merely because an older post or screenshot says it
was once needed.

## Why copying an old catalog is unsafe

`model_catalog_json` loads a complete catalog, not a one-field overlay. A
copied catalog can become stale after a Codex update and keep obsolete model
metadata, messages, hashes, availability, or effort settings active.

Never commit or share the generated catalog. It is machine- and
version-specific and can contain internal model messages and client metadata.

## Safe procedure

1. Fully quit Codex Desktop.
2. Make sure `~/.codex/models_cache.json` is fresh for the installed client.
3. Run the optional builder explicitly:

   ```bash
   python3 scripts/build_luna_v2_catalog.py
   ```

4. The builder must refuse to write unless:
   - the JSON is valid;
   - the top-level `models` list exists;
   - exactly one entry has `slug = "gpt-5.6-luna"`;
   - that entry currently says `multi_agent_version = "v1"`;
   - the destination does not already exist, unless `--force` is supplied.
5. Review the reported source, destination, and changed field.
6. Add an absolute `model_catalog_json` path to the user's `config.toml`.
7. Parse the TOML and generated JSON.
8. Restart Codex fully.
9. Run the parent/child runtime smoke test from `VERIFICATION.md`.

## After every Codex update

1. Disable the catalog override.
2. Restart and test native Luna support.
3. If native support works, delete the override and generated file.
4. If it still fails for the same verified reason, rebuild from the new fresh
   cache. Never keep the old generated catalog.

## Rollback

Remove the `model_catalog_json` line from the user configuration, move the
generated file out of the active path, restart Codex, and re-run native model
discovery.
