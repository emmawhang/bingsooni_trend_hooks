#!/usr/bin/env python3
"""
Test script to compare simulation vs real-time data collection
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append(str(Path(__file__).parent / "src"))

def test_current_system():
    """Test the current trend collection system"""
    print("🔍 Testing Current Trend Collection System\n")
    
    try:
        from bingsooni.fetchers.trends_fetchers import get_final_keywords, fetch_pytrends_keywords, fetch_reddit_keywords
        from bingsooni.fetchers.web_trends_scraper import integrate_web_trends_to_system
        
        print("1️⃣ **Google Trends Keywords:**")
        pytrends_data = fetch_pytrends_keywords()
        for keyword, score in pytrends_data:
            status = "🔴 SIMULATION" if score in [0.6, 0.55, 0.5, 0.45, 0.4] else "✅ REAL DATA"
            print(f"   {keyword:<15} (score: {score:.2f}) {status}")
        
        print("\n2️⃣ **Reddit Keywords:**")
        reddit_data = fetch_reddit_keywords()
        for keyword, score in reddit_data:
            status = "🔴 SIMULATION" if score in [0.4, 0.35, 0.3] else "✅ REAL DATA"
            print(f"   {keyword:<15} (score: {score:.2f}) {status}")
        
        print("\n3️⃣ **Final Merged Keywords:**")
        final_keywords = get_final_keywords()
        for i, keyword in enumerate(final_keywords, 1):
            print(f"   {i:2d}. {keyword}")
        
        print("\n4️⃣ **Web Trends Integration:**")
        try:
            web_trends = integrate_web_trends_to_system()
            for i, (trend, score, source) in enumerate(web_trends[:5], 1):
                status = "✅ REAL" if source in ['google_trends', 'naver_api'] else "🔴 SIMULATION"
                print(f"   {i}. {trend:<20} ({score:.2f}) from {source} {status}")
        except Exception as e:
            print(f"   ⚠️  Web trends error: {e}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")

def check_api_status():
    """Check which APIs are configured"""
    print("\n🔑 API Configuration Status:\n")
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    apis = {
        "Google Trends": ("pytrends", "No API key needed"),
        "Naver Search": ("NAVER_CLIENT_ID", os.getenv('NAVER_CLIENT_ID')),
        "Reddit": ("REDDIT_CLIENT_ID", os.getenv('REDDIT_CLIENT_ID')), 
        "Instagram": ("INSTAGRAM_ACCESS_TOKEN", os.getenv('INSTAGRAM_ACCESS_TOKEN')),
        "YouTube": ("YOUTUBE_API_KEY", os.getenv('YOUTUBE_API_KEY')),
        "OpenAI": ("OPENAI_API_KEY", os.getenv('OPENAI_API_KEY'))
    }
    
    for service, (key, value) in apis.items():
        if key == "pytrends":
            try:
                import pytrends
                status = "✅ AVAILABLE"
            except ImportError:
                status = "❌ NOT INSTALLED (pip install pytrends)"
        else:
            status = "✅ CONFIGURED" if value else "🔴 NOT CONFIGURED"
        
        print(f"   {service:<15}: {status}")

def test_real_vs_simulation():
    """Show the difference between real and simulation data"""
    print("\n📊 Real vs Simulation Data Comparison:\n")
    
    print("🔴 **CURRENT SIMULATION DATA:**")
    print("   - Same keywords every time: 빙수, 카페, 여름디저트")
    print("   - Fixed scores: 0.6, 0.55, 0.5")
    print("   - No trending adaptation")
    print("   - Static hashtag patterns")
    
    print("\n✅ **WITH REAL-TIME DATA:**")
    print("   - Dynamic keywords based on actual searches")
    print("   - Scores reflect real popularity")
    print("   - Seasonal trend adaptation")
    print("   - Trending hashtags from actual Instagram posts")
    print("   - Location-based trending (연남동, 성수동, etc.)")

def show_next_steps():
    """Show how to enable real-time data"""
    print("\n🚀 How to Enable Real-Time Data:\n")
    
    print("**Quick Start (Google Trends only - FREE):**")
    print("   1. pip install pytrends")
    print("   2. Run hook generator - will automatically use real trends!")
    
    print("\n**Full Setup (All sources):**")
    print("   1. Read: docs/REAL_TIME_DATA_SETUP.md")
    print("   2. Get API keys from Naver, Reddit, Instagram")
    print("   3. Configure .env file")
    print("   4. Run: python src/bingsooni/hook_generator.py --use-ai")
    
    print("\n**Test individual components:**")
    print("   - Google: python -c \"from src.bingsooni.fetchers.trends_fetchers import fetch_pytrends_keywords; print(fetch_pytrends_keywords())\"")
    print("   - Web trends: python src/bingsooni/fetchers/web_trends_scraper.py")

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 BINGSOONI TREND COLLECTION ANALYSIS")
    print("=" * 60)
    
    test_current_system()
    check_api_status()
    test_real_vs_simulation()
    show_next_steps()
    
    print("\n" + "=" * 60)
    print("📖 For detailed setup instructions, see:")
    print("   docs/REAL_TIME_DATA_SETUP.md")
    print("=" * 60)
