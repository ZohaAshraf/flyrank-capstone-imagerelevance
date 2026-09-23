"""
Forces the wolf image as a candidate for the fox post, to prove the
mismatch guard rejects a wrong pairing with an explanation.
This is Probe 3 from the FlyRank brief.
"""

from src.guard.mismatch_guard import evaluate

decision = evaluate(
    image_subject="gray wolf",
    image_category="animal",
    expected_subject="fox",
    similarity_score=0.85,  # pretend it ranked highly on similarity
    image_confidence=0.9,
)

print(f"Accepted: {decision.accepted}")
print(f"Reason: {decision.reason}")