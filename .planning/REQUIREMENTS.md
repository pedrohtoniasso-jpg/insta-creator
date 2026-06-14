# Requirements

## Functional requirements
- The system must ingest content ideas from a cron-driven signal source.
- The system must support a project-specific spec document that defines branding, tone, and content rules.
- The system must generate a structured content bundle for each post.
- The system must save each post into its own folder.
- The system must support multiple projects with separate specs but shared core skills.
- The system must include a bootstrap flow for installing and configuring the skill suite in new environments.
- The system must preserve traceability from idea → cards/JSON → caption → approval package → publication.

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
- Brand-specific logic should live outside the shared skills.
- Outputs should be easy to replicate across other projects.

## Out of scope for the first milestone
- Fully automated multi-platform publishing for every network.
- Project-specific branding stored inside the shared bootstrap package.
- Deep content strategy research beyond the cron idea feed.
