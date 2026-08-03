#!/usr/bin/env python3
"""Read-only static verifier for the Sol–Luna Codex workflow."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    print("ERROR: Python 3.11+ is required for tomllib", file=sys.stderr)
    raise SystemExit(2)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        (self.passes if condition else self.errors).append(message)

    def warn(self, condition: bool, message: str) -> None:
        if not condition:
            self.warnings.append(message)

    def print(self) -> None:
        for message in self.passes:
            print(f"PASS: {message}")
        for message in self.warnings:
            print(f"WARN: {message}")
        for message in self.errors:
            print(f"FAIL: {message}")


def load_toml(path: Path, report: Report, label: str) -> dict[str, Any]:
    if not path.is_file():
        report.errors.append(f"{label} is missing")
        return {}
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        report.errors.append(f"{label} does not parse: {error}")
        return {}
    report.passes.append(f"{label} parses as TOML")
    return data


def find_luna_entry(catalog: Any) -> list[dict[str, Any]]:
    if not isinstance(catalog, dict):
        return []
    models = catalog.get("models")
    if not isinstance(models, list):
        return []
    return [
        model
        for model in models
        if isinstance(model, dict) and model.get("slug") == "gpt-5.6-luna"
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    default_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    parser.add_argument("--codex-home", type=Path, default=default_home)
    args = parser.parse_args()

    report = Report()
    root = args.codex_home.expanduser()
    config_path = root / "config.toml"
    agent_path = root / "agents" / "luna_worker.toml"
    instructions_path = root / "AGENTS.md"

    config = load_toml(config_path, report, "user config.toml")
    agent = load_toml(agent_path, report, "luna_worker.toml")

    if config:
        report.require(config.get("model") == "gpt-5.6-luna", "global default model is Luna")
        report.require(config.get("model_reasoning_effort") == "max", "global default effort is Max")

        features = config.get("features") if isinstance(config.get("features"), dict) else {}
        v2 = features.get("multi_agent_v2") if isinstance(features.get("multi_agent_v2"), dict) else {}
        agents = config.get("agents") if isinstance(config.get("agents"), dict) else {}

        report.require(features.get("multi_agent") is True, "multi_agent feature is enabled")
        report.require(v2.get("enabled") is True, "multi_agent_v2 is enabled")
        report.require(v2.get("tool_namespace") == "agents", "multi-agent tool namespace is agents")
        report.require(agents.get("enabled") is True, "custom agents are enabled")
        report.require(agents.get("default_subagent_model") == "gpt-5.6-luna", "default subagent model is Luna")
        report.require(agents.get("default_subagent_reasoning_effort") == "max", "default subagent effort is Max")

        ceiling = agents.get("max_concurrent_threads_per_session")
        report.warn(isinstance(ceiling, int) and ceiling > 0, "max_concurrent_threads_per_session is absent or invalid")

        catalog_value = config.get("model_catalog_json")
        if isinstance(catalog_value, str) and catalog_value:
            catalog_path = Path(catalog_value).expanduser()
            if not catalog_path.is_file():
                report.errors.append("configured model catalog does not exist")
            else:
                try:
                    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as error:
                    report.errors.append(f"configured model catalog is invalid: {error}")
                else:
                    luna_entries = find_luna_entry(catalog)
                    report.require(len(luna_entries) == 1, "configured catalog has exactly one Luna entry")
                    if len(luna_entries) == 1:
                        version = luna_entries[0].get("multi_agent_version")
                        if version == "v2":
                            report.passes.append("configured catalog exposes Luna as multi-agent V2")
                        else:
                            report.errors.append(f"configured catalog reports Luna multi-agent version {version!r}, expected 'v2'")
                    report.warnings.append("a full model_catalog_json override is active; retest native support after Codex updates")

    if agent:
        report.require(agent.get("name") == "luna_worker", "custom agent name is luna_worker")
        report.require(agent.get("model") == "gpt-5.6-luna", "custom agent model is Luna")
        report.require(agent.get("model_reasoning_effort") == "max", "custom agent effort is Max")
        instructions = agent.get("developer_instructions")
        report.require(isinstance(instructions, str) and "two distinct evidence-based attempts" in instructions.lower(), "custom agent has the two-attempt stop rule")

    if not instructions_path.is_file():
        report.errors.append("global AGENTS.md is missing")
    else:
        try:
            text = instructions_path.read_text(encoding="utf-8")
        except OSError as error:
            report.errors.append(f"cannot read global AGENTS.md: {error}")
        else:
            required_checks = {
                "luna_worker": "luna_worker routing token is present",
                'agent_type = "luna_worker"': "custom-agent routing rule is present",
                'fork_turns = "none"': "custom-agent no-history-fork rule is present",
                "CODEX_THREAD_ID": "runtime identity rule is present",
            }
            lowered = text.lower()
            for needle, message in required_checks.items():
                report.require(needle.lower() in lowered, message)
            report.warn(
                "two" in lowered or "deux" in lowered,
                "two-attempt escalation language was not detected",
            )
            report.warn(
                "owner" in lowered or "propriétaire" in lowered or "proprietaire" in lowered,
                "file ownership language was not detected",
            )
            report.warn(
                "codex-sol-luna-orchestration:" in lowered,
                "workflow version marker is absent; translated/custom instructions may require manual review",
            )

    report.print()
    raise SystemExit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
