#!/usr/bin/env python3
"""Print the current Codex process model from its exact local rollout.

Read-only. The script fails closed when it cannot prove a unique match between
CODEX_THREAD_ID and the owning rollout's first session_meta.payload.id.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, NoReturn


def fail(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def parse_rollout(
    path: Path, thread_id: str
) -> tuple[bool, dict[str, Any] | None, int]:
    owner_session_id: str | None = None
    first_session_meta_seen = False
    latest_context: dict[str, Any] | None = None
    context_count = 0

    try:
        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                try:
                    event = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                if event.get("type") == "session_meta" and not first_session_meta_seen:
                    # Ownership is defined only by the first session_meta. A
                    # malformed first event rejects the candidate; a later
                    # inherited or repeated event can never repair it.
                    first_session_meta_seen = True
                    payload = event.get("payload") or {}
                    candidate_id = payload.get("id")
                    if isinstance(candidate_id, str):
                        owner_session_id = candidate_id
                elif event.get("type") == "turn_context":
                    payload = event.get("payload")
                    if isinstance(payload, dict):
                        latest_context = payload
                        context_count += 1
    except OSError as error:
        fail(f"cannot read a rollout candidate: {error}")

    return owner_session_id == thread_id, latest_context, context_count


def friendly_model(model: str) -> str:
    known = {
        "gpt-5.6-sol": "Sol",
        "gpt-5.6-terra": "Terra",
        # Manual model selection still takes precedence over routing defaults.
        "gpt-5.6-luna": "Luna",
    }
    return known.get(model, model)


def friendly_effort(effort: str) -> str:
    aliases = {"xhigh": "XHigh"}
    return aliases.get(effort.lower(), effort.capitalize())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=default_codex_home(),
        help="Codex home to inspect (default: CODEX_HOME or ~/.codex)",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="emit auditable JSON")
    output.add_argument("--explain", action="store_true", help="show proof details")
    args = parser.parse_args()

    thread_id = os.environ.get("CODEX_THREAD_ID")
    if not thread_id:
        fail("CODEX_THREAD_ID is not available")

    root = args.codex_home.expanduser()
    session_roots = [path for path in (root / "sessions", root / "archived_sessions") if path.is_dir()]
    if not session_roots:
        fail("the Codex sessions and archived-sessions directories are unavailable")

    # Filenames normally end with the session ID. This keeps the scan bounded,
    # but every candidate is still validated structurally below.
    candidates = [
        candidate
        for sessions_root in session_roots
        for candidate in sessions_root.rglob(f"*{thread_id}.jsonl")
    ]
    if not candidates:
        fail("no rollout filename candidate matches the current thread ID")

    exact_matches: list[tuple[Path, dict[str, Any] | None, int]] = []
    for candidate in candidates:
        exact, context, context_count = parse_rollout(candidate, thread_id)
        if exact:
            exact_matches.append((candidate, context, context_count))

    if len(exact_matches) != 1:
        fail(f"expected exactly one exact session match, found {len(exact_matches)}")

    rollout_path, context, context_count = exact_matches[0]
    if not context:
        fail("the exact rollout contains no turn_context")

    model = context.get("model")
    effort = context.get("effort") or context.get("reasoning_effort")
    if not isinstance(model, str) or not model:
        fail("the latest turn_context has no model")
    if not isinstance(effort, str) or not effort:
        fail("the latest turn_context has no reasoning effort")

    footer = f"Model : {friendly_model(model)} {friendly_effort(effort)}"
    relative_rollout = rollout_path.relative_to(root)

    if args.json:
        print(
            json.dumps(
                {
                    "thread_id": thread_id,
                    "rollout": str(relative_rollout),
                    "owner_session_id": thread_id,
                    "turn_context_count": context_count,
                    "model": model,
                    "reasoning_effort": effort,
                    "footer": footer,
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif args.explain:
        print(f"Exact rollout: {relative_rollout}")
        print(f"First session_meta owner: {thread_id}")
        print(f"turn_context events: {context_count}")
        print(f"Latest runtime: {model} / {effort}")
        print(footer)
    else:
        print(footer)


if __name__ == "__main__":
    main()
