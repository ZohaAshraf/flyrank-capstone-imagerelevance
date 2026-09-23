"""
Manual test of the full pipeline: embed a post, rank images, run the
guard, print the resulting suggestion. Paste in a real post_id from
seed_posts.py output before running.
"""

from src.match import match_post_to_image

POST_ID = "998c6732-419f-47d7-a8f9-2d00608c2b11"

suggestion = match_post_to_image(POST_ID)

print(f"Guard result: {suggestion.guard_result}")
print(f"Reason: {suggestion.guard_reason}")
print(f"Image ID: {suggestion.image_id}")
print(f"Similarity score: {suggestion.similarity_score}")