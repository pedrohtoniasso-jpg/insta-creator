---
name: insta-creator-approval-package
description: Use when assembling the review bundle for an Instagram content package in the shared workflow. Collects brief, cards, caption, manifest, and reply drafts into one approval-ready folder.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [instagram, approval, review-bundle, packaging, audit]
    related_skills: [insta-creator-workflow-orchestrator, insta-creator-brief, insta-creator-cards, insta-creator-caption]
---

# Insta Creator Approval Package Skill

## Overview

This skill assembles the final review bundle for a post. The goal is to put everything a reviewer needs in one place so approval does not require hunting through scattered files.

## When to Use

- Brief, cards, and caption are already generated.
- You need a single approval bundle inside the deterministic post folder.
- Reply drafts, when relevant, need to be included before sending.

Do not use this skill for:
- generating the content from scratch
- creating project-specific brand rules
- cron intake or growth queueing

## Approval package contents

The approval bundle should include:
- `manifest.json`
- `brief.md`
- `cards.json`
- `caption.md`
- `approval.md`
- `assets/`
- reply drafts when they are relevant to the review

## Approval rules

- Keep the package self-contained.
- Preserve the same post identifier in every artifact.
- Include a concise summary of the chosen content direction.
- Make the reviewer’s decision path obvious.
- Keep any reply drafts in the bundle rather than as separate loose files.

## Common Pitfalls

1. **Forgetting the manifest.** The manifest is the traceability anchor.
2. **Splitting the bundle.** The package should stay in one post folder.
3. **Leaving out reply drafts.** If they matter to the approval, include them in the bundle.

## Verification Checklist

- [ ] The bundle contains all required artifacts.
- [ ] The manifest matches the post folder and idea source.
- [ ] Reply drafts are included when relevant.
- [ ] The package is easy to approve in one pass.
- [ ] The deterministic folder layout is respected.
