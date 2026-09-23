"""
Downloads a small labeled image corpus from Pexels (free API, no card)
for the capstone's image library. One-off dev script — not part of the
final pipeline. Run once, then delete or keep for reproducibility
(brief Section 3 allows either committing the corpus or a download
script).
"""

import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["PEXELS_API_KEY"]
HEADERS = {"Authorization": API_KEY}
OUTPUT_DIR = "data/images"

# subject: number of images to grab
SUBJECTS = {
    "red fox": 3,
    "gray wolf": 3,
    "dog": 3,
    "bear": 3,
    "deer": 3,
    "mountain landscape": 3,
    "beach": 3,
    "forest": 3,
    "desert": 3,
    "pizza": 3,
    "sushi": 3,
    "salad": 3,
    "burger": 3,
    "car": 3,
    "bicycle": 3,
}

os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_for_subject(query: str, count: int):
    slug = query.replace(" ", "_")
    resp = requests.get(
        "https://api.pexels.com/v1/search",
        headers=HEADERS,
        params={"query": query, "per_page": count},
    )
    resp.raise_for_status()
    photos = resp.json().get("photos", [])

    for i, photo in enumerate(photos, start=1):
        url = photo["src"]["medium"]
        img_data = requests.get(url).content
        filename = f"{OUTPUT_DIR}/{slug}_{i:02d}.jpg"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Saved {filename}")
        time.sleep(0.5)  # be polite to the free API


if __name__ == "__main__":
    total = 0
    for subject, count in SUBJECTS.items():
        download_for_subject(subject, count)
        total += count
    print(f"\nDone. Downloaded ~{total} images into {OUTPUT_DIR}/")