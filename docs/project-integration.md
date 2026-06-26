# Project Integration

This repository keeps project-specific behavior outside the shared bootstrap and reusable workflow core.

## What this layer does
The integration layer connects three things:
- a project-specific Markdown spec
- a project-specific visual template
- a cron-fed idea intake signal
- a user selection gate
- an approval-gated content and growth workflow with traceability

It also stores the continuation state after a theme is selected so the workflow can resume without a second cron.

## Core objects

### `ProjectSpec`
A parsed, validated project spec loaded from Markdown. It is the source of truth for brand voice, visual identity, CTA conventions, approval behavior, and prohibited angles.

Expected sections include:
- Project name
- Target platform
- Brand personality
- Brand voice
- Visual rules
- Color palette
- Typography direction
- Logo / mark rules
- CTA conventions
- Growth strategy
- Approval behavior
- Prohibited angles
- Asset constraints
- Operational notes

### `CronIdeaIntake`
A normalized intake shape for cron-fed ideas.

It preserves:
- free-form idea text
- priority hints
- format hints for carousel or story content
- structured metadata
- traceability identifiers

### `IdeaSelectionGate`
A numbered shortlist used between discovery and production.

It preserves:
- exactly 5 numbered ideas
- theme / angle / why-now / format metadata
- a lightweight reply rule so the user can answer with `1`-`5`
- persisted latest-shortlist state at `state/latest-shortlist/<project_id>.json`
- traceability back to the intake that produced the shortlist

### `SelectionHandoff`
The normalized payload created when the user replies to a shortlist.

It preserves:
- `project_id`
- `selection.shortlist_id`
- `selection.selected_option` or an explicit theme
- `selection.user_action` (`select` or `revise`)
- `selection.change_request` when revising
- optional `project_spec_path` and `visual_template_path`
- the trace that bridges shortlist → production

### `ContentWorkflowRun`
The hidden production run owned by the orchestrator.

It preserves:
- selected idea and trace context
- stage validation status
- bundle folder
- rendered image artifact list
- final approval payload state

### `GrowthActionQueue`
A split view of growth actions:
- `automatic` for low-sensitivity actions like follows, unfollows, and likes
- `approval_required` for reply drafts and similar public-facing actions
- `reply_batches` for grouped approval of reply drafts before sending

### `ApprovalDeliveryContract`
A visible-output contract for the main approval channel.

It preserves:
- the approval channel name or destination
- which payload is visible externally
- whether the final output is approval-only

### `WorkflowContinuation`
A state object that carries the selected theme and the hidden internal stages so the workflow can resume after the user chooses a topic.

## Example flow

1. Load the project spec.
2. Normalize the incoming cron idea.
3. Produce a numbered shortlist when the cron is doing discovery.
4. Persist the shortlist to `state/latest-shortlist/<project_id>.json` so a later terse reply can be resolved without the user naming the cron.
5. Let the user pick `1`-`5` or explicitly name a theme from the latest shortlist.
6. Normalize the reply into a selection handoff with `project_id`, `selection.shortlist_id`, `selection.selected_option` or `selection.theme`, and `selection.user_action`.
7. Build a trace context for the selected idea.
8. Start post creation through `skills/social-media/insta-creator-workflow/SKILL.md` (`insta-creator`).
9. Run the full production pipeline autonomously:
   - brief → brief checklist
   - narrative → narrative checklist
   - cards JSON + caption → content checklist
   - rendered card images from selected visual template → visual checklist
   - final audit → approval package
10. Send the user-facing approval payload: caption + rendered card images.
11. Queue growth actions only after content approval.
12. Approve reply batches before sending.

## Example usage

```python
from insta_creator_bootstrap import (
    build_trace_context,
    load_project_spec,
    normalize_cron_intake,
    queue_growth_actions,
)

spec = load_project_spec("docs/project-spec.md")
intake = normalize_cron_intake(
    {
        "idea_text": "Write about reusable content workflows",
        "priority": "high",
        "format": "carousel",
    },
    project_name=spec.project_name,
    project_spec_path=spec.path,
)
trace = build_trace_context(spec, intake)
queue = queue_growth_actions([
    "follow",
    {"action_type": "reply_draft", "body": "Thanks for reading!"},
], trace=trace)
```

## Contract rules
- The shared bootstrap stays generic.
- Brand rules remain in the project spec.
- Cron can suggest priority and format, but it does not produce final content.
- Discovery jobs should surface exactly 5 numbered ideas so the next step can be a one-digit reply.
- Discovery jobs must persist the latest shortlist to `state/latest-shortlist/<project_id>.json` before final delivery.
- The user reply is normalized into a selection handoff before production starts.
- The user is not asked to approve internal steps.
- The approval payload is caption + rendered card images, not a full internal bundle dump.
- Reply drafts are approved in batches before sending.
- Every growth action keeps traceability metadata.
- The approval channel comes from the project spec or the selected main channel, and only the final deliverable is visible there.
