import json

from batterymind.real_tool_agent import run_real_tool_agent


def test_real_tool_round_trip_executes_observation_then_calls_model_again() -> None:
    responses = [
        {
            "response": {
                "content": None,
                "tool_calls": [
                    {
                        "id": "call-1",
                        "name": "inspect_battery_csv",
                        "arguments": json.dumps(
                            {"input_csv": "tests/fixtures/week2/clean.csv"}
                        ),
                    }
                ],
            }
        },
        {
            "response": {
                "content": "CSV 字段完整，质量检查通过。",
                "tool_calls": [],
                "usage": {"total_tokens": 55},
            }
        },
    ]
    calls = []

    def fake_completion(messages, **kwargs):
        calls.append({"messages": list(messages), "kwargs": kwargs})
        return responses[len(calls) - 1]

    result = run_real_tool_agent(
        "请检查 tests/fixtures/week2/clean.csv",
        call_completion=fake_completion,
        settings={"api_key": "test", "base_url": "https://example.test/v1", "model": "qwen-plus"},
    )

    assert len(calls) == 2
    assert calls[1]["messages"][-1]["role"] == "tool"
    assert result["observation"]["ok"] is True
    assert result["answer"] == "CSV 字段完整，质量检查通过。"
    assert result["stop_reason"] == "task_complete"
