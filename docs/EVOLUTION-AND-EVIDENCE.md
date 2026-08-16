# Evolution, evidence, and attribution

> Status: checked against public sources and the current local Codex runtime on
> 2026-08-16. Model availability and orchestration behavior can change; verify
> the current official documentation and your own runtime before treating this
> document as permanent product behavior.

This page explains why the repository now uses Sol Ultra as the parent, Luna Max
as the default terminal subagent, and Terra High only for a collaborative
branch. It also explains why older advice about Luna was reasonable when it was
published and is no longer the right installation strategy.

## Source hierarchy

The project uses four evidence levels, in this order:

1. **Official OpenAI documentation** defines supported public configuration,
   model guidance, precedence, permissions, and the current subagent surface.
2. **Observed runtime metadata** proves what one concrete parent or child
   actually used in one client and one run.
3. **Public product-team explanations** help interpret rollout changes and
   capability boundaries that may not yet be described with the same detail in
   formal documentation.
4. **Repository policy** chooses a conservative default for this workflow. It
   is an opinionated operating model, not an OpenAI requirement.

A lower level never overrides a higher one. In particular, an X post does not
replace the official configuration reference, and `config.toml` does not prove
the model that actually ran.

## Timeline

### Official release track — V2 stabilizes and gains leaf models

The official
[ChatGPT and Codex changelog](https://learn.chatgpt.com/docs/changelog)
records two decisive product changes: the opt-in Multi-Agent V2 experience was
stabilized with configurable subagent models and reasoning levels, and V2 later
added support for leaf models. This is the official release evidence that the
current workflow should enable `features.multi_agent_v2` instead of treating
that key as an unsupported workaround.

The broad configuration reference still documents `multi_agent` and the
`[agents]` surface without necessarily reflecting every release-specific V2
key. On a target installation, the exact client resolves that gap through
`codex features list`: enable V2 only when the installed client exposes it, and
update the client rather than patching a catalog when it does not.

### 2026-07-24 — practical orchestration guidance

[Eric Provencher](https://x.com/pvncher), who works on Codex DX at OpenAI,
published the X article
[Practical multi-agent orchestration in Codex](https://x.com/pvncher/status/2080707291603407077).
It provided the broader operating context for keeping a strong parent focused
on decisions while delegating bounded work.

This is useful background, not the source for any `config.toml` key in this
repository.

### 2026-07-31 — do not force Luna into an unsupported capability tier

In [this post](https://x.com/pvncher/status/2083300990350954981), Eric warned:

> “I do not recommend messing with your model catalog.”

He explained that proactive inter-agent communication was associated with Sol
and Terra, not Luna. At that moment, the safe conclusion was:

- do not patch the model catalog;
- do not pretend Luna is a collaborative peer;
- keep collaborative Multi-Agent V2 branches on Sol or Terra;
- use only capability surfaces exposed natively by the client.

That warning remains valid. This repository never asks users to patch the
catalog, even though native Luna delegation has since expanded.

### 2026-08-15 — V2 coordinators can delegate to Luna

Eric then announced that Codex had shipped the ability for models with
Multi-Agent V2 capabilities to
[delegate to any supported model, including Luna](https://x.com/pvncher/status/2088641056237580632).

The key distinction is directionality:

```text
Sol or Terra coordinator  ── delegates to ──>  Luna leaf
Luna leaf                 ── does not become ─> collaborative peer
```

This removed the need for the old catalog workaround. It requires the native
V2 runtime, and it did not turn Luna into a Sol- or Terra-like coordinator.

### 2026-08-15 — the two-tier model is made explicit

In a second post, Eric described
[two tiers of Codex subagents](https://x.com/pvncher/status/2088666195381592153):

1. collaborative agents that can message each other and recursively delegate:
   Sol and Terra;
2. leaf agents used for delegation: Luna and older models.

That public explanation is the clearest rationale for this repository's
topology:

```text
Sol Ultra parent
├── Luna Max leaf
├── Luna Max leaf
└── Terra High collaborative branch
    ├── Luna Max leaf
    └── Luna Max leaf
```

Sol can coordinate Luna leaves directly. Terra is inserted only when a bounded
subproject needs its own collaborative coordinator.

### 2026-08-16 — quality-first reasoning profile

The repository changed the parent default from Sol Max to Sol Ultra so the
owner can proactively delegate suitable independent work. It intentionally
kept Luna Max for every default leaf. OpenAI documents that higher effort costs
more time and tokens and recommends using the lowest sufficient effort; keeping
Luna at Max is therefore a local quality/cost decision, not a claim that every
Codex installation should do the same.

## What changed in this repository

The workflow evolved through three states:

| State | Default child | Why it existed | Why it changed |
|---|---|---|---|
| Initial native workflow | Terra High | Terra was the safe native collaborative worker. | Luna became attractive for high-volume terminal work. |
| Rejected workaround | Forced Luna through a catalog or custom profile | It appeared to expose Luna before native support was complete. | It depended on internal compatibility metadata, could drift after updates, and contradicted product-team guidance. |
| Current native workflow | Luna Max leaf | Current Codex supports delegation from V2 coordinators to supported leaf models, including Luna, with the stable opt-in V2 feature enabled. | This is the current design; re-evaluate when official behavior changes. |

The repository URL retains its historical `sol-terra` name so existing links
continue to work. The actual public title and architecture now include all
three roles: Sol, Luna, and Terra.

## What did not change

Native Luna support does not relax any safety or ownership boundary:

- the user still owns authorization;
- the parent still owns architecture and final acceptance;
- Luna remains a terminal assignment in this policy;
- Terra is not added merely because a task is large;
- one writable file has one owner in a parallel batch;
- a child stops at a protected boundary;
- a child stops after two distinct evidence-based failures;
- external publication, production changes, commits, pushes, and deployments
  require user authorization;
- runtime identity must be proven, not inferred from configuration.

## What “automatic” means

The Codex harness handles spawning, routing follow-up instructions, waiting for
results, and closing agent threads. Current releases can delegate after a
direct user request or when applicable `AGENTS.md` or skill instructions call
for delegation. Ultra can delegate more proactively.

“Automatic” does **not** mean:

- every task should be delegated;
- Luna can coordinate peers;
- a model-catalog patch is needed;
- the parent can grant authority the user did not grant;
- the configured default proves the runtime result.

This repository makes automatic routing predictable by combining the native
`multi_agent` and `multi_agent_v2` switches, documented `[agents]` defaults,
and explicit behavioral rules in `AGENTS.md`.

## Attribution and independence

Special thanks to
[Eric Provencher (@pvncher on X)](https://x.com/pvncher) for publicly
explaining the rollout from collaborative-only delegation to the current
collaborative-plus-leaf model. His dated posts made it possible to distinguish
an obsolete workaround from the native product behavior now available.

This is an independent community repository. Eric Provencher and OpenAI have
not reviewed, sponsored, or endorsed it. The links above are citations and
acknowledgements, not claims of affiliation.

## Revalidation checklist

When Codex updates materially:

1. read the current official
   [Subagents documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents);
2. read the current
   [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference);
3. confirm that Luna remains listed for fast, narrow, clear, repeatable, or
   high-volume agents;
4. confirm `[agents]` precedence and supported keys;
5. confirm `codex features list` exposes and enables `multi_agent_v2`;
6. run the smoke tests in [VERIFICATION.md](VERIFICATION.md) from a fresh task;
7. update this timeline only when a dated source or observed runtime changes
   the conclusion.
