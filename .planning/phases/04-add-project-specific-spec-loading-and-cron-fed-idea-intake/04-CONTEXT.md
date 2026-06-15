# Phase 4: Project integration and growth ops - Context

**Gathered:** 2026-06-15
**Status:** Ready for planning

<domain>
## Phase Boundary
Connect project-specific specs, cron-fed idea intake, and approval-gated growth workflows to the shared system.

This phase integrates the shared content workflow with project-level branding and operational rules. It does not redefine the shared core; it wires the core to per-project inputs and outbound engagement behavior.
</domain>

<decisions>
## Implementation Decisions

### Project-spec loading
- Each project should keep its own external spec file.
- The shared workflow should read the project spec rather than embed brand rules.
- The spec should stay Markdown-based with headings so it is human-readable and easy to validate.
- The bootstrap should not need to change when a new project spec is introduced.

### Cron-fed intake
- The cron source is the upstream idea signal.
- Intake should accept a hybrid shape: free-form idea text plus structured fields where available.
- The workflow should normalize the intake so traceability is preserved even when the source is noisy.
- Cron may suggest priority and format, but it should not make the final editorial decision on its own.

### Growth actions
- Follow/unfollow and comment likes are automatic.
- Reply drafts require batch approval before sending.
- Growth actions must remain auditable and governed by project-specific rules.
- Low-sensitivity actions can be automated, while public-facing replies and similar outputs require human review.

### Traceability
- The system should preserve an end-to-end chain from idea to brief to cards to caption to approval to publication or engagement action.
- Shared core logic should stay in the shared suite, with project-specific adapters used only for project differences.
- The workflow should be able to explain why a post or engagement action exists.
</decisions>

<specifics>
## Specific Ideas
- Use a separate Markdown spec per project.
- Keep the shared suite generic and let project adapters handle brand-specific behavior.
</specifics>

<canonical_refs>
## Canonical References
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/phases/02-bootstrap-package/02-CONTEXT.md`
- `.planning/phases/03-implement-the-reusable-content-workflow-skills-for-brief-car/03-CONTEXT.md`
</canonical_refs>

<deferred>
## Deferred Ideas
- Exact intake schema for cron-sourced ideas.
- Exact adapter interface for project-specific differences.
- Whether automated suggestions should include alternative post formats.
</deferred>

---
*Phase: 04-project-integration-and-growth-ops*
*Context gathered: 2026-06-15*
