# Roadmap: Insta Creator System

## Overview
Build a reusable Instagram content-creation system for Hermes Agent. The system will accept ideas from a cron-fed signal, apply project-specific brand rules, generate structured content artifacts, run growth engagement workflows where approved, and store every post in its own folder.

## Phases

- [ ] **Phase 1: System specification** - Define shared workflow boundaries, storage contracts, project-spec rules, and growth boundaries.
- [ ] **Phase 2: Bootstrap package** - Build the reusable bootstrap for the shared skill suite.
- [ ] **Phase 3: Content workflow skills** - Implement the reusable brief, cards, copy, package, and publish skills.
- [ ] **Phase 4: Project integration and growth ops** - Add project-specific spec loading, cron-fed idea intake, and approval-gated engagement workflows.
- [ ] **Phase 5: Operational hardening** - Verify outputs, deterministic naming, and bootstrap reproducibility.

## Phase Details

### Phase 1: System specification
**Goal**: Define the shared architecture, storage contract, project-spec boundaries, and growth rules for the reusable content system.
**Depends on**: Nothing (first phase)
**Requirements**: REQ-02, REQ-03, REQ-04, REQ-06, REQ-07
**Success Criteria** (what must be TRUE):
  1. The shared skill suite boundary is clearly separated from project-specific branding.
  2. The per-post folder contract is documented with required artifacts.
  3. The bootstrap scope is explicitly limited to the shared suite.
  4. The growth workflow boundary is defined, including approval gates for outbound engagement.
  5. The project-spec contract is defined well enough to support later implementation.
**Plans**: TBD

Plans:
- [ ] 01-01: Formalize the system architecture and storage contract
- [ ] 01-02: Define the project-spec contract, bootstrap boundary, and growth rules

### Phase 2: Bootstrap package
**Goal**: Create the reusable bootstrap flow for installing and configuring the skill suite in a new environment.
**Depends on**: Phase 1
**Requirements**: REQ-05, REQ-03
**Success Criteria** (what must be TRUE):
  1. A new environment can be prepared with the shared workflow scaffold.
  2. Bootstrap templates and defaults are separated from project branding.
  3. The onboarding path is repeatable across projects.
**Plans**: TBD

Plans:
- [ ] 02-01: Create suite bootstrap and project onboarding scaffolding
- [ ] 02-02: Add validation and template defaults for new environments

### Phase 3: Content workflow skills
**Goal**: Implement the reusable skills that turn an idea into a content package.
**Depends on**: Phase 2
**Requirements**: REQ-01, REQ-03, REQ-04, REQ-06
**Success Criteria** (what must be TRUE):
  1. The system can produce a brief, cards JSON, caption, and approval package.
  2. Post artifacts are written into a deterministic folder per content item.
  3. The workflow stays generic enough to support other brands.
**Plans**: TBD

Plans:
- [ ] 03-01: Implement brief, cards, and caption generation workflow
- [ ] 03-02: Implement approval package and artifact storage flow

### Phase 4: Project integration and growth ops
**Goal**: Connect cron-sourced ideas, project-specific specs, and approval-gated growth workflows to the shared system.
**Depends on**: Phase 3
**Requirements**: REQ-01, REQ-02, REQ-06, REQ-07
**Success Criteria** (what must be TRUE):
  1. A project-specific spec can be loaded without changing the shared bootstrap.
  2. Cron-fed ideas can enter the workflow as structured inputs.
  3. The system can automatically handle growth actions such as follows, unfollows, likes, and comment replies.
  4. Reply drafts can be assembled for batch approval before sending.
  5. The system preserves traceability from idea to publication or engagement action.
**Plans**: TBD

Plans:
- [ ] 04-01: Add project-spec loading and idea intake wiring
- [ ] 04-02: Add growth engagement queueing and approval flow
- [ ] 04-03: Add traceability hooks from idea to publishable or engagement-ready artifact bundle

### Phase 5: Operational hardening
**Goal**: Prove the system is reproducible and safe to reuse across future projects.
**Depends on**: Phase 4
**Requirements**: REQ-04, REQ-05, REQ-06, REQ-07
**Success Criteria** (what must be TRUE):
  1. Folder naming is deterministic and repeatable.
  2. Bootstrap works in a clean environment.
  3. Verification steps can confirm the expected artifacts exist.
  4. Growth workflows remain auditable and approval-gated.
**Plans**: TBD

Plans:
- [ ] 05-01: Verify folder outputs and naming determinism
- [ ] 05-02: Verify bootstrap reproducibility in a clean environment
- [ ] 05-03: Verify approval gates for growth actions and batch replies

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. System specification | 0/2 | Not started | - |
| 2. Bootstrap package | 0/2 | Not started | - |
| 3. Content workflow skills | 0/2 | Not started | - |
| 4. Project integration and growth ops | 0/3 | Not started | - |
| 5. Operational hardening | 0/3 | Not started | - |

