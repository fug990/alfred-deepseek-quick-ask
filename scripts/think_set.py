#!/usr/bin/env python3
"""Persist the DeepSeek V4 thinking-mode choice in Workflow Variables."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from session import clear_session


VALUES = {"enabled", "disabled"}


def main() -> None:
    value = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()
    if value not in VALUES:
        print("⚠️ 仅支持 enabled 或 disabled。请输入 dsthink 后选择。")
        return
    workflow_plist = Path(__file__).resolve().parents[1] / "info.plist"
    command = ["/usr/libexec/PlistBuddy", "-c", f"Set :variables:DEEPSEEK_THINKING {value}", str(workflow_plist)]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        result = subprocess.run(
            ["/usr/libexec/PlistBuddy", "-c", f"Add :variables:DEEPSEEK_THINKING string {value}", str(workflow_plist)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print("⚠️ 思考模式未保存。请在 Alfred Workflow Variables 中设置 DEEPSEEK_THINKING。")
            return
    clear_session()
    label = "开启" if value == "enabled" else "关闭"
    print(f"DeepSeek 思考模式已{label}，当前会话已清除。")


if __name__ == "__main__":
    main()
