"""
Vision client — sends an image to Gemini Flash and returns validated,
structured metadata matching the ImageMetadata schema.

Never trusts raw model output: every response is schema-validated before
being returned. Invalid or malformed responses raise, they are never
silently accepted (per DESIGN.md).
"""

import os

from google import genai
from dotenv import load_dotenv
from pydantic import ValidationError

from src.vision.schema import ImageMetadata

load_dotenv()

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

_PROMPT = """
Look at this image and respond with ONLY a JSON object (no markdown, no
extra text) matching exactly this shape:

{
  "subject": "<main subject, e.g. 'red fox'>",
  "category": "<coarse bucket, e.g. 'animal', 'landscape', 'object'>",
  "attributes": ["<short descriptive tag>", "..."],
  "caption": "<one-sentence natural-language description>",
  "confidence": <float between 0 and 1, your own confidence in this tagging>
}
"""


def classify_image(image_path: str) -> ImageMetadata:
    """
    Send one image to Gemini Flash and return validated metadata.

    Raises pydantic.ValidationError if the model's response doesn't match
    the required schema — callers must catch this and flag/retry rather
    than trust the raw output.
    """
    uploaded_file = _client.files.upload(file=image_path)

    response = _client.models.generate_content(
        model="gemini-flash-latest",
        contents=[uploaded_file, _PROMPT],
    )

    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json\n", "", 1)

    try:
        return ImageMetadata.model_validate_json(raw_text)
    except ValidationError as e:
        raise ValidationError(f"Gemini response failed schema validation: {e}") from e