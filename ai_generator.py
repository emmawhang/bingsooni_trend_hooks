#!/usr/bin/env python3
"""
AI-powered hook and hashtag generation using LLM APIs
"""

from openai import OpenAI
import json
import os
from typing import List, Dict
import random
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIGenerator:
    def __init__(self, api_key: str = None):
        # Initialize OpenAI client (you can also use other LLM APIs)
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
        
    def generate_ai_hooks(self, keywords: List[str], context: str = "Korean food and cafe content", target_n: int = 20) -> List[str]:
        """Generate hooks using AI/LLM"""
        
        if not self.api_key or not self.client:
            # Fallback to rule-based generation with AI-style patterns
            return self._generate_ai_style_hooks_locally(keywords, target_n)
        
        try:
            # Create a comprehensive prompt for hook generation
            prompt = f"""
            Generate {target_n} engaging Korean social media hooks about {', '.join(keywords[:5])}.
            
            Context: {context}
            
            Requirements:
            - Write in Korean
            - Each hook should be 4-12 words
            - Use emotional triggers and curiosity gaps
            - Include trending social media language
            - Make them feel authentic and shareable
            - Avoid repetitive patterns
            
            Style examples:
            - "이거 모르면 진짜 손해"
            - "알고보니 여기가 맛집이었다"
            - "MZ가 열광하는 이유 있었네"
            
            Keywords to incorporate: {', '.join(keywords)}
            
            Return only the hooks, one per line:
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.8
            )
            
            hooks = response.choices[0].message.content.strip().split('\n')
            return [hook.strip() for hook in hooks if hook.strip()][:target_n]
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_ai_style_hooks_locally(keywords, target_n)
    
    def _generate_ai_style_hooks_locally(self, keywords: List[str], target_n: int) -> List[str]:
        """Generate AI-style hooks locally without API"""
        
        # AI-inspired patterns with more natural language flow
        patterns = [
            # Emotional revelations
            lambda kw: f"{kw} 이렇게 감동적일 줄 몰랐다",
            lambda kw: f"왜 {kw}에 이제야 왔을까",
            lambda kw: f"{kw} 때문에 인생이 바뀜",
            
            # Social proof with authenticity
            lambda kw: f"로컬들이 진짜 가는 {kw}",
            lambda kw: f"셰프가 인정한 {kw}",
            lambda kw: f"연예인도 몰래 가는 {kw}",
            
            # FOMO with urgency
            lambda kw: f"{kw} 지금 안 가면 후회",
            lambda kw: f"이 {kw} 곧 유명해질 듯",
            lambda kw: f"{kw} 예약 안 되기 전에",
            
            # Personal discovery
            lambda kw: f"우연히 발견한 {kw}의 비밀",
            lambda kw: f"{kw}에서 일어난 기적",
            lambda kw: f"내 인생 {kw} 원탑 발견",
            
            # Comparison and contrast
            lambda kw: f"다른 {kw}와 차원이 다름",
            lambda kw: f"{kw} 클래스가 다르네",
            lambda kw: f"이게 진짜 {kw}구나",
            
            # Question-based curiosity
            lambda kw: f"{kw} 이렇게 맛있어도 되나",
            lambda kw: f"어떻게 {kw}가 이렇게 완벽해",
            lambda kw: f"왜 다들 이 {kw} 모를까",
        ]
        
        hooks = []
        seen = set()
        
        for _ in range(target_n * 3):  # Generate more than needed
            kw = random.choice(keywords) if keywords else "맛집"
            pattern = random.choice(patterns)
            hook = pattern(kw)
            
            if hook not in seen and len(hook.split()) <= 12:
                hooks.append(hook)
                seen.add(hook)
                
            if len(hooks) >= target_n:
                break
                
        return hooks[:target_n]
    
    def generate_ai_hashtags(self, keywords: List[str], hooks: List[str], target_n: int = 25) -> List[str]:
        """Generate hashtags using AI/LLM"""
        
        if not self.api_key or not self.client:
            return self._generate_ai_style_hashtags_locally(keywords, hooks, target_n)
        
        try:
            prompt = f"""
            Generate {target_n} trending Korean hashtags for social media posts about {', '.join(keywords[:3])}.
            
            Context: Korean food, cafe, and lifestyle content
            Hooks for reference: {'; '.join(hooks[:5])}
            
            Requirements:
            - Mix Korean and English naturally
            - Include location-specific tags
            - Use current social media slang
            - Create unique combinations
            - Make them searchable and trendy
            
            Style examples:
            - #서울맛집헌터
            - #감성카페탐방
            - #MZ맛집인정
            - #인생샷명소
            
            Return only hashtags starting with #, one per line:
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.9
            )
            
            hashtags = response.choices[0].message.content.strip().split('\n')
            return [tag.strip() for tag in hashtags if tag.strip().startswith('#')][:target_n]
            
        except Exception as e:
            print(f"AI hashtag generation failed: {e}")
            return self._generate_ai_style_hashtags_locally(keywords, hooks, target_n)
    
    def _generate_ai_style_hashtags_locally(self, keywords: List[str], hooks: List[str], target_n: int) -> List[str]:
        """Generate AI-style hashtags locally"""
        
        # AI-inspired hashtag components
        prefixes = ["진짜", "완벽한", "숨은", "찐", "레알", "갓", "킹", "퀸"]
        suffixes = ["러버", "홀릭", "헌터", "마스터", "킹", "퀸", "스타"]
        contexts = ["라이프", "바이브", "무드", "스타일", "씬", "컬처"]
        actions = ["탐방", "투어", "체크", "클리어", "정복", "챌린지"]
        
        hashtags = []
        seen = set()
        
        # Generate from keywords
        for kw in keywords:
            clean_kw = kw.replace(' ', '').replace('과', '').replace('와', '')
            
            combinations = [
                f"#{random.choice(prefixes)}{clean_kw}",
                f"#{clean_kw}{random.choice(suffixes)}",
                f"#{clean_kw}{random.choice(actions)}",
                f"#{clean_kw}{random.choice(contexts)}",
                f"#{clean_kw}인정",
                f"#{clean_kw}맛집",
                f"#{clean_kw}체험단"
            ]
            
            for combo in combinations:
                if combo not in seen:
                    hashtags.append(combo)
                    seen.add(combo)
        
        # Generate from hook words
        for hook in hooks[:5]:
            words = hook.split()
            for word in words:
                if len(word) > 1:
                    clean_word = word.replace('가', '').replace('를', '').replace('을', '')
                    if len(clean_word) > 1:
                        combo = f"#{clean_word}{random.choice(contexts)}"
                        if combo not in seen:
                            hashtags.append(combo)
                            seen.add(combo)
        
        # Add trendy generic hashtags
        trendy_hashtags = [
            "#감성오버로드", "#인생샷명소", "#MZ인정", "#서울핫플레이스",
            "#가성비갑", "#힙플레이스탐방", "#맛집헌터", "#카페홀릭",
            "#데일리맛집", "#서울라이프", "#푸드스타그램", "#맛스타그램"
        ]
        
        hashtags.extend(trendy_hashtags)
        
        # Remove duplicates and return
        final_hashtags = []
        for tag in hashtags:
            if tag not in seen and len(tag) > 3:
                final_hashtags.append(tag)
                seen.add(tag)
                
        return final_hashtags[:target_n]

# Integration function
def create_ai_powered_generator():
    """Create an AI-powered version of the hook generator"""
    return AIGenerator()

if __name__ == "__main__":
    # Test the AI generator
    ai_gen = AIGenerator()
    
    test_keywords = ["카페", "아이스크림", "와인", "디저트"]
    
    print("🤖 AI-Generated Hooks:")
    hooks = ai_gen.generate_ai_hooks(test_keywords, target_n=10)
    for i, hook in enumerate(hooks, 1):
        print(f"{i:2d}. {hook}")
    
    print("\n🔥 AI-Generated Hashtags:")
    hashtags = ai_gen.generate_ai_hashtags(test_keywords, hooks, target_n=15)
    for i, tag in enumerate(hashtags, 1):
        print(f"{i:2d}. {tag}")
