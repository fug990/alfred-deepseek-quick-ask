from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import answer_viewer


class AnswerViewerTests(unittest.TestCase):
    def test_writes_answer_and_opens_a_native_panel(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_dir = Path(temporary_directory)
            with patch("answer_viewer.workflow_data_dir", return_value=data_dir), patch(
                "answer_viewer.subprocess.Popen"
            ) as popen:
                answer_path = answer_viewer.open_answer_window("第一行\n第二行\n")
                self.assertEqual(answer_path.read_text(encoding="utf-8"), "第一行\n第二行\n")
                self.assertEqual(
                    popen.call_args.args[0][:3],
                    ["/usr/bin/osascript", "-l", "JavaScript"],
                )
                self.assertEqual(popen.call_args.args[0][-1], str(answer_path))
                self.assertTrue(popen.call_args.kwargs["start_new_session"])


if __name__ == "__main__":
    unittest.main()
