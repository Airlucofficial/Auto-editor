"""
OpenRouter API Client for AutoEditor.

Provides ultra-low-cost LLM access (DeepSeek-V3, Qwen 2.5) via OpenRouter
for AI-powered video editing decisions.
"""

import json
import os
import time
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

class OpenRouterError(Exception):
    """Custom exception for OpenRouter API errors."""
    pass

def _build_system_prompt(style_profile: Optional[Dict[str, Any]] = None) -> str:
    """Build the video editing system prompt."""
    prompt = (
        "You are a professional video editor AI. "
        "Your task is to analyze transcript data and user creative direction to output a structured video editing plan.\n"
        "You must respond ONLY with valid JSON matching this structure:\n"
        "{\n"
        '  "cuts": [{"timestamp": 12.5, "type": "jump"}],\n'
        '  "sticker_placements": [{"timestamp": 14.0, "concept": "explosion", "position": "center"}],\n'
        '  "text_overlays": [{"timestamp": 5.0, "text": "Wow!", "duration": 2.0}],\n'
        '  "zoom_events": [{"timestamp": 8.0, "scale": 1.2, "duration": 1.5}],\n'
        '  "sfx_events": [{"timestamp": 14.0, "type": "boom"}]\n'
        "}\n"
    )
    if style_profile:
        prompt += f"\nStyle Guidelines:\n{json.dumps(style_profile, indent=2)}\n"
    return prompt

def _parse_llm_response(raw_text: str) -> Dict[str, Any]:
    """Extract JSON from LLM response handling markdown code blocks and partial JSON."""
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except json.JSONDecodeError:
                pass
        raise OpenRouterError(f"Failed to parse JSON from response: {raw_text}")


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODELS_URL = "https://openrouter.ai/api/v1/models"
    
    def __init__(self, config_path: str = 'storage/openrouter_config.json') -> None:
        """Initialize client with config path."""
        self.config_path = config_path
        self._cached_models: List[Dict[str, Any]] = []
        self._models_cache_time = 0.0
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def save_config(self, api_key: Any, preferred_model: Optional[str] = None, tier: str = 'economy') -> None:
        """Save configuration to JSON file."""
        if isinstance(api_key, dict):
            cfg = api_key
            preferred_model = cfg.get("preferred_model", preferred_model)
            tier = cfg.get("tier", tier)
            api_key = cfg.get("api_key", "")
            
        self.config = {
            "api_key": str(api_key or ""),
            "preferred_model": preferred_model,
            "tier": tier,
            "site_name": self.config.get("site_name", "AutoEditor AI"),
            "site_url": self.config.get("site_url", "https://autoeditor.local")
        }
        os.makedirs(os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return bool(self.config.get("api_key"))

    def fetch_models(self) -> List[Dict[str, Any]]:
        """Query models from OpenRouter, caching for 5 minutes."""
        current_time = time.time()
        if self._cached_models and (current_time - self._models_cache_time < 300):
            return self._cached_models
            
        req = urllib.request.Request(self.MODELS_URL)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                models = []
                for m in data.get('data', []):
                    pricing = m.get('pricing', {})
                    prompt_price = float(pricing.get('prompt', 0)) * 1000000
                    completion_price = float(pricing.get('completion', 0)) * 1000000
                    
                    models.append({
                        'id': m.get('id'),
                        'name': m.get('name'),
                        'context_length': m.get('context_length'),
                        'pricing': {'prompt_1M': prompt_price, 'completion_1M': completion_price},
                        'provider': m.get('architecture', {}).get('provider', 'unknown')
                    })
                self._cached_models = models
                self._models_cache_time = current_time
                return models
        except Exception as e:
            raise OpenRouterError(f"Failed to fetch models: {e}")

    def select_optimal_model(self, tier: str = 'economy') -> str:
        """Select model ID based on preferred tier."""
        if tier == 'economy':
            preferences = ['deepseek/deepseek-chat', 'qwen/qwen-2.5-72b-instruct']
        else:
            preferences = ['deepseek/deepseek-r1', 'anthropic/claude-3.5-sonnet']
            
        try:
            models = self.fetch_models()
            available_ids = {m['id'] for m in models}
            for pref in preferences:
                if pref in available_ids:
                    return pref
        except OpenRouterError:
            pass
            
        return preferences[0]

    def estimate_cost(self, text: str, model_id: Optional[str] = None) -> Dict[str, Any]:
        """Estimate token count and cost in dollars."""
        token_count = len(text) // 4
        cost = 0.0
        
        if model_id:
            try:
                models = self.fetch_models()
                for m in models:
                    if m['id'] == model_id:
                        cost = (token_count / 1000000) * m['pricing']['prompt_1M']
                        break
            except OpenRouterError:
                pass
                
        return {
            'tokens': token_count,
            'estimated_cost_usd': cost
        }

    def generate_edit_plan(self, transcript_data: Dict[str, Any], style_profile: Optional[Dict[str, Any]] = None, user_prompt: str = '', mode: str = 'economy') -> Dict[str, Any]:
        """Generate a video editing plan from transcript and user direction."""
        if not self.is_configured():
            raise OpenRouterError("OpenRouter API key not configured.")
            
        model = self.config.get('preferred_model') or self.select_optimal_model(mode)
        system_prompt = _build_system_prompt(style_profile)
        
        user_content = f"Transcript:\n{json.dumps(transcript_data)}\n"
        if user_prompt:
            user_content += f"\nUser Direction:\n{user_prompt}\n"
            
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.config.get("site_url", "https://autoeditor.local"),
            "X-Title": self.config.get("site_name", "AutoEditor AI"),
        }
        
        req = urllib.request.Request(
            self.API_URL, 
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers, 
            method='POST'
        )
        
        retries = 2
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    content = data['choices'][0]['message']['content']
                    return _parse_llm_response(content)
            except urllib.error.HTTPError as e:
                error_msg = e.read().decode('utf-8')
                if attempt == retries:
                    raise OpenRouterError(f"HTTP Error {e.code}: {error_msg}")
            except urllib.error.URLError as e:
                if attempt == retries:
                    raise OpenRouterError(f"Network Error: {e.reason}")
            except Exception as e:
                if attempt == retries:
                    raise OpenRouterError(f"Unexpected Error: {e}")
            time.sleep(2 ** attempt)
            
        raise OpenRouterError("Failed to generate edit plan after retries.")

if __name__ == '__main__':
    client = OpenRouterClient('storage/openrouter_config_test.json')
    try:
        print("Fetching models...")
        models = client.fetch_models()
        print(f"Found {len(models)} models.")
        
        if models:
            first_model = models[0]
            print(f"First model: {first_model['name']} (ID: {first_model['id']})")
            
        text_sample = "This is a sample text used to estimate token usage and cost for the editing API."
        print("\\nEstimating cost for text:")
        print(f"Text: '{text_sample}'")
        cost_est = client.estimate_cost(text_sample, 'deepseek/deepseek-chat')
        print(f"Cost Estimate: {cost_est}")
    except OpenRouterError as e:
        print(f"Error: {e}")
