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
