"""
Batch processing for image classification.

Runs classify_image() over a folder of images with retries and per-call
cost tracking, saving results to the database. Per DESIGN.md and the
brief's requirement that vision calls run as background batch jobs with
retries, never blocking a single request.
"""

from dataclasses import dataclass
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential

from src.vision.client import classify_image
from src.vision.schema import ImageMetadata
from src.db.session import SessionLocal, init_db
from src.db.models import Image

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
    return classify_image(image_path)


def run_batch(image_dir: str) -> list[BatchResult]:
    init_db()
    session = SessionLocal()
    results: list[BatchResult] = []
    image_paths = sorted(
        p for p in Path(image_dir).iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )

    for path in image_paths:
        try:
            metadata = _classify_with_retry(str(path))
            results.append(
                BatchResult(str(path), metadata, True, None, COST_PER_CALL_USD)
            )
            db_image = Image(
                file_path=str(path),
                subject=metadata.subject,
                category=metadata.category,
                attributes=metadata.attributes,
                caption=metadata.caption,
                confidence=metadata.confidence,
                flagged=metadata.is_low_confidence,
                cost_usd=COST_PER_CALL_USD,
            )
            session.add(db_image)
            session.commit()
            print(f"[OK] {path.name} -> {metadata.subject} (confidence={metadata.confidence})")
        except Exception as e:
            results.append(BatchResult(str(path), None, False, str(e), 0.0))
            print(f"[FAILED after retries] {path.name} -> {e}")

    session.close()
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