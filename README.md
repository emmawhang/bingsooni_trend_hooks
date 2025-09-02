# Bingsooni Trend Hooks

Automated system for generating daily **hooks + hashtag sets** for Instagram content.  
Focus: consistency, reduced manual work, and data-driven improvement.

---

## Features
- **Daily consistency**: Generates 20 hooks + 25–28 hashtags at 09:00 AM.  
- **Data-driven**: Merges Google Trends (pytrends), Reddit, TikTok, and internal IG data.  
- **Workflow loop**: Track hook performance → feed back into templates.  
- **Brand tone**: Templates keep Bingsooni’s voice consistent.  
- **KPI tracking**: Saves, Shares, Comments, Profile clicks, Follower growth, Hashtag reach.  

---

## Repo Structure

/bingsooni_trend_hooks
hook_generator.py # Build hooks from keywords
trends_fetchers.py # Fetch pytrends / Reddit / TikTok keywords
hashtags_manager.py # Hashtag rotation logic
utils.py # Shared helpers (logging, KPI parsing)
data/
hashtags.csv # Broad / Mid / Niche / Local pools
stopwords.txt # Forbidden words & tags
outputs/ # Daily results (YYYYMMDD_hooks.csv|.md)
state/
rotation.json # Tracks last hashtag set

---

## Daily Workflow
1. **09:00** → Auto-run pipeline.  
2. Output: `YYYYMMDD_hooks.csv` (20 hooks + hashtags).  
3. Reviewer (e.g. Jiyoon) picks 3–5 hooks → write captions & upload.  
4. After 24h/72h → log metrics (best vs. worst hooks).  
5. Weekly: update templates with winning patterns.  

---

## Guidelines
- **Hooks**:  
  - Length 8–14 words.  
  - Use numbers, contrast, or surprise.  
  - Avoid exaggeration, medical/sexual/offensive terms.  

- **Hashtags**:  
  - Broad 6–8 + Mid 6–8 + Niche 5–7 + Local 4–6.  
  - Rotate sets (48–72h before reuse).  
  - Place 5–8 in caption, rest in first comment.  

- **A/B Test**:  
  - Same content, 2 hooks (48h apart).  
  - If save-rate gap ≥30%, update templates with winner.  

---

## Setup
```bash
git clone <repo-url>
cd bingsooni_trend_hooks
pip install -r requirements.txt
