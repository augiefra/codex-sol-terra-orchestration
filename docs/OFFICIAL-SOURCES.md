# Sources, timeline, and evidence boundaries

This repository combines documented Codex capabilities, observed runtime
evidence, and a local routing policy. Those categories are deliberately kept
separate.

> Last source review: 2026-08-15.

## Evidence hierarchy

| Level | Can establish | Cannot establish alone |
|---|---|---|
| Official OpenAI documentation | Supported public configuration, model guidance, precedence, permissions, and documented workflows | What one local process actually ran |
| Exact runtime metadata | Effective model and effort for one process in one run | Universal availability or future behavior |
| Dated product-team post | Rollout context, warnings, and intended capability distinctions | A permanent configuration contract |
| Repository policy | The conservative defaults chosen by this project | A universal OpenAI recommendation |

A lower level never overrides a higher one. When two public statements appear
to conflict, check their dates and scope before deciding that either is wrong.

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

The official documentation also supports custom agents. This repository does
not claim that custom agents are bad or unsupported; it simply does not require
one for this baseline because global `[agents]` defaults are sufficient.

## Product-team rollout guidance

[Eric Provencher (@pvncher on X)](https://x.com/pvncher), who works on Codex DX
at OpenAI, has published unusually clear explanations of the rollout. They are
attributed product-team notes, not official documentation.

### 2026-07-24 — practical orchestration

- [Practical multi-agent orchestration in Codex](https://x.com/pvncher/status/2080707291603407077)
- Contribution: broader operating context for bounded delegation and parent
  coordination.
- Boundary: it is not the source for any TOML key in this repository.

### 2026-07-31 — do not patch the model catalog

- [Warning against forcing Luna through a model catalog](https://x.com/pvncher/status/2083300990350954981)
- Short excerpt: “I do not recommend messing with your model catalog.”
- Contribution: proactive inter-agent communication belonged to Sol and Terra;
  users should not force Luna into that capability tier.
- Enduring rule: use only capability surfaces exposed natively by the client.

### 2026-08-15 — native delegation to Luna ships

- [Multi-Agent V2 models can delegate to supported models, including Luna](https://x.com/pvncher/status/2088641056237580632)
- Short excerpt: “delegate to any supported model, including Luna!”
- Contribution: Sol or Terra can now delegate terminal work to a supported Luna
  child without a catalog workaround.
- Boundary: the post does not say Luna becomes a collaborative peer.

### 2026-08-15 — two subagent tiers

- [Collaborative agents and leaf agents](https://x.com/pvncher/status/2088666195381592153)
- Short excerpt: “There are now two tiers of sub agents in codex.”
- Contribution: Sol and Terra are collaborative; Luna and older models are
  leaves used for delegation.
- Architectural result: Sol can own Luna leaves directly, while Terra is
  useful only when a bounded branch needs its own coordinator.

Together, the posts describe a rollout rather than a contradiction:

```text
Earlier: do not force Luna into a collaborative peer slot
Now:     Sol/Terra coordinator -> supported Luna leaf
Still:   Luna leaf             -/-> collaborative peer
```

The detailed interpretation is in
[EVOLUTION-AND-EVIDENCE.md](EVOLUTION-AND-EVIDENCE.md). These posts are not a
substitute for official documentation, client capability discovery, or
observed runtime metadata.

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

## Attribution and independence

Special thanks to
[Eric Provencher (@pvncher on X)](https://x.com/pvncher) for publishing the
dated capability distinctions that motivated this update.

This is an independent community project. The citations do not imply review,
sponsorship, affiliation, or endorsement by Eric Provencher or OpenAI.
