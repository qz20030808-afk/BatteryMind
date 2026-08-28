from batterymind.tooling import dispatch_tool


def test_clean_csv_returns_successful_tool_result() -> None:
    result = dispatch_tool({"tool_name": "inspect_battery_csv", "arguments": {"input_csv": "tests/fixtures/week2/clean.csv"}})
    assert result["ok"] is True
    assert result["data"]["report"]["quality_ok"] is True


def test_quality_issues_are_data_not_execution_failure() -> None:
    result = dispatch_tool({"tool_name": "inspect_battery_csv", "arguments": {"input_csv": "tests/fixtures/week2/issues.csv"}})
    assert result["ok"] is True
    assert result["data"]["report"]["quality_ok"] is False


def test_unknown_tool_and_missing_file_are_wrapped() -> None:
    unknown = dispatch_tool({"tool_name": "delete_files", "arguments": {}})
    missing = dispatch_tool({"tool_name": "inspect_battery_csv", "arguments": {"input_csv": "missing.csv"}})
    assert unknown["error"]["type"] == "UnknownTool"
    assert missing["error"]["type"] == "FileNotFoundError"
