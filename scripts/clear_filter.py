#!/usr/bin/env python3
"""Alfred result for clearing the stored local conversation."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common import alfred_items
from session import has_session


print(alfred_items([{
    "title": "清除 DeepSeek 当前会话",
    "subtitle": "会删除本机保存的最近问答。" if has_session() else "当前没有保存的会话，仍可按回车确认。",
    "arg": "clear",
    "valid": True,
}]))
