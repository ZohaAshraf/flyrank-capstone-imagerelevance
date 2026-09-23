"""
Tests for the ImageMetadata schema (src/vision/schema.py).

Confirms the schema accepts well-formed vision-model output and rejects
malformed output — the core "never trust invalid model output" rule
from DESIGN.md.
"""

import pytest
from pydantic import ValidationError

from src.vision.schema import ImageMetadata


def test_valid_metadata_is_accepted():
    data = {
        "subject": "red fox",
        "category": "animal",
        "attributes": ["orange fur", "wild", "forest"],
        "caption": "A red fox standing in a forest",
        "confidence": 0.94,
    }
    result = ImageMetadata(**data)
    assert result.subject == "red fox"
    assert result.confidence == 0.94


def test_missing_required_field_is_rejected():
    data = {
        "category": "animal",
        "attributes": ["orange fur"],
        "caption": "A red fox standing in a forest",
        "confidence": 0.94,
        # "subject" missing
    }
    with pytest.raises(ValidationError):
        ImageMetadata(**data)


def test_confidence_out_of_range_is_rejected():
    data = {
        "subject": "red fox",
        "category": "animal",
        "attributes": [],
        "caption": "A red fox standing in a forest",
        "confidence": 1.5,  # invalid — must be between 0 and 1
    }
    with pytest.raises(ValidationError):
        ImageMetadata(**data)


def test_low_confidence_flagging():
    data = {
        "subject": "red fox",
        "category": "animal",
        "attributes": [],
        "caption": "A blurry animal in the forest",
        "confidence": 0.3,
    }
    result = ImageMetadata(**data)
    assert result.is_low_confidence is True