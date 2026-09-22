"""
Main entry point for LinkedIn Post Generator
"""

import os
import json
import glob
import textwrap
import argparse
from datetime import datetime
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel

# Local imports
from config import OUTPUT_DIR, POSTS_PER_RUN, CONCEPT_POSTS_PER_RUN, AI_PROVIDER
from news_fetcher import get_latest_news
from post_generator import LinkedInPostGenerator
from concept_posts import ConceptPostGenerator, TipOfTheDayGenerator

# Initialize Rich console
console = Console()

def ensure_output_dir():
    """Ensure output directory exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def load_previous_posts() -> List[Dict]:
    """Load posts from previous output files to avoid duplicates"""
    all_posts = []
    # Use glob to find all json files
    output_files = glob.glob(os.path.join(OUTPUT_DIR, '*.json'))
    
    for filename in output_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle different file structures
                if isinstance(data, list):
                    all_posts.extend(data)
                elif isinstance(data, dict):
                    if 'news_posts' in data:
                        all_posts.extend(data['news_posts'])
                    if 'concept_posts' in data:
                        all_posts.extend(data['concept_posts'])
                    if 'post_content' in data: # Single post format
                        all_posts.append(data)
        except Exception as e:
            console.print(f"[yellow]⚠️ Could not load {filename}: {e}[/yellow]")
            continue
            
    return all_posts

def save_posts(data: Dict, prefix: str) -> str:
    """Save generated posts to JSON file"""
    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    return filepath

def save_readable_txt(news_posts: List[Dict], concept_posts: List[Dict]) -> str:
    """Save posts in a human-readable text file"""
    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"posts_readable_{timestamp}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"LINKEDIN POSTS GENERATED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        if news_posts:
            f.write("📰 NEWS POSTS\n")
            f.write("-" * 20 + "\n\n")
            for i, post in enumerate(news_posts, 1):
                f.write(f"--- POST {i} ---\n\n")
                f.write(textwrap.fill(post.get('post_content', ''), width=80))
                f.write("\n\n")
                f.write(f"[Image Prompt]: {textwrap.fill(post.get('image_prompt', ''), width=80)}\n")
                f.write(f"[Source]: {post.get('source_article', 'Unknown')}\n\n")
                
        if concept_posts:
            f.write("📚 CONCEPT POSTS\n")
            f.write("-" * 20 + "\n\n")
            for i, post in enumerate(concept_posts, 1):
                f.write(f"--- CONCEPT {i} ---\n\n")
                f.write(textwrap.fill(post.get('post_content', ''), width=80))
                f.write("\n\n")
                f.write(f"[Image Prompt]: {textwrap.fill(post.get('image_prompt', ''), width=80)}\n")
                f.write(f"[Topic]: {post.get('topic', 'Unknown')}\n\n")
                
    return filepath

def generate_news_posts(limit: int = 2) -> List[Dict]:
    """Generate posts from news articles"""
    console.print("\n[bold blue]🔍 Fetching latest news...[/bold blue]")
    articles = get_latest_news(limit=10) # Fetch more to filter
    
    if not articles:
        console.print("[red]❌ No news found![/red]")
        return []

    console.print(f"[green]✅ Found {len(articles)} relevant articles[/green]")
    
    generator = LinkedInPostGenerator()
    posts = generator.generate_batch_news_posts(articles, count=limit)
    
    return posts

def generate_concept_posts(limit: int = 2) -> List[Dict]:
    """Generate educational concept posts"""
    console.print("\n[bold purple]📚 Generating concept posts...[/bold purple]")
    
    generator = ConceptPostGenerator()
    posts = generator.generate_batch_concept_posts(count=limit)
    
    return posts

def generate_tip():
    """Generate a quick tip post"""
    console.print("\n[bold yellow]💡 Generating quick tip...[/bold yellow]")
    
    generator = TipOfTheDayGenerator()
    post = generator.generate_quick_tip()
    
    if post:
        filepath = save_posts(post, "tip")
        console.print(Panel(post.get('post_content', ''), title="Generated Tip", border_style="yellow"))
        console.print(f"\n[green]💾 Tip saved to: {filepath}[/green]")

def main():
    parser = argparse.ArgumentParser(description='LinkedIn Post Generator')
    parser.add_argument('--news-only', action='store_true', help='Generate only news posts')
    parser.add_argument('--concepts-only', action='store_true', help='Generate only concept posts')
    parser.add_argument('--tip', action='store_true', help='Generate a quick tip post')
    parser.add_argument('--digest', action='store_true', help='Generate a news digest summary')
    parser.add_argument('--no-save', action='store_true', help='Do not save output to files')
    
    args = parser.parse_args()
    
    console.print(Panel.fit("🚀 LinkedIn Post Generator", style="bold cyan"))
    console.print(f"Using AI Provider: [bold]{AI_PROVIDER}[/bold]")

    if args.tip:
        generate_tip()
        return

    if args.digest:
        from config import DIGEST_LIMIT
        console.print(f"\n[bold blue]🔍 Generating News Digest (Top {DIGEST_LIMIT})...[/bold blue]")
        articles = get_latest_news(limit=DIGEST_LIMIT)
        
        if not articles:
            console.print("[red]❌ No news found![/red]")
            return

        generator = LinkedInPostGenerator()
        summaries = []
        
        for article in articles:
            console.print(f"📝 Summarizing: {article.get('title', '')[:50]}...")
            summary = generator.generate_news_summary(article)
            summaries.append(summary)
            
        # Save digest
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"news_digest_{timestamp}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        ensure_output_dir()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"NEWS DIGEST - {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("="*60 + "\n\n")
            
            for i, item in enumerate(summaries, 1):
                f.write(f"HEADER: {item['title']}\n")
                f.write(f"SOURCE: {item['source']}\n")
                f.write(f"LINK: {item.get('url', 'N/A')}\n\n")
                f.write(textwrap.fill(item['summary'], width=80))
                f.write("\n" + "="*80 + "\n\n")
                
        console.print(f"\n[green]📄 Digest saved to: {filepath}[/green]")
        return

    all_generated_data = {
        "generated_at": datetime.now().isoformat(),
        "ai_provider": AI_PROVIDER,
        "news_posts": [],
        "concept_posts": []
    }
    
    # Generate News Posts
    if not args.concepts_only:
        news_posts = generate_news_posts(limit=POSTS_PER_RUN)
        all_generated_data["news_posts"] = news_posts
        console.print(f"[green]✅ Generated {len(news_posts)} news posts[/green]")

    # Generate Concept Posts
    if not args.news_only:
        concept_posts = generate_concept_posts(limit=CONCEPT_POSTS_PER_RUN)
        all_generated_data["concept_posts"] = concept_posts
        console.print(f"[green]✅ Generated {len(concept_posts)} concept posts[/green]")
        
    # Save results
    if not args.no_save and (all_generated_data["news_posts"] or all_generated_data["concept_posts"]):
        saved_file = save_posts(all_generated_data, "linkedin_posts")
        txt_file = save_readable_txt(all_generated_data["news_posts"], all_generated_data["concept_posts"])
        
        console.print(f"\n[green]💾 JSON saved to: {saved_file}[/green]")
        console.print(f"[green]📄 Readable TXT saved to: {txt_file}[/green]")
        
    console.print("\n[bold green]✨ All Done![/bold green]")

if __name__ == "__main__":
    main()