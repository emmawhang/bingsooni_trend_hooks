#!/usr/bin/env python3
"""
Web scraping module for fetching trending hashtags and keywords from various sources
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time
import random
from typing import List, Dict, Tuple
from urllib.parse import urljoin
import json

class TrendsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_instagram_hashtags(self, keywords: List[str]) -> List[Tuple[str, float]]:
        """Scrape trending hashtags from Instagram-related sources"""
        trending_hashtags = []
        
        # Simulate trending hashtags based on keywords (since Instagram API requires auth)
        # In real implementation, you'd use Instagram Basic Display API or third-party services
        base_trends = [
            "맛스타그램", "foodstagram", "카페스타그램", "dessertgram", "Seoul맛집",
            "힙플레이스", "데일리카페", "서울카페", "인스타핫플", "감성카페"
        ]
        
        for keyword in keywords:
            # Generate contextual hashtags
            trending_hashtags.extend([
                (f"#{keyword}스타그램", 0.8),
                (f"#{keyword}추천", 0.7),
                (f"#{keyword}맛집", 0.9),
                (f"#{keyword}데일리", 0.6)
            ])
        
        # Add base trending hashtags
        for hashtag in base_trends:
            trending_hashtags.append((f"#{hashtag}", random.uniform(0.5, 0.9)))
            
        return trending_hashtags[:15]

    def scrape_naver_blog_trends(self) -> List[Tuple[str, float]]:
        """Scrape trending keywords from Naver Blog using real API"""
        try:
            # Use Naver Search API
            client_id = os.getenv('NAVER_CLIENT_ID')
            client_secret = os.getenv('NAVER_CLIENT_SECRET')
            
            if not all([client_id, client_secret]):
                print("⚠️  Naver API credentials not configured")
                return self._fallback_naver_trends()
            
            headers = {
                'X-Naver-Client-Id': client_id,
                'X-Naver-Client-Secret': client_secret,
                'User-Agent': self.headers['User-Agent']
            }
            
            trending_keywords = []
            
            # Search for trending food/cafe posts
            search_terms = ["서울맛집", "카페추천", "디저트맛집", "빙수추천", "핫플레이스"]
            
            for term in search_terms:
                url = "https://openapi.naver.com/v1/search/blog.json"
                params = {
                    'query': term,
                    'display': 20,
                    'sort': 'date'  # Most recent posts
                }
                
                response = self.session.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract keywords from blog titles and descriptions
                    for item in data.get('items', []):
                        title = item.get('title', '')
                        description = item.get('description', '')
                        
                        # Clean HTML tags
                        import re
                        title = re.sub('<[^<]+?>', '', title)
                        description = re.sub('<[^<]+?>', '', description)
                        
                        # Extract relevant keywords
                        text = f"{title} {description}".lower()
                        
                        # Score based on how recent and relevant the post is
                        score = 0.7 + (len(data['items']) - data['items'].index(item)) * 0.01
                        
                        # Add location-based trends
                        if any(loc in text for loc in ['연남', '성수', '홍대', '강남']):
                            location_kw = next(loc for loc in ['연남', '성수', '홍대', '강남'] if loc in text)
                            trending_keywords.append((f"{location_kw}맛집", min(score + 0.1, 1.0)))
                        
                        # Add content-based trends  
                        if any(food in text for food in ['빙수', '카페', '디저트']):
                            food_kw = next(food for food in ['빙수', '카페', '디저트'] if food in text)
                            trending_keywords.append((f"{food_kw}추천", score))
                
                time.sleep(0.1)  # Rate limiting
            
            return trending_keywords if trending_keywords else self._fallback_naver_trends()
            
        except Exception as e:
            print(f"Error scraping Naver trends: {e}")
            return self._fallback_naver_trends()
    
    def _fallback_naver_trends(self) -> List[Tuple[str, float]]:
        """Fallback data when Naver API is unavailable"""
        return [
            ("서울핫플", 0.85), ("감성카페", 0.82), ("인생샷맛집", 0.78),
            ("MZ추천", 0.75), ("숨은맛집", 0.73), ("가성비카페", 0.70),
            ("데이트코스", 0.68), ("주말나들이", 0.65)
        ]

    def scrape_google_trends_korea(self, keywords: List[str]) -> List[Tuple[str, float]]:
        """Fetch trending searches related to Korean food/cafe topics"""
        # This would integrate with Google Trends API in real implementation
        # For now, simulating trending terms
        korean_food_trends = [
            ("연남동카페", 0.88),
            ("성수동맛집", 0.85),
            ("홍대디저트", 0.82),
            ("강남카페", 0.78),
            ("이태원맛집", 0.75),
            ("망원동카페", 0.72),
            ("서촌맛집", 0.70),
            ("신사동카페", 0.68)
        ]
        
        return korean_food_trends

    def scrape_youtube_trending_titles(self) -> List[str]:
        """Scrape trending video titles for hook inspiration"""
        # This would use YouTube Data API in real implementation
        trending_patterns = [
            "이거 모르면 손해",
            "진짜 맛있는 곳 찾았다",
            "서울 숨은 맛집 대공개",
            "MZ세대가 열광하는",
            "인생 카페 발견",
            "가성비 끝판왕",
            "현지인만 아는 비밀",
            "줄 서서 먹을 가치 있나",
            "솔직 후기만 모음",
            "이 조합 미쳤다"
        ]
        
        return trending_patterns

    def get_all_trends(self, keywords: List[str]) -> Dict[str, List[Tuple[str, float]]]:
        """Fetch all trending data from various sources"""
        trends = {
            'instagram_hashtags': self.scrape_instagram_hashtags(keywords),
            'naver_trends': self.scrape_naver_blog_trends(),
            'google_trends': self.scrape_google_trends_korea(keywords),
            'youtube_patterns': [(pattern, 0.8) for pattern in self.scrape_youtube_trending_titles()]
        }
        
        return trends

def integrate_web_trends_to_system():
    """Integration function to fetch and merge web trends with existing system"""
    scraper = TrendsScraper()
    
    # Get base keywords from existing system
    from trends_fetchers import get_final_keywords
    base_keywords = get_final_keywords()
    
    # Fetch web trends
    web_trends = scraper.get_all_trends(base_keywords)
    
    # Merge and rank all trends
    all_trends = []
    for source, trends in web_trends.items():
        for trend, score in trends:
            all_trends.append((trend, score, source))
    
    # Sort by score and return top trends
    all_trends.sort(key=lambda x: x[1], reverse=True)
    return all_trends[:30]

if __name__ == "__main__":
    trends = integrate_web_trends_to_system()
    print("🔥 Top Trending Terms:")
    for i, (trend, score, source) in enumerate(trends[:10], 1):
        print(f"{i:2d}. {trend:<20} ({score:.2f}) from {source}")
