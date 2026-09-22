"""
Fetch news articles + concept topics for Claude-authored posts.
No AI provider call here - just the free RSS/topic-selection logic.
Prints JSON to stdout: {"articles": [...], "concepts": [...]}
"""
import contextlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_fetcher import get_latest_news
from concept_posts import ConceptPostGenerator
from config import POSTS_PER_RUN, CONCEPT_POSTS_PER_RUN


def main():
    # news_fetcher/concept_posts print progress messages to stdout; redirect
    # them to stderr so stdout stays clean JSON.
    with contextlib.redirect_stdout(sys.stderr):
        articles = get_latest_news(limit=10)[:POSTS_PER_RUN]
        concepts = ConceptPostGenerator().get_random_concepts(CONCEPT_POSTS_PER_RUN)

    print(json.dumps({"articles": articles, "concepts": concepts}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
