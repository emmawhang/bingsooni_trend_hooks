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

import random

def generate_ai_powered_hooks(keywords: list[str], target_n=20) -> list[str]:
    """Generate hooks using AI-style patterns and web trends"""
    try:
        # Try to use AI generator if available
        from ai_generator import AIGenerator
        ai_gen = AIGenerator()
        ai_hooks = ai_gen.generate_ai_hooks(keywords, target_n=target_n)
        if ai_hooks and len(ai_hooks) >= target_n // 2:
            return ai_hooks[:target_n]
    except ImportError:
        print("AI generator not available, using enhanced local generation")
    
    # Enhanced local generation with AI-style patterns
    hooks, seen = [], set()
    
    # Trending social media patterns (updated regularly from web scraping)
    trending_patterns = [
        # Current viral patterns
        lambda kw: f"{kw} 이게 진짜 맛집이구나",
        lambda kw: f"도대체 {kw} 얼마나 맛있길래",
        lambda kw: f"{kw} 한 번 가면 단골됨",
        lambda kw: f"이 {kw} 때문에 살이 찌는 중",
        lambda kw: f"{kw} 예약 전쟁 이유 있었네",
        
        # Emotional discovery
        lambda kw: f"{kw}에서 감동받은 썰",
        lambda kw: f"내 인생 {kw} 원탑 등장",
        lambda kw: f"{kw} 때문에 다른 곳 못 감",
        lambda kw: f"왜 이제야 {kw} 알았을까",
        lambda kw: f"{kw} 처음 먹고 충격받음",
        
        # Social proof
        lambda kw: f"셰프도 인정한 {kw}",
        lambda kw: f"현지인만 아는 {kw} 발견",
        lambda kw: f"연예인도 줄 서는 {kw}",
        lambda kw: f"미식가들 사이에서 유명한 {kw}",
        lambda kw: f"입소문만으로 뜬 {kw}",
        
        # FOMO and urgency  
        lambda kw: f"{kw} 곧 예약 불가될 듯",
        lambda kw: f"이 {kw} 아는 사람만 안다",
        lambda kw: f"{kw} 지금 안 가면 후회",
        lambda kw: f"소문나기 전 {kw} 가자",
        lambda kw: f"{kw} 웨이팅 늘기 전에",
        
        # Authentic experience
        lambda kw: f"{kw} 진짜 맛의 차이",
        lambda kw: f"이런 {kw} 처음이야",
        lambda kw: f"{kw} 클래스가 다르네",
        lambda kw: f"평생 기억할 {kw}",
        lambda kw: f"{kw} 수준이 미쳤다",
    ]
    
    # Add web-scraped trending patterns
    try:
        from web_trends_scraper import integrate_web_trends_to_system
        web_trends = integrate_web_trends_to_system()
        for trend, score, source in web_trends[:10]:
            if score > 0.7:  # High confidence trends
                trend_clean = trend.replace('#', '').strip()
                trending_patterns.append(lambda kw, t=trend_clean: f"{kw} {t}")
    except ImportError:
        pass
    
    i = 0
    attempts = 0
    max_attempts = target_n * 30
    
    while len(hooks) < target_n and attempts < max_attempts:
        attempts += 1
        i += 1
        
        if not keywords:
            kw = "맛집"
        else:
            kw = keywords[(i - 1) % len(keywords)]
            
        pattern = random.choice(trending_patterns)
        text = _clean(pattern(kw))
        
        if not text:
            continue
            
        word_count = _wc(text)
        if 4 <= word_count <= 15 and text not in seen:
            # Avoid too similar hooks
            if not any(similar_hook in text or text in similar_hook for similar_hook in list(seen)[-5:]):
                hooks.append(text)
                seen.add(text)
    
    return hooks[:target_n]

def generate_truly_creative_hooks(keywords: list[str], target_n=20) -> list[str]:
    """Generate truly creative hooks using linguistic patterns and combinations"""
    hooks, seen = [], set()
    
    # Emotional triggers and descriptors
    emotions = ["감동", "놀라운", "충격적인", "미친", "대박", "환상적인", "완벽한", "절대적인"]
    intensifiers = ["진짜로", "정말로", "완전히", "극도로", "엄청나게", "심각하게", "무조건"]
    actions = ["발견했다", "찾았다", "알아냈다", "확인했다", "경험했다", "시도했다", "도전했다"]
    results = ["성공", "실패", "반전", "변화", "혁명", "돌파구", "해답", "비밀"]
    
    # Time/context markers
    time_contexts = ["오늘", "어제", "이번주", "요즘", "최근에", "방금", "드디어", "처음으로"]
    social_contexts = ["혼자서", "친구와", "가족과", "연인과", "동료와", "우연히", "계획적으로"]
    
    # Question starters and curiosity hooks
    question_starters = ["왜", "어떻게", "언제", "어디서", "누가", "무엇이"]
    curiosity_hooks = ["사실은", "알고보니", "놀랍게도", "의외로", "실제로는", "진실은"]
    
    # Personal story elements
    personal_elements = ["내가", "우리가", "모든 사람이", "아무도", "누구나", "처음 온 사람도"]
    
    def create_hook_variant(kw):
        variants = []
        
        # Emotional discovery pattern
        if random.choice([True, False]):
            emotion = random.choice(emotions)
            action = random.choice(actions)
            variants.append(f"{emotion} {kw} {action}")
            
        # Question-based curiosity
        if random.choice([True, False]):
            question = random.choice(question_starters)
            variants.append(f"{question} {kw}가 이렇게 좋은지 몰랐다")
            
        # Personal experience
        if random.choice([True, False]):
            personal = random.choice(personal_elements)
            time = random.choice(time_contexts)
            variants.append(f"{personal} {time} {kw}에서 놀란 이유")
            
        # Social proof with twist
        if random.choice([True, False]):
            curiosity = random.choice(curiosity_hooks)
            variants.append(f"{curiosity} {kw} 이게 정답이었다")
            
        # Problem-solution narrative
        if random.choice([True, False]):
            intensifier = random.choice(intensifiers)
            result = random.choice(results)
            variants.append(f"{kw} {intensifier} {result}인 이유")
            
        # Contrast/comparison
        if random.choice([True, False]):
            variants.append(f"{kw} vs 다른 곳, 차이가 심각했다")
            variants.append(f"모든 {kw} 가봤지만 여기가 다른 이유")
            
        # Time-sensitive urgency
        if random.choice([True, False]):
            social = random.choice(social_contexts)
            variants.append(f"{social} {kw} 가기 전 알았으면 좋았을 것")
            
        # Unexpected discovery
        if random.choice([True, False]):
            variants.append(f"우연히 찾은 {kw}, 인생이 바뀜")
            variants.append(f"{kw} 이런 곳이 있다니 믿기지 않음")
            
        return variants
    
    i = 0
    attempts = 0
    max_attempts = target_n * 20
    
    while len(hooks) < target_n and attempts < max_attempts:
        attempts += 1
        i += 1
        
        if not keywords:
            kw = "맛집"
        else:
            kw = keywords[(i - 1) % len(keywords)]
            
        # Generate multiple variants and pick randomly
        variants = create_hook_variant(kw)
        if variants:
            text = _clean(random.choice(variants))
            
            if not text:
                continue
                
            # Quality filters
            word_count = _wc(text)
            if 4 <= word_count <= 12 and text not in seen:
                # Additional creativity check - avoid too similar patterns
                if not any(similar_hook in text or text in similar_hook for similar_hook in list(seen)[-5:]):
                    hooks.append(text)
                    seen.add(text)
    
    return hooks[:target_n]

def generate_hooks(keywords: list[str], target_n=20, use_templates=True, use_ai=False) -> list[str]:
    """Generate hooks with option to use templates, creative generation, or AI"""
    if use_ai:
        return generate_ai_powered_hooks(keywords, target_n)
    elif not use_templates:
        return generate_truly_creative_hooks(keywords, target_n)
    
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

def optimize_hashtags_for_hook(hook: str, all_hashtags: list[str]) -> list[str]:
    """Select the most relevant hashtags for a specific hook"""
    optimized = []
    
    # Core hashtags that should always be included
    core_tags = ["#카페추천", "#travel", "#foodie", "#instafood", "#reels"]
    optimized.extend([tag for tag in core_tags if tag in all_hashtags])
    
    # Content-specific hashtags based on hook content
    hook_lower = hook.lower()
    
    # Location-based selection
    if "연남" in hook_lower:
        optimized.extend([tag for tag in all_hashtags if "연남" in tag or "yeonnam" in tag])
    if "성수" in hook_lower:
        optimized.extend([tag for tag in all_hashtags if "성수" in tag or "seongsu" in tag])
    if "서울" in hook_lower:
        optimized.extend([tag for tag in all_hashtags if "서울" in tag or "seoul" in tag])
    
    # Content-based selection
    if "빙수" in hook_lower:
        optimized.extend([tag for tag in all_hashtags if "빙수" in tag])
    if "카페" in hook_lower:
        optimized.extend([tag for tag in all_hashtags if "카페" in tag])
    if "맛집" in hook_lower:
        optimized.extend([tag for tag in all_hashtags if "맛집" in tag])
    
    # Experience-based selection
    if any(word in hook_lower for word in ["후기", "리뷰", "체험"]):
        optimized.extend([tag for tag in all_hashtags if any(exp in tag for exp in ["후기", "review", "체험"])])
    if any(word in hook_lower for word in ["가성비", "돈", "예산"]):
        optimized.extend([tag for tag in all_hashtags if any(val in tag for val in ["budget", "가성비"])])
    if any(word in hook_lower for word in ["숨은", "숨겨진", "비밀"]):
        optimized.extend([tag for tag in all_hashtags if any(hid in tag for hid in ["hidden", "숨은"])])
    
    # Add trending and general tags to fill remaining slots
    remaining_tags = [tag for tag in all_hashtags if tag not in optimized]
    optimized.extend(remaining_tags)
    
    # Remove duplicates while preserving order
    seen = set()
    final_optimized = []
    for tag in optimized:
        if tag not in seen:
            final_optimized.append(tag)
            seen.add(tag)
    
    return final_optimized[:20]  # Return top 20 most relevant hashtags

def save_outputs(hooks: list[str], hashtags: list[str], date_str: str):
    Path("outputs").mkdir(parents=True, exist_ok=True)
    csv_path = Path(f"outputs/{date_str}_hooks.csv")
    md_path  = Path(f"outputs/{date_str}_hooks.md")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["hook", "hashtags_joined", "optimized_hashtags"])
        for h in hooks:
            optimized_tags = optimize_hashtags_for_hook(h, hashtags)
            w.writerow([h, " ".join(hashtags), " ".join(optimized_tags)])
    with md_path.open("w", encoding="utf-8") as f:
        f.write("| # | Hook | Optimized Hashtags (top 10) |\n|---|---|---|\n")
        for idx, h in enumerate(hooks, 1):
            optimized_tags = optimize_hashtags_for_hook(h, hashtags)
            f.write(f"| {idx} | {h} | {' '.join(optimized_tags[:10])} |\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    ap.add_argument("--broad", type=int, default=7)
    ap.add_argument("--mid",   type=int, default=7)
    ap.add_argument("--niche", type=int, default=6)
    ap.add_argument("--local", type=int, default=5)
    ap.add_argument("--no-templates", action="store_true", 
                   help="Generate hooks without using predefined templates")
    ap.add_argument("--use-ai", action="store_true",
                   help="Use AI-powered generation with web trends")
    args = ap.parse_args()

    keywords = get_final_keywords()
    hooks = generate_hooks(keywords, target_n=20, use_templates=not args.no_templates, use_ai=args.use_ai)
    picked = get_hashtag_set(args.broad, args.mid, args.niche, args.local, keywords=keywords, hooks=hooks)
    hashtags = flatten_hashtags(picked)

    save_outputs(hooks, hashtags, args.date)
    print(f"Generated {len(hooks)} hooks and {len(hashtags)} hashtags → outputs/{args.date}_hooks.*")
    generation_mode = "AI-POWERED" if args.use_ai else ("CREATIVE" if args.no_templates else "TEMPLATE")
    print(f"Generation mode: {generation_mode}")

if __name__ == "__main__":
    main()
