#!/usr/bin/env bash
set -euo pipefail

# repo root
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pytrends pandas requests

mkdir -p data outputs state

# .gitignore
cat > .gitignore <<'EOF'
.venv/
__pycache__/
outputs/
state/
.DS_Store
EOF

# data files
cat > data/hashtags.csv <<'EOF'
tag,tier
#travel,broad
#foodie,broad
#카페추천,broad
#instafood,broad
#reels,broad
#koreanfood,mid
#맛집탐방,mid
#카페투어,mid
#yeonnamfood,mid
#seoulfood,mid
#빙수,niche
#hiddenrestaurant,niche
#budgeteats,niche
#줄서서먹는,niche
#연남카페,local
#성수카페,local
#seongsu,local
#yeonnam,local
EOF

cat > data/stopwords.txt <<'EOF'
단 1분만에
기적
100% 보장
의료
치료
성인
혐오
혐오표현
과장광고
EOF

cat > data/internal_keywords.csv <<'EOF'
keyword,score
빙수,0.9
연남,0.7
성수,0.6
카페,0.8
EOF

# trends_fetchers.py
cat > trends_fetchers.py <<'EOF'
from __future__ import annotations
from pathlib import Path
import csv

def fetch_pytrends_keywords() -> list[tuple[str, float]]:
    return [("빙수", 0.6), ("카페", 0.55), ("여름디저트", 0.5), ("서울맛집", 0.45), ("노포", 0.4)]

def fetch_reddit_keywords() -> list[tuple[str, float]]:
    return [("hidden gem", 0.4), ("budget eats", 0.35), ("line hacks", 0.3)]

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
EOF

# hashtags_manager.py
cat > hashtags_manager.py <<'EOF'
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
EOF

# hook_generator.py
cat > hook_generator.py <<'EOF'
from __future__ import annotations
import argparse, csv, re
from datetime import datetime
from pathlib import Path

from trends_fetchers import get_final_keywords
from hashtags_manager import get_hashtag_set, flatten_hashtags

STOPWORDS = set()
if Path("data/stopwords.txt").exists():
    STOPWORDS = set(
        line.strip() for line in Path("data/stopwords.txt").read_text(encoding="utf-8").splitlines() if line.strip()
    )

TEMPLATES = [
    "이거 {kw} 모르면 {alt} 놓친다",
    "{kw} 성지, 서울 말고 여기가 진짜야",
    "{num}번 먹고 알았다, {kw}는 이렇게 가자",
    "돈 아끼려면 {kw} 여기부터 저장",
    "줄 서는 이유 있음: {kw} 핵심만 정리",
    "{kw} 초보도 실패 없게: 체크리스트",
    "{kw} 대신 이 조합, 현지인 픽",
    "관광객 몰라요: {kw} 숨은 포인트 {num}개",
    "{kw} 가격대비 미쳤다, 동의하면 저장",
    "서울러도 모르는 {kw} 루트 공개",
]
ALT_WORDS = ["지갑", "여름", "주말", "점심", "퇴근길", "데이트", "비오는날"]
NUMS = ["3", "5", "7", "10"]

def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    for b in STOPWORDS:
        if b and b in text:
            return ""
    return text

def _wc(s: str) -> int:
    return len(s.split())

def generate_hooks(keywords: list[str], target_n=20) -> list[str]:
    hooks, seen = [], set()
    i = 0
    while len(hooks) < target_n and i < target_n * 5:
        i += 1
        kw = keywords[(i - 1) % max(1, len(keywords))] if keywords else "오늘의 맛집"
        tpl = TEMPLATES[i % len(TEMPLATES)]
        text = _clean(tpl.format(kw=kw, alt=ALT_WORDS[i % len(ALT_WORDS)], num=NUMS[i % len(NUMS)]))
        if not text:
            continue
        if 8 <= _wc(text) <= 14 and text not in seen:
            hooks.append(text); seen.add(text); continue
        alt = f"{text} | 저장 필수"
        if 8 <= _wc(alt) <= 14 and alt not in seen:
            hooks.append(alt); seen.add(alt)
    return hooks[:target_n]

def save_outputs(hooks: list[str], hashtags: list[str], date_str: str):
    Path("outputs").mkdir(parents=True, exist_ok=True)
    csv_path = Path(f"outputs/{date_str}_hooks.csv")
    md_path  = Path(f"outputs/{date_str}_hooks.md")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["hook", "hashtags_joined"])
        for h in hooks:
            w.writerow([h, " ".join(hashtags)])
    with md_path.open("w", encoding="utf-8") as f:
        f.write("| # | Hook | Hashtags (excerpt) |\n|---|---|---|\n")
        for idx, h in enumerate(hooks, 1):
            f.write(f"| {idx} | {h} | {' '.join(hashtags[:10])} |\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    ap.add_argument("--broad", type=int, default=7)
    ap.add_argument("--mid",   type=int, default=7)
    ap.add_argument("--niche", type=int, default=6)
    ap.add_argument("--local", type=int, default=5)
    args = ap.parse_args()

    keywords = get_final_keywords()
    hooks = generate_hooks(keywords, target_n=20)
    picked = get_hashtag_set(args.broad, args.mid, args.niche, args.local, keywords=keywords)
    hashtags = flatten_hashtags(picked)

    save_outputs(hooks, hashtags, args.date)
    print(f"Generated {len(hooks)} hooks and {len(hashtags)} hashtags → outputs/{args.date}_hooks.*")

if __name__ == "__main__":
    main()
EOF

# git init (quiet)
git init >/dev/null 2>&1 || true
git add .
git commit -m "scaffold: initial files" >/dev/null 2>&1 || true

# first dry run
python hook_generator.py --date "$(date +%Y%m%d)"
echo "Done. See outputs/ and state/rotation.json"
