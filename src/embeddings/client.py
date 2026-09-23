"""
Embedding client — turns text (image captions, post bodies) into vectors
using Gemini's embedding model, for semantic similarity matching.
"""

import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

EMBEDDING_MODEL = "gemini-embedding-001"


def embed_text(text: str) -> list[float]:
    """Return an embedding vector for the given text."""
    result = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return result.embeddings[0].values