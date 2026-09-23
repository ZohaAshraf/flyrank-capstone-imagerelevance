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
