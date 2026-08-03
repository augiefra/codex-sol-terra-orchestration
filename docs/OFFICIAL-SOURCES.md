# Official sources and evidence boundaries

This repository combines documented Codex capabilities with a local operating
policy. They are deliberately separate.

## Official documentation

- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  documents local subagent workflows, model and reasoning choice, and guidance
  to use `gpt-5.6-terra` for faster, lower-cost lighter subagent work.
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
  documents `features.multi_agent`, `[agents]`, default subagent model and
  effort, the concurrency ceiling, and spawn-time precedence.
- [Advancing the price-performance frontier with GPT-5.6](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)
  announces a 20% Terra price reduction effective July 30, 2026 and says the
  lower price is reflected in paid-subscription usage accounting for Codex and
  ChatGPT Work. It does not claim that every task uses 20% fewer tokens.

These are the sources for every configuration key used by this repository.

## Guidance distinct from official documentation

[Eric Provencher's post on X](https://x.com/pvncher/status/2083300990350954981)
may be useful practical guidance from a Codex team member. It is not a
substitute for the official documentation and does not create a compatibility
or performance guarantee.

## Repository policy

The following are workflow choices made by this repository, not universal
OpenAI rules:

- Sol High is the parent orchestrator for the documented topology;
- Terra High is the default native subagent;
- routing considers difficulty and risk instead of size alone;
- a batch assigns one writable owner per file;
- a child stops after two distinct evidence-based failures or on a protected
  boundary;
- final responses identify actual runtime when it can be proven.

The repository does not prescribe a model catalog, compatibility patch,
internal feature flag, or custom agent profile.
