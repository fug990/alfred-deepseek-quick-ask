#!/usr/bin/env python3
"""Display the final DeepSeek answer in a scrollable native macOS window."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from answer_viewer import open_answer_window


def main() -> None:
    answer = sys.argv[1] if len(sys.argv) > 1 else ""
    if answer:
        open_answer_window(answer)


if __name__ == "__main__":
    main()
