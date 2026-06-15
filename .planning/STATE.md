# State

## Current decisions
- This is a greenfield project for a reusable Instagram content-creation system.
- The cron feed is the idea source; `last30days` is treated as the upstream signal.
- Brand rules belong in project-specific spec files, not in the shared bootstrap.
- The bootstrap belongs to the shared skill suite.
- The bootstrap is modular: a minimal core with optional templates, validation, and guided onboarding.
- The bootstrap entrypoint is `python -m insta_creator_bootstrap` with `plan`, `apply`, and `validate` commands.
- The onboarding shape is hybrid: one command with defaults, plus prompts only when needed.
- The bootstrap should generate only the essential structural files and stay extensible.
- Validation should be strong and include a dry-run mode.
- The workflow is nucleus-plus-subskills: one orchestrator skill plus specialized brief/cards/caption/approval skills.
- The phase 3 skill suite is organized as `insta-creator-workflow-orchestrator`, `insta-creator-brief`, `insta-creator-cards`, `insta-creator-caption`, and `insta-creator-approval-package`.
- The content flow runs brief first, then cards and caption in parallel, then approval packaging.
- The content package should include brief, cards JSON, caption, approval package, manifest, and operational metadata.
- Cards should be structured JSON with validation.
- The shared cards schema lives at `schemas/cards.schema.json`.
- Captions should follow a predictable structure with style-based variation.
- The approval package should keep all reviewer inputs in one deterministic post folder.
- The project spec should be a separate Markdown file per project.
- The reusable project integration layer lives in `insta_creator_bootstrap/integration.py`.
- `ProjectSpec`, `CronIdeaIntake`, and `GrowthActionQueue` are the phase 4 integration primitives.
- Cron intake should be hybrid: free-form idea text plus structured fields where available.
- The shared workflow should normalize cron intake and preserve traceability.
- Follow/unfollow and comment likes are automatic.
- Reply drafts are approved in batches before sending.
- Growth actions are approval-gated and auditable.
- Generated images should be checked against the brief, cards, and project-spec visual rules before approval.
- The hardening verifier is `scripts/phase5_hardening_check.py` and it exercises bootstrap reproducibility plus deterministic post-bundle checks.
- The phase 5 sample bundle records image-verification audit notes in `manifest.json` when no live image file is available.
- Rejected or revised posts should feed back into the project documentation so the next run improves.
- Each post must be stored in its own folder.
- The post storage root is configurable per project, with a local bootstrap default.
- The default local root is `content/posts/`.
- The agreed folder naming pattern is `YYYY.MM.DD - Short subject`.
- The target publication platform is Instagram.

## Roadmap evolution
- Phase 1 added: Define system architecture, storage contract, and project-spec boundaries.
- Phase 1 is now complete and ready for Phase 2 bootstrap work.
- Growth strategy was added as a first-class project concern.

## Open questions

## Notes
- The initial GSD `init` attempt hit a login blocker for the internal Claude-based synthesis step, so the project planning files were scaffolded manually.
