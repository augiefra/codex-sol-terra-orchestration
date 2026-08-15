# Official sources and evidence boundaries

This repository combines documented Codex capabilities, observed runtime
evidence, and a local routing policy. Those categories are deliberately kept
separate.

## Official documentation

- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  documents native subagent workflows, applicable `AGENTS.md` delegation,
  model and reasoning selection, global `[agents]` defaults, and explicit-spawn
  precedence. It describes `gpt-5.6-luna` for fast, narrowly scoped, clear,
  repeatable, or high-volume agents and `gpt-5.6-terra` for stronger efficient
  supporting agents.
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
  documents `features.multi_agent`, `agents.enabled`,
  `agents.default_subagent_model`,
  `agents.default_subagent_reasoning_effort`, and
  `agents.max_concurrent_threads_per_session`.
- [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model)
  positions Sol for frontier capability, Terra for a balance of intelligence
  and cost, and Luna for efficient high-volume workloads. It also documents
  that higher reasoning effort increases work and should be evaluated against
  latency and token use.
- [Advancing the price-performance frontier with GPT-5.6](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)
  records the family pricing changes. Pricing is not proof that a particular
  routing decision is correct or that a task emits a fixed percentage fewer
  tokens.

These are the sources for every public configuration key used by this
repository. The repository does not require an undocumented key.

## Product-team guidance

Eric Provencher's public posts and replies are useful guidance from a Codex
team member:

- [multi-model delegation announcement](https://x.com/pvncher/status/2088641056237580632);
- [collaborative agents and leaf-only delegation](https://x.com/pvncher/status/2088666195381592153);
- [practical multi-agent orchestration](https://x.com/pvncher/status/2080707291603407077).

Those posts support the operating distinction between collaborative Sol/Terra
branches and terminal Luna workers. They are not a substitute for official
documentation, current client capability discovery, or observed runtime
metadata.

## Observed runtime evidence

The effective model and effort of one process are proven only by directly
injected runtime metadata or by the canonical rollout whose first
`session_meta.payload.id` exactly equals that process's `CODEX_THREAD_ID`, then
its latest `turn_context`.

A successful smoke test proves that exact client and run. It must not be
generalized to every account, older CLI release, managed workspace, or future
version.

## Repository policy

The following are deliberate workflow choices, not universal OpenAI rules:

- Sol Max is the default parent owner;
- Luna Max is the ordinary native leaf default;
- Terra High is explicitly selected for a collaborative branch;
- Sol may coordinate several Luna leaves without inserting Terra;
- Luna receives a self-contained packet and minimal inherited history by
  default;
- routing considers difficulty, ambiguity, risk, communication, validation,
  and ownership rather than size alone;
- one writable file has one owner per batch;
- a child stops after two distinct evidence-based failures or immediately on a
  protected boundary;
- creating a separate user-owned Luna task requires explicit approval;
- final responses identify the actual runtime when it can be proven.

The repository does not prescribe a model catalog, cache patch, compatibility
override, internal feature flag, or custom agent profile.
