"""Shared cleanup helpers for generated LinkedIn content."""

import re
from typing import Dict, Iterable


HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z][A-Za-z0-9_]*")


def clean_post_content(content: str) -> str:
    """Remove hashtags and tidy whitespace from a generated post."""
    if not isinstance(content, str):
        return content

    cleaned = HASHTAG_RE.sub("", content)
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r" {2,}", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def clean_posts(posts: Iterable[Dict]) -> None:
    """Clean post content in place for a collection of post dictionaries."""
    for post in posts:
        if isinstance(post, dict) and isinstance(post.get("post_content"), str):
            post["post_content"] = clean_post_content(post["post_content"])
