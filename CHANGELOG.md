# Changelog

## 2026-08-15 — native Luna leaf orchestration

### Changed

- Made Luna Max the default native terminal leaf for unpinned child work.
- Kept Sol Max as the parent owner and Terra High as an explicit collaborative
  branch lead.
- Replaced the obsolete model-catalog workaround with documented `[agents]`
  defaults and native delegation.
- Added a dated evidence timeline crediting Eric Provencher's rollout notes,
  an evidence hierarchy, compatibility status, routing recipes, and a guarded
  beginner quickstart.
- Made `docs/ARCHITECTURE.md` the canonical policy.

### Verification

- Fixed the static verifier so valid-but-empty TOML fails required checks.
- Added a paired managed-block marker, protected-boundary checks, and
  duplicate-block detection.
- Added auditable `--json` and `--explain` runtime-inspector modes.
- Made rollout ownership fail closed on the first `session_meta`; a later event
  cannot repair malformed or mismatched ownership.
- Added local unit tests for configuration, instructions, runtime identity,
  source attribution, and relative documentation links.

### Migration note

An earlier v3 install may contain only this opening marker:

```text
<!-- codex-sol-luna-terra-orchestration:v3 -->
```

The managed block is now enclosed by an ordered pair:

```text
<!-- codex-sol-luna-terra-orchestration:v3 -->
...
<!-- /codex-sol-luna-terra-orchestration:v3 -->
```

Add the closing marker immediately after the existing workflow section, or
replace that section with the current template. Preserve all unrelated global
instructions. The verifier intentionally fails until exactly one ordered pair
exists.
