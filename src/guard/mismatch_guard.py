"""
The mismatch guard — decides whether the top-ranked image is actually a
good enough match, or should be rejected/marked "no confident match".
Combines subject/category match, similarity threshold, and confidence
floor, per DESIGN.md.
"""

from dataclasses import dataclass

SIMILARITY_THRESHOLD = 0.65
CONFIDENCE_FLOOR = 0.60


@dataclass
class GuardDecision:
    accepted: bool
    reason: str


def evaluate(
    image_subject: str,
    image_category: str,
    expected_subject: str | None,
    similarity_score: float,
    image_confidence: float,
) -> GuardDecision:
    if expected_subject and expected_subject.lower() not in image_subject.lower():
        return GuardDecision(
            accepted=False,
            reason=f"Subject mismatch: expected '{expected_subject}', detected '{image_subject}'",
        )

    if similarity_score < SIMILARITY_THRESHOLD:
        return GuardDecision(
            accepted=False,
            reason=f"Similarity too low: {similarity_score:.2f} (threshold {SIMILARITY_THRESHOLD})",
        )

    if image_confidence < CONFIDENCE_FLOOR:
        return GuardDecision(
            accepted=False,
            reason=f"Image confidence too low: {image_confidence:.2f} (floor {CONFIDENCE_FLOOR})",
        )

    return GuardDecision(accepted=True, reason="Passed all checks")