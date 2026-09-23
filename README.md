# AI Image Understanding & Content Matching Engine

FlyRank Backend Track capstone. Given a library of images and a set of blog
posts, this system understands what's actually in each image (vision AI),
matches the right image to the right post by meaning (semantic embeddings),
and — most importantly — refuses to suggest a wrong match (the mismatch
guard).

Example: a post about red foxes gets the red-fox photo. A similar-looking
wolf photo is rejected, with a reason.

## Status
🚧 Phase 1 — Design (just getting started)

## Stack
- Python + FastAPI
- Gemini Flash (free tier) for vision + embeddings, or local Ollama as a
  fallback
- PostgreSQL for storage
- Pydantic schema validation on every AI response

## How to run
_(to be filled in once the app boots — see `capstone.yaml`)_

## Architecture
_(diagram + explanation to be added in Phase 3/4)_

## Limitations
_(to be filled in honestly as the project develops)_
