"""
Review API — lets a human inspect suggestions and approve/reject them.
Per brief Section 4 (Review API) and Section 6 (review workflow exists).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.db.session import SessionLocal, init_db
from src.db.models import Suggestion, Post, Image
from src.match import match_post_to_image

app = FastAPI(title="AI Image Matching Engine — Review API")


class ReviewDecision(BaseModel):
    status: str  # "approved" or "rejected"


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": "AI Image Matching Engine"}


@app.post("/posts/{post_id}/match")
def create_match(post_id: str):
    """Run the matching pipeline for a post and return the suggestion."""
    session = SessionLocal()
    post = session.get(Post, post_id)
    session.close()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    suggestion = match_post_to_image(post_id)
    return {
        "suggestion_id": suggestion.id,
        "guard_result": suggestion.guard_result,
        "guard_reason": suggestion.guard_reason,
        "image_id": suggestion.image_id,
        "similarity_score": suggestion.similarity_score,
    }


@app.get("/suggestions/{suggestion_id}")
def get_suggestion(suggestion_id: str):
    """Inspect a suggestion — why an image was selected or refused."""
    session = SessionLocal()
    suggestion = session.get(Suggestion, suggestion_id)
    session.close()
    if suggestion is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    return {
        "id": suggestion.id,
        "post_id": suggestion.post_id,
        "image_id": suggestion.image_id,
        "guard_result": suggestion.guard_result,
        "guard_reason": suggestion.guard_reason,
        "similarity_score": suggestion.similarity_score,
        "review_status": suggestion.review_status,
    }


@app.post("/suggestions/{suggestion_id}/review")
def review_suggestion(suggestion_id: str, decision: ReviewDecision):
    """Approve or reject a suggested pairing."""
    if decision.status not in {"approved", "rejected"}:
        raise HTTPException(status_code=400, detail="status must be 'approved' or 'rejected'")

    session = SessionLocal()
    suggestion = session.get(Suggestion, suggestion_id)
    if suggestion is None:
        session.close()
        raise HTTPException(status_code=404, detail="Suggestion not found")

    suggestion.review_status = decision.status
    session.commit()
    session.refresh(suggestion)
    session.close()

    return {"id": suggestion.id, "review_status": suggestion.review_status}


@app.get("/suggestions")
def list_suggestions():
    """List all suggestions — a simple admin table view."""
    session = SessionLocal()
    suggestions = session.query(Suggestion).all()
    result = [
        {
            "id": s.id,
            "post_id": s.post_id,
            "image_id": s.image_id,
            "guard_result": s.guard_result,
            "review_status": s.review_status,
        }
        for s in suggestions
    ]
    session.close()
    return result