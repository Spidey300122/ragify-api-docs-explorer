__version__ = "1.0.0"

from .scraper import APIDocsScraper
from .embeddings import EmbeddingsManager
from .rag import SmartAPIAssistant
from .utils import API_DOCS_URLS

__all__ = ["APIDocsScraper", "EmbeddingsManager", "SmartAPIAssistant", "API_DOCS_URLS"]