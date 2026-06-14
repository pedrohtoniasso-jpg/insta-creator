---
name: insta-creator-system
kind: project
status: active
---

# Insta Creator System

## Vision
Build a reusable content-creation system for Hermes Agent that can generate Instagram-style content for multiple projects from a shared skill suite.

## What it must do
- Accept content ideas from a cron-driven source, using a recent-trends signal such as `last30days`.
- Apply project-specific brand rules before generating output.
- Produce structured card/slide JSON, captions, approval packages, and publish-ready artifacts.
- Store each post in its own folder with a predictable naming convention.
- Support multiple client brands without rewriting the core workflow.
- Include a bootstrap workflow for installing/configuring the skill suite in new environments.

## Core architecture decisions
- Separate *workflow skills* from *project-specific branding*.
- Keep the bootstrap at the skill-suite level, not inside any single project folder.
- Store project rules in a dedicated spec document per brand.
- Treat each post as an artifact bundle saved to disk.

## Initial scope
This project starts with system design, contracts, folder conventions, and bootstrap scaffolding. Content generation and publication are downstream phases.

## Success looks like
- A generic skill package that can be reused across brands.
- A clear project-spec contract for brand rules.
- A stable per-post storage layout.
- A bootstrap path that makes onboarding a new brand predictable.
