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

import random

def _generate_truly_creative_hashtags(keywords: List[str], hooks: List[str] = None) -> List[str]:
    """Generate truly creative hashtags using AI-style combinations"""
    creative_tags = []
    
    # Emotional and descriptive components
    emotions = ["감동", "놀라운", "완벽한", "미친", "대박", "환상적인", "극한", "절대"]
    descriptors = ["핫", "힙", "트렌디", "감성", "빈티지", "모던", "클래식", "유니크"]
    experiences = ["체험", "여행", "탐험", "발견", "모험", "힐링", "휴식", "즐거움"]
    qualities = ["꿀", "진짜", "찐", "레알", "개꿀", "갓", "킹", "퀸"]
    
    # Content types and contexts
    content_types = ["플레이스", "스팟", "존", "라이프", "스타일", "바이브", "무드", "씬"]
    social_contexts = ["솔로", "커플", "친구", "가족", "데이트", "모임", "파티", "셀카"]
    time_contexts = ["주말", "평일", "저녁", "아침", "점심", "새벽", "밤", "오후"]
    
    # Action words and outcomes
    actions = ["탐방", "투어", "호핑", "체크", "클리어", "정복", "도전", "시도"]
    outcomes = ["성공", "만족", "행복", "감동", "놀람", "즐거움", "힐링", "추억"]
    
    def create_creative_combinations():
        combinations = []
        
        # Emotion + Content combinations
        for emotion in emotions[:5]:
            for content in content_types[:4]:
                combinations.append(f"#{emotion}{content}")
                
        # Quality + Action combinations
        for quality in qualities[:4]:
            for action in actions[:4]:
                combinations.append(f"#{quality}{action}")
                
        # Descriptor + Experience combinations
        for desc in descriptors[:5]:
            for exp in experiences[:4]:
                combinations.append(f"#{desc}{exp}")
                
        # Social + Time context combinations
        for social in social_contexts[:4]:
            for time in time_contexts[:3]:
                combinations.append(f"#{social}{time}")
                
        # Keyword-based creative combinations
        for kw in keywords[:5]:
            # Clean keyword (remove spaces, special chars)
            clean_kw = re.sub(r'[^가-힣a-zA-Z]', '', kw)
            if clean_kw:
                combinations.extend([
                    f"#{clean_kw}{random.choice(descriptors)}",
                    f"#{random.choice(qualities)}{clean_kw}",
                    f"#{clean_kw}{random.choice(actions)}",
                    f"#{random.choice(emotions)}{clean_kw}",
                ])
        
        # Hook-inspired hashtags
        if hooks:
            for hook in hooks[:3]:
                words = hook.split()
                for word in words:
                    clean_word = re.sub(r'[^가-힣a-zA-Z]', '', word)
                    if len(clean_word) > 1:
                        combinations.extend([
                            f"#{clean_word}{random.choice(content_types)}",
                            f"#{random.choice(descriptors)}{clean_word}",
                        ])
        
        return combinations
    
    # Generate creative combinations
    all_combinations = create_creative_combinations()
    
    # Add some truly unique generative hashtags
    unique_patterns = [
        f"#{random.choice(['서울', '강남', '홍대'])}{random.choice(['러버', '홀릭', '키드', '걸'])}",
        f"#{random.choice(['맛집', '카페', '디저트'])}{random.choice(['헌터', '마스터', '킹', '퀸'])}",
        f"#{random.choice(['힙', '핫', '쿨'])}{random.choice(['플레이스', '스팟', '존'])}",
        f"#{random.choice(['감성', '빈티지', '모던'])}{random.choice(['라이프', '바이브', '무드'])}",
        f"#{random.choice(['꿀', '개꿀', '갓'])}{random.choice(['맛집', '카페', '디저트'])}",
    ]
    
    # Combine all and remove duplicates
    all_creative = all_combinations + unique_patterns
    seen = set()
    for tag in all_creative:
        if tag not in seen and len(tag) > 3 and len(tag) < 15:
            creative_tags.append(tag)
            seen.add(tag)
    
    # Shuffle for randomness
    random.shuffle(creative_tags)
    return creative_tags[:20]

def _generate_dynamic_hashtags(keywords: List[str]) -> List[str]:
    """Generate dynamic hashtags based on current keywords and trends"""
    dynamic_tags = []
    
    # Base trending hashtags for food/cafe content
    trending_base = [
        "#트렌드맛집", "#힙플레이스", "#맛스타그램", "#foodstagram", 
        "#데일리카페", "#카페스타그램", "#서울핫플", "#맛집추천",
        "#푸드트립", "#맛집투어", "#카페호핑", "#foodlover"
    ]
    
    # Seasonal and contextual hashtags
    seasonal_tags = [
        "#여름간식", "#시원한디저트", "#무더위탈출", "#여름카페",
        "#아이스크림", "#빙수맛집", "#시원달달", "#여름휴가"
    ]
    
    # Experience-based hashtags
    experience_tags = [
        "#솔직후기", "#진짜맛집", "#찐추천", "#가성비갑", 
        "#숨은맛집", "#현지맛집", "#핫플인정", "#맛집인증"
    ]
    
    # Location-based dynamic tags
    location_tags = []
    for kw in keywords:
        if any(area in kw.lower() for area in ['연남', '성수', '홍대', '강남', '서울']):
            location_tags.extend([f"#{kw}맛집", f"#{kw}카페", f"#{kw}핫플"])
    
    # Content-type dynamic tags
    content_tags = []
    for kw in keywords:
        if any(food in kw.lower() for food in ['빙수', '디저트', '카페', '맛집']):
            content_tags.extend([f"#{kw}추천", f"#{kw}리뷰", f"#{kw}탐방"])
    
    # Combine all dynamic tags
    all_dynamic = trending_base + seasonal_tags + experience_tags + location_tags + content_tags
    
    # Remove duplicates and return
    seen = set()
    for tag in all_dynamic:
        if tag not in seen and len(tag) > 1:
            dynamic_tags.append(tag)
            seen.add(tag)
    
    return dynamic_tags[:15]  # Return top 15 dynamic hashtags

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

def get_hashtag_set(broad_n=7, mid_n=7, niche_n=6, local_n=5, keywords: List[str] | None=None, hooks: List[str] | None=None) -> Dict[str, List[str]]:
    tiers = _load_hashtags()
    state = _load_state()
    keywords = keywords or []
    hooks = hooks or []
    picked = {"broad": [], "mid": [], "niche": [], "local": []}
    
    # Check if we should update hashtags from Instagram trends
    try:
        from instagram_hashtag_updater import InstagramHashtagUpdater
        updater = InstagramHashtagUpdater()
        
        # Check if we need daily update (if state file is old)
        import datetime
        if STATE_PATH.exists():
            last_modified = datetime.datetime.fromtimestamp(STATE_PATH.stat().st_mtime)
            if (datetime.datetime.now() - last_modified).days >= 1:
                print("🔄 Running daily hashtag trend update...")
                updater.run_daily_update()
                # Reload hashtags after update
                tiers = _load_hashtags()
    except ImportError:
        print("📱 Instagram updater not available")
    
    # Try to use AI generator for hashtags if available
    ai_hashtags = []
    try:
        from ai_generator import AIGenerator
        ai_gen = AIGenerator()
        ai_hashtags = ai_gen.generate_ai_hashtags(keywords, hooks, target_n=15)
        print(f"🤖 Generated {len(ai_hashtags)} AI hashtags")
    except ImportError:
        print("💡 AI generator not available, using creative generation")
    
    # Generate truly creative hashtags based on keywords and hooks
    creative_hashtags = _generate_truly_creative_hashtags(keywords, hooks)
    
    # Also generate some dynamic hashtags for variety
    dynamic_hashtags = _generate_dynamic_hashtags(keywords)
    
    # Combine AI, creative and dynamic hashtags
    all_generated = ai_hashtags + creative_hashtags + dynamic_hashtags
    
    # Add generated hashtags to appropriate tiers
    tiers["broad"].extend(all_generated[:8])    # Add top 8 to broad
    tiers["mid"].extend(all_generated[8:16])    # Add next 8 to mid  
    tiers["niche"].extend(all_generated[16:24]) # Add next 8 to niche
    tiers["local"].extend(all_generated[24:])   # Add remaining to local
    
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
