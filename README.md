# Insta Creator System

A reusable Instagram content creation system for Hermes Agent.

It combines:
- a shared bootstrap package for new environments
- reusable content workflow skills for briefs, cards, captions, audits, and approval packages
- project-specific spec loading and idea intake
- approval-gated growth workflows
- operational hardening and reproducibility checks

## What this repository provides

- `insta_creator_bootstrap`: a local Python package that can plan, apply, and validate a shared scaffold
- a reusable skill suite for turning ideas into structured content packages
- project documentation and contracts for storage, project specs, workflow boundaries, and audit checks
- verification artifacts and hardening checks for deterministic reuse

## Quick start

### 1) Set up a project scaffold

```bash
python -m insta_creator_bootstrap --help
python -m insta_creator_bootstrap plan --target <dir>
python -m insta_creator_bootstrap apply --target <dir>
python -m insta_creator_bootstrap validate --target <dir>
```

### 2) Fill the project spec

Use the project spec template created by the bootstrap and make sure the required sections are present:
- project name
- target platform
- brand personality
- brand voice
- visual rules
- color palette
- typography direction
- logo / mark rules
- CTA conventions
- approval behavior
- prohibited angles
- asset constraints
- operational notes

### 3) Run the shared content workflow

The shared workflow is split into specialized skills for:
- brief generation
- carousel narrative planning
- carousel cards in validated JSON
- caption generation
- audit / review pass
- approval package assembly

Useful references:
- `docs/content-workflow-contract.md`
- `docs/insta-creator-system-spec.md`
- `docs/project-integration.md`
- `schemas/cards.schema.json`
- `skills/social-media/insta-creator-workflow/SKILL.md`
- `skills/social-media/insta-creator-brief/SKILL.md`
- `skills/social-media/insta-creator-cards/SKILL.md`
- `skills/social-media/insta-creator-caption/SKILL.md`
- `skills/social-media/insta-creator-approval-package/SKILL.md`

## Recommended content flow

1. Read the project spec.
2. Build the brief.
3. Shape the carousel narrative arc before drafting cards.
4. Generate cards JSON and caption content.
5. Run the audit checklist before final approval.
6. Assemble the approval package.
7. Store everything in a deterministic per-post folder.

## Audit workflow

The audit pass is stage-based and question-driven.

Suggested stages:
- subject / thesis audit
- storyline audit
- data / evidence audit
- copy / readability audit
- visual audit
- CTA audit
- packaging / delivery audit

Rule of thumb:
- every error, objection, or change request should become a new checklist question for the next run
- repeated mistakes should be promoted into the project baseline so future posts start with them already covered

## Cron presets

Use cron to automate three common queues: content discovery, content creation, and growth operations.

Suggested schedules:

- **Content ideas / trend intake**
  - schedule: `0 8 * * *`
  - purpose: collect recent signals, normalize ideas, and queue candidate topics

- **Content creation**
  - schedule: `30 8 * * *`
  - purpose: generate the brief, cards, caption, and approval package for the selected idea

- **Audit pass**
  - schedule: `0 9 * * *`
  - purpose: run the stage-based checklist before approval

- **Growth actions**
  - schedule: `*/30 * * * *`
  - purpose: queue low-sensitivity actions automatically and batch reply drafts for approval

- **Review / follow-up queue**
  - schedule: `0 17 * * 1-5`
  - purpose: review pending approval items, revise outputs, and prepare the next content cycle

Notes:
- keep growth actions approval-gated when they involve public replies or sensitive engagement
- keep project-specific cron logic outside the shared bootstrap
- use the project spec to decide which actions are automatic and which need review

## Verification

- `python -m unittest discover -s tests -v`
- `python scripts/phase5_hardening_check.py`

## Notes

The system is designed to keep project-specific brand rules outside the shared bootstrap while preserving traceability from idea to publishable artifact.
Generated post bundles should stay out of version control unless a repo explicitly needs them as fixtures or examples.
