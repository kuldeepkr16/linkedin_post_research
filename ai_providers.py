"""
AI Provider Module
Supports multiple FREE AI backends: Groq, Ollama, or Template-based
"""

import json
import re
import requests
from typing import Dict, Optional
from abc import ABC, abstractmethod

from config import (
    AI_PROVIDER,
    GROQ_API_KEY,
    GROQ_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    POST_STYLE,
)


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        pass


class GroqProvider(AIProvider):
    """Groq API provider."""

    FALLBACK_MODEL = "openai/gpt-oss-120b"
    
    def __init__(self):
        try:
            from groq import Groq
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model = GROQ_MODEL
        except ImportError:
            raise ImportError("Please install groq: pip install groq")
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            if getattr(e, "status_code", None) == 404 and self.model != self.FALLBACK_MODEL:
                print(
                    f"⚠️ Groq model '{self.model}' is unavailable. "
                    f"Retrying with '{self.FALLBACK_MODEL}'..."
                )
                try:
                    response = self.client.chat.completions.create(
                        model=self.FALLBACK_MODEL,
                        messages=messages,
                        temperature=0.8,
                        max_tokens=2000,
                    )
                    self.model = self.FALLBACK_MODEL
                    return response.choices[0].message.content
                except Exception as fallback_error:
                    print(f"⚠️ Groq fallback error: {fallback_error}")
                    return ""

            print(f"⚠️ Groq API error: {e}")
            return ""


class OllamaProvider(AIProvider):
    """Ollama local provider (FREE, runs locally)"""
    
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
                    "stream": False,
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                print(f"⚠️ Ollama error: {response.status_code}")
                return ""
        except Exception as e:
            print(f"⚠️ Ollama error: {e}")
            print("Make sure Ollama is running: ollama serve")
            return ""


class GeminiProvider(AIProvider):
    """Google Gemini API provider (FREE tier)"""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = GEMINI_MODEL
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            url = f"{self.base_url}/{self.model}:generateContent"
            headers = {
                "x-goog-api-key": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.8, "maxOutputTokens": 2000},
            }
            if system_prompt:
                payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                return ""

            error_message = ""
            try:
                error_message = response.json().get("error", {}).get("message", "")
            except (ValueError, AttributeError):
                pass

            suffix = f" - {error_message}" if error_message else ""
            print(f"⚠️ Gemini API error: HTTP {response.status_code}{suffix}")
            return ""
        except requests.RequestException as e:
            print(f"⚠️ Gemini API request failed: {type(e).__name__}: {e}")
            return ""
        except Exception as e:
            print(f"⚠️ Gemini API error: {type(e).__name__}: {e}")
            return ""


class TemplateProvider(AIProvider):
    """Template-based provider (No AI needed)"""
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        # This returns a template that the user can fill in
        return "TEMPLATE_MODE"


def get_ai_provider() -> AIProvider:
    """Get the configured AI provider"""
    provider = AI_PROVIDER.lower()
    
    if provider == "groq":
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            print("⚠️ GROQ_API_KEY not set. Get FREE key from: https://console.groq.com/keys")
            print("Falling back to template mode...")
            return TemplateProvider()
        return GroqProvider()
    
    elif provider == "ollama":
        return OllamaProvider()

    elif provider == "gemini":
        if not GEMINI_API_KEY:
            print("⚠️ GEMINI_API_KEY not set. Get a key from: https://aistudio.google.com/apikey")
            if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
                print("Falling back to Groq...")
                return GroqProvider()
            print("Falling back to template mode...")
            return TemplateProvider()

        # Google AI Studio API keys currently use the standard Google API-key
        # form (typically beginning with 'AIza'). Tokens such as 'AQ.A...' are
        # OAuth-style credentials and are rejected by generateContent.
        if not GEMINI_API_KEY.startswith("AIza"):
            print("⚠️ GEMINI_API_KEY does not look like a Google AI Studio API key.")
            print("Create one at: https://aistudio.google.com/apikey")
            if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
                print("Falling back to Groq...")
                return GroqProvider()
            print("Falling back to template mode...")
            return TemplateProvider()

        return GeminiProvider()

    else:
        return TemplateProvider()


def _decode_json_string(value: str) -> str:
    """Decode one JSON string value captured without its surrounding quotes."""
    try:
        return json.loads(f'"{value}"', strict=False).strip()
    except json.JSONDecodeError:
        return value.replace('\\n', '\n').replace('\\"', '"').strip()


def _parse_json_response(response: str) -> Optional[Dict]:
    """Parse model JSON, tolerating code fences and literal control characters."""
    clean_response = response.strip()

    if clean_response.startswith("```"):
        clean_response = re.sub(r"^```(?:json)?\s*", "", clean_response, count=1, flags=re.IGNORECASE)
        clean_response = re.sub(r"\s*```$", "", clean_response, count=1)

    json_start = clean_response.find("{")
    json_end = clean_response.rfind("}")
    candidates = [clean_response]
    if json_start != -1 and json_end > json_start:
        candidates.insert(0, clean_response[json_start:json_end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            try:
                # Models sometimes put literal newlines/tabs inside JSON strings.
                parsed = json.loads(candidate, strict=False)
            except json.JSONDecodeError:
                continue
        if isinstance(parsed, dict):
            for field in ("post_content", "image_prompt"):
                if isinstance(parsed.get(field), str):
                    parsed[field] = parsed[field].strip()
            return parsed

    # Salvage individual string fields from a truncated JSON object. This is
    # common when a model hits its output-token limit after post_content.
    field_pattern = r'"{name}"\s*:\s*"((?:\\.|[^"\\])*)"'
    post_match = re.search(field_pattern.format(name="post_content"), clean_response, re.DOTALL)
    if post_match:
        result: Dict = {
            "post_content": _decode_json_string(post_match.group(1)),
            "image_prompt": "",
        }
        image_match = re.search(field_pattern.format(name="image_prompt"), clean_response, re.DOTALL)
        topic_match = re.search(field_pattern.format(name="key_topic"), clean_response, re.DOTALL)
        if image_match:
            result["image_prompt"] = _decode_json_string(image_match.group(1))
        if topic_match:
            result["key_topic"] = _decode_json_string(topic_match.group(1))
        result["recovered"] = True
        return result

    return None


def generate_with_json(provider: AIProvider, prompt: str, system_prompt: str = "") -> Dict:
    """Generate content and parse it as a structured JSON post."""
    response = provider.generate(prompt, system_prompt)
    
    if response == "TEMPLATE_MODE":
        return {"template_mode": True}
    
    if not response:
        return {"post_content": "", "image_prompt": "", "error": "Empty response"}
    
    parsed = _parse_json_response(response)
    if parsed is not None:
        return parsed

    # Plain-text output can still be useful, but a broken JSON object should
    # never be displayed to the user as if it were a finished LinkedIn post.
    if response.lstrip().startswith("{"):
        return {
            "post_content": "",
            "image_prompt": "",
            "error": "Could not parse structured AI response",
        }

    return {"post_content": response.strip(), "image_prompt": "", "raw": True}
