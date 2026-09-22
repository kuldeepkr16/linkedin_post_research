"""
Save Claude-authored LinkedIn posts using the project's standard output format
(same JSON + readable-txt structure that main.py produces).

Usage: ./venv/bin/python scripts/claude_save.py posts.json
Input JSON shape: {"news_posts": [...], "concept_posts": [...]}
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import save_posts, save_readable_txt


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    raw = open(path, encoding="utf-8").read() if path else sys.stdin.read()
    data = json.loads(raw)

    news_posts = data.get("news_posts", [])
    concept_posts = data.get("concept_posts", [])

    all_data = {
        "generated_at": datetime.now().isoformat(),
        "ai_provider": "claude",
        "news_posts": news_posts,
        "concept_posts": concept_posts,
    }

    saved_file = save_posts(all_data, "linkedin_posts")
    txt_file = save_readable_txt(news_posts, concept_posts)

    print(f"JSON saved to: {saved_file}")
    print(f"Readable TXT saved to: {txt_file}")


if __name__ == "__main__":
    main()
