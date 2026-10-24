"""
LinkedIn Post Generator Module
Uses FREE AI (Groq/Ollama) to generate engaging LinkedIn posts from news
"""

from typing import List, Dict
from ai_providers import get_ai_provider, generate_with_json
from config import POST_STYLE
from content_utils import clean_post_content


class LinkedInPostGenerator:
    """Generates LinkedIn posts using FREE AI providers"""
    
    def __init__(self):
        self.provider = get_ai_provider()
    
    def generate_news_post(self, article: Dict, variation: str = "direct lesson") -> Dict:
        """Generate a LinkedIn post based on a news article"""
        prompt = f"""
You are a data engineering professional sharing insights on LinkedIn.

{POST_STYLE}

Based on this news article, create a simple LinkedIn post:

ARTICLE TITLE: {article.get('title', '')}
ARTICLE DESCRIPTION: {article.get('description', '')}
ARTICLE CONTENT: {article.get('content', '')[:1000]}
SOURCE: {article.get('source', '')}

VARIATION FOR THIS POST: {variation}

Write a LinkedIn post that:
1. Sounds natural and conversational, like talking to a friend
2. Shares your perspective on this news
3. Provides practical value to data professionals
4. Uses simple language, no jargon
5. Uses the requested variation instead of a generic question-led opening

CRITICAL RULES:
- NO emojis or emoticons anywhere in the post
- Add line breaks after sentences for readability
- Keep paragraphs short (1-2 sentences each)
- Sound human, not robotic or marketing-like
- Do not invent first-person experience, tests, benchmarks, or claims about "my team"
- If you use a scenario, clearly present it as an example rather than something you personally did
- Do not include hashtags

Also generate an image prompt for Nano Banana AI image generator.

IMPORTANT: Respond in valid JSON format only:
{{
    "post_content": "The LinkedIn post text with NO emojis, no hashtags, and proper line breaks",
    "image_prompt": "Detailed prompt for Nano Banana image generation",
    "key_topic": "Main topic in 2-3 words"
}}
"""
        
        system_prompt = "You are a data engineering expert who creates engaging LinkedIn content. Always respond with valid JSON only, no extra text."
        
        result = generate_with_json(self.provider, prompt, system_prompt)
        
        if result.get("template_mode"):
            return self._generate_template_post(article)

        result["post_content"] = clean_post_content(result.get("post_content", ""))
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

The useful part is not the announcement itself.
It is the decision or practice you can apply after reading it."""
        
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
        
        variations = [
            "Open with a direct practical lesson, then explain the evidence.",
            "Open with a clearly hypothetical work scenario and use a short contrast structure.",
            "Open with a common mistake, then show a better approach without using a question hook.",
        ]
        for index, article in enumerate(articles[:count]):
            print(f"📝 Generating post for: {article.get('title', '')[:50]}...")
            post = self.generate_news_post(article, variation=variations[index % len(variations)])
            if post.get("post_content"):
                posts.append(post)
        
        return posts

    def generate_ai_news_post(self, article: Dict) -> Dict:
        """Generate a LinkedIn post about a current AI or LLM development."""
        prompt = f"""
You are a technology professional sharing a thoughtful update on LinkedIn.

{POST_STYLE}

Use this current AI or LLM news as source material for an educational LinkedIn post:

ARTICLE TITLE: {article.get('title', '')}
ARTICLE DESCRIPTION: {article.get('description', '')}
ARTICLE CONTENT: {article.get('content', '')[:1000]}
SOURCE: {article.get('source', '')}

The post must teach a durable idea that readers can apply after the headline is old.
Choose the strongest learning angle from the source, such as architecture, evaluation,
security, cost, model selection, data design, governance, or implementation trade-offs.

Write a post that:
1. Opens with the lesson or problem, not the announcement
2. Uses the news in no more than two sentences as a concrete example
3. Explains the underlying concept in simple terms
4. Includes a practical framework, checklist, or worked example
5. Separates confirmed facts from interpretation
6. Avoids hype, unsupported claims, and generic statements

CRITICAL RULES:
- NO emojis or emoticons anywhere in the post
- Add line breaks after sentences for readability
- Keep paragraphs short (1-2 sentences each)
- Use simple language and define unfamiliar terms
- Do not invent first-person experience, tests, benchmarks, or claims about "my team"
- Mention the source naturally once for context
- End with a specific recommendation or concise lesson; a question is optional
- Do not include hashtags
- Do not read like a news report or announcement summary

Also generate an image prompt for Nano Banana AI image generator.

IMPORTANT: Respond in valid JSON format only:
{{
    "post_content": "An educational LinkedIn post with no hashtags",
    "image_prompt": "Detailed prompt for Nano Banana image generation",
    "key_topic": "Main AI or LLM topic in 2-4 words"
}}
"""
        system_prompt = "You explain current AI and LLM developments accurately and without hype. Respond with valid JSON only."
        result = generate_with_json(self.provider, prompt, system_prompt)

        fallback_reason = result.get("error", "")
        if not result.get("template_mode") and not result.get("post_content"):
            retry_prompt = f"""
Turn this source into a concise educational LinkedIn post.

TITLE: {article.get('title', '')}
DESCRIPTION: {article.get('description', '')}
CONTENT: {article.get('content', '')[:1200]}
SOURCE: {article.get('source', '')}

Teach one specific technical idea from the source using a practical example or checklist.
Use the announcement only as context. Do not write a news summary.
Do not invent experience, benchmarks, or facts. Do not use hashtags or emojis.
Keep the post between 140 and 220 words.

Return valid JSON only with string fields: post_content, image_prompt, and key_topic.
"""
            result = generate_with_json(self.provider, retry_prompt, system_prompt)
            fallback_reason = result.get("error", fallback_reason)

        if result.get("template_mode") or not result.get("post_content"):
            result = self._generate_template_ai_learning_post(article)
            result["fallback_reason"] = fallback_reason or "AI provider unavailable"

        result["post_content"] = clean_post_content(result.get("post_content", ""))
        result["source_article"] = article.get("title", "")
        result["source_url"] = article.get("url", "")
        result["post_type"] = "ai_news"
        result["content_category"] = "AI / LLM"
        return result

    def _generate_template_ai_learning_post(self, article: Dict) -> Dict:
        """Create a topic-specific educational post when the model is unavailable."""
        title = article.get("title", "Current AI development")
        source_text = " ".join(
            str(article.get(field, "")) for field in ("title", "description", "content")
        ).lower()

        if any(word in source_text for word in ("robot", "simulation", "sim-to-real", "sim2real")):
            key_topic = "Simulation to reality"
            post_content = f"""Teaching a robot in simulation is useful because failure is cheap there.

The article “{title}” is a practical example of reinforcement learning: an agent tries actions, receives a reward signal, and adjusts its policy to improve future behavior.

The difficult part is the simulation-to-reality gap.
A controller that works in a clean virtual world may fail when a real motor has delay, a sensor is noisy, or the floor has different friction.

Three techniques help close that gap:

1. Randomize the environment.
Vary mass, friction, delay, lighting, and sensor noise during training.

2. Design rewards around the real objective.
Reward stable forward movement while penalizing falls, excessive energy use, and unsafe joint motion.

3. Validate in stages.
Move from simulation to hardware with speed limits, safety constraints, and measurable stop conditions.

The lesson applies beyond robotics: synthetic training works best when variation and failure modes reflect the environment where the system will actually operate."""
        elif "agent" in source_text or "govern" in source_text:
            key_topic = "Governed AI agents"
            post_content = f"""An AI agent should be allowed to improve only inside a controlled feedback loop.

The article “{title}” points to a growing design problem: agents can plan, call tools, and adapt, but every new behavior also changes operational risk.

A governed agent needs four separate controls:

1. Version the agent.
Store its prompt, tools, model, permissions, and evaluation results as one releasable unit.

2. Limit its authority.
Give each tool the smallest required scope, and require approval for actions with material impact.

3. Gate every change.
Test proposed updates against fixed tasks, adversarial cases, cost limits, and safety rules before promotion.

4. Preserve an audit trail and rollback path.
Record what the agent observed, decided, and changed so an operator can investigate and restore a known version.

“Self-evolving” should describe an automated proposal process, not uncontrolled production changes.
The durable architecture is a measured loop: observe, propose, evaluate, approve, deploy, and monitor."""
        elif any(word in source_text for word in ("cloud", "inference", "hosting", "provider")):
            key_topic = "LLM deployment tradeoffs"
            post_content = f"""Choosing where to run an LLM is a workload decision, not a brand decision.

The article “{title}” is a useful reason to review the factors that determine whether a model deployment will work in production.

Compare providers with the same representative prompts and measure:

1. Quality: task success and failure patterns on your own data.
2. Latency: median and tail response times at expected concurrency.
3. Cost: input, output, caching, networking, and idle capacity.
4. Governance: data location, retention, access control, and audit logs.
5. Portability: API differences, tool calling behavior, and the effort required to move.

Run a small evaluation before changing architecture.
A provider that looks cheaper per token may cost more after retries, slower responses, or migration work are included.

The useful outcome is a decision backed by workload evidence and a documented exit path."""
        elif any(word in source_text for word in ("security", "attack", "prompt injection", "vulnerability")):
            key_topic = "AI threat modeling"
            post_content = f"""AI security starts by mapping what the model can read, decide, and change.

The article “{title}” provides a useful prompt for a simple threat model.

Review four boundaries:

1. Inputs: Can untrusted text influence instructions or tool arguments?
2. Data: Can the model retrieve records that the requesting user cannot access directly?
3. Tools: Can one model call create, delete, purchase, publish, or change permissions?
4. Outputs: Can generated content trigger another system without validation?

For each boundary, define authentication, authorization, input validation, logging, and a human approval point where impact is significant.

Model-level safeguards help, but system controls carry the real security guarantee.
Treat the model as an untrusted decision component inside a trusted application boundary."""
        else:
            key_topic = "Evaluating AI systems"
            post_content = f"""A new AI capability matters only when it improves a real task under real constraints.

Use the article “{title}” as a starting point for an evaluation, rather than as proof that the technology is ready for adoption.

Build a small test in four steps:

1. Define the task and a current baseline.
2. Use representative inputs, including difficult and unsafe cases.
3. Measure quality, latency, cost, and failure severity separately.
4. Set a promotion threshold and a rollback condition before seeing the result.

Keep confirmed source facts separate from assumptions about your own system.
A benchmark improvement does not automatically predict reliability on different data, tools, or operating conditions.

The durable skill is turning an AI claim into a falsifiable test with a clear adoption decision."""

        return {
            "post_content": clean_post_content(post_content),
            "image_prompt": f"A clean educational diagram about {key_topic}, professional minimalist LinkedIn visual, no text",
            "key_topic": key_topic,
            "template_mode": True,
        }

    def generate_batch_ai_news_posts(self, articles: List[Dict], count: int = 1) -> List[Dict]:
        """Generate a small dedicated batch of AI/LLM news posts."""
        posts = []
        for article in articles[:count]:
            print(f"Generating AI/LLM post for: {article.get('title', '')[:50]}...")
            post = self.generate_ai_news_post(article)
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
