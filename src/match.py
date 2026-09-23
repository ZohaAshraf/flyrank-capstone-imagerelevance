"""
End-to-end matching: given a post, embed it, rank all images, run the
mismatch guard on the top candidate, and save a Suggestion row.
"""

from src.db.session import SessionLocal, init_db
from src.db.models import Image, ImageVector, Post, PostVector, Suggestion
from src.embeddings.client import embed_text
from src.embeddings.similarity import rank_images
from src.guard.mismatch_guard import evaluate


def match_post_to_image(post_id: str) -> Suggestion:
    init_db()
    session = SessionLocal()

    post = session.get(Post, post_id)
    if post.vector is None:
        embedding = embed_text(post.body)
        post.vector = PostVector(post_id=post.id, embedding=embedding)
        session.commit()
    else:
        embedding = post.vector.embedding

    images = session.query(Image).all()
    image_embeddings = {}
    for img in images:
        if img.vector is None:
            img.vector = ImageVector(image_id=img.id, embedding=embed_text(img.caption))
            session.commit()
        image_embeddings[img.id] = img.vector.embedding

    ranked = rank_images(embedding, image_embeddings)

    if not ranked:
        suggestion = Suggestion(
            post_id=post.id, image_id=None, similarity_score=None,
            guard_result="no_match", guard_reason="No images available",
        )
    else:
        top_image_id, top_score = ranked[0]
        top_image = session.get(Image, top_image_id)

        
        decision = evaluate(
    image_subject=top_image.subject,
    image_category=top_image.category,
    expected_subject=post.expected_category,  # reused field, now holds a subject keyword like "fox"
    similarity_score=top_score,
    image_confidence=top_image.confidence,
)

        suggestion = Suggestion(
            post_id=post.id,
            image_id=top_image.id if decision.accepted else None,
            similarity_score=top_score,
            guard_result="accepted" if decision.accepted else "rejected",
            guard_reason=decision.reason,
        )

    session.add(suggestion)
    session.commit()
    session.refresh(suggestion)
    session.close()
    return suggestion