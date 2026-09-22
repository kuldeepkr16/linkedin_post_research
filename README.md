# 🚀 LinkedIn Post Generator for Data Engineering

**100% FREE** - No paid API keys required!

Automatically generate engaging LinkedIn posts about data engineering news and advanced concepts.

## ✨ Features

- **📰 News-Based Posts**: Fetches latest data engineering news from FREE RSS feeds
- **📚 Concept Posts**: Creates educational posts about advanced topics (SQL, Python, Spark, etc.)
- **🎨 Image Prompts**: Generates complementary image prompts for Nano Banana AI tool
- **💡 Quick Tips**: Short, punchy tip posts for daily engagement
- **🆓 100% Free**: Uses Groq (free tier) or Ollama (local) - no paid APIs!

## 📋 Requirements

- Python 3.9+
- Groq API key (FREE) OR Ollama (local, free)

## 🛠️ Quick Setup

```bash
# 1. Navigate to project
cd linkedin_post_generator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your FREE Groq API key
# Get it from: https://console.groq.com/keys (takes 30 seconds!)
echo "GROQ_API_KEY=your_key_here" > .env
echo "AI_PROVIDER=groq" >> .env

# 5. Run!
python main.py
```

## 🆓 FREE AI Options

### Option 1: Groq (Recommended - FREE Cloud)
1. Go to https://console.groq.com/keys
2. Sign up (free, no credit card)
3. Create an API key
4. Add to `.env`:
   ```
   GROQ_API_KEY=your_key_here
   AI_PROVIDER=groq
   ```

### Option 2: Ollama (FREE Local)
1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3.2`
3. Start Ollama: `ollama serve`
4. Add to `.env`:
   ```
   AI_PROVIDER=ollama
   OLLAMA_MODEL=llama3.2
   ```

### Option 3: Template Mode (No AI)
If no API is configured, the script generates templates you can customize.

## 🚀 Usage

### Generate All Posts (2 News + 2 Concepts)
```bash
python main.py
```

### Generate Only News Posts
```bash
python main.py --news-only
```

### Generate Only Concept Posts
```bash
python main.py --concepts-only
```

### Generate Quick Tip
```bash
python main.py --tip
```

## 📂 Output

Generated posts are saved to `output/` as JSON files:
```
output/
├── linkedin_posts_20241216_100000.json
└── tip_20241216_110000.json
```

Each output contains:
- Full post content (ready to copy-paste)
- Image prompt (for Nano Banana)
- Source references

## 🎯 Topics Covered

### News Sources (FREE RSS)
- Google News (data engineering topics)
- Reddit (/r/dataengineering, /r/SQL, /r/Python)
- Hacker News

### Concept Topics
- **SQL**: Window Functions, CTEs, Query Optimization
- **Python**: Generators, Async, Pandas Optimization
- **PostgreSQL**: VACUUM, Replication, EXPLAIN
- **Spark**: Catalyst, Partitioning, Memory Management
- **QuickSight**: SPICE, LAA, Embedding
- **Data Engineering**: Medallion Architecture, CDC, Data Mesh

## 🖼️ Using Image Prompts with Nano Banana

1. Copy the image prompt from the output
2. Go to Nano Banana (or your preferred AI image tool)
3. Paste the prompt and generate
4. Download and attach to your LinkedIn post

## ⏰ Daily Automation (Cron)

```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/linkedin_post_generator && /path/to/venv/bin/python main.py
```

## 🌐 GitHub Actions + Review Dashboard

This repository also includes a static review dashboard in `frontend/`.
The scheduled GitHub Action runs every day at **8:00 AM IST**, generates fresh
drafts, updates the dashboard history, and deploys the site to GitHub Pages.

### One-time GitHub setup

1. Push the repository to GitHub.
2. Open **Settings → Secrets and variables → Actions** and add a repository
   secret named `GROQ_API_KEY`.
3. Open **Settings → Pages** and set the source to **GitHub Actions**.
4. Open the **Actions** tab and run **Daily LinkedIn Posts** once manually.

The dashboard lets you:

- Review news and concept drafts.
- Open the source article for news posts.
- Copy a finished draft.
- Mark drafts as **Ready to post** or **Skip** in your browser.
- Browse previous generated runs.

Generated dashboard history is stored under `frontend/data/`. Raw local
`output/` files and `.env` remain ignored by Git.

## 📝 Example Output

### Generated Post
```
🚀 Data engineering just got a major upgrade!

Apache Spark 4.0 brings game-changing performance improvements:

📊 50% faster query execution
💾 Smarter memory management  
⚡ Native Python UDF optimization

What this means for you:
→ Faster pipeline processing
→ Lower cloud costs
→ Better developer experience

Are you planning to upgrade? What features excite you most?

#DataEngineering #ApacheSpark #BigData #Analytics
```

### Nano Banana Image Prompt
```
Modern data engineering visualization showing data flowing through 
distributed computing clusters, blue and orange gradient, abstract 
geometric patterns, dark background with glowing data streams, 
professional LinkedIn style, no text
```

## 🔧 Customization

Edit `config.py` to:
- Modify post style (`POST_STYLE`)
- Add new concept topics (`CONCEPT_TOPICS`)
- Adjust RSS feeds (`RSS_FEEDS`)

---

Built with ❤️ for Data Engineers | 100% FREE
