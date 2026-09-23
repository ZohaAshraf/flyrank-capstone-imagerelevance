"""
Cosine similarity for ranking image embeddings against a post embedding.
"""

import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def rank_images(post_embedding: list[float], image_embeddings: dict[str, list[float]]) -> list[tuple[str, float]]:
    """
    Given a post's embedding and a dict of {image_id: embedding}, return a
    list of (image_id, similarity_score) sorted highest first.
    """
    scored = [
        (image_id, cosine_similarity(post_embedding, emb))
        for image_id, emb in image_embeddings.items()
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)