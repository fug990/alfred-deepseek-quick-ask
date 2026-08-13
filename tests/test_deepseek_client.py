from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import deepseek_client
from common import UserFacingError
from models import resolve_model


class DeepSeekClientTests(unittest.TestCase):
    def test_resolves_supported_model_shortcuts(self) -> None:
        self.assertEqual(resolve_model("flash"), "deepseek-v4-flash")
        self.assertEqual(resolve_model("deepseek-v4-pro"), "deepseek-v4-pro")
        self.assertIsNone(resolve_model("deepseek-chat"))
    @patch("deepseek_client.get_api_key", return_value=None)
    def test_requires_a_key(self, _get_api_key: MagicMock) -> None:
        with self.assertRaisesRegex(UserFacingError, "尚未配置"):
            deepseek_client.ask("你好")

    @patch("deepseek_client.get_api_key", return_value="test-key")
    @patch("deepseek_client.request.urlopen")
    def test_returns_chat_content(self, mock_urlopen: MagicMock, _get_api_key: MagicMock) -> None:
        response = MagicMock()
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "测试回答"}}]}
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertEqual(deepseek_client.ask("测试问题"), "测试回答")
        api_request = mock_urlopen.call_args.args[0]
        self.assertEqual(api_request.get_header("Authorization"), "Bearer test-key")
        self.assertNotIn("test-key", api_request.data.decode("utf-8"))

    @patch("deepseek_client.get_api_key", return_value="test-key")
    @patch("deepseek_client.request.urlopen")
    def test_uses_reasoning_content_when_content_is_empty(
        self, mock_urlopen: MagicMock, _get_api_key: MagicMock
    ) -> None:
        response = MagicMock()
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "", "reasoning_content": "推理结果"}}]}
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertEqual(deepseek_client.ask("测试问题"), "推理结果")

    @patch("deepseek_client.get_api_key", return_value="test-key")
    @patch("deepseek_client.request.urlopen")
    def test_includes_prior_messages_for_follow_up(
        self, mock_urlopen: MagicMock, _get_api_key: MagicMock
    ) -> None:
        response = MagicMock()
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "后续回答"}}]}
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = response
        history = [
            {"role": "user", "content": "第一个问题"},
            {"role": "assistant", "content": "第一个回答"},
        ]

        deepseek_client.ask("继续问题", history=history)

        payload = json.loads(mock_urlopen.call_args.args[0].data.decode("utf-8"))
        self.assertEqual(payload["messages"][1:-1], history)
        self.assertEqual(payload["messages"][-1], {"role": "user", "content": "继续问题"})


if __name__ == "__main__":
    unittest.main()
