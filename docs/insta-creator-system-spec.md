# Insta Creator System Spec

## Shared workflow boundary
The shared skill suite is responsible for reusable content-creation logic only. It accepts an idea, applies generic workflow steps, and produces structured artifacts. It must not contain brand-specific rules for any one client or project.

## Project-specific spec
Every project must provide a separate brand/spec document. That spec is the source of truth for tone, voice, visual style, CTA conventions, and approval behavior. The shared workflow reads the spec; it does not own it.

## Idea intake
The upstream idea source is a cron-fed signal. `last30days` is the default trend-discovery input, but the shared workflow treats it as just another idea source and does not bake the trend logic into the brand layer.

## Per-post artifact storage
Each post must be stored in its own folder so the post can be reviewed, approved, published, and audited as a single bundle.

## Bootstrap scope
Bootstrap belongs to the shared suite. It sets up the generic workflow, validates the environment, and prepares templates and defaults. It does not store brand rules inside the bootstrap package.

## System flow
1. Cron produces an idea signal.
2. The workflow reads the project spec.
3. The workflow generates a brief.
4. The workflow generates cards/JSON.
5. The workflow generates caption/CTA/hashtags.
6. The workflow packages the post for approval.
7. The workflow saves the post bundle in a deterministic folder.
8. Publication happens after approval.

## Design principles
- Reusable across projects
- Brand rules externalized
- Deterministic storage
- Clear traceability
- Minimal project coupling
