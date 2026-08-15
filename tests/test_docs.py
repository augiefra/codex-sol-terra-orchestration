from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class DocumentationTests(unittest.TestCase):
    def markdown_files(self) -> list[Path]:
        return sorted(
            path
            for path in ROOT.rglob("*.md")
            if ".git" not in path.parts
        )

    def test_every_relative_markdown_link_resolves(self) -> None:
        missing: list[str] = []
        for document in self.markdown_files():
            contents = document.read_text(encoding="utf-8")
            for target in MARKDOWN_LINK.findall(contents):
                destination = target.strip().split(maxsplit=1)[0].strip("<>")
                if destination.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path_text = unquote(destination.split("#", 1)[0])
                if path_text and not (document.parent / path_text).resolve().exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {destination}")
        self.assertEqual(missing, [], "Missing relative links:\n" + "\n".join(missing))

    def test_rollout_sources_are_directly_attributed(self) -> None:
        sources = (ROOT / "docs" / "OFFICIAL-SOURCES.md").read_text(encoding="utf-8")
        required = {
            "https://x.com/pvncher/status/2083300990350954981",
            "https://x.com/pvncher/status/2088641056237580632",
            "https://x.com/pvncher/status/2088666195381592153",
            "https://learn.chatgpt.com/docs/agent-configuration/subagents",
            "https://learn.chatgpt.com/docs/config-file/config-reference",
        }
        self.assertEqual({url for url in required if url not in sources}, set())
        self.assertIn("independent community project", sources.lower())
        self.assertIn("do not imply", sources.lower())


if __name__ == "__main__":
    unittest.main()
