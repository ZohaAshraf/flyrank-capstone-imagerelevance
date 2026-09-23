"""
Batch processing for image classification.

Runs classify_image() over a folder of images with retries and per-call
cost tracking, instead of one-off single calls. Per DESIGN.md and the
brief's requirement that vision calls run as background batch jobs with
retries, never blocking a single request.
"""

import time
from dataclasses import dataclass, field
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential

from src.vision.client import classify_image
from src.vision.schema import ImageMetadata

# Gemini Flash free-tier approximate cost per image (placeholder — refine
# once real usage/pricing is confirmed via Google AI Studio dashboard).
COST_PER_CALL_USD = 0.0


@dataclass
class BatchResult:
    file_path: str
    metadata: ImageMetadata | None
    success: bool
    error: str | None
    cost_usd: float


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _classify_with_retry(image_path: str) -> ImageMetadata:
    """Wraps classify_image with retry-with-backoff: 3 attempts, exponential wait."""
    return classify_image(image_path)


def run_batch(image_dir: str) -> list[BatchResult]:
    """
    Classify every image in image_dir. Never raises on a single failure —
    each image's outcome (success or error) is captured in its own
    BatchResult so one bad image doesn't stop the whole batch.
    """
    results: list[BatchResult] = []
    image_paths = sorted(
        p for p in Path(image_dir).iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )

    for path in image_paths:
        try:
            metadata = _classify_with_retry(str(path))
            results.append(
                BatchResult(
                    file_path=str(path),
                    metadata=metadata,
                    success=True,
                    error=None,
                    cost_usd=COST_PER_CALL_USD,
                )
            )
            print(f"[OK] {path.name} -> {metadata.subject} (confidence={metadata.confidence})")
        except Exception as e:
            results.append(
                BatchResult(
                    file_path=str(path),
                    metadata=None,
                    success=False,
                    error=str(e),
                    cost_usd=0.0,
                )
            )
            print(f"[FAILED after retries] {path.name} -> {e}")

    return results


if __name__ == "__main__":
    outcomes = run_batch("data/images")
    total_cost = sum(r.cost_usd for r in outcomes)
    flagged = [r for r in outcomes if r.metadata and r.metadata.is_low_confidence]

    print(f"\nProcessed {len(outcomes)} images.")
    print(f"Succeeded: {sum(1 for r in outcomes if r.success)}")
    print(f"Failed: {sum(1 for r in outcomes if not r.success)}")
    print(f"Flagged (low confidence): {len(flagged)}")
    print(f"Total cost tracked: ${total_cost:.4f}")