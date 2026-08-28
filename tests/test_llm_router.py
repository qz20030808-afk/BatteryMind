import json

from batterymind.llm_router import route_question


def test_real_router_boundary_validates_model_json() -> None:
    captured = {}

    def fake_model(question: str, **kwargs):
        captured["question"] = question
        captured.update(kwargs)
        content = json.dumps(
            {
                "route": "tool",
                "tool_name": "inspect_battery_csv",
                "arguments": {"input_csv": "tests/fixtures/week2/clean.csv"},
                "reason": "用户要求检查 CSV",
            },
            ensure_ascii=False,
        )
        return {"response": {"content": content, "usage": {"total_tokens": 42}}}

    result = route_question(
        "检查 CSV",
        csv_path="tests/fixtures/week2/clean.csv",
        call_model=fake_model,
    )

    assert captured["response_format"] == {"type": "json_object"}
    assert "clean.csv" in captured["question"]
    assert result["decision"]["tool_name"] == "inspect_battery_csv"
