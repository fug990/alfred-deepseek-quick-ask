#!/usr/bin/env python3
"""Show supported model choices for the `dsmodel` Alfred command."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common import alfred_items, configured_model
from models import MODELS


def main() -> None:
    query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""
    current_model = configured_model()
    items = []
    for model_id, details in MODELS.items():
        searchable = f"{model_id} {details['alias']} {details['title']}".lower()
        if query and query not in searchable:
            continue
        marker = "（当前使用）" if model_id == current_model else ""
        items.append({
            "title": f"切换到 {details['title']} {marker}".strip(),
            "subtitle": f"{model_id} · {details['subtitle']} 按回车立即切换并清除当前会话。",
            "arg": model_id,
            "variables": {"deepseek_model_target": model_id},
            "valid": True,
        })
    if not items:
        items.append({
            "title": "仅支持 flash 或 pro",
            "subtitle": "例如：dsmodel flash 或 dsmodel pro",
            "valid": False,
        })
    print(alfred_items(items))


if __name__ == "__main__":
    main()
