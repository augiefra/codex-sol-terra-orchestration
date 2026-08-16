from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_install.py"
INSPECT = ROOT / "scripts" / "inspect_runtime_model.py"
CONFIG_TEMPLATE = ROOT / "templates" / "config.fragment.toml"
AGENTS_TEMPLATE = ROOT / "templates" / "AGENTS-routing.md"


class InstallVerifierTests(unittest.TestCase):
    def make_home(self, config: str | None = None, agents: str | None = None) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        home = Path(temporary.name)
        if config is not None:
            (home / "config.toml").write_text(config, encoding="utf-8")
        if agents is not None:
            (home / "AGENTS.md").write_text(agents, encoding="utf-8")
        return home

    def run_verifier(self, home: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VERIFY), "--codex-home", str(home)],
            capture_output=True,
            check=False,
            text=True,
        )

    def test_minimal_template_install_passes(self) -> None:
        home = self.make_home(
            CONFIG_TEMPLATE.read_text(encoding="utf-8"),
            AGENTS_TEMPLATE.read_text(encoding="utf-8"),
        )
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: exactly one v3 routing marker pair is installed", result.stdout)

    def test_valid_but_empty_toml_fails_required_values(self) -> None:
        home = self.make_home("", AGENTS_TEMPLATE.read_text(encoding="utf-8"))
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: parent default model is Sol", result.stdout)
        self.assertIn("FAIL: native agents are enabled", result.stdout)

    def test_wrong_child_model_fails(self) -> None:
        config = CONFIG_TEMPLATE.read_text(encoding="utf-8").replace(
            'default_subagent_model = "gpt-5.6-luna"',
            'default_subagent_model = "gpt-5.6-terra"',
        )
        home = self.make_home(config, AGENTS_TEMPLATE.read_text(encoding="utf-8"))
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: default native leaf model is Luna", result.stdout)

    def test_missing_multi_agent_v2_fails(self) -> None:
        config = CONFIG_TEMPLATE.read_text(encoding="utf-8").replace(
            "multi_agent_v2 = true\n",
            "",
        )
        home = self.make_home(config, AGENTS_TEMPLATE.read_text(encoding="utf-8"))
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: multi_agent_v2 feature is enabled", result.stdout)

    def test_disabled_multi_agent_v2_fails(self) -> None:
        config = CONFIG_TEMPLATE.read_text(encoding="utf-8").replace(
            "multi_agent_v2 = true",
            "multi_agent_v2 = false",
        )
        home = self.make_home(config, AGENTS_TEMPLATE.read_text(encoding="utf-8"))
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: multi_agent_v2 feature is enabled", result.stdout)

    def test_duplicate_routing_marker_fails(self) -> None:
        agents = AGENTS_TEMPLATE.read_text(encoding="utf-8")
        home = self.make_home(
            CONFIG_TEMPLATE.read_text(encoding="utf-8"),
            agents + "\n" + agents,
        )
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: exactly one v3 routing marker pair is installed", result.stdout)

    def test_unrelated_custom_profile_outside_managed_block_is_ignored(self) -> None:
        agents = (
            "# User-owned instructions\nUse my unrelated custom profile luna_fast elsewhere.\n\n"
            + AGENTS_TEMPLATE.read_text(encoding="utf-8")
        )
        home = self.make_home(CONFIG_TEMPLATE.read_text(encoding="utf-8"), agents)
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_protected_boundary_fails(self) -> None:
        agents = AGENTS_TEMPLATE.read_text(encoding="utf-8").replace(
            "Security, authentication, authorization, data integrity",
            "Sensitive matters",
        )
        home = self.make_home(CONFIG_TEMPLATE.read_text(encoding="utf-8"), agents)
        result = self.run_verifier(home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: protected-boundary escalation rule is present", result.stdout)


class RuntimeInspectorTests(unittest.TestCase):
    def make_rollout(
        self,
        requested_thread_id: str,
        owner_thread_id: str,
        model: str = "gpt-5.6-luna",
        effort: str = "max",
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        home = Path(temporary.name)
        sessions = home / "sessions" / "2026" / "08" / "15"
        sessions.mkdir(parents=True)
        rollout = sessions / f"rollout-test-{requested_thread_id}.jsonl"
        events = [
            {"type": "session_meta", "payload": {"id": owner_thread_id}},
            {
                "type": "turn_context",
                "payload": {"model": model, "effort": effort},
            },
        ]
        rollout.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )
        return temporary, home

    def run_inspector(
        self, home: Path, thread_id: str, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["CODEX_THREAD_ID"] = thread_id
        return subprocess.run(
            [sys.executable, str(INSPECT), "--codex-home", str(home), *arguments],
            capture_output=True,
            check=False,
            text=True,
            env=environment,
        )

    def test_default_output_is_exact_footer(self) -> None:
        thread_id = "019-test-luna"
        temporary, home = self.make_rollout(thread_id, thread_id)
        self.addCleanup(temporary.cleanup)
        result = self.run_inspector(home, thread_id)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Model : Luna Max\n")

    def test_json_output_contains_auditable_relative_rollout(self) -> None:
        thread_id = "019-test-terra"
        temporary, home = self.make_rollout(
            thread_id, thread_id, model="gpt-5.6-terra", effort="high"
        )
        self.addCleanup(temporary.cleanup)
        result = self.run_inspector(home, thread_id, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["model"], "gpt-5.6-terra")
        self.assertEqual(payload["reasoning_effort"], "high")
        self.assertEqual(payload["footer"], "Model : Terra High")
        self.assertFalse(Path(payload["rollout"]).is_absolute())

    def test_filename_match_without_owner_match_is_rejected(self) -> None:
        thread_id = "019-test-owner"
        temporary, home = self.make_rollout(thread_id, "019-different-owner")
        self.addCleanup(temporary.cleanup)
        result = self.run_inspector(home, thread_id)
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected exactly one exact session match, found 0", result.stderr)

    def test_later_session_meta_cannot_repair_malformed_first_owner(self) -> None:
        thread_id = "019-test-first-meta"
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        home = Path(temporary.name)
        sessions = home / "sessions"
        sessions.mkdir()
        rollout = sessions / f"rollout-test-{thread_id}.jsonl"
        events = [
            {"type": "session_meta", "payload": {}},
            {"type": "session_meta", "payload": {"id": thread_id}},
            {
                "type": "turn_context",
                "payload": {"model": "gpt-5.6-luna", "effort": "max"},
            },
        ]
        rollout.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )
        result = self.run_inspector(home, thread_id)
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected exactly one exact session match, found 0", result.stderr)


if __name__ == "__main__":
    unittest.main()
