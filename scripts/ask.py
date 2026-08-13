#!/usr/bin/env python3
"""Workflow action that sends one confirmed question to DeepSeek."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common import UserFacingError
from deepseek_client import ask
from session import load_messages, save_exchange


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else ""
    mode = __import__("os").environ.get("deepseek_mode", "new")
    try:
        history = load_messages() if mode == "follow" else []
        answer = ask(question, history=history)
        save_exchange(question, answer, history)
        print(answer)
    except UserFacingError as error:
        print(f"⚠️ {error}")


if __name__ == "__main__":
    main()
