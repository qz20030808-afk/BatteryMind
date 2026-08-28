from types import SimpleNamespace

import pytest

from batterymind.llm_client import (
    ModelConfigurationError,
    build_messages,
    call_chat_completion,
    dry_run_request,
    load_model_settings,
)


def test_messages_keep_roles_and_context() -> None:
    messages = build_messages("问题", "证据")
    assert [message["role"] for message in messages] == ["system", "user"]
    assert "证据" in messages[1]["content"]


def test_dry_run_never_exposes_a_real_key() -> None:
    request = dry_run_request("问题")
    assert request["mode"] == "dry_run"
    assert request["headers"]["Authorization"] == "Bearer <redacted>"


class FakeCompletions:
    def __init__(self) -> None:
        self.request = None

    def create(self, **request):
        self.request = request
        message = SimpleNamespace(content="真实接口形状的回答", tool_calls=None)
        choice = SimpleNamespace(message=message, finish_reason="stop")
        usage = SimpleNamespace(prompt_tokens=20, completion_tokens=8, total_tokens=28)
        return SimpleNamespace(
            id="chatcmpl-test",
            model="qwen-plus",
            choices=[choice],
            usage=usage,
        )


def test_real_call_boundary_sends_messages_and_keeps_usage() -> None:
    completions = FakeCompletions()
    client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
    settings = {"api_key": "test-only", "base_url": "https://example.test/v1", "model": "qwen-plus"}

    result = call_chat_completion(
        [{"role": "user", "content": "问题"}],
        client=client,
        settings=settings,
    )

    assert completions.request["model"] == "qwen-plus"
    assert completions.request["messages"][0]["content"] == "问题"
    assert result["response"]["id"] == "chatcmpl-test"
    assert result["response"]["usage"]["total_tokens"] == 28
    assert "api_key" not in result["request"]


def test_missing_key_is_a_hard_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("BATTERYMIND_API_KEY", raising=False)
    with pytest.raises(ModelConfigurationError):
        load_model_settings()
