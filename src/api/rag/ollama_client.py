"""
PAIMANA AI - Legacy Ollama Client Shim (Backward Compatibility Layer)
Retained for legacy test harnesses and backwards compatibility.
"""

import os
import httpx
from typing import Optional, Tuple
from src.api.rag.gemini_client import sanitize_user_input

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
MAX_PROMPT_CHARS = 2500


def check_ollama_health(
    ollama_url: str = OLLAMA_BASE_URL,
    default_model: str = OLLAMA_MODEL
) -> Tuple[bool, Optional[str]]:
    """Pings local Ollama endpoint if running, otherwise returns graceful offline state."""
    try:
        with httpx.Client(timeout=1.0) as client:
            res = client.get(f"{ollama_url.rstrip('/')}/api/tags")
            if res.status_code == 200:
                data = res.json()
                model_objs = data.get('models', [])
                if not model_objs:
                    return False, None
                model_names = [m.get('name', '') for m in model_objs]
                model_bases = [m.split(':')[0] for m in model_names]
                if default_model in model_bases:
                    return True, default_model
                for full_name in model_names:
                    if default_model in full_name:
                        return True, full_name
                if model_names:
                    return True, model_names[0]
    except Exception:
        pass
    return False, None


def query_ollama(
    ollama_url: str,
    system_context: str,
    user_question: str,
    model_name: str
) -> Optional[str]:
    """Queries Ollama endpoint if reachable, otherwise returns None for deterministic fallback."""
    if not model_name:
        return None
    try:
        clean_q = sanitize_user_input(user_question, max_chars=1000)
        structured_prompt = (
            "<|system|>\n"
            "You are PAIMANA AI, an expert decision-support assistant for Ministry of Statistics & "
            "Programme Implementation (MoSPI) officials.\n"
            f"PROJECT CONTEXT:\n{system_context[:MAX_PROMPT_CHARS]}\n"
            "<|user|>\n"
            f"{clean_q}\n"
            "<|assistant|>\n"
        )
        payload = {
            "model": model_name,
            "prompt": structured_prompt,
            "stream": False,
            "options": {"temperature": 0.1, "top_p": 0.9}
        }
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(f"{ollama_url.rstrip('/')}/api/generate", json=payload)
            if resp.status_code == 200:
                answer = resp.json().get("response", "").strip()
                if answer:
                    return answer
    except Exception:
        pass
    return None
