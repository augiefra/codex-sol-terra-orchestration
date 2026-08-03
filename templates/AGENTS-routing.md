<!-- codex-sol-luna-orchestration:v1 -->

## Model identification

- End every completed task with a final line exactly formatted as
  `Model : <Model> <effort>`, for example `Model : Sol High` or
  `Model : Luna Max`.
- Report the model and reasoning effort actually used for the turn, not merely
  the requested or default profile.
- Prefer directly injected runtime metadata such as `turn_context` or
  `thread_settings_applied`.
- If those metadata are not directly visible and local shell access plus
  `CODEX_THREAD_ID` are available, locate your own rollout read-only under the
  Codex sessions directory. Retain a candidate only when
  `session_meta.payload.id` is structurally equal to your own
  `CODEX_THREAD_ID`, then read the latest `turn_context` for the actual model
  and effort.
- Never select a rollout only because it contains the ID, has the newest
  modification time, or has a plausible filename. A parent or child rollout
  may mention another thread's UUID.
- Never infer the actual model from `config.toml`, global instructions, the
  `/root` role, task type, custom-agent name, or what should theoretically have
  run.
- If neither direct runtime metadata nor an exact validated rollout can prove
  the identity, write `Model : non exposed by the runtime` rather than
  inventing it.
- Keep the model line as the last line of the final response.

## Delegation contract

- Use the single global custom agent `luna_worker` for delegated subtasks.
- When the delegation tool exposes an agent type, explicitly select
  `agent_type = "luna_worker"`.
- Launch a custom `luna_worker` with `fork_turns = "none"` and send a
  self-contained delegation packet. Do not combine a custom agent with a full
  fork of the parent history.
- The packet must define: objective, scope, boundaries, authorized actions,
  invariants, expected result, exact validation, writable files with one owner
  per file, and precise conditions for returning to the parent.
- Include the runtime-identification/footer rule in the child message because
  global instructions may not propagate to the child runtime.
- Use the minimum useful number of subagents. Do not delegate a trivial local
  fix merely to demonstrate delegation.
- Parallelize only genuinely independent, objectively verifiable packets with
  disjoint writable files. Two agents must never modify the same file in one
  batch.
- Start read-only unless mutation is explicitly authorized.
- External mutation, publication, production changes, commits, pushes, and
  deployments require both explicit user authorization and an in-scope
  instruction from the parent. A parent instruction never creates authority
  the user did not grant.

## Routing

- A model explicitly selected by the user in the Codex UI, Chrome extension,
  CLI, task settings, or creation call takes precedence over this default
  routing. Never silently replace that choice.
- Use Luna Max as the economical global default for routine, repeatable,
  token-heavy, or objectively verifiable work.
- Explicitly select Sol High for architecture threads, cross-system decisions,
  authorization, arbitration, product/security/production judgment, heavy
  coding, evidence review, and final acceptance.
- Inside a Sol High architecture thread, prefer `luna_worker` for independent
  repository/document/log exploration, web research, browser inspection,
  bounded console operations, targeted tests, deterministic transformations,
  and small changes already decided by Sol.
- Do not ask the user to choose a worker profile. Infer whether delegation is
  useful from the objective while keeping the selected parent model in control
  of the work and conclusion.
- Do not use Terra unless the user explicitly requests it or a verified
  technical constraint requires it.

## Escalation gates

- Evaluate delegation by reasoning difficulty, ambiguity, blast radius,
  reversibility, and objective verifiability—not by task size alone.
- A large deterministic mechanical task may fit Luna. A small high-impact
  security or contract change may require Sol.
- `luna_worker` must stop and return the exact issue to the parent when the
  mission becomes materially ambiguous, depends on an unresolved decision,
  crosses its boundaries, or affects security, authentication, authorization,
  data integrity, destructive migrations, or a public/cross-system contract.
- After two distinct evidence-based attempts fail, stop further attempts and
  return the evidence, remaining plausible hypotheses, and blocker to the
  parent. In a Sol-led architecture thread, the next decision belongs to Sol.
