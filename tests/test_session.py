from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import session


class SessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.previous_path = os.environ.get("alfred_workflow_data")
        os.environ["alfred_workflow_data"] = self.temporary_directory.name

    def tearDown(self) -> None:
        if self.previous_path is None:
            os.environ.pop("alfred_workflow_data", None)
        else:
            os.environ["alfred_workflow_data"] = self.previous_path
        self.temporary_directory.cleanup()

    def test_save_load_and_clear_exchange(self) -> None:
        session.save_exchange("问题", "回答", [])
        self.assertEqual(
            session.load_messages(),
            [{"role": "user", "content": "问题"}, {"role": "assistant", "content": "回答"}],
        )
        self.assertTrue(session.has_session())
        session.clear_session()
        self.assertEqual(session.load_messages(), [])

    def test_session_keeps_the_most_recent_six_rounds(self) -> None:
        history: list[dict[str, str]] = []
        for number in range(7):
            session.save_exchange(f"问题{number}", f"回答{number}", history)
            history = session.load_messages()
        self.assertEqual(len(history), 12)
        self.assertEqual(history[0]["content"], "问题1")
        self.assertEqual(history[-1]["content"], "回答6")


if __name__ == "__main__":
    unittest.main()
