"""
The mismatch guard — decides whether the top-ranked image is actually a
good enough match, or should be rejected/marked "no confident match".
Combines category match, similarity threshold, and confidence floor,
per DESIGN.md.
"""

from dataclasses import dataclass

SIMILARITY_THRESHOLD = 0.70
CONFIDENCE_FLOOR = 0.60


@dataclass
class GuardDecision:
    accepted: bool
    reason: str


def evaluate(
    image_category: str,
    expected_category: str | None,
    similarity_score: float,
    image_confidence: float,
) -> GuardDecision:
    """
    Runs the three checks in order and returns the first failure reason,
    or an acceptance if all three pass.
    """
    if expected_category and image_category != expected_category:
        return GuardDecision(
            accepted=False,
            reason=f"Category mismatch: expected '{expected_category}', detected '{image_category}'",
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