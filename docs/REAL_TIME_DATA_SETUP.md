# 🔴 Real-Time Data Collection Setup Guide

## Current Status: SIMULATION MODE ⚠️

Your system is currently using **simulated/mock data** instead of real-time trends. Here's how to enable actual data collection from Instagram, Naver, Google Trends, and other sources.

---

## 🚀 Step 1: Install Real API Dependencies

```bash
# Install additional packages for real-time data
pip install pytrends selenium

# Or update all requirements
pip install -r requirements.txt
```

---

## 🔑 Step 2: Get API Credentials

### **Google Trends (Free)**
- ✅ **No API key needed** - pytrends works directly
- Used for: Korean food/cafe trending searches

### **Naver Search API**
1. Go to https://developers.naver.com/
2. Register an application
3. Get `Client ID` and `Client Secret`
4. Used for: Blog trends, local restaurant mentions

### **Instagram Basic Display API**
1. Go to https://developers.facebook.com/apps/
2. Create Facebook app → Add Instagram Basic Display
3. Get `access_token`
4. Used for: Hashtag trends, location-based posts

### **YouTube Data API**
1. Go to https://console.developers.google.com/
2. Enable YouTube Data API v3
3. Get API key
4. Used for: Trending video titles for hook patterns

---

## 🔧 Step 3: Configure Environment Variables

Create `.env` file in project root:

```bash
# Copy the example file
cp docs/.env.example .env
```

Edit `.env` with your actual credentials:

```bash
# Real-time data APIs
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here

INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Optional: AI APIs
OPENAI_API_KEY=your_openai_api_key_here

# Rate limiting
REQUEST_DELAY=1.0
MAX_RETRIES=3
```

---

## 📊 Step 4: Verify Real Data Collection

### Test Google Trends (Works Immediately)
```bash
python -c "
from src.bingsooni.fetchers.trends_fetchers import fetch_pytrends_keywords
print('Google Trends:', fetch_pytrends_keywords())
"
```

### Test All Sources
```bash
python src/bingsooni/fetchers/web_trends_scraper.py
```

Expected output with real data:
```
🔥 Top Trending Terms:
 1. 연남동카페           (0.88) from google_trends
 2. #서울맛집           (0.85) from instagram_hashtags  
 3. 성수동맛집           (0.82) from naver_trends
 4. 이거 모르면 손해     (0.80) from youtube_patterns
```

---

## 🎯 What Changes When Real Data Is Enabled

### **Before (Simulation)**
```python
# Always returns the same mock data
fetch_pytrends_keywords() 
# → [("빙수", 0.6), ("카페", 0.55)]  # STATIC

fetch_naver_blog_keywords()
# → [("숨은맛집", 0.4), ("가성비맛집", 0.35)]  # STATIC
```

### **After (Real Data)**
```python
# Returns actual trending searches from Google Trends
fetch_pytrends_keywords()
# → [("성수동카페", 0.8), ("연남동빙수", 0.7)]  # DYNAMIC

# Returns trending keywords from actual Naver blog posts
fetch_naver_blog_keywords()
# → [("연남동카페", 0.85), ("성수동맛집", 0.75)]  # DYNAMIC
```

### **Hook Generation Impact**
- **Simulation**: Uses same keywords every time
- **Real Data**: Adapts to actual trending topics daily

### **Hashtag Generation Impact**  
- **Simulation**: Static hashtag combinations
- **Real Data**: Trending hashtags from actual Instagram posts

---

## 🔍 Data Sources Breakdown

| Source | Data Type | API Required | Real-Time? |
|--------|-----------|--------------|------------|
| **Google Trends** | Search volumes | ❌ No | ✅ Yes |
| **Naver Blogs** | Post mentions | ✅ Yes | ✅ Yes |
| **Instagram** | Hashtag trends | ✅ Yes | ✅ Yes |
| **YouTube** | Video titles | ✅ Yes | ✅ Yes |

---

## ⚡ Quick Enable (Minimal Setup)

If you only want to enable **Google Trends** (no API key needed):

1. Install pytrends: `pip install pytrends`
2. Run: `python src/bingsooni/hook_generator.py --use-ai`
3. ✅ You'll now get real Korean trending searches!

---

## 🚨 Current Fallback System

The system is designed to **gracefully degrade**:

1. **Try real API** → If credentials available
2. **Fallback to simulation** → If API fails
3. **Show warning message** → So you know what's happening

Example output:
```
⚠️  Naver API credentials not configured
✅ Using Google Trends real data
💡 AI generator not available, using creative generation
Generated 20 hooks and 28 hashtags → outputs/20250905_hooks.*
Generation mode: CREATIVE
```

---

## 🎉 Benefits of Real-Time Data

- **Trending Topics**: Hooks about actually viral content
- **Seasonal Relevance**: Summer drinks vs winter foods automatically
- **Local Trends**: Specific Seoul neighborhoods gaining popularity  
- **Fresh Hashtags**: Tags people are actually using today
- **Competitive Edge**: Content aligned with current social media trends

Your content will be **10x more relevant** when using real-time data! 🚀

---

## 🔧 Troubleshooting

### "Import pytrends could not be resolved"
```bash
pip install pytrends
```

### "Naver API credentials not configured"
- Add your Naver API keys to `.env` file
- Or it will use fallback simulation data

### Rate limiting issues
- Increase `REQUEST_DELAY` in `.env`
- The system respects API rate limits automatically

### Want to test without APIs?
- Current system works perfectly in simulation mode
- No setup required, just run as-is
