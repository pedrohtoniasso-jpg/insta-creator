# Insta Creator System

A reusable Instagram content creation system for Hermes Agent.

It combines:
- a shared bootstrap package for new environments
- reusable content workflow skills for briefs, cards, captions, and approval packages
- project-specific spec loading and idea intake
- approval-gated growth workflows
- operational hardening and reproducibility checks

## What this repository provides

- `insta_creator_bootstrap`: a local Python package that can plan, apply, and validate a shared scaffold
- a reusable skill suite for turning ideas into structured content packages
- project documentation and contracts for storage, project specs, and workflow boundaries
- verification artifacts and hardening checks for deterministic reuse

## Bootstrap CLI

Run the shared bootstrap package with:

```bash
python -m insta_creator_bootstrap --help
```

## Main components

### Bootstrap package
The bootstrap package seeds a clean project scaffold, validates the required project spec sections, and supports dry-run onboarding.

### Content workflow skills
The shared workflow is split into specialized skills for:
- brief generation
- carousel cards in validated JSON
- caption generation
- approval package assembly

Useful references:
- `docs/content-workflow-contract.md`
- `schemas/cards.schema.json`
- `skills/social-media/insta-creator-workflow/SKILL.md`
- `skills/social-media/insta-creator-brief/SKILL.md`
- `skills/social-media/insta-creator-cards/SKILL.md`
- `skills/social-media/insta-creator-caption/SKILL.md`
- `skills/social-media/insta-creator-approval-package/SKILL.md`

### Project integration
The repository also includes a reusable project integration layer for loading project specs, normalizing cron-fed idea intake, and queueing approval-gated growth actions.

Useful reference:
- `docs/project-integration.md`
- `insta_creator_bootstrap/integration.py`

### Trend research skill
The repository also includes the `last30days` skill for finding recent signals and turning them into content opportunities.

Useful reference:
- `skills/research/last30days/SKILL.md`

## Verification

- `python -m unittest discover -s tests -v`
- `python scripts/phase5_hardening_check.py`

## Notes

The system is designed to keep project-specific brand rules outside the shared bootstrap while preserving traceability from idea to publishable artifact.
