# Insta Creator System Spec

## Shared workflow boundary
The shared skill suite is responsible for reusable content-creation logic only. It accepts a selected idea, applies generic workflow steps, and produces structured artifacts. It must not hardcode brand-specific rules for any one client or project.

## Project-specific spec
Every project must provide a separate brand/spec document and may provide a separate visual template. The spec is the source of truth for tone, voice, visual style, CTA conventions, growth strategy, approval behavior, and revision learnings. The visual template turns those rules into concrete rendering constraints such as counters, text containers, margins, logo placement, background, and typography limits.

## Idea intake
The upstream idea source is a cron-fed signal. `last30days` is the default trend-discovery input, but cron is discovery only. It returns a numbered shortlist and stops. Production starts only after the user selects one option or explicitly names a theme.

## Orchestration rule
The user is not the orchestrator. The content workflow must run hidden production steps internally and expose only:
- the theme shortlist / selection gate
- the final approval payload

The execution entrypoint is `skills/social-media/insta-creator-workflow/SKILL.md` (`insta-creator`). Stage-specific skills are internal workers, not user-facing entrypoints.

## Audit and validation gates
Checklist validation is required after each major stage, not only at the end:
1. brief checklist
2. narrative checklist
3. cards/caption checklist
4. visual assets checklist
5. final package audit

The final audit should verify the theme, narrative arc, data support, copy legibility, visual identity, CTA focus, package completeness, and user-facing approval payload. The approval payload delivered in chat must be the rendered images plus a copy-ready caption block.

## Image and revision verification
Generated images must be checked against the approved brief, cards, and project-spec visual rules before a post is approved. If a post is rejected, changed, or off-brand, the workflow must capture the feedback and feed it back into the project documentation so the next run starts with the corrected rule.

## Per-post artifact storage
Each post must be stored in its own deterministic folder so it can be reviewed, approved, published, revised, and audited as a single bundle.

## Bootstrap scope
Bootstrap belongs to the shared suite. It sets up the generic workflow, validates the environment, and prepares templates and defaults. It does not store brand rules inside the bootstrap package.

## System flow
1. Cron produces exactly 5 idea options.
2. User selects one option or explicitly names a theme.
3. The orchestrator reads the selected project spec, selected visual template, and trace context.
4. The orchestrator generates and validates the brief.
5. The orchestrator generates and validates the narrative.
6. The orchestrator generates and validates cards JSON + caption.
7. The orchestrator renders and validates card images using the selected visual template.
8. The orchestrator runs the final package audit.
9. The orchestrator stores the full bundle.
10. The user receives only the final caption + rendered card images for approval.
11. Publication or public engagement happens only after approval.

## Design principles
- Reusable across projects
- Brand rules externalized in the project spec
- Deterministic storage
- Clear traceability
- Stage-level validation
- Hidden orchestration
- Approval-gated publication and public replies
