#!/usr/bin/env python3
"""Print the current Codex process model from its exact local rollout.

Read-only. The script fails closed when it cannot prove a unique match between
CODEX_THREAD_ID and session_meta.payload.id.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def parse_rollout(path: Path, thread_id: str) -> tuple[bool, dict[str, Any] | None]:
    exact_session = False
    latest_context: dict[str, Any] | None = None

    try:
        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                try:
                    event = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                if event.get("type") == "session_meta":
                    payload = event.get("payload") or {}
                    exact_session = payload.get("id") == thread_id
                elif event.get("type") == "turn_context":
                    payload = event.get("payload")
                    if isinstance(payload, dict):
                        latest_context = payload
    except OSError as error:
        fail(f"cannot read a rollout candidate: {error}")

    return exact_session, latest_context


def friendly_model(model: str) -> str:
    known = {
        "gpt-5.6-sol": "Sol",
        "gpt-5.6-terra": "Terra",
        "gpt-5.6-luna": "Luna",
    }
    return known.get(model, model)


def friendly_effort(effort: str) -> str:
    aliases = {"xhigh": "XHigh"}
    return aliases.get(effort.lower(), effort.capitalize())


def main() -> None:
    thread_id = os.environ.get("CODEX_THREAD_ID")
    if not thread_id:
        fail("CODEX_THREAD_ID is not available")

    root = codex_home()
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

    exact_matches: list[tuple[Path, dict[str, Any] | None]] = []
    for candidate in candidates:
        exact, context = parse_rollout(candidate, thread_id)
        if exact:
            exact_matches.append((candidate, context))

    if len(exact_matches) != 1:
        fail(f"expected exactly one exact session match, found {len(exact_matches)}")

    _, context = exact_matches[0]
    if not context:
        fail("the exact rollout contains no turn_context")

    model = context.get("model")
    effort = context.get("effort") or context.get("reasoning_effort")
    if not isinstance(model, str) or not model:
        fail("the latest turn_context has no model")
    if not isinstance(effort, str) or not effort:
        fail("the latest turn_context has no reasoning effort")

    print(f"Model : {friendly_model(model)} {friendly_effort(effort)}")


if __name__ == "__main__":
    main()
