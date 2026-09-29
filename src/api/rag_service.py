"""
PAIMANA AI - RAG Service Re-export Shim for Backward Compatibility
"""

from src.api.rag.gemini_client import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    check_gemini_health,
    query_gemini,
)
from src.api.rag.ollama_client import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    MAX_PROMPT_CHARS,
    sanitize_user_input,
    check_ollama_health,
    query_ollama,
)
from src.api.rag.retriever import HybridRetriever, safe_parse_json
from src.api.rag.prompts import generate_template_response
from src.api.rag.service import ProjectIntelligenceService

__all__ = [
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "check_gemini_health",
    "query_gemini",
    "OLLAMA_BASE_URL",
    "OLLAMA_MODEL",
    "MAX_PROMPT_CHARS",
    "sanitize_user_input",
    "check_ollama_health",
    "query_ollama",
    "HybridRetriever",
    "safe_parse_json",
    "generate_template_response",
    "ProjectIntelligenceService",
]
