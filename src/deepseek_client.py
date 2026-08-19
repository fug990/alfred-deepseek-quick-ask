"""Minimal DeepSeek Chat Completions client."""

from __future__ import annotations

import json
from urllib import error, request

from common import (
    UserFacingError,
    configured_base_url,
    configured_max_tokens,
    configured_model,
    configured_system_prompt,
    configured_temperature,
    get_api_key,
    thinking_enabled,
)


def _message_from_error(payload: bytes) -> str | None:
    try:
        data = json.loads(payload.decode("utf-8"))
        return str(data.get("error", {}).get("message") or "") or None
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
        return None


def ask(question: str, history: list[dict[str, str]] | None = None, timeout: int = 30) -> str:
    """Ask DeepSeek and return the assistant answer, or a safe user-facing error."""
    question = question.strip()
    if not question:
        raise UserFacingError("请输入要询问的问题。")

    api_key = get_api_key()
    if not api_key:
        raise UserFacingError("尚未配置 API Key。请在 Alfred Workflow Variables 中填写 DEEPSEEK_API_KEY。")

    payload = {
        "model": configured_model(),
        "messages": [{"role": "system", "content": configured_system_prompt()}]
        + (history or [])
        + [{"role": "user", "content": question}],
        "temperature": configured_temperature(),
        "max_tokens": configured_max_tokens(),
        "thinking": {"type": "enabled" if thinking_enabled() else "disabled"},
        "stream": False,
    }
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    api_request = request.Request(
        f"{configured_base_url()}/chat/completions",
        data=encoded,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=timeout) as response:
            body = response.read()
    except error.HTTPError as response_error:
        detail = _message_from_error(response_error.read())
        if response_error.code in (401, 403):
            raise UserFacingError("API Key 无效或没有访问权限，请检查 Alfred Workflow Variables。") from None
        if response_error.code == 429:
            raise UserFacingError("请求过于频繁或额度不足，请稍后重试。") from None
        if response_error.code >= 500:
            raise UserFacingError("DeepSeek 服务暂时不可用，请稍后重试。") from None
        raise UserFacingError(detail or f"请求失败（HTTP {response_error.code}）。") from None
    except error.URLError as connection_error:
        reason = str(getattr(connection_error, "reason", ""))
        if "timed out" in reason.lower():
            raise UserFacingError("请求超时，请检查网络后重试。") from None
        raise UserFacingError("无法连接 DeepSeek API，请检查网络或 API 地址。") from None
    except TimeoutError:
        raise UserFacingError("请求超时，请检查网络后重试。") from None

    try:
        data = json.loads(body.decode("utf-8"))
        message = data["choices"][0]["message"]
        answer = str(message.get("content") or "").strip()
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError):
        raise UserFacingError("DeepSeek 返回了无法识别的内容，请稍后重试。") from None
    if not answer:
        raise UserFacingError("DeepSeek 未返回最终答案，请稍后重试。")
    return answer
