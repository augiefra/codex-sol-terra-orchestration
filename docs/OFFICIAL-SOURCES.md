# Official sources and evidence boundaries

This workflow combines official Codex capabilities with a community routing
policy and locally observed runtime behavior. Keep those layers separate.

## Officially documented capabilities

- [Codex configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Sample Codex configuration](https://learn.chatgpt.com/docs/config-file/config-sample)
- [`AGENTS.md` instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Sandboxing](https://learn.chatgpt.com/docs/sandboxing)
- [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [GPT-5.6 Sol model](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
- [GPT-5.6 Luna model](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [Latest model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [Responses API Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent)

Official documentation supports user/project configuration, layered
`AGENTS.md` instructions, custom agents under user or project directories,
per-agent model and reasoning settings, and sandbox/approval controls.

## Community policy in this repository

The following are this repository's operating decisions, not universal OpenAI
rules:

- Luna Max as the economical global default;
- explicitly selecting Sol High for architecture threads;
- one custom agent named `luna_worker`;
- the exact task packet and escalation gates;
- the two-failed-attempt rule;
- one writable owner per file;
- the final `Model : <Model> <effort>` convention;
- using `CODEX_THREAD_ID` and exact rollout matching as runtime proof.

## Version-dependent local observations

The following were observed in a tested Codex Desktop build and must be
revalidated after updates:

- the `[features.multi_agent_v2]` keys used by this setup;
- `fork_turns="none"` for custom-agent spawns in the active delegation tool;
- the local availability of Luna Max and Sol High labels;
- `CODEX_THREAD_ID` in local task environments;
- the local rollout JSONL structure;
- a cached Luna V1 entry being filtered while a locally patched V2 entry was
  accepted.

## Important API distinction

Local Codex custom agents can have their own model settings. The Responses API
Multi-agent beta is a separate feature and currently documents a shared request
model/tool context. Do not claim that this local Sol/Luna topology describes
the API feature.
