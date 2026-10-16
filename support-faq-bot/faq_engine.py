"""Framework-agnostic FAQ engine using fuzzy matching (stdlib difflib)."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

_WORD = re.compile(r"[a-z0-9']+")


def normalize(text: str) -> str:
    return " ".join(_WORD.findall(text.lower()))


@dataclass(frozen=True)
class Match:
    question: str
    answer: str
    score: float


class FAQEngine:
    def __init__(self, entries: list[dict], threshold: float = 0.5):
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
        self.entries = [(normalize(e["question"]), e["question"], e["answer"]) for e in entries]
        self.threshold = threshold

    @classmethod
    def from_file(cls, path: str | Path, threshold: float = 0.5) -> "FAQEngine":
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f), threshold)

    @staticmethod
    def score(a: str, b: str) -> float:
        """Blend of character similarity and word overlap."""
        seq = SequenceMatcher(None, a, b).ratio()
        wa, wb = set(a.split()), set(b.split())
        overlap = len(wa & wb) / len(wa | wb) if wa | wb else 0.0
        return round(0.6 * seq + 0.4 * overlap, 4)

    def rank(self, query: str, limit: int = 3) -> list[Match]:
        q = normalize(query)
        if not q:
            return []
        scored = [Match(orig, ans, self.score(q, norm)) for norm, orig, ans in self.entries]
        return sorted(scored, key=lambda m: m.score, reverse=True)[:limit]

    def ask(self, query: str) -> Match | None:
        best = self.rank(query, 1)
        return best[0] if best and best[0].score >= self.threshold else None
