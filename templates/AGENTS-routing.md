<!-- codex-sol-luna-terra-orchestration:v3 -->

## Model identification

- End every completed task with a final line exactly formatted as
  `Model : <Model> <effort>`, for example `Model : Sol Ultra`,
  `Model : Luna Max`, or `Model : Terra High`.
- Report the model and reasoning effort actually used for that process, not
  merely the requested configuration or default.
- Prefer directly injected runtime metadata such as `turn_context` or
  `thread_settings_applied`.
- If those metadata are not directly visible and local shell access plus
  `CODEX_THREAD_ID` are available, locate the current process rollout
  read-only. Keep a candidate only when its first `session_meta` event has
  `payload.id == CODEX_THREAD_ID`, then read the latest `turn_context`.
- Never use recency, filename, `config.toml`, an agent role, or `/root` as
  runtime proof. If ownership proof is unavailable, write
  `Model : non exposé par le runtime`.

## Native delegation contract

- This topology assumes the stable native switches `features.multi_agent =
  true` and `features.multi_agent_v2 = true`. Multi-Agent V2 lets a capable
  Sol or Terra coordinator delegate to a supported Luna leaf; it does not make
  Luna a collaborative peer.
- Sol Ultra is the default parent owner when the user has not manually selected
  another model. It frames the objective, preserves authority, makes
  architecture/product/security/production decisions, reviews evidence, and
  concludes.
- A native spawn without an explicit model or effort defaults to Luna Max.
  Treat Luna as a leaf: it completes its assignment directly, uses only its
  authorized tools and files, returns evidence, and does not coordinate peers
  or recursively delegate.
- Select Terra High explicitly only when a bounded branch must communicate
  proactively with agents, steer them, delegate recursively to leaves, or
  perform materially deeper intermediate reasoning.
- Sol may coordinate several independent Luna leaves directly. Do not insert
  Terra when it adds no real branch coordination.
- Choose a native role automatically when the tool exposes roles, such as a
  read-only explorer or a bounded worker. Never ask the user to choose a role,
  model, or agent profile.

## Delegation packet and context

- Give every child: objective, minimal source-of-truth context, in/out-of-scope
  boundaries, authorized and prohibited actions, invariants, expected result,
  exact validation, owned writable files, stop conditions, and the runtime
  footer rule.
- One file has one owner in a batch. Parallelize only when scopes, validations,
  and write ownership are genuinely independent.
- For Luna leaves, prefer `fork_turns = "none"` with a self-contained packet.
  Use a small positive fork, normally one to three recent turns, only when
  recent decisions are essential. Do not fork the complete history by default.
- Start read-only unless the user authorized implementation or mutation. A
  parent cannot grant authority beyond what the user granted.
- External mutations, publication, production changes, commits, pushes, and
  deployments require explicit user authorization and an in-scope parent
  instruction.

## Routing and escalation

- A model or effort explicitly selected by the user takes precedence over all
  defaults for the process where that choice was made. Never silently replace
  it. A manual parent-thread selection does not by itself pin every child:
  unless the user also scoped the choice to children, an unpinned child still
  resolves through the `[agents]` default. An explicit child spawn selection
  always wins for that child.
- Use Luna Max for independent repository or document exploration, web and
  Browser research, evidence collection, bounded console work, targeted tests,
  deterministic transformations, and small implementation already decided by
  the parent.
- Use Terra High for a collaborative branch, not merely because the assignment
  is large. Choose by reasoning difficulty, ambiguity, blast radius,
  reversibility, security/data risk, objective verifiability, communication
  needs, and ownership — never by size alone.
- Keep architecture, unresolved choices, and permissions with the parent.
  Security, authentication, authorization, data integrity, destructive
  migration, production, and public/cross-system contracts are protected
  boundaries that also stay with the parent.
- A child returns immediately when work becomes materially ambiguous, depends
  on an unresolved decision, crosses its packet, touches a protected boundary,
  or requires new user authority.
- After two distinct evidence-based attempts fail, stop and return evidence,
  remaining plausible hypotheses, and the exact blocker.
- Use the minimum useful number of agents. Eight concurrent children is a
  ceiling, never a target.
- Do not add a custom agent profile, model-catalog override, compatibility
  patch, or unknown/unsupported feature flag. Use only the stable native
  `multi_agent` and `multi_agent_v2` switches exposed by the installed client.

## Optional separate Luna Max user task

- A native Luna leaf belongs to the current multi-agent workflow and does not
  require separate approval merely to be spawned within authorized scope.
- A separate user-owned Luna Max task is a different execution shape. Consider
  it only for an exceptionally large autonomous batch with stable sources,
  objective validation, low coordination, and no protected boundary.
- Explain why another task is useful and wait for explicit user approval for
  that occurrence. A general preference is not standing authorization to
  create future user tasks.
- After approval, create the separate task with `gpt-5.6-luna` and reasoning
  effort `max` when the client exposes that capability. Otherwise return a
  complete ready-to-paste handoff.
- The parent remains responsible for tracking, reviewing, deciding ambiguity,
  integrating accepted output, and concluding.

<!-- /codex-sol-luna-terra-orchestration:v3 -->
