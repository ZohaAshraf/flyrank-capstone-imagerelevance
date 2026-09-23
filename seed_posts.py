"""
Creates a couple of test blog posts in the database so we can run the
full matching pipeline end-to-end. Throwaway/dev script.
"""

from src.db.session import SessionLocal, init_db
from src.db.models import Post

init_db()
session = SessionLocal()

posts = [
    Post(
        title="The secret life of red foxes",
        body="Red foxes are cunning, adaptable animals found across forests "
             "and even cities. This post explores their hunting habits, "
             "family structure, and why they thrive where other wild "
             "animals struggle.",
        expected_category="animal",
    ),
    Post(
        title="How gray wolves shaped North American ecosystems",
        body="Gray wolves are apex predators whose presence reshapes entire "
             "food webs. We look at wolf pack behavior and their return to "
             "Yellowstone.",
        expected_category="animal",
    ),
]

for p in posts:
    session.add(p)
session.commit()

for p in posts:
    print(f"Created post: {p.id} — {p.title}")

session.close()