#!/usr/bin/env python3
"""Alfred Script Filter for non-secret workflow configuration."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common import alfred_items


def main() -> None:
    print(
        alfred_items(
            [
                {
                    "title": "在 Workflow Variables 中设置 DEEPSEEK_API_KEY",
                    "subtitle": "打开 Alfred Preferences → Workflows → DeepSeek Quick Ask，点击右上角 [x]，粘贴 API Key。",
                    "valid": False,
                },
            ]
        )
    )


if __name__ == "__main__":
    main()
