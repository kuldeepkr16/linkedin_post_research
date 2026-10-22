"""
Concept Posts Module
Generates educational LinkedIn posts about advanced data engineering concepts
Uses FREE AI providers (Groq/Ollama)
"""

import random
from typing import List, Dict
from ai_providers import get_ai_provider, generate_with_json
from config import POST_STYLE, CONCEPT_TOPICS
from content_utils import clean_post_content


class ConceptPostGenerator:
    """Generates educational posts about data engineering concepts"""
    
    def __init__(self):
        self.provider = get_ai_provider()
        self.topics = CONCEPT_TOPICS
    
    def get_random_concepts(self, count: int = 2) -> List[Dict]:
        """Select random concepts from different topics"""
        all_concepts = []
        
        for topic_key, topic_data in self.topics.items():
            for concept in topic_data["advanced_concepts"]:
                all_concepts.append({
                    "topic_key": topic_key,
                    "topic_name": topic_data["name"],
                    "concept": concept
                })
        
        random.shuffle(all_concepts)
        selected = []
        used_topics = set()
        
        for concept in all_concepts:
            if len(selected) >= count:
                break
            if concept["topic_key"] not in used_topics or len(selected) < count // 2:
                selected.append(concept)
                used_topics.add(concept["topic_key"])
        
        return selected
    
    def generate_concept_post(self, topic_name: str, concept: str, variation: str = "worked example") -> Dict:
        """Generate an educational LinkedIn post about a specific concept"""
        prompt = f"""
You are a data engineering professional sharing knowledge on LinkedIn.

{POST_STYLE}

Create a simple educational LinkedIn post about this {topic_name} concept:

CONCEPT: {concept}

VARIATION FOR THIS POST: {variation}

Your post should:
1. Use the requested opening and structure; do not start with a generic question
2. Explain the concept in simple terms with a practical example
3. Share 2-3 key points as bullet points
4. Mention a common mistake to avoid
5. End with a useful rule, recommendation, or a specific question

CRITICAL RULES:
- NO emojis or emoticons anywhere in the post
- Add line breaks after sentences for readability
- Keep paragraphs short (1-2 sentences each)
- Sound like you're explaining to a colleague, not lecturing
- Use simple everyday language
- Do not invent first-person experience, projects, benchmarks, or claims about "my team"
- Clearly label any scenario as an example
- Do not include hashtags

Also create an image prompt for Nano Banana AI image generator.

IMPORTANT: Respond in valid JSON format only:
{{
    "post_content": "The LinkedIn post text with NO emojis, no hashtags, and proper line breaks",
    "image_prompt": "Detailed prompt for Nano Banana image generation",
    "key_topic": "{topic_name}: {concept}"
}}
"""
        
        system_prompt = "You are a senior data engineer who loves teaching. Create engaging, educational content. Respond with valid JSON only."
        
        result = generate_with_json(self.provider, prompt, system_prompt)
        
        if result.get("template_mode"):
            return self._generate_template_concept_post(topic_name, concept)

        result["post_content"] = clean_post_content(result.get("post_content", ""))
        result["topic"] = topic_name
        result["concept"] = concept
        result["post_type"] = "concept"
        return result
    
    def _generate_template_concept_post(self, topic_name: str, concept: str) -> Dict:
        """Generate a template concept post when AI is not available"""
        post_content = f"""{topic_name} concept worth knowing: {concept}

I've seen many engineers overlook this one.

Here's the quick breakdown:

What it is:
{concept} is a technique that can make a real difference in your day-to-day work.

When to use it:
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

Common mistake to avoid:
[Add the pitfall here]

The best next step is to test this pattern on one small workload before standardizing it."""

        image_prompt = f"Educational infographic style visualization of {concept} in {topic_name}, modern tech aesthetic, gradient blue and purple colors, clean layout with icons, professional LinkedIn style, no text in image"
        
        return {
            "post_content": post_content,
            "image_prompt": image_prompt,
            "key_topic": f"{topic_name}: {concept}",
            "topic": topic_name,
            "concept": concept,
            "post_type": "concept",
            "template_mode": True
        }
    
    def generate_batch_concept_posts(self, count: int = 2) -> List[Dict]:
        """Generate multiple concept posts"""
        concepts = self.get_random_concepts(count)
        posts = []
        
        variations = [
            "Start with a concrete example and teach the concept by walking through it.",
            "Start with a common implementation mistake and build a practical checklist.",
            "Use a before-and-after comparison with a concise closing recommendation.",
        ]
        for index, concept_info in enumerate(concepts):
            print(f"📚 Generating concept post: {concept_info['topic_name']} - {concept_info['concept'][:40]}...")
            post = self.generate_concept_post(
                concept_info["topic_name"],
                concept_info["concept"],
                variation=variations[index % len(variations)],
            )
            if post.get("post_content"):
                posts.append(post)
        
        return posts
    
    def generate_specific_concept_post(self, topic_key: str, concept_index: int = None) -> Dict:
        """Generate a post for a specific topic"""
        if topic_key not in self.topics:
            available = ", ".join(self.topics.keys())
            raise ValueError(f"Topic '{topic_key}' not found. Available: {available}")
        
        topic_data = self.topics[topic_key]
        
        if concept_index is None:
            concept = random.choice(topic_data["advanced_concepts"])
        else:
            concept = topic_data["advanced_concepts"][concept_index]
        
        return self.generate_concept_post(topic_data["name"], concept)


class TipOfTheDayGenerator:
    """Generates quick tip posts for daily engagement"""
    
    def __init__(self):
        self.provider = get_ai_provider()
    
    def generate_quick_tip(self, topic: str = None) -> Dict:
        """Generate a quick tip post (shorter format)"""
        if topic is None:
            topics = ["SQL", "Python", "PostgreSQL", "Spark", "Data Engineering", "ETL"]
            topic = random.choice(topics)
        
        prompt = f"""
Create a quick LinkedIn tip post about {topic}.

Format:
- Start with a simple hook like "Quick {topic} tip:" or "One thing about {topic}:"
- One practical, actionable tip
- Brief code snippet or example if applicable
- Maximum 100 words
- NO emojis or emoticons
- Do not include hashtags

Also provide an image prompt for Nano Banana.

IMPORTANT: Respond in valid JSON:
{{
    "post_content": "The quick tip post with NO emojis",
    "image_prompt": "Image prompt for Nano Banana",
    "topic": "{topic}"
}}
"""
        
        result = generate_with_json(
            self.provider, 
            prompt, 
            "Create concise, valuable tips. NO emojis. Respond with valid JSON only."
        )
        
        if result.get("template_mode"):
            return {
                "post_content": f"""Quick {topic} tip:

[Your tip here]

Example:
```
[Your code example]
```

Apply it first to one small example, then compare the result before using it more broadly.""",
                "image_prompt": f"Clean minimalist tip card design for {topic}, modern gradient background, icon representing the concept, professional LinkedIn style",
                "topic": topic,
                "post_type": "quick_tip",
                "template_mode": True
            }
        
        result["post_content"] = clean_post_content(result.get("post_content", ""))
        result["post_type"] = "quick_tip"
        return result


if __name__ == "__main__":
    print("🧪 Testing Concept Post Generator (FREE AI)...\n")
    
    generator = ConceptPostGenerator()
    concepts = generator.get_random_concepts(2)
    
    print("Selected concepts:")
    for c in concepts:
        print(f"  - {c['topic_name']}: {c['concept']}")
    
    print("\n" + "="*60)
    print("Generating first concept post...")
    print("="*60)
    
    if concepts:
        post = generator.generate_concept_post(
            concepts[0]["topic_name"],
            concepts[0]["concept"]
        )
        print("\n📱 GENERATED POST:")
        print(post.get("post_content", "No content generated"))
        print("\n🎨 IMAGE PROMPT:")
        print(post.get("image_prompt", "No prompt generated"))
