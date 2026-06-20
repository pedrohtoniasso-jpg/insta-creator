# Insta Creator System Spec

## Shared workflow boundary
The shared skill suite is responsible for reusable content-creation logic only. It accepts an idea, applies generic workflow steps, and produces structured artifacts. It must not contain brand-specific rules for any one client or project.

## Project-specific spec
Every project must provide a separate brand/spec document. That spec is the source of truth for tone, voice, visual style, CTA conventions, growth strategy, and approval behavior. The shared workflow reads the spec; it does not own it.

## Idea intake
The upstream idea source is a cron-fed signal. `last30days` is the default trend-discovery input, but the shared workflow treats it as just another idea source and does not bake the trend logic into the brand layer.

## Growth workflow boundary
Growth actions such as following, unfollowing, liking, drafting comment replies, and publishing support content are part of the project workflow, but they must be governed by project-specific rules and approval gates. Follow/unfollow and comment likes are automatic. Reply drafts should always be prepared for batch review and approved before sending.

## Audit gate
Before final approval, the workflow should run a checklist-driven audit pass over the draft package. The audit should verify the theme, narrative arc, data support, copy legibility, visual clarity, CTA focus, and package completeness. Any error or change request should be converted into a new checklist question for the next revision cycle.

## Approval channel boundary
The approval channel is the user's main channel for the project. It should receive only the final approved deliverable, while the internal workflow stages remain hidden.

## Image and revision verification
Generated images must be checked against the approved brief, cards, and project-spec visual rules before a post is approved. If a post is changed or rejected, the workflow should capture the feedback and feed it back into the project documentation so the next run is more accurate.

## Per-post artifact storage
Each post must be stored in its own folder so the post can be reviewed, approved, published, and audited as a single bundle.

## Bootstrap scope
Bootstrap belongs to the shared suite. It sets up the generic workflow, validates the environment, and prepares templates and defaults. It does not store brand rules inside the bootstrap package.

## System flow
1. Cron produces an idea signal.
2. The workflow reads the project spec.
3. The workflow generates a brief.
4. The workflow generates cards/JSON or story-frame JSON.
5. The workflow generates caption/CTA/hashtags.
6. The workflow runs a checklist-driven audit pass.
7. The workflow packages the post for approval.
8. The workflow saves the post bundle in a deterministic folder.
9. Growth actions are queued or drafted when allowed by the project spec.
10. Publication or engagement happens after approval.

The internal stages are not user-facing; the user should only choose the topic and approve the final output.

## Design principles
- Reusable across projects
- Brand rules externalized
- Deterministic storage
- Clear traceability
- Approval-gated growth actions
- Minimal project coupling
