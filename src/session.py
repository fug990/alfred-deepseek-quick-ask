"""Short, local conversation memory for the `dsf` follow-up command."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from common import workflow_data_dir


MAX_MESSAGES = 12
SESSION_FILENAME = "conversation.json"


def session_path() -> Path:
    return workflow_data_dir() / SESSION_FILENAME


def load_messages() -> list[dict[str, str]]:
    """Return validated conversation messages, or an empty history."""
    try:
        payload: Any = json.loads(session_path().read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, list):
        return []
    messages = [
        {"role": item["role"], "content": item["content"]}
        for item in payload
        if isinstance(item, dict)
        and item.get("role") in {"user", "assistant"}
        and isinstance(item.get("content"), str)
    ]
    return messages[-MAX_MESSAGES:]


def has_session() -> bool:
    return bool(load_messages())


def save_exchange(question: str, answer: str, prior_messages: list[dict[str, str]]) -> None:
    """Persist a bounded conversation only after a successful API response."""
    messages = prior_messages + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
    destination = session_path()
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps(messages[-MAX_MESSAGES:], ensure_ascii=False), encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, destination)


def clear_session() -> None:
    """Remove only this workflow's local conversation file."""
    try:
        session_path().unlink()
    except FileNotFoundError:
        pass
