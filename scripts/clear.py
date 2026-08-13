#!/usr/bin/env python3
"""Clear the local ds/dsf conversation and return a notification message."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from session import clear_session

clear_session()
print("DeepSeek 当前会话已清除。")
