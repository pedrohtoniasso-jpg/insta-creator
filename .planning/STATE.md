# State

## Current decisions
- This is a greenfield project for a reusable Instagram content-creation system.
- The cron feed is the idea source; `last30days` is treated as the upstream signal.
- Brand rules belong in project-specific spec files, not in the shared bootstrap.
- The bootstrap belongs to the shared skill suite.
- Each post must be stored in its own folder.
- Growth workflows are part of the project, but they must be approval-gated and auditable.
- Follow/unfollow and comment likes are automatic.
- Reply drafts are approved in batches before sending.
- The project-spec format will be Markdown with headings.
- The target publication platform is Instagram.
- The post storage root is configurable per project, with a local bootstrap default.
- The default local root is `content/posts/`.
- The agreed folder naming pattern is `YYYY.MM.DD - Short subject`.

## Roadmap evolution
- Phase 1 added: Define system architecture, storage contract, and project-spec boundaries.
- Phase 1 is now complete and ready for Phase 2 bootstrap work.
- Growth strategy was added as a first-class project concern.

## Open questions

## Notes
- The initial GSD `init` attempt hit a login blocker for the internal Claude-based synthesis step, so the project planning files were scaffolded manually.
