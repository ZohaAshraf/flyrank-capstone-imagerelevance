# AI Image Understanding & Content Matching Engine

> FlyRank Backend Track Capstone — matches blog posts to the right image using vision AI tagging and semantic embeddings, with a mismatch guard that rejects wrong pairings instead of guessing.

[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

Given a library of images and a set of blog posts, this system automatically suggests the right image for each post — based on what the image actually *means*, not filenames or keywords.

Just as important as finding a good match is **refusing a bad one**. A similar-looking but wrong image (a wolf on a fox post, for example) is rejected with a human-readable explanation, rather than guessed. That refusal behavior — the **mismatch guard** — is the core engineering focus of this project.

**Behavior this system targets:**
- A blog post about red foxes surfaces a red-fox image
- A similar-looking wolf image is rejected, with a stated reason
- When no image is a good enough match, the system says so explicitly

---

## Architecture

```
Images —(batch job, retries)→ Vision Model (Gemini) → {subject, category,
                                                          attributes, caption,
                                                          confidence}
                                                              │
                                                    image_metadata (DB)
                                                              │
                                              embed(caption) → image_vectors (DB)

Posts ─────────────────────→ embed(post body) ──────────→ post_vectors (DB)

POST /posts/{id}/match
  │
  ├─→ Similarity Ranking      (cosine similarity: image_vectors × post_vector)
  │
  ├─→ Mismatch Guard          (subject match + similarity threshold + confidence floor)
  │
  └─→ Suggestion (DB)         accepted / rejected / no_match — always with a reason

GET  /suggestions/{id}        inspect why an image was selected or refused
POST /suggestions/{id}/review approve or reject a suggested pairing
```

Full design rationale, the image metadata schema, and the database schema are documented in [`DESIGN.md`](DESIGN.md).

---

## Stack

| Layer | Choice |
|---|---|
| Language / framework | Python 3.14, FastAPI |
| Persistence | PostgreSQL (via Docker), SQLAlchemy ORM |
| Vision model | Gemini Flash (free tier) |
| Embeddings | Gemini embeddings (free tier) |
| Schema validation | Pydantic |
| Retry handling | Tenacity (exponential backoff) |
| Testing | pytest |

Everything above is free with no credit card, per the capstone's $0 constraint.

---

## Getting Started

### 1. Clone and set up the environment

```bash
git clone https://github.com/ZohaAshraf/flyrank-capstone-imagerelevance.git
cd flyrank-capstone-imagerelevance

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in real values:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:devpassword@localhost:5432/imagerelevance
ENVIRONMENT=development
```

Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — no card required.

### 3. Start PostgreSQL

```bash
docker run --name imagerelevance-db \
  -e POSTGRES_PASSWORD=devpassword \
  -e POSTGRES_DB=imagerelevance \
  -p 5432:5432 -d postgres:16
```

### 4. Seed the database

```bash
python seed_eval_set.py
```

### 5. Run the vision batch job

```bash
python -m src.vision.batch
```

> **Note:** Gemini's free tier caps at 20 requests/day per model. A full ~45-image corpus is processed incrementally across a few days. The batch job automatically skips already-processed images, so it can be safely re-run daily until the full corpus is tagged.

### 6. Start the API

```bash
uvicorn src.api.main:app --reload
```

### 7. Explore it

Open **http://127.0.0.1:8000/docs** for interactive API documentation.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/posts/{post_id}/match` | Run the matching pipeline for a post |
| `GET` | `/suggestions/{suggestion_id}` | Inspect why an image was selected or refused |
| `POST` | `/suggestions/{suggestion_id}/review` | Approve or reject a suggested pairing |
| `GET` | `/suggestions` | List all suggestions |

---

## Project Structure

```
.
├── src/
│   ├── vision/          # Gemini vision client, schema validation, batch job
│   ├── embeddings/      # Text embedding client, cosine similarity ranking
│   ├── guard/           # Mismatch guard decision logic
│   ├── api/             # FastAPI review endpoints
│   ├── db/              # SQLAlchemy models, session setup
│   └── match.py         # Orchestrates: embed → rank → guard → save suggestion
├── tests/               # pytest test suite
├── data/images/         # Image corpus
├── DESIGN.md            # Schema, matching strategy, database design
├── EVIDENCE.md          # Requirement-by-requirement proof
├── BUILDLOG.md          # Honest log of AI assistance and what broke
└── requirements.txt
```

---

## Limitations

- **Free-tier daily quota** (20 requests/day/model) means the full image corpus is processed incrementally across several days rather than in a single run.
- **Similarity threshold** (currently `0.65`) was hand-tuned on a small initial sample. A larger labeled evaluation set would support more rigorous, data-driven tuning — see `EVIDENCE.md` for current status.
- **Review workflow is API-only.** No frontend UI is included; per the capstone's scope, validated endpoints and a listing view are sufficient.
- **Cost tracking** is currently a placeholder (`$0.00`) — real per-call metering against Gemini's usage dashboard is a planned refinement.

---

## Further Reading

- [`DESIGN.md`](DESIGN.md) — problem statement, image metadata schema, matching & guard strategy, database design
- [`EVIDENCE.md`](EVIDENCE.md) — proof for every requirement in the capstone brief
- [`BUILDLOG.md`](BUILDLOG.md) — where AI tools helped, what broke, and what changed

---

## License

MIT — see [`LICENSE`](LICENSE).