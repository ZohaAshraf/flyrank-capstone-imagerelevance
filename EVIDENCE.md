# Evidence

One pasted proof per requirement checkbox from Section 6 of the capstone
brief (a test output, curl transcript, or log line). Filled in as each
requirement is actually done — a claim with no evidence here counts as
not done.

## AI processing
- [ ] Vision model produces structured, schema-validated output
- [ ] Low-confidence classifications are flagged, not accepted
- [ ] Images processed via batch background job with retries

## Matching system
- [ ] Vision/embedding costs tracked per call
- [ ] Image and post embeddings stored; posts return ranked suggestions
- [ ] Semantic matching works for equivalent concepts

## Safety layer
- [ ] Mismatch guard rejects incorrect recommendations
- [ ] Rejections include a human-readable explanation
- [ ] "No confident match" case handled with reasons

## Backend
- [ ] Database models + indexes for images, tags, embeddings, posts, suggestions, approvals/rejections
- [ ] API endpoints validated; review workflow (approve/reject/inspect) exists

## Quality & documentation
- [ ] Labeled eval dataset measures top-1 precision (number in README)
- [ ] README has architecture explanation + diagram; required files present
## Vision processing
- Vision model produces structured output validated against schema: see `src/vision/schema.py`, `tests/test_schema.py` (4/4 tests pass)
- Batch job with retries: `src/vision/batch.py`, run via `python -m src.vision.batch`, both fox_01.jpg and wolf_01.jpg tagged successfully

## Matching system
- Semantic matching works: fox post matched fox image with similarity 0.69
- Command: `python test_match_manual.py`
- Output:
Guard result: accepted
Reason: Passed all checks
Image ID: 3726be41-2946-4160-bf87-70b7d87b0b02
Similarity score: 0.6905698244106772

## Safety layer (mismatch guard)
- Guard rejects wolf-as-fox scenario with explanation (Probe 3)
- Command: `python test_guard_reject.py`
- Output:
Accepted: False
Reason: Subject mismatch: expected 'fox', detected 'gray wolf'