# Project Integration

This repository keeps project-specific behavior outside the shared bootstrap and reusable workflow core.

## What this layer does
The integration layer connects three things:

- a project-specific Markdown spec
- a cron-fed idea intake signal
- approval-gated growth actions with traceability

It also stores the continuation state after a theme is selected so the workflow can resume without a second cron.

## Core objects

### `ProjectSpec`
A parsed, validated project spec loaded from Markdown.

Expected sections include:
- Project name
- Target platform
- Brand voice
- Visual rules
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
3. Build a trace context.
4. Queue growth actions.
5. Run the audit checklist on the draft package when the task is content creation.
6. Approve reply batches before sending.

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
- Cron can suggest priority and format, but it does not make the final editorial decision.
- Reply drafts are approved in batches before sending.
- Every growth action keeps traceability metadata.
- The approval channel comes from the project spec or the selected main channel, and only the final deliverable is visible there.
