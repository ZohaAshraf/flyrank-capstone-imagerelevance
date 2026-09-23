# Evidence

One pasted proof per requirement checkbox from Section 6 of the capstone
brief (a test output, curl transcript, or log line). Filled in as each
requirement is actually done — a claim with no evidence here counts as
not done.

## AI processing
- [x] Vision model produces structured, schema-validated output
  - `src/vision/schema.py` + `tests/test_schema.py` — 4/4 tests pass
- [x] Low-confidence classifications are flagged, not accepted
  - `ImageMetadata.is_low_confidence` property, tested in `test_low_confidence_flagging`
- [x] Images processed via batch background job with retries
  - `src/vision/batch.py`, run via `python -m src.vision.batch`
  - Both `fox_01.jpg` and `wolf_01.jpg` tagged successfully with retry wrapper (`tenacity`, 3 attempts, exponential backoff)

## Matching system
- [ ] Vision/embedding costs tracked per call
  - *(cost tracking field exists in DB models, currently hardcoded to 0.0 — free tier usage not yet metered — TODO)*
- [x] Image and post embeddings stored; posts return ranked suggestions
  - `src/embeddings/client.py`, `src/embeddings/similarity.py`, stored via `ImageVector`/`PostVector` models
- [x] Semantic matching works for equivalent concepts
  - Fox post matched fox image with similarity 0.69:
  ```
  Command: python test_match_manual.py
  Guard result: accepted
  Reason: Passed all checks
  Image ID: 3726be41-2946-4160-bf87-70b7d87b0b02
  Similarity score: 0.6905698244106772
  ```

## Safety layer
- [x] Mismatch guard rejects incorrect recommendations
  - `src/guard/mismatch_guard.py`
- [x] Rejections include a human-readable explanation
  - Proof — Probe 3 (wolf forced onto fox post):
  ```
  Command: python test_guard_reject.py
  Accepted: False
  Reason: Subject mismatch: expected 'fox', detected 'gray wolf'
  ```
- [ ] "No confident match" case handled with reasons
  - *(logic exists in `src/match.py` for the empty-images case — not yet tested with a real "no good match" scenario — TODO)*

## Backend
- [x] Database models + indexes for images, tags, embeddings, posts, suggestions, approvals/rejections
  - `src/db/models.py`
- [ ] API endpoints validated; review workflow (approve/reject/inspect) exists
  - *(not yet built — TODO)*

## Quality & documentation
- [ ] Labeled eval dataset measures top-1 precision (number in README)
  - *(not yet built — TODO, needs 10+ labeled posts + larger image corpus)*
- [ ] README has architecture explanation + diagram; required files present
  - *(TODO)*