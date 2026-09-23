"""
Creates the labeled eval set: posts paired with their correct expected
image subject. Used to measure top-1 precision (brief Section 7 + 13).
"""

from src.db.session import SessionLocal, init_db
from src.db.models import Post

init_db()
session = SessionLocal()

# (title, body, expected_subject_keyword)
EVAL_POSTS = [
    ("The secret life of red foxes", "Red foxes are cunning, adaptable animals found across forests and cities.", "fox"),
    ("How gray wolves shaped ecosystems", "Gray wolves are apex predators whose presence reshapes food webs.", "wolf"),
    ("Why dogs became humanity's best friend", "Dogs have lived alongside humans for thousands of years.", "dog"),
    ("The grizzly bear's yearly hibernation", "Bears spend months hibernating to survive harsh winters.", "bear"),
    ("Deer populations in suburban areas", "Deer have adapted remarkably well to human-populated regions.", "deer"),
    ("Climbing the world's tallest peaks", "Mountain climbing requires preparation for extreme altitude.", "mountain"),
    ("A guide to the world's best beaches", "Sandy beaches attract millions of tourists every year.", "beach"),
    ("Exploring dense forest ecosystems", "Forests are home to a huge share of the planet's biodiversity.", "forest"),
    ("Surviving in the desert heat", "Desert environments push both plants and animals to extremes.", "desert"),
    ("The history of pizza", "Pizza originated in Naples and became a global favorite.", "pizza"),
    ("The art of sushi making", "Sushi is a Japanese dish combining rice, fish, and precision.", "sushi"),
    ("Building the perfect salad", "A good salad balances greens, protein, and dressing.", "salad"),
    ("What makes a great burger", "Burgers are a staple of casual dining worldwide.", "burger"),
    ("The evolution of the modern car", "Cars have transformed transportation over the last century.", "car"),
    ("Why cycling is booming in cities", "Bicycles are a popular, eco-friendly urban transport option.", "bicycle"),
]

for title, body, expected_subject in EVAL_POSTS:
    post = Post(title=title, body=body, expected_category=expected_subject)
    session.add(post)

session.commit()
print(f"Created {len(EVAL_POSTS)} eval posts.")
session.close()