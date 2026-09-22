---
name: generating-linkedin-posts
description: Use when asked to generate LinkedIn posts in the linkedin_post_generator project - write the post content directly instead of calling Groq/Gemini/Ollama, so no AI API key or quota is needed.
---

# Generating LinkedIn Posts (Claude-authored)

## Overview
This project normally calls an external AI provider (Groq/Gemini/Ollama, see `ai_providers.py`) to write post text. When asked to generate posts here, write the post content yourself instead - skip the external provider entirely.

## When to use
- User asks to "generate", "generate posts", "make a post" etc. while working in this project.
- Not for other projects - this depends on this repo's file layout and output format.

## Workflow
1. Fetch raw data (no AI call, just RSS + topic selection):
   ```bash
   ./venv/bin/python scripts/claude_fetch.py > /tmp/fetch.json
   ```
   Returns `{"articles": [...], "concepts": [...]}`.

2. Read `/tmp/fetch.json`. For each article and each concept, write `post_content` and `image_prompt` yourself, following `config.py`'s `POST_STYLE`:
   - Conversational tone, no emojis anywhere
   - Line breaks after sentences, short paragraphs (1-2 sentences)
   - 150-250 words, ends with a discussion question
   - 3-4 relevant hashtags at the end
   - News posts: reference the article's angle/insight (see prompt in `post_generator.py`)
   - Concept posts: hook, plain-language explanation, 2-3 bullet takeaways, one common mistake to avoid (see prompt in `concept_posts.py`)

3. Assemble:
   ```json
   {
     "news_posts": [{"post_content": "...", "image_prompt": "...", "key_topic": "...", "source_article": "...", "source_url": "..."}],
     "concept_posts": [{"post_content": "...", "image_prompt": "...", "topic": "...", "concept": "...", "post_type": "concept"}]
   }
   ```

4. Save in the project's standard output format (matches what `main.py` produces):
   ```bash
   ./venv/bin/python scripts/claude_save.py /tmp/generated.json
   ```
   Writes `output/linkedin_posts_<timestamp>.json` and `output/posts_readable_<timestamp>.txt`.

## Quick reference
| Step | Command |
|---|---|
| Fetch news + concepts | `scripts/claude_fetch.py` |
| Save in standard format | `scripts/claude_save.py <file.json>` |

## Common mistakes
- Don't call `ai_providers.py` / `get_ai_provider()` - that's the external-API path this skill replaces.
- Don't skip `POST_STYLE` rules - no emojis is a hard requirement, checked by eye since nothing enforces it in code.
- `claude_save.py` expects the exact keys shown above; missing `post_content` means `main.py`'s dedup/display logic downstream will show blank posts.
