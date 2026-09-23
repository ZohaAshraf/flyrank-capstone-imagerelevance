import os
from dotenv import load_dotenv

load_dotenv()
print("KEY LOADED:", repr(os.environ.get("GEMINI_API_KEY")))

from src.vision.client import classify_image

result = classify_image("data/images/wolf_01.jpg")
print(result.model_dump_json(indent=2))