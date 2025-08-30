import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAGify")

API_DOCS_URLS = {
    "stripe": [
        "https://stripe.com/docs/api",
        "https://stripe.com/docs/api/payment_intents",
        "https://stripe.com/docs/api/customers",
        "https://stripe.com/docs/api/subscriptions"
    ],
    "github": [
        "https://docs.github.com/en/rest/repos",
        "https://docs.github.com/en/rest/authentication",
        "https://docs.github.com/en/rest/issues",
        "https://docs.github.com/en/rest/users"
    ],
    "twilio": [
        "https://www.twilio.com/docs/sms/api",
        "https://www.twilio.com/docs/voice/api",
        "https://www.twilio.com/docs/usage/api",
        "https://www.twilio.com/docs/messaging/api"
    ]
}

def clean_text(text: str) -> str:
    if not text: return ""
    return " ".join(text.split()).replace('\u00a0', ' ').strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    if len(text) <= chunk_size: return [text]
    
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            # Break at sentence or word boundary
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start + chunk_size // 2:
                end = sentence_end + 1
            else:
                word_end = text.rfind(' ', start, end)
                if word_end > start + chunk_size // 2:
                    end = word_end
        
        chunk = text[start:end].strip()
        if chunk: chunks.append(chunk)
        start = end - overlap
        if start >= len(text): break
    
    return chunks