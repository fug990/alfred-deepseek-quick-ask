#!/usr/bin/env python3
"""Show choices for DeepSeek's V4 thinking mode."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common import alfred_items, thinking_enabled


def main() -> None:
    query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""
    current = thinking_enabled()
    choices = [
        ("disabled", "关闭思考（推荐）", "只显示最终答案；速度更快，适合日常使用。", False),
        ("enabled", "开启思考", "适合复杂推理；最终答案仍会单独显示，不会显示思考过程。", True),
    ]
    items = []
    for value, title, subtitle, enabled in choices:
        if query and query not in f"{value} {title}".lower():
            continue
        marker = "（当前使用）" if enabled == current else ""
        items.append({
            "title": f"{title} {marker}".strip(),
            "subtitle": subtitle + " 按回车立即切换并清除当前会话。",
            "arg": value,
            "variables": {"deepseek_thinking_target": value},
            "valid": True,
        })
    if not items:
        items.append({
            "title": "请输入 enabled 或 disabled",
            "subtitle": "例如：dsthink disabled",
            "valid": False,
        })
    print(alfred_items(items))


if __name__ == "__main__":
    main()
