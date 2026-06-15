# Requirements

## REQ-01 — Idea intake
The system must ingest content ideas from a cron-driven signal source, with `last30days` treated as the upstream discovery signal.

## REQ-02 — Project-specific branding
The system must support a project-specific spec document that defines branding, tone, content rules, and approval conventions.

## REQ-03 — Shared workflow core
The system must keep the content-creation workflow generic so the same skill suite can be reused across projects.

## REQ-04 — Per-post artifact storage
The system must save each post in its own folder with a deterministic naming convention.

## REQ-05 — Bootstrap for new environments
The system must include a bootstrap flow for installing and configuring the shared skill suite in a new environment.

## REQ-06 — Traceability
The system must preserve traceability from idea → cards/JSON → caption → approval package → publication.

## REQ-07 — Growth engagement workflows
The system must support project-specific growth workflows such as follow/unfollow queues, comment engagement, and reply draft approval gates before sending.

## Artifact requirements
Each post folder should contain, at minimum:
- `manifest.json`
- `brief.md`
- `cards.json`
- `caption.md`
- `approval.md`
- `assets/`

## Non-functional requirements
- Paths and naming should be deterministic.
- The core workflow should remain project-agnostic.
- Brand-specific logic should live outside the shared bootstrap.
- Growth workflows should be explicit, auditable, and approval-gated where needed.
- Outputs should be easy to replicate across other projects.

## Out of scope for the first milestone
- Fully automated multi-platform publishing for every network.
- Project-specific branding stored inside the shared bootstrap package.
- Deep content strategy research beyond the cron idea feed.
- Aggressive or policy-breaking engagement automation.
