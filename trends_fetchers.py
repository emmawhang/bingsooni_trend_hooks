from __future__ import annotations
from pathlib import Path
import csv

def fetch_pytrends_keywords() -> list[tuple[str, float]]:
    return [("빙수", 0.6), ("카페", 0.55), ("여름디저트", 0.5), ("서울맛집", 0.45), ("노포", 0.4)]

def fetch_reddit_keywords() -> list[tuple[str, float]]:
    return [("숨은맛집", 0.4), ("가성비맛집", 0.35), ("맛집팁", 0.3)]

def load_internal_keywords(path: str = "data/internal_keywords.csv") -> list[tuple[str, float]]:
    p = Path(path)
    if not p.exists():
        return []
    out: list[tuple[str, float]] = []
    with p.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                out.append((row["keyword"], float(row["score"])))
            except Exception:
                pass
    return out

def merge_keywords(
    internal: list[tuple[str, float]],
    external: list[tuple[str, float]],
    w_internal: float = 1.5,
    w_external: float = 1.3,
    top_n: int = 20,
) -> list[str]:
    from collections import defaultdict
    score = defaultdict(float)
    for k, s in external: score[k] += s * w_external
    for k, s in internal: score[k] += s * w_internal
    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)
    return [k for k, _ in ranked[:top_n]]

def get_final_keywords() -> list[str]:
    internal = load_internal_keywords()
    externals = fetch_pytrends_keywords() + fetch_reddit_keywords()
    return merge_keywords(internal, externals)
