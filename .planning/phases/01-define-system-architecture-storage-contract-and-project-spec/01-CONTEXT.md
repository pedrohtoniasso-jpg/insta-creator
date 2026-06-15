# Phase 1: System specification - Context

**Gathered:** 2026-06-14
**Status:** Ready for planning

<domain>
## Phase Boundary
Define the shared architecture for the reusable Instagram content system: the generic workflow core, the storage contract for per-post artifacts, the project-spec contract, and the growth boundary.

This phase does *not* implement content generation, publishing, or engagement automation. It establishes the rules the later phases will use.
</domain>

<decisions>
## Implementation Decisions

### Shared workflow boundary
- The workflow must be generic and reusable across projects.
- Brand-specific logic must live outside the shared bootstrap.
- The shared suite should not hardcode GranaFlow-specific behavior.

### Project-spec contract
- Every project gets a separate brand-spec document.
- The project spec will use **Markdown with headings** as the standard format.
- The project spec should define tone, visual rules, CTA style, growth strategy, and prohibited angles.
- The project spec must be loadable by the later workflow skills without changing the bootstrap.

### Growth boundary
- Growth actions such as follows, unfollows, likes, and reply drafting belong to the project workflow.
- Reply drafts are approved in batches before sending.
- Approval gates are required for outbound engagement actions that could be noisy or risky.

### Post artifact storage
- Every post must be stored in its own folder.
- The post storage root is configurable per project, with a local bootstrap default.
- A post folder should contain a manifest, brief, cards JSON, caption, approval package, and assets.
- Folder naming must be deterministic and reproducible.
- The agreed folder naming pattern is `YYYY.MM.DD - Short subject`.

### Bootstrap scope
- Bootstrap belongs to the shared skill suite, not any project folder.
- The bootstrap should create or validate the shared scaffolding and templates.
- Project onboarding should be handled through a generic bootstrap flow that accepts a project spec.

### Claude's Discretion
- Exact file root for the project-spec documents.
- Exact local default path for the storage root.
- Internal naming conventions for the skill modules themselves.
</decisions>

<specifics>
## Specific Ideas
- Cron is the source of ideas.
- `last30days` is the upstream trend signal.
- The current target project is GranaFlow, but the system must work for other projects too.
- The bootstrap must stay outside `/granaflow/`.
</specifics>

<canonical_refs>
## Canonical References

### Planning source of truth
- `.planning/PROJECT.md` — project vision and initial scope
- `.planning/ROADMAP.md` — phases, requirements, and execution order
- `.planning/STATE.md` — current decisions and open questions

### External source of ideas
- Cron workflow using `last30days` — upstream content signal
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- GSD project scaffold already exists in `.planning/`.
- Phase directories are ready to be filled with plan and summary artifacts.

### Integration Points
- Future workflow skills will read this phase's storage and spec contracts.
- Later phases will reuse the per-post folder schema defined here.
</code_context>

<deferred>
## Deferred Ideas
- Exact markdown section names and ordering for the project-spec template.
- Publication channel strategy.
</deferred>

---
*Phase: 01-define-system-architecture-storage-contract-and-project-spec*
*Context gathered: 2026-06-14*
