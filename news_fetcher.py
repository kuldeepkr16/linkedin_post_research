"""
News Fetcher Module
Fetches data engineering news from FREE open-source RSS feeds
No API keys required!
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re
from config import RSS_FEEDS, TECH_RSS_FEEDS, HACKERNEWS_FEEDS


class NewsFetcher:
    """Fetches news from free RSS sources for data engineering topics"""
    
    def __init__(self):
        # Use timezone-aware datetime for comparison
        from datetime import timezone
        self.cutoff_date = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)
    
    def fetch_all_news(self) -> List[Dict]:
        """
        Fetch news from all available free sources
        Returns combined and deduplicated list of news articles
        """
        all_news = []
        
        # Fetch from Google News RSS (free, no API)
        google_news = self._fetch_from_google_rss()
        all_news.extend(google_news)
        print(f"📰 Fetched {len(google_news)} articles from Google News RSS")
        
        # Fetch from Reddit RSS (free, no API)
        reddit_news = self._fetch_from_reddit_rss()
        all_news.extend(reddit_news)
        print(f"🤖 Fetched {len(reddit_news)} posts from Reddit RSS")
        
        # Fetch from Hacker News RSS (free, no API)
        hn_news = self._fetch_from_hackernews_rss()
        all_news.extend(hn_news)
        print(f"🔶 Fetched {len(hn_news)} posts from Hacker News RSS")
        
        # Deduplicate by title similarity
        deduplicated = self._deduplicate_news(all_news)
        print(f"✅ Total unique articles: {len(deduplicated)}")
        
        return deduplicated
    
    def _fetch_from_google_rss(self) -> List[Dict]:
        """Fetch news from Google News RSS feeds (FREE)"""
        articles = []
        
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                if getattr(feed, "bozo", False) and not feed.entries:
                    error = getattr(feed, "bozo_exception", "Unknown feed error")
                    print(f"⚠️ Google RSS fetch failed: {type(error).__name__}: {error}")
                    continue
                for entry in feed.entries[:10]:
                    pub_date = self._parse_date(entry.get("published", ""))
                    if pub_date and pub_date > self.cutoff_date:
                        articles.append({
                            "title": self._clean_text(entry.get("title", "")),
                            "description": self._clean_text(entry.get("summary", "")),
                            "url": entry.get("link", ""),
                            "source": "Google News",
                            "published": entry.get("published", ""),
                            "content": self._clean_text(entry.get("summary", "")),
                        })
            except Exception as e:
                print(f"⚠️ Google RSS error: {e}")
        
        return articles
    
    def _fetch_from_reddit_rss(self) -> List[Dict]:
        """Fetch posts from Reddit RSS feeds (FREE)"""
        articles = []
        
        for feed_url in TECH_RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                if getattr(feed, "bozo", False) and not feed.entries:
                    error = getattr(feed, "bozo_exception", "Unknown feed error")
                    print(f"⚠️ Reddit RSS fetch failed: {type(error).__name__}: {error}")
                    continue
                for entry in feed.entries[:15]:
                    pub_date = self._parse_date(entry.get("published", entry.get("updated", "")))
                    if pub_date and pub_date > self.cutoff_date:
                        content = self._extract_reddit_content(
                            entry.get("content", [{}])[0].get("value", "") if entry.get("content") else entry.get("summary", "")
                        )
                        if len(content) > 50:
                            articles.append({
                                "title": self._clean_text(entry.get("title", "")),
                                "description": content[:500],
                                "url": entry.get("link", ""),
                                "source": "Reddit",
                                "published": entry.get("published", ""),
                                "content": content,
                            })
            except Exception as e:
                print(f"⚠️ Reddit RSS error: {e}")
        
        return articles
    
    def _fetch_from_hackernews_rss(self) -> List[Dict]:
        """Fetch from Hacker News RSS (FREE)"""
        articles = []
        
        for feed_url in HACKERNEWS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                if getattr(feed, "bozo", False) and not feed.entries:
                    error = getattr(feed, "bozo_exception", "Unknown feed error")
                    print(f"⚠️ Hacker News RSS fetch failed: {type(error).__name__}: {error}")
                    continue
                for entry in feed.entries[:10]:
                    pub_date = self._parse_date(entry.get("published", ""))
                    if pub_date and pub_date > self.cutoff_date:
                        articles.append({
                            "title": self._clean_text(entry.get("title", "")),
                            "description": self._clean_text(entry.get("summary", entry.get("description", ""))),
                            "url": entry.get("link", ""),
                            "source": "Hacker News",
                            "published": entry.get("published", ""),
                            "content": self._clean_text(entry.get("summary", "")),
                        })
            except Exception as e:
                print(f"⚠️ HN RSS error: {e}")
        
        return articles
    
    def _extract_reddit_content(self, html_content: str) -> str:
        """Extract text content from Reddit HTML"""
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            for tag in soup.find_all(['a', 'img']):
                tag.decompose()
            text = soup.get_text(separator=' ', strip=True)
            return self._clean_text(text)
        except:
            return self._clean_text(html_content)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())
        text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
        return text.strip()
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse various date formats and return timezone-naive datetime"""
        if not date_string:
            return None
        
        try:
            from dateutil import parser
            parsed = parser.parse(date_string)
            # Convert to naive datetime for comparison
            if parsed.tzinfo is not None:
                from datetime import timezone
                parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
            return parsed
        except:
            pass
        
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S+00:00",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_string.replace("GMT", "+0000"), fmt)
                if parsed.tzinfo is not None:
                    parsed = parsed.replace(tzinfo=None)
                return parsed
            except:
                continue
        
        return datetime.now()  # Assume recent if can't parse
    
    def _deduplicate_news(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get("title", "").lower()
            title_words = set(title.split())
            
            is_duplicate = False
            for seen in seen_titles:
                seen_words = set(seen.split())
                if len(title_words & seen_words) / max(len(title_words), 1) > 0.6:
                    is_duplicate = True
                    break
            
            if not is_duplicate and title:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    def filter_relevant_news(self, articles: List[Dict], min_relevance: int = 1) -> List[Dict]:
        """Filter articles by relevance to data engineering topics"""
        scored_articles = []
        
        relevance_keywords = [
            "sql", "postgres", "postgresql", "database", "query",
            "spark", "hadoop", "data engineering", "etl", "pipeline",
            "python", "pandas", "data analysis", "analytics",
            "quicksight", "tableau", "power bi", "visualization",
            "snowflake", "databricks", "bigquery", "redshift",
            "kafka", "airflow", "dbt", "data warehouse",
            "machine learning", "ml", "ai", "data science",
        ]
        
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            score = sum(1 for kw in relevance_keywords if kw in text)
            
            if score >= min_relevance:
                article["relevance_score"] = score
                scored_articles.append(article)
        
        scored_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return scored_articles


def get_latest_news(limit: int = 10) -> List[Dict]:
    """Convenience function to get latest relevant news"""
    fetcher = NewsFetcher()
    all_news = fetcher.fetch_all_news()
    relevant_news = fetcher.filter_relevant_news(all_news)
    return relevant_news[:limit]


if __name__ == "__main__":
    print("🔍 Fetching latest data engineering news (FREE sources)...\n")
    news = get_latest_news(limit=5)
    
    for i, article in enumerate(news, 1):
        print(f"\n{'='*60}")
        print(f"📰 Article {i}")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Relevance: {article.get('relevance_score', 0)}")
        print(f"Description: {article['description'][:200]}...")
