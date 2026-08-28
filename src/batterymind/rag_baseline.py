"""Transparent keyword retrieval baseline with source-preserving results."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KNOWLEDGE_PATH = PROJECT_ROOT / "data" / "knowledge" / "battery_knowledge.json"
BATTERY_TERMS = {
    "电池", "容量", "衰减", "高温", "低温", "温度", "循环", "内阻",
    "健康状态", "soh", "soc", "充电", "放电",
}


def load_knowledge(path: Path = DEFAULT_KNOWLEDGE_PATH) -> list[dict[str, str]]:
    """Load small source-labelled chunks from JSON."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("知识文件最外层必须是列表")
    return value


def extract_terms(text: str) -> set[str]:
    """Extract explainable Chinese domain terms plus English word tokens."""

    lowered = text.lower()
    terms = {term for term in BATTERY_TERMS if term in lowered}
    terms.update(re.findall(r"[a-z0-9_]{2,}", lowered))
    return terms


def retrieve(
    query: str,
    *,
    documents: list[dict[str, str]] | None = None,
    top_k: int = 2,
) -> list[dict[str, Any]]:
    """Rank chunks by shared terms; zero-score chunks are not returned."""

    if top_k < 1:
        raise ValueError("top_k 必须大于等于 1")
    query_terms = extract_terms(query)
    candidates: list[dict[str, Any]] = []
    for document in documents if documents is not None else load_knowledge():
        score = len(query_terms & extract_terms(document["text"]))
        if score:
            candidates.append({**document, "score": score})
    candidates.sort(key=lambda item: (-item["score"], item["id"]))
    return candidates[:top_k]
