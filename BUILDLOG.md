# Build Log

Tracks where AI tools helped, where they were wrong, and what I changed.
Kept honest and updated as I go — this is graded on honesty, not polish.

## 2026-09-23
- Repo created, folder skeleton set up (src/, data/, tests/, required docs).
- No AI-generated code yet — this session was scaffolding only.
## 2026-09-23
- Vision client hit two breaking changes: `google.generativeai` package was
  fully deprecated (migrated to `google-genai`), and the model name
  `gemini-2.0-flash-001` was retired (switched to `gemini-flash-latest`).
  Verified working end-to-end on both fox and wolf test images.