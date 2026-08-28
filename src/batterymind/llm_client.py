"""Real OpenAI-compatible chat-model boundary used by BatteryMind."""

from __future__ import annotations

import os
from time import perf_counter
from typing import Any


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen3.7-plus"


class ModelConfigurationError(RuntimeError):
    """Raised when a real model call cannot start because credentials are absent."""


def build_messages(
    question: str,
    context: str = "",
    *,
    system_prompt: str | None = None,
) -> list[dict[str, str]]:
    """Build the ordered messages visible to the model for one request."""

    system = system_prompt or (
        "你是 BatteryMind 助手。只能根据给定证据回答；证据不足时明确说明。"
    )
    user = question if not context else f"证据：\n{context}\n\n问题：{question}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_request_payload(
    *,
    model: str,
    messages: list[dict[str, str]],
    tools: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create the JSON-ready body that an OpenAI-compatible endpoint expects."""

    payload: dict[str, Any] = {"model": model, "messages": messages}
    if tools:
        payload["tools"] = tools
    return payload


def dry_run_request(
    question: str,
    *,
    model: str = "demo-model",
    context: str = "",
    tools: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return the request boundary without sending data to any provider."""

    return {
        "mode": "dry_run",
        "endpoint": "<provider>/chat/completions",
        "headers": {"Authorization": "Bearer <redacted>"},
        "payload": build_request_payload(
            model=model,
            messages=build_messages(question, context),
            tools=tools,
        ),
    }


def load_model_settings() -> dict[str, str]:
    """Read the real provider settings without ever printing the API key."""

    api_key = os.getenv("BATTERYMIND_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ModelConfigurationError(
            "没有检测到 DASHSCOPE_API_KEY（也可使用 BATTERYMIND_API_KEY）"
        )
    return {
        "api_key": api_key,
        "base_url": os.getenv("BATTERYMIND_BASE_URL", DEFAULT_BASE_URL),
        "model": os.getenv("BATTERYMIND_MODEL", DEFAULT_MODEL),
    }


def _create_client(settings: dict[str, str]) -> Any:
    """Create the official SDK client only when a real call is requested."""

    try:
        from openai import OpenAI
    except ImportError as error:
        raise ModelConfigurationError(
            "缺少 openai 依赖，请先执行 python -m pip install -e ."
        ) from error
    return OpenAI(
        api_key=settings["api_key"],
        base_url=settings["base_url"],
        timeout=60.0,
    )


def _normalise_tool_calls(message: Any) -> list[dict[str, str]]:
    calls: list[dict[str, str]] = []
    for call in message.tool_calls or []:
        calls.append(
            {
                "id": call.id,
                "name": call.function.name,
                "arguments": call.function.arguments,
            }
        )
    return calls


def _normalise_usage(usage: Any) -> dict[str, int] | None:
    if usage is None:
        return None
    if hasattr(usage, "model_dump"):
        value = usage.model_dump()
        return {
            key: value[key]
            for key in ("prompt_tokens", "completion_tokens", "total_tokens")
            if value.get(key) is not None
        }
    return {
        key: getattr(usage, key)
        for key in ("prompt_tokens", "completion_tokens", "total_tokens")
        if getattr(usage, key, None) is not None
    }


def call_chat_completion(
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    response_format: dict[str, str] | None = None,
    tool_choice: str | None = None,
    max_tokens: int = 128,
    client: Any | None = None,
    settings: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Send a real request and return a small, provider-neutral trace."""

    resolved_settings = settings or load_model_settings()
    resolved_client = client or _create_client(resolved_settings)
    request: dict[str, Any] = {
        "model": resolved_settings["model"],
        "messages": messages,
        "max_tokens": max_tokens,
    }
    if tools:
        request["tools"] = tools
    if response_format:
        request["response_format"] = response_format
    if tool_choice:
        request["tool_choice"] = tool_choice

    started = perf_counter()
    completion = resolved_client.chat.completions.create(**request)
    latency_ms = round((perf_counter() - started) * 1000, 1)
    choice = completion.choices[0]
    message = choice.message
    return {
        "request": {
            "base_url": resolved_settings["base_url"],
            "model": resolved_settings["model"],
            "messages": messages,
            "has_tools": bool(tools),
        },
        "response": {
            "id": completion.id,
            "model": completion.model,
            "content": message.content,
            "tool_calls": _normalise_tool_calls(message),
            "finish_reason": choice.finish_reason,
            "usage": _normalise_usage(completion.usage),
            "latency_ms": latency_ms,
        },
    }


def call_chat_model(
    question: str,
    *,
    context: str = "",
    system_prompt: str | None = None,
    tools: list[dict[str, Any]] | None = None,
    response_format: dict[str, str] | None = None,
    tool_choice: str | None = None,
    max_tokens: int = 128,
    client: Any | None = None,
    settings: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build messages and execute one real model request."""

    messages = build_messages(question, context, system_prompt=system_prompt)
    return call_chat_completion(
        messages,
        tools=tools,
        response_format=response_format,
        tool_choice=tool_choice,
        max_tokens=max_tokens,
        client=client,
        settings=settings,
    )
