"""Build static dashboard data from generated LinkedIn post JSON files.

The raw ``output/`` directory stays gitignored. This script copies generated
runs into ``frontend/data/runs`` and creates small manifest/latest files that
the GitHub Pages frontend can load directly.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
DATA_DIR = ROOT / "frontend" / "data"
RUNS_DIR = DATA_DIR / "runs"


def read_json(path: Path) -> Optional[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def sanitize_run(data: dict) -> dict:
    """Remove unusable drafts before publishing a run to the dashboard."""
    cleaned = dict(data)
    for group in ("news_posts", "concept_posts"):
        posts = []
        for post in data.get(group) or []:
            if not isinstance(post, dict):
                continue
            content = post.get("post_content")
            if not isinstance(content, str) or not content.strip():
                continue
            # Older runs may contain a truncated JSON object stored as the
            # post itself after a model response exceeded its output limit.
            if post.get("raw") and content.lstrip().startswith("{"):
                continue
            posts.append(post)
        cleaned[group] = posts
    return cleaned


def generated_at(data: dict, path: Path) -> str:
    value = data.get("generated_at")
    if isinstance(value, str) and value:
        return value

    # Fallback for older files that may not contain generated_at.
    prefix = "linkedin_posts_"
    stamp = path.stem[len(prefix):] if path.stem.startswith(prefix) else path.stem
    try:
        return datetime.strptime(stamp, "%Y%m%d_%H%M%S").isoformat()
    except ValueError:
        return datetime.fromtimestamp(path.stat().st_mtime).isoformat()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    # Add any newly generated local runs to the versioned dashboard history.
    if OUTPUT_DIR.exists():
        for source in sorted(OUTPUT_DIR.glob("linkedin_posts_*.json")):
            data = read_json(source)
            if not data:
                continue
            data = sanitize_run(data)
            target = RUNS_DIR / source.name
            target.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    runs = []
    for path in RUNS_DIR.glob("linkedin_posts_*.json"):
        data = read_json(path)
        if not data:
            continue
        data = sanitize_run(data)
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        news = data.get("news_posts") or []
        concepts = data.get("concept_posts") or []
        runs.append(
            {
                "generated_at": generated_at(data, path),
                "ai_provider": data.get("ai_provider", "unknown"),
                "news_count": len(news),
                "concept_count": len(concepts),
                "total_count": len(news) + len(concepts),
                "path": f"data/runs/{path.name}",
                "filename": path.name,
            }
        )

    runs.sort(key=lambda item: item["generated_at"], reverse=True)
    if not runs:
        raise SystemExit("No generated LinkedIn post runs found.")

    latest_path = ROOT / "frontend" / runs[0]["path"]
    latest = read_json(latest_path)
    if not latest:
        raise SystemExit(f"Could not read latest run: {latest_path}")

    (DATA_DIR / "latest.json").write_text(
        json.dumps(latest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (DATA_DIR / "history.json").write_text(
        json.dumps(
            {
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "runs": runs,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"Dashboard data ready: {len(runs)} runs, "
        f"latest={runs[0]['generated_at']} ({runs[0]['total_count']} posts)"
    )


if __name__ == "__main__":
    main()
