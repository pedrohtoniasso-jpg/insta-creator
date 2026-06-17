# Content Workflow Contract

This document defines the reusable shared workflow that turns an idea into an approval-ready content package.

## Workflow order
1. Build a brief from the idea and the project spec.
2. Shape the carousel narrative arc before drafting cards.
3. Generate cards JSON and caption content in parallel.
4. Validate the generated artifacts.
5. Run a checklist-driven audit of the draft package.
6. Assemble the approval package.
7. Store everything in a deterministic per-post folder.

## Carousel narrative standard
For carousel posts, the shared workflow should prefer a consistent story arc:
1. Open with the theme or problem.
2. Show the problem with supporting data or evidence.
3. Explain the cause with supporting data or evidence.
4. Connect the issue to the broader audience or population.
5. Offer the organizing principle, rule, or takeaway.
6. End with a dedicated CTA slide that drives the objective.

The default pattern should feel like a single continuous story, not isolated slide-by-slide facts.

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

## Shared typography defaults
For card generation, use these as the starting point unless the project spec overrides them:
- Card title size: 90–110 px, extrabold
- Card subtitle size: 35–50 px, regular
- Sizes may be adjusted during review or audit; these values are the starting working range, not the final locked range.

## Shared audit structure
The audit step should run after draft generation and before final approval. It should be implemented as a checklist of questions, not as a single pass/fail label.

### Audit stages
1. Strategy audit
2. Narrative audit
3. Copy audit
4. Visual audit
5. CTA audit
6. Packaging audit
7. Revision loop audit

### Core rule
Every error, inconsistency, or change request must become a new checklist question for the current or next audit stage so the same issue can be verified in future runs.

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
