"""Shared helpers for the DeepSeek Quick Ask Alfred workflow.

This module deliberately uses Python's standard library only. Configuration is
read from Alfred Workflow Variables, so the workflow has no Keychain or other
macOS-automation dependency.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


BUNDLE_ID = "com.gangfu.alfred.deepseek-quick-ask"
DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024
DEFAULT_SYSTEM_PROMPT = (
    "你是通过 DeepSeek API 提供的准确、简洁、乐于助人的中文助手。"
    "不要声称自己由 OpenAI 或其他公司构建；不确定的信息请明确说明不确定。"
)


class UserFacingError(RuntimeError):
    """An error that may safely be shown in Alfred."""


def configured_model() -> str:
    return os.environ.get("DEEPSEEK_MODEL") or DEFAULT_MODEL


def configured_base_url() -> str:
    return (os.environ.get("DEEPSEEK_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def configured_temperature() -> float:
    value = os.environ.get("DEEPSEEK_TEMPERATURE") or DEFAULT_TEMPERATURE
    try:
        return min(2.0, max(0.0, float(value)))
    except (TypeError, ValueError):
        return DEFAULT_TEMPERATURE


def configured_max_tokens() -> int:
    value = os.environ.get("DEEPSEEK_MAX_TOKENS") or DEFAULT_MAX_TOKENS
    try:
        return min(8192, max(1, int(value)))
    except (TypeError, ValueError):
        return DEFAULT_MAX_TOKENS


def configured_system_prompt() -> str:
    return os.environ.get("DEEPSEEK_SYSTEM_PROMPT") or DEFAULT_SYSTEM_PROMPT


def get_api_key() -> str | None:
    """Read the API key supplied in Alfred Workflow Variables."""
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    return key or None


def workflow_data_dir() -> Path:
    """Return Alfred's private data directory for this workflow."""
    configured_path = os.environ.get("alfred_workflow_data")
    if configured_path:
        path = Path(configured_path)
    else:
        path = Path.home() / "Library" / "Application Support" / "Alfred" / "Workflow Data" / BUNDLE_ID
    path.mkdir(parents=True, exist_ok=True)
    return path


def alfred_items(items: list[dict[str, Any]]) -> str:
    return json.dumps({"items": items}, ensure_ascii=False)
