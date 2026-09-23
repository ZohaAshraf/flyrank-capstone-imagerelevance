"""
Pydantic schema for validating vision-model output.

Every image tagging response from the vision model must match this shape
exactly. Anything that fails validation is never trusted — it gets
retried or flagged, per DESIGN.md.
"""

from pydantic import BaseModel, Field


class ImageMetadata(BaseModel):
    subject: str = Field(..., description="Main subject of the image, e.g. 'red fox'")
    category: str = Field(..., description="Coarse bucket, e.g. 'animal', 'landscape', 'object'")
    attributes: list[str] = Field(default_factory=list, description="Short descriptive tags")
    caption: str = Field(..., description="One-sentence natural-language description")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model's self-reported confidence, 0-1")

    @property
    def is_low_confidence(self, threshold: float = 0.6) -> bool:
        """True if this result should be flagged for review instead of trusted."""
        return self.confidence < threshold