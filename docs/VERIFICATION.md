# Verification

Static configuration proves intent, not execution. Verify syntax and routing
rules, then prove the actual parent and child runtimes.

All smoke tests below are read-only. Run them in a fresh projectless task after
restarting Codex when global settings changed.

## 1. Static verification

From the repository root:

```bash
python3 scripts/verify_install.py
```

It checks:

- `config.toml` exists, parses, and contains every required value even when the
  file is otherwise empty;
- parent default is Sol Ultra;
- `features.multi_agent`, `features.multi_agent_v2`, and `agents.enabled` are
  true;
- native child default is Luna Max;
- concurrency ceiling is eight;
- no model-catalog override is present;
- global instructions define Luna as a leaf and Terra High as a conditional
  collaborative branch;
- exactly one ordered v3 routing marker pair is installed;
- model proof, authority, owner, protected-boundary, and two-attempt rules are
  present;
- a separate user-owned Luna task remains explicitly approval-gated.

## 2. Native default-leaf smoke test

Create a fresh projectless task whose parent is Sol Ultra and send:

```text
ROUTING SMOKE TEST ONLY. Do not modify files, settings, repositories, or
external systems.

Remain the parent. Spawn exactly one native subagent using the configured
default model and effort. Do not use a custom agent and do not pass an explicit
model or effort override. Give it a self-contained packet with no inherited
parent turns.

The leaf must complete the assignment directly without spawning or
coordinating another agent. It may run exactly this local read-only command:

printf %s SOL-LUNA-LEAF-2026 | openssl dgst -sha256

It must return the command, exact hash, and its actual runtime model and effort
from its own metadata or canonical rollout. Wait for it, verify the hash
independently, then report the proven parent and child runtimes. Do not infer a
runtime from config.toml or the requested route.
```

Expected hash:

```text
eb30541a07d807c3792d2331b51b3aee29d4b5adc9b4d62d62f82cff43aa4779
```

Expected runtime after a successful installation:

```text
Parent: gpt-5.6-sol / ultra
Child:  gpt-5.6-luna / max
```

This test exercises the stable opt-in Multi-Agent V2 leaf route. Before the
test, `codex features list` must report both `multi_agent` and
`multi_agent_v2` enabled for the exact client binary under test.

## 3. Parallel Luna leaves

Use this test to prove that Sol can coordinate Luna directly without an
unnecessary Terra layer:

```text
PARALLEL LUNA SMOKE TEST ONLY. Read-only; no file or external mutation.

Spawn exactly two independent native subagents using the configured default
model and effort, no custom type, no explicit model/effort override, and no
full-history fork. Give each a self-contained packet. Neither child may spawn
or coordinate another agent.

Child A computes SHA-256 for ASCII CODEX-LUNA-A-2026 with no trailing newline.
Child B computes SHA-256 for ASCII CODEX-LUNA-B-2026 with no trailing newline.

Wait for both, independently verify both hashes, and prove each process's
runtime from its own metadata or exact rollout. Report whether both were Luna
Max and whether either attempted subdelegation.
```

Expected hashes:

```text
CODEX-LUNA-A-2026  a44c0526cf21608d6ae11c668984a85838cf8cf541bf60aec6acbf54f775455c
CODEX-LUNA-B-2026  d9c6769cd74b28554abd21c0d4613c53bb7f2bfa57569910eaa4be7b674fea01
```

## 4. Conditional Terra-to-Luna branch

This test validates the exception: Terra is selected explicitly because the
branch must itself delegate and integrate a leaf result.

```text
TERRA COORDINATION SMOKE TEST ONLY. Read-only; no file or external mutation.

Remain the Sol Ultra parent. Spawn exactly one native branch lead explicitly as
gpt-5.6-terra with high reasoning and a self-contained packet. The Terra branch
must spawn exactly one terminal child using the configured default model and
effort. That leaf must not spawn another agent.

The Luna leaf computes SHA-256 for ASCII TERRA-LUNA-LEAF-2026 with no trailing
newline and returns the command, hash, and proven runtime to Terra. Terra
verifies and integrates the leaf result, then returns its own proven runtime
and the evidence to the parent. The parent independently verifies the hash and
reports all three runtimes.
```

Expected hash:

```text
965c011fda9d646b733ec192fa4664190bd0b61f9469ede80d7259798c6823e3
```

Expected runtime:

```text
Parent:      gpt-5.6-sol / ultra
Branch lead: gpt-5.6-terra / high
Leaf:        gpt-5.6-luna / max
```

If the current client exposes Luna leaves but not recursive Terra delegation,
report that exact capability boundary. Verify the stable V2 switch and client
version; do not patch a catalog or add unknown feature fields.

## 5. Existing-thread test

Repeat one bounded read-only Luna assignment in an established Sol-led thread.
The packet must still contain objective, minimal context, scope, authorized
commands, no-mutation boundary, validation, and return conditions. Prefer no
inherited turns; use one to three only when a recent decision is essential.

This proves that old thread history is not silently copied into every leaf.

## 6. Optional separate-task test

This is not part of native installation acceptance. Run it only when testing
the optional creation of another user-owned Luna Max task, and only after the
user explicitly approves creating that task. See
[STANDALONE-LUNA-TASKS.md](STANDALONE-LUNA-TASKS.md).

Native Luna success does not prove separate-task creation, and separate-task
success does not prove native subagent routing.

## 7. Exact runtime identity

For the current process only:

```bash
python3 scripts/inspect_runtime_model.py
```

For an auditable explanation or machine-readable evidence:

```bash
python3 scripts/inspect_runtime_model.py --explain
python3 scripts/inspect_runtime_model.py --json
```

The helper requires `CODEX_THREAD_ID`, finds candidate rollouts, and retains
one only when its first `session_meta.payload.id` belongs to the current
process. It then reads the latest `turn_context`. A later inherited parent
`session_meta` inside a child rollout is deliberately ignored.

The following are insufficient proof: a config value, requested model, role
name, hard-coded footer, `/root`, task title, or rollout recency.

## 8. Repository self-tests

Before publishing a change to the templates or scripts:

```bash
python3 -m unittest discover -s tests -v
```

The suite covers a valid minimal install, empty TOML, an incorrect child
default, duplicate routing blocks, a missing protected-boundary rule, exact
runtime ownership, JSON evidence, rejection of a misleading filename whose
first `session_meta` belongs to another process, and rejection of a later
matching `session_meta` after a malformed first ownership event.
