"""Supported DeepSeek API model choices exposed by the Alfred workflow."""

from __future__ import annotations


MODELS = {
    "deepseek-v4-flash": {
        "alias": "flash",
        "title": "DeepSeek V4 Flash",
        "subtitle": "速度与成本优先，适合日常问答。",
    },
    "deepseek-v4-pro": {
        "alias": "pro",
        "title": "DeepSeek V4 Pro",
        "subtitle": "效果与复杂推理优先，响应通常更慢。",
    },
}


def resolve_model(value: str) -> str | None:
    """Resolve an Alfred command argument to a supported API model identifier."""
    normalized = value.strip().lower()
    for model_id, details in MODELS.items():
        if normalized in {model_id, details["alias"]}:
            return model_id
    return None
