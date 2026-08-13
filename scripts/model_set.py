#!/usr/bin/env python3
"""Persist the selected model to this Alfred workflow's Variables."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import MODELS, resolve_model
from session import clear_session


def main() -> None:
    requested_model = sys.argv[1] if len(sys.argv) > 1 else ""
    model_id = resolve_model(requested_model)
    if not model_id:
        print("⚠️ 不支持的模型。请输入 dsmodel，选择 Flash 或 Pro。")
        return

    workflow_plist = Path(__file__).resolve().parents[1] / "info.plist"
    result = subprocess.run(
        ["/usr/libexec/PlistBuddy", "-c", f"Set :variables:DEEPSEEK_MODEL {model_id}", str(workflow_plist)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("⚠️ 模型切换未保存。请在 Alfred Workflow Variables 中手动设置 DEEPSEEK_MODEL。")
        return
    clear_session()
    print(f"已切换到 {MODELS[model_id]['title']}（{model_id}），当前会话已清除。")


if __name__ == "__main__":
    main()
