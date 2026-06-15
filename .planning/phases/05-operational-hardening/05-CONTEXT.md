# Phase 5: Operational hardening - Context

**Gathered:** 2026-06-15
**Status:** Ready for planning

<domain>
## Phase Boundary
Prove the reusable Instagram content system is reproducible, verifiable, and safe to reuse.

This phase focuses on validation, evidence, deterministic outputs, image verification, and the feedback loop that turns approvals/rejections into better future runs. It does not redefine the core brand rules; it checks and reinforces them.
</domain>

<decisions>
## Implementation Decisions

### Hardening scope
- Hardening includes output verification, reproducibility checks, and operational safety.
- The phase must verify that the bootstrap and workflow produce the expected artifacts in a clean environment.
- Failures should be specific, actionable, and should not leave confusing partial state behind.

### Image verification
- Generated images must be checked against the approved brief, cards, and project-spec visual rules.
- The verification step belongs in hardening because it proves the output matches what was requested before approval or publication.
- Image verification should leave an audit trail in the approval bundle or manifest notes.

### Feedback-driven improvement
- If a post is changed or rejected, the workflow should capture the user feedback.
- That feedback should be folded back into the project documentation so the next run is more accurate.
- Repeated mistakes should be promoted into explicit rules or prohibited patterns where appropriate.
- The improvement loop should update project docs, not silently mutate the shared bootstrap.

### Verification style
- Prefer automated checks with human-readable reports.
- Include dry-run behavior where it helps prove the workflow without side effects.
- Verify both structure and content, including traceability and approval-gate behavior.
</decisions>

<specifics>
## Specific Ideas
- The user wants image verification to ensure generated assets match the requested output.
- The user wants rejected or revised posts to improve future documentation and results.
</specifics>

<canonical_refs>
## Canonical References
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `docs/insta-creator-system-spec.md`
- `docs/insta-creator-project-spec-contract.md`
- `docs/insta-creator-storage-contract.md`
</canonical_refs>

<deferred>
## Deferred Ideas
- Exact mechanism for image similarity or rubric-based visual checks.
- Exact destination and format for captured feedback notes.
- Whether repeated rejection patterns should auto-open documentation tasks.
</deferred>

---
*Phase: 05-operational-hardening*
*Context gathered: 2026-06-15*
