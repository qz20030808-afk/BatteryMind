from batterymind.rag_baseline import retrieve


def test_capacity_and_temperature_queries_keep_sources() -> None:
    results = retrieve("高温为什么影响电池容量衰减？")
    assert results
    assert all(result["source"] for result in results)
    assert results[0]["score"] >= results[-1]["score"]


def test_unrelated_query_returns_no_fake_evidence() -> None:
    assert retrieve("今天南京天气怎么样？") == []
