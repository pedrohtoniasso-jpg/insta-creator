# Content Workflow Contract

This document defines the reusable shared workflow that turns an idea into an approval-ready content package.

## Workflow order
1. Build a brief from the idea and the project spec.
2. Generate cards JSON and caption content in parallel.
3. Validate the generated artifacts.
4. Assemble the approval package.
5. Store everything in a deterministic per-post folder.

## Deterministic folder layout
Each post lives in its own folder under the project-configured storage root, with a local default of `content/posts/`.

Expected files:
- `manifest.json`
- `brief.md`
- `cards.json`
- `caption.md`
- `approval.md`
- `assets/`

Recommended naming pattern:
- `YYYY.MM.DD - Short subject`

## Shared artifact roles

### `manifest.json`
The manifest is the traceability anchor. It should record:
- a stable post identifier
- the idea source
- the project spec path or version identifier
- the selected content angle
- artifact filenames
- validation status
- approval status

### `brief.md`
The brief captures the problem, audience, angle, content objective, risks, and CTA direction.

### `cards.json`
Cards are structured JSON. They must be deterministic, ordered, easy to validate, and shaped like a single narrative rather than disconnected mini-posts.

### `caption.md`
The caption should keep a predictable structure that supports the same narrative arc as the cards: hook, body, CTA, hashtags.

### `approval.md`
The approval package should summarize the chosen direction and provide the reviewer with everything needed in one place.

## Traceability rules
- Every artifact must reference the same post identifier.
- The brief, cards, caption, and approval package must all point back to the originating idea.
- Revisions should preserve the same folder and increment the traceability metadata rather than scattering files.

## Validation rules
- Cards JSON must be syntactically valid and schema-compatible.
- The content package must contain all required files before approval.
- The workflow must remain generic and must not absorb project-specific branding rules.

## Notes
- Project-specific rules belong in the project spec, not in this shared contract.
- Approval-gated reply drafts, when relevant, are included in the approval package rather than as loose files.
