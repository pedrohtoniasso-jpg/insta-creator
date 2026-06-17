---
name: insta-creator-workflow-orchestrator
description: Use when turning an idea into a complete reusable Instagram content package. Orchestrates brief, cards, caption, and approval packaging while preserving traceability.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [instagram, social-media, workflow, orchestrator, traceability]
    related_skills: [insta-creator-brief, insta-creator-cards, insta-creator-caption, insta-creator-approval-package]
---

# Insta Creator Workflow Orchestrator

## Overview

This skill coordinates the shared content pipeline for the Insta Creator system. It keeps the workflow generic, routes brand-specific decisions to the project spec, and ensures each post ends up in a deterministic folder with full traceability.

Use this skill as the entrypoint when an idea needs to become a reviewable content package.

## When to Use

- An idea is ready to become a post package.
- You already have a project spec and want a reusable shared workflow.
- You need a brief, cards JSON, caption, and approval bundle in one deterministic flow.

Do not use this skill for:
- writing the brand spec itself
- ingesting cron ideas directly
- project-specific growth operations

## Workflow

1. Read the project spec and the shared content workflow contract.
2. Build the brief first.
3. Define the carousel narrative arc before card copy.
4. Dispatch cards JSON generation and caption generation in parallel from the brief.
5. Validate the cards JSON using the shared schema contract.
6. Run a checklist-driven audit of the draft package.
7. Assemble the approval package only after the artifacts are ready.
8. Write the bundle into the deterministic post folder.

## Carousel narrative standard

When the output format is a carousel, use a continuous story arc rather than isolated slide copy.

Default sequence:
1. Theme / problem
2. Problem with data
3. Cause with data
4. Broader impact on the audience
5. Organizing principle, rule, or takeaway
6. Dedicated CTA slide

This sequence should be treated as the default pattern unless the project spec explicitly overrides it.

## Shared typography defaults

When generating card copy layouts, use these as the starting point unless the project spec says otherwise:
- Card title size: 90–110 px, extrabold
- Card subtitle size: 35–50 px, regular
- Sizes may be adjusted during review or audit; these values are the starting working range, not the final locked range.

## Required outputs

The package should contain:
- `manifest.json`
- `brief.md`
- `cards.json`
- `caption.md`
- `approval.md`
- `assets/`

## Traceability rules

- Keep one post identifier across all artifacts.
- Preserve the originating idea in the manifest.
- Reference the source project spec version or path.
- Keep revisions in the same folder instead of fragmenting the bundle.

## Common Pitfalls

1. **Skipping the brief.** The brief is the shared anchor; cards and caption should not be built before it exists.
2. **Merging brand rules into the shared flow.** Brand behavior belongs in the project spec.
3. **Treating cards as prose.** Cards must stay structured JSON and remain schema-valid.
4. **Assembling approval too early.** The approval bundle should only be built after the artifacts exist and validate.

## Verification Checklist

- [ ] The brief is produced first.
- [ ] Cards JSON and caption are generated from the brief.
- [ ] Cards JSON validates against the shared schema.
- [ ] The approval package contains the full review bundle.
- [ ] The post folder uses the deterministic naming contract.
- [ ] Traceability from idea to approval package is preserved.

## Reference material

- `docs/content-workflow-contract.md` — shared workflow order, narrative arc, typography defaults, and audit structure.
- `docs/insta-creator-system-spec.md` — system-level boundaries for the shared bootstrap and project workflow.
- `docs/project-integration.md` — normalized cron intake and growth-action queueing.
