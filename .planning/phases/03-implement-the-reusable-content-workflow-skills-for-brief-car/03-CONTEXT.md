# Phase 3: Content workflow skills - Context

**Gathered:** 2026-06-15
**Status:** Ready for planning

<domain>
## Phase Boundary
Implement the reusable workflow skills that turn an idea into a content package.

This phase defines the shared content-production flow: brief creation, cards/JSON generation, caption/CTA/hashtags, approval packaging, and artifact storage conventions. It does not own project-specific branding or the cron source logic.
</domain>

<decisions>
## Implementation Decisions

### Skill architecture
- Use a nucleus-plus-subskills structure.
- Keep one orchestrating skill for the overall flow.
- Split specialized work into smaller skills so brief, cards, caption, and approval logic can evolve independently.
- Keep extension points explicit so future brands can swap only the pieces they need.

### Workflow order
- The flow starts with a brief.
- Cards and caption generation can happen in parallel after the brief is set.
- The approval package is assembled only after the content artifacts are ready.
- The workflow should stay readable and deterministic rather than collapsing everything into one opaque pass.

### Required outputs
- The workflow should produce a brief, cards JSON, caption, and approval package.
- The bundle should also preserve operational metadata and traceability fields so later phases can audit the run.
- Post artifacts must remain organized in a deterministic per-post folder.

### Cards and caption contract
- Cards should be structured JSON, not free-form prose.
- The cards schema should be validated so slide order, objective, and copy structure remain consistent.
- Captions should follow a predictable structure with room for style-based variation.
- Hashtag and CTA handling should remain consistent with the project spec.

### Approval package
- The approval package should include a concise summary plus the full artifacts needed to review the post.
- Reviewers should be able to approve without hunting through multiple scattered files.
- Reply drafts, when relevant, should be included in the approval bundle rather than left out of band.
</decisions>

<specifics>
## Specific Ideas
- Brief first, then cards/caption in parallel, then approval.
- Keep the workflow generic enough to support multiple brands.
</specifics>

<canonical_refs>
## Canonical References
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/phases/01-define-system-architecture-storage-contract-and-project-spec/01-CONTEXT.md`
- `.planning/phases/02-bootstrap-package/02-CONTEXT.md`
</canonical_refs>

<deferred>
## Deferred Ideas
- Exact internal skill names and command boundaries.
- Exact schema shape for the cards JSON.
- Whether the approval package should always include visual previews.
</deferred>

---
*Phase: 03-content-workflow-skills*
*Context gathered: 2026-06-15*
