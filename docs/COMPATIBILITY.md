# Compatibility and proof status

This page separates three things that are easy to confuse:

1. a capability documented by OpenAI;
2. a product rollout explained publicly by a Codex team member;
3. behavior observed in one concrete client and run.

None of them makes a configured value proof of the runtime that actually ran.

## Current baseline

Last maintained check: **2026-08-15**.

| Item | Status | Evidence or required check |
|---|---|---|
| `features.multi_agent` | Public, documented setting | Official configuration reference |
| `[agents].enabled` and child defaults | Public, documented settings | Official configuration reference and Subagents docs |
| Sol and Terra as collaborative coordinators | Current capability guidance | Official model guidance plus Eric Provencher's dated rollout explanation |
| Luna as a native terminal leaf | Current capability guidance; observed locally with an explicit Luna Max child | Official Luna subagent guidance, Eric's 2026-08-15 posts, exact child rollout |
| Unpinned child resolves to Luna Max | Repository configuration expectation | Must pass the fresh-task default-leaf smoke test on the target client |
| Terra can recursively delegate to a Luna leaf | Repository topology expectation | Must pass the conditional Terra-to-Luna smoke test on the target client |
| Model/effort footer | Reporting convention only | Must be backed by injected metadata or the exact owning rollout |

The maintainer's local static baseline on 2026-08-15 used
`codex-cli 0.148.0-alpha.9`, parsed the native Sol Max / Luna Max settings, and
contained no `multi_agent_v2` key or model-catalog override. This is a dated
observation, not a minimum-version guarantee.

## What a successful test proves

A passing smoke test proves only the tested account, client build,
configuration layers, model availability, and run at that time. It does not
prove behavior for:

- an older CLI or desktop build;
- a managed workspace with policy overrides;
- a project with local configuration or instructions;
- a thread that was already running when global settings changed;
- an account on a different rollout;
- a future Codex release.

Record the client version, repository commit, test date, exact smoke-test
prompt, and runtime evidence when filing an issue. Do not include secrets,
complete configs, session histories, or private repository content.

## Fresh task versus restart

Use this order after changing global settings:

1. create a fresh task and run the default-leaf smoke test;
2. if it still sees stale behavior, fully quit and restart the Codex client;
3. create another fresh task and repeat;
4. inspect explicit spawn settings, custom roles, project config, and managed
   policy before changing anything else;
5. never patch a model catalog or add an undocumented feature flag to make the
   expected result appear.

An existing parent or child is not retroactively reconfigured by editing a
file on disk.

## Revalidation after an update

Run, in order:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_install.py --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

Then run the fresh-task native tests in [VERIFICATION.md](VERIFICATION.md).
Review [Evolution, evidence, and attribution](EVOLUTION-AND-EVIDENCE.md) before
changing the capability model in response to an announcement.

## Source links

- [Official Subagents documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Eric Provencher: native delegation to Luna](https://x.com/pvncher/status/2088641056237580632)
- [Eric Provencher: collaborative versus leaf tiers](https://x.com/pvncher/status/2088666195381592153)

This is an independent community compatibility note. It does not imply review,
affiliation, sponsorship, or endorsement by Eric Provencher or OpenAI.
