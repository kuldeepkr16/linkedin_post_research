"""
LinkedIn Post Generator Module
Uses FREE AI (Groq/Ollama) to generate engaging LinkedIn posts from news
"""

from typing import List, Dict
from ai_providers import get_ai_provider, generate_with_json
from config import POST_STYLE


class LinkedInPostGenerator:
    """Generates LinkedIn posts using FREE AI providers"""
    
    def __init__(self):
        self.provider = get_ai_provider()
    
    def generate_news_post(self, article: Dict) -> Dict:
        """Generate a LinkedIn post based on a news article"""
        prompt = f"""
You are a data engineering professional sharing insights on LinkedIn.

{POST_STYLE}

Based on this news article, create a simple LinkedIn post:

ARTICLE TITLE: {article.get('title', '')}
ARTICLE DESCRIPTION: {article.get('description', '')}
ARTICLE CONTENT: {article.get('content', '')[:1000]}
SOURCE: {article.get('source', '')}

Write a LinkedIn post that:
1. Sounds natural and conversational, like talking to a friend
2. Shares your perspective on this news
3. Provides practical value to data professionals
4. Uses simple language, no jargon

CRITICAL RULES:
- NO emojis or emoticons anywhere in the post
- Add line breaks after sentences for readability
- Keep paragraphs short (1-2 sentences each)
- Sound human, not robotic or marketing-like

Also generate an image prompt for Nano Banana AI image generator.

IMPORTANT: Respond in valid JSON format only:
{{
    "post_content": "The LinkedIn post text with NO emojis, proper line breaks, and hashtags at end",
    "image_prompt": "Detailed prompt for Nano Banana image generation",
    "key_topic": "Main topic in 2-3 words"
}}
"""
        
        system_prompt = "You are a data engineering expert who creates engaging LinkedIn content. Always respond with valid JSON only, no extra text."
        
        result = generate_with_json(self.provider, prompt, system_prompt)
        
        if result.get("template_mode"):
            return self._generate_template_post(article)
        
        result["source_article"] = article.get("title", "")
        result["source_url"] = article.get("url", "")
        return result
    
    def _generate_template_post(self, article: Dict) -> Dict:
        """Generate a template post when AI is not available"""
        title = article.get('title', 'Data Engineering Update')
        
        post_content = f"""Interesting development: {title}

This caught my attention today.

Here's why it matters for data professionals:

- [Add your insight about the impact]
- [Add a practical takeaway]
- [Add what you think we should do about it]

What's your take on this?

#DataEngineering #SQL #Analytics"""
        
        image_prompt = f"Modern data engineering visualization, professional tech aesthetic, blue and white color scheme, abstract data flow patterns, clean minimalist design for LinkedIn - topic: {title}"
        
        return {
            "post_content": post_content,
            "image_prompt": image_prompt,
            "key_topic": "Data Engineering",
            "source_article": title,
            "source_url": article.get("url", ""),
            "template_mode": True
        }
    
    def generate_batch_news_posts(self, articles: List[Dict], count: int = 2) -> List[Dict]:
        """Generate multiple posts from a list of articles"""
        posts = []
        
        for article in articles[:count]:
            print(f"📝 Generating post for: {article.get('title', '')[:50]}...")
            post = self.generate_news_post(article)
            if post.get("post_content"):
                posts.append(post)
        
        return posts

    def generate_news_summary(self, article: Dict) -> Dict:
        """Generate a concise summary for news digest"""
        from config import DIGEST_STYLE
        
        prompt = f"""
{DIGEST_STYLE}

Summarize this article:
TITLE: {article.get('title', '')}
CONTENT: {article.get('content', '')[:1000]}

IMPORTANT: Respond in valid JSON format only:
{{
    "summary": "Concise 2-3 sentence summary",
    "title": "Article Title"
}}
"""
        system_prompt = "You are a precise news summarizer. Respond with valid JSON only."
        
        result = generate_with_json(self.provider, prompt, system_prompt)
        
        if result.get("template_mode"):
            return {
                "title": article.get("title", ""),
                "summary": article.get("description", "")[:200],
                "source": article.get("source", "Unknown"),
                "url": article.get("url", "")
            }
            
        return {
            "title": result.get("title", article.get("title", "")),
            "summary": result.get("summary", ""),
            "source": article.get("source", "Unknown"),
            "url": article.get("url", "")
        }


class ImagePromptGenerator:
    """Generates image prompts for Nano Banana tool"""
    
    def __init__(self):
        self.provider = get_ai_provider()
    
    def generate_standalone_prompt(self, topic: str) -> str:
        """Generate an image prompt for a given data engineering topic"""
        prompt = f"""
Create a detailed image prompt for Nano Banana AI image generator
for a LinkedIn post about: {topic}

The image should be:
- Professional and modern
- Suitable for a data engineering/tech LinkedIn post
- Visually represent the concept without text
- Eye-catching and shareable
- Clean, minimalist aesthetic

Provide only the image prompt text, nothing else.
"""
        
        response = self.provider.generate(prompt, "You are an expert at creating AI image prompts.")
        
        if response and response != "TEMPLATE_MODE":
            return response.strip()
        
        return f"Modern data engineering visualization representing {topic}, professional LinkedIn style, blue and teal gradient, abstract geometric patterns, clean minimalist design, no text"


if __name__ == "__main__":
    test_article = {
        "title": "Apache Spark 4.0 Released with Major Performance Improvements",
        "description": "The Apache Software Foundation announces Spark 4.0 with significant improvements.",
        "content": "Apache Spark 4.0 introduces a new adaptive query execution engine.",
        "source": "Tech News",
        "url": "https://example.com"
    }
    
    print("🧪 Testing LinkedIn Post Generator (FREE AI)...\n")
    generator = LinkedInPostGenerator()
    post = generator.generate_news_post(test_article)
    
    print("="*60)
    print("📱 GENERATED POST:")
    print("="*60)
    print(post.get("post_content", "No content generated"))
    print("\n" + "="*60)
    print("🎨 IMAGE PROMPT (for Nano Banana):")
    print("="*60)
    print(post.get("image_prompt", "No prompt generated"))
