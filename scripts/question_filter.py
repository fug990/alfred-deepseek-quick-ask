#!/usr/bin/env python3
"""Build the Alfred result for a new question or a contextual follow-up."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common import alfred_items, configured_model, get_api_key
from session import has_session


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "new"
    query = sys.argv[2].strip() if len(sys.argv) > 2 else ""
    if not get_api_key():
        print(alfred_items([{
            "title": "尚未设置 DeepSeek API Key",
            "subtitle": "在 Alfred 工作流右上角 [x] 的 Variables 中填写 DEEPSEEK_API_KEY。",
            "valid": False,
        }]))
        return
    if mode == "follow" and not has_session():
        print(alfred_items([{
            "title": "还没有可继续的对话",
            "subtitle": "请先用 ds 提一个问题；输入 dsclear 可随时清除会话。",
            "valid": False,
        }]))
        return
    if not query:
        label = "继续追问" if mode == "follow" else "向 DeepSeek 提问"
        subtitle = "输入问题后按回车发送；会带上最近的上下文。" if mode == "follow" else f"输入问题后按回车发送（当前模型：{configured_model()}）"
        print(alfred_items([{"title": label, "subtitle": subtitle, "valid": False}]))
        return
    title = f"继续追问：{query}" if mode == "follow" else f"询问 DeepSeek：{query}"
    subtitle = "按回车发送；会携带本地最近对话的上下文。" if mode == "follow" else "按回车发送一次请求；这会开始一段新对话。"
    print(alfred_items([{
        "title": title,
        "subtitle": subtitle,
        "arg": query,
        "variables": {"deepseek_question": query, "deepseek_mode": mode},
        "valid": True,
    }]))


if __name__ == "__main__":
    main()
