#!/usr/bin/env python3
"""Build an opt-in local Luna V2 catalog from the current Codex model cache.

UNSUPPORTED WORKAROUND: this is not an official OpenAI migration mechanism.
The script never modifies the source cache and refuses ambiguous input.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def fail(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def defaults() -> tuple[Path, Path]:
    root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    return root / "models_cache.json", root / "model-catalogs" / "desktop-multi-agent.json"


def display_path(path: Path) -> str:
    """Mask the user's Codex home in normal output."""
    root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    try:
        relative = path.resolve().relative_to(root)
    except ValueError:
        return str(path)
    return f"<CODEX_HOME>/{relative}"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("source models_cache.json does not exist")
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot parse the source cache: {error}")
    if not isinstance(value, dict):
        fail("source cache must be a JSON object")
    return value


def main() -> None:
    source_default, destination_default = defaults()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=source_default)
    parser.add_argument("--destination", type=Path, default=destination_default)
    parser.add_argument("--force", action="store_true", help="Back up and replace an existing destination")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    destination = args.destination.expanduser().resolve()
    if source == destination:
        fail("source and destination must be different; the cache is never modified")

    catalog = load_json(source)
    models = catalog.get("models")
    if not isinstance(models, list):
        fail("source cache has no top-level models list")

    matches = [
        (index, model)
        for index, model in enumerate(models)
        if isinstance(model, dict) and model.get("slug") == "gpt-5.6-luna"
    ]
    if len(matches) != 1:
        fail(f"expected exactly one gpt-5.6-luna entry, found {len(matches)}")

    index, luna = matches[0]
    current = luna.get("multi_agent_version")
    if current == "v2":
        print("No catalog written: the fresh local cache already exposes Luna as V2.")
        return
    if current != "v1":
        fail(f"expected Luna multi_agent_version 'v1', found {current!r}")

    patched = copy.deepcopy(catalog)
    patched["models"][index]["multi_agent_version"] = "v2"

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not args.force:
        fail("destination already exists; review it and rerun with --force to back it up and replace it")

    if destination.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = destination.with_name(f"{destination.name}.backup-{stamp}")
        shutil.copy2(destination, backup)
        print(f"Backed up the previous destination to: {display_path(backup)}")

    encoded = json.dumps(patched, indent=2, ensure_ascii=False) + "\n"
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(encoded)
            temporary = Path(handle.name)
        os.replace(temporary, destination)
    except OSError as error:
        fail(f"cannot write the destination atomically: {error}")

    # Re-read and prove the one intended semantic change.
    written = load_json(destination)
    written_models = written.get("models")
    if not isinstance(written_models, list) or len(written_models) != len(models):
        fail("post-write validation failed: model list changed unexpectedly")

    normalized = copy.deepcopy(written)
    normalized["models"][index]["multi_agent_version"] = "v1"
    if normalized != catalog:
        fail("post-write validation failed: more than the Luna compatibility field changed")

    print(f"Created local catalog: {display_path(destination)}")
    print("Verified semantic change: gpt-5.6-luna multi_agent_version v1 -> v2")
    print("Next: review the file, add its absolute path as model_catalog_json, restart Codex, and run the runtime smoke test.")


if __name__ == "__main__":
    main()
