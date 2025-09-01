from __future__ import annotations
import csv, json, re
from pathlib import Path
from typing import Dict, List, Tuple

STATE_PATH = Path("state/rotation.json")
DATA_PATH = Path("data/hashtags.csv")

def _load_hashtags() -> Dict[str, List[str]]:
    tiers = {"broad": [], "mid": [], "niche": [], "local": []}
    with DATA_PATH.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            tag = row["tag"].strip()
            tier = row["tier"].strip().lower()
            if tier in tiers and tag and tag.startswith("#"):
                tiers[tier].append(tag)
    return tiers

def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {"broad": 0, "mid": 0, "niche": 0, "local": 0}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))

def _save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def _rotate_pick(arr: List[str], start: int, count: int) -> Tuple[List[str], int]:
    if not arr:
        return [], start
    out: List[str] = []
    i = start % len(arr)
    taken = 0
    used = set()
    while taken < min(count, len(arr)):
        if arr[i] not in used:
            out.append(arr[i]); used.add(arr[i]); taken += 1
        i = (i + 1) % len(arr)
    return out, i

def _pick_for_keywords(tier_tags: List[str], want_n: int, keywords: List[str]) -> Tuple[List[str], int]:
    if not keywords or not tier_tags:
        return [], want_n
    kw_re = re.compile("|".join(map(re.escape, keywords)), flags=re.IGNORECASE)
    matched = [t for t in tier_tags if kw_re.search(t)]
    seen = set(); matched_dedup = []
    for t in matched:
        if t not in seen:
            matched_dedup.append(t); seen.add(t)
    return matched_dedup[:want_n], max(0, want_n - len(matched_dedup))

def get_hashtag_set(broad_n=7, mid_n=7, niche_n=6, local_n=5, keywords: List[str] | None=None) -> Dict[str, List[str]]:
    tiers = _load_hashtags()
    state = _load_state()
    keywords = keywords or []
    picked = {"broad": [], "mid": [], "niche": [], "local": []}
    plan = [("broad", broad_n), ("mid", mid_n), ("niche", niche_n), ("local", local_n)]
    for name, need in plan:
        kw_hits, remaining = _pick_for_keywords(tiers[name], need, keywords)
        picked[name].extend(kw_hits)
        remaining_pool = [t for t in tiers[name] if t not in picked[name]]
        fill, state[name] = _rotate_pick(remaining_pool, state.get(name, 0), remaining)
        picked[name].extend(fill)
    _save_state(state)
    return picked

def flatten_hashtags(picked: Dict[str, List[str]]) -> List[str]:
    return picked["broad"] + picked["mid"] + picked["niche"] + picked["local"]
