"""Open DeepSeek answers in a compact, scrollable native macOS panel."""

from __future__ import annotations

import subprocess
from pathlib import Path

from common import workflow_data_dir

WINDOW_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "answer_window.js"

def open_answer_window(answer: str) -> Path:
    """Show an answer in an in-app native panel, without opening a document.

    Alfred Large Type has no scrolling support. The JXA panel uses standard
    macOS controls instead: its answer text is selectable and scrollable, but
    it has no document editor or file window visible to the user.
    """
    answer_path = workflow_data_dir() / "latest-answer.txt"
    answer_path.write_text(answer.rstrip() + "\n", encoding="utf-8")
    subprocess.Popen(
        ["/usr/bin/osascript", "-l", "JavaScript", str(WINDOW_SCRIPT), str(answer_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return answer_path
