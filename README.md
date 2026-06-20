# Insta Creator System

A reusable Instagram content creation system for Hermes Agent.

It combines:
- a shared bootstrap package for new environments
- reusable content workflow skills for briefs, cards, stories, captions, audits, and approval packages
- project-specific spec loading and idea intake
- approval-gated growth workflows
- operational hardening and reproducibility checks

## What this repository provides

- `insta_creator_bootstrap`: a local Python package that can plan, apply, and validate a shared scaffold
- a reusable skill suite for turning ideas into structured content packages
- project documentation and contracts for storage, project specs, workflow boundaries, and audit checks
- verification artifacts and hardening checks for deterministic reuse
- a project-local `.env` contract for companion Instagram posting automation

## Quick start

### 1) Install the local package

This repository now includes Python packaging metadata, so you can install it in editable mode:

```bash
python -m pip install -e .
```

### 2) Set up a project scaffold

```bash
python -m insta_creator_bootstrap --help
python -m insta_creator_bootstrap plan --target <dir>
python -m insta_creator_bootstrap apply --target <dir>
python -m insta_creator_bootstrap validate --target <dir>
```

### 3) Fill the project spec

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

### 4) Connect the second brain

Set the second brain path before running a new agent:

```bash
export SECOND_BRAIN_PATH=/home/openclaw/cerebro
```

Core files to read first:
- `CODEX.md` — profile, working style, and sync rule
- `HEARTBEAT.md` — operational triage for the current heartbeat
- `PROPAGATION.md` — what to update when state changes
- `memory/context/pendencias.md` — open work and closure criteria
- `memory/context/deadlines.md` — time-sensitive items
- `memory/context/people.md` — people and roles
- `memory/context/business-context.md` — consolidated operating context
- `memory/projects/_index.md` — project overview and next steps
- `memory/projects/<project>.md` — project-specific notes
- `memory/YYYY-MM-DD.md` — daily sync notes

### 5) Configure Instagram posting credentials

The shared workflow in this repo does not post to Meta by itself, but companion posting helpers do. The repo now ships a root `.env.example` documenting the expected variables.

Recommended setup:

```bash
cp .env.example .env
```

Populate:

```env
INSTAGRAM_ACCESS_TOKEN=<long-lived-instagram-token>
FACEBOOK_USER_ACCESS_TOKEN=<optional-facebook-user-token>
FACEBOOK_APP_ID=<optional-meta-app-id>
FACEBOOK_APP_SECRET=<optional-meta-app-secret>
```

Recommended secret layout:
- keep your canonical secrets in `~/.hermes/.env`
- if a project-local helper expects a local `.env`, symlink it:

```bash
ln -sf ~/.hermes/.env .env
```

Use this when your posting workflow runs from the project directory and should reuse the same token without copying it.

### 6) Run the shared content workflow

The shared workflow is split into specialized skills for:
- brief generation
- carousel narrative planning
- carousel cards and stories in validated JSON
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
- `skills/social-media/insta-creator-stories/SKILL.md`
- `skills/social-media/insta-creator-caption/SKILL.md`
- `skills/social-media/insta-creator-approval-package/SKILL.md`

The integration layer also carries the workflow continuation state after the user selects a theme, so a single cron can feed the idea while the approval channel stays generic and final-only.

### 7) Optional trend research skill

The repository also includes the `last30days` skill for finding recent signals and turning them into content opportunities.

Useful reference:
- `skills/research/last30days/SKILL.md`

## Recommended content flow

1. Read the project spec.
2. Build the brief.
3. Shape the narrative arc before drafting cards or story frames.
4. Generate cards/stories JSON and caption content.
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

## Hermes cron examples

If you are using Hermes cron, create self-contained jobs and point them at this repo as the `--workdir`.

### Content idea intake

```bash
hermes cron create "0 8 * * *" \
  "Use the last30days skill to collect recent Instagram content opportunities, normalize them into candidate ideas, and deliver a shortlist for review." \
  --name "insta-creator-idea-intake" \
  --deliver telegram \
  --workdir /home/openclaw/insta-creator
```

### Content creation

```bash
hermes cron create "30 8 * * *" \
  "Use the insta-creator workflow to turn the currently selected idea into a brief, structured cards or story frames, caption, and final approval package." \
  --name "insta-creator-content-creation" \
  --deliver telegram \
  --workdir /home/openclaw/insta-creator
```

### Audit pass

```bash
hermes cron create "0 9 * * *" \
  "Run the insta-creator audit pass against the latest draft package and report any issues that must be fixed before approval." \
  --name "insta-creator-audit" \
  --deliver telegram \
  --workdir /home/openclaw/insta-creator
```

You can inspect and manage them with:

```bash
hermes cron list
hermes cron edit <job-id>
hermes cron run <job-id>
hermes cron pause <job-id>
hermes cron resume <job-id>
hermes cron remove <job-id>
```

## Verification

- `python -m unittest discover -s tests -v`
- `python scripts/phase5_hardening_check.py`

## Agent routines

### Hermes / Codex
- Start by reading `CODEX.md`, `HEARTBEAT.md`, and `PROPAGATION.md`.
- Check `memory/context/pendencias.md` before planning or creating anything new.
- Update the matching memory file as soon as a state change happens.
- Write a daily note in `memory/YYYY-MM-DD.md` when a session changes the operating picture.
- Prefer concrete closures: action, owner, artifact, and completion criteria.
- Use the second brain as the operational source of truth, not as a passive archive.

### Zapia
- Treat the second brain as the historical/context source for business, projects, and decisions.
- Read the relevant project note before generating a new output.
- Pull from `memory/projects/_index.md` and `memory/context/business-context.md` before making assumptions.
- Keep canonical context in memory files; keep drafts and experiments separate.
- Mirror important decisions back into the right note so the backup stays useful as a reference source.
- Use the backup workspace as context supply, not as a place for ephemeral scratch-only work.

## Routine for a new agent

1. Set `SECOND_BRAIN_PATH`.
2. Read `CODEX.md`.
3. Read `HEARTBEAT.md`.
4. Read `PROPAGATION.md`.
5. Read `memory/context/pendencias.md`, `deadlines.md`, `people.md`, and `business-context.md`.
6. Read the relevant project note in `memory/projects/`.
7. Load the task-specific skills, and load a `cerebro` skill too if the runtime exposes one.
8. Complete the task.
9. Propagate the state change to the matching memory file.
10. Add or update the day note in `memory/YYYY-MM-DD.md`.

## Notes

The system is designed to keep project-specific brand rules outside the shared bootstrap while preserving traceability from idea to publishable artifact.
Generated post bundles should stay out of version control unless a repo explicitly needs them as fixtures or examples.
The second brain is the operational source of truth for active context, while the repo README stays focused on how to start, sync, and route work.

## Optional second-brain layers to consider

If you want a more complete brain-like setup for future agents, consider adding:
- `memory/context/inbox.md` for raw intake before classification
- `skills/_registry.md` so an agent can discover which skills already exist
- `scripts/brain-boot.sh` or a similar SessionStart hook for automatic briefing
- a daily sync cron for the second brain snapshot or backup repo
- a dedicated `memory/sessions/` history so agents can recap recent work without searching chats
