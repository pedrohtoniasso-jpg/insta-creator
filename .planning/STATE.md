# State

## Current decisions
- This is a greenfield project for a reusable Instagram content-creation system.
- The cron feed is the idea source; `last30days` is treated as the upstream signal.
- Brand rules belong in project-specific spec files, not in the shared bootstrap.
- The bootstrap belongs to the shared skill suite.
- Each post must be stored in its own folder.
- Growth workflows are part of the project, but they must be approval-gated and auditable.

## Roadmap evolution
- Phase 1 added: Define system architecture, storage contract, and project-spec boundaries.
- Phase 1 is now the active starting point for the system design.
- Growth strategy was added as a first-class project concern.

## Open questions
- Exact file format for the project-spec contract.
- Exact folder root for post artifacts.
- Whether publication is Facebook-only, Instagram-only, or multi-platform.
- Whether follow/unfollow actions should be automatic or manually approved in batches.

## Notes
- The initial GSD `init` attempt hit a login blocker for the internal Claude-based synthesis step, so the project planning files were scaffolded manually.
