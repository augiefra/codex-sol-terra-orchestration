#!/usr/bin/env python3
"""Read-only verifier for the native Sol–Luna–Terra Codex workflow."""

from __future__ import annotations

import argparse
import os
import re
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


def load_toml(path: Path, report: Report) -> dict[str, Any]:
    if not path.is_file():
        report.errors.append("user config.toml is missing")
        return {}
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        report.errors.append(f"user config.toml does not parse: {error}")
        return {}
    report.passes.append("user config.toml parses as TOML")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    default_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    parser.add_argument("--codex-home", type=Path, default=default_home)
    args = parser.parse_args()

    report = Report()
    root = args.codex_home.expanduser()
    config = load_toml(root / "config.toml", report)

    if config:
        report.require(config.get("model") == "gpt-5.6-sol", "parent default model is Sol")
        report.require(config.get("model_reasoning_effort") == "max", "parent default effort is Max")
        features = config.get("features") if isinstance(config.get("features"), dict) else {}
        agents = config.get("agents") if isinstance(config.get("agents"), dict) else {}
        report.require(features.get("multi_agent") is True, "multi_agent feature is enabled")
        report.require(agents.get("enabled") is True, "native agents are enabled")
        report.require(
            agents.get("default_subagent_model") == "gpt-5.6-luna",
            "default native leaf model is Luna",
        )
        report.require(
            agents.get("default_subagent_reasoning_effort") == "max",
            "default native leaf effort is Max",
        )
        report.require(
            agents.get("max_concurrent_threads_per_session") == 8,
            "max_concurrent_threads_per_session is 8",
        )
        report.require("model_catalog_json" not in config, "no model catalog override is configured")
        report.require(
            "multi_agent_v2" not in features,
            "no internal multi-agent V2 configuration is present",
        )

    instructions_path = root / "AGENTS.md"
    if not instructions_path.is_file():
        report.errors.append("global AGENTS.md is missing")
    else:
        try:
            instructions = instructions_path.read_text(encoding="utf-8").lower()
        except OSError as error:
            report.errors.append(f"cannot read global AGENTS.md: {error}")
        else:
            checks = {
                (
                    "feuille native en `gpt-5.6-luna`",
                    "native luna max leaf",
                    "luna max is the ordinary native leaf",
                    "sous-agent feuille luna natif",
                    "a native spawn without an explicit model or effort defaults to luna max",
                ): "Luna Max native-leaf routing rule is present",
                (
                    "terra high seulement pour une branche collaborative",
                    "terra high only for a collaborative branch",
                    "terra high is selected only",
                    "select terra high explicitly only when",
                ): "Terra High conditional branch rule is present",
                (
                    "ne coordonne pas d’agents pairs",
                    "does not coordinate peers",
                    "terminal worker",
                ): "Luna leaf coordination boundary is present",
                ("codex_thread_id",): "runtime identity rule is present",
                (
                    "two distinct evidence-based attempts",
                    "deux tentatives distinctes fondées sur des preuves",
                ): "two-attempt stop rule is present",
                (
                    "one file has one owner",
                    "propriétaire unique",
                ): "single file-owner rule is present",
                (
                    "cannot grant authority beyond",
                    "ne peut jamais accorder une autorisation que l’utilisateur n’a pas donnée",
                ): "parent authorization boundary is present",
                ("fork_turns", "historique complet"): "minimal Luna context rule is present",
                ("luna max",): "Luna Max routing is present",
                (
                    "separate user-owned luna max task",
                    "task utilisateur luna max séparé",
                    "tasks utilisateur séparés luna max",
                ): "optional separate Luna task is distinguished from native leaves",
                (
                    "wait for explicit user approval",
                    "attends l’accord explicite",
                    "attends l'accord explicite",
                    "après accord explicite",
                ): "separate user task requires explicit approval",
            }
            for alternatives, message in checks.items():
                report.require(any(needle in instructions for needle in alternatives), message)
            report.require(
                any(
                    needle in instructions
                    for needle in (
                        "do not add a custom agent profile",
                        "n’ajoute jamais de catalogue de modèles modifié",
                        "n'ajoute jamais de catalogue de modèles modifié",
                    )
                ),
                "routing policy forbids custom agent profiles",
            )
            report.require(
                re.search(r"\bluna_[a-z0-9_-]+\b", instructions) is None,
                "no named custom Luna profile is referenced by routing policy",
            )
            report.require("model_catalog_json" not in instructions, "no model catalog override is recommended")
            report.require("multi_agent_v2" not in instructions, "no internal multi_agent_v2 flag is recommended")

    report.print()
    raise SystemExit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
