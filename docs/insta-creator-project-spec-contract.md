# Project Spec Contract

## Purpose
This contract defines the minimum shape of a project-specific branding document used by the shared Insta Creator workflow.

## Required fields
A project spec must define:
- Project name
- Target platform
- Brand voice
- Visual rules
- CTA conventions
- Growth strategy
- Approval behavior
- Prohibited angles or topics
- Asset constraints, if any
- Operational notes, if any

## Voice
Describe how the project should sound.
- Tone
- Form of address
- Vocabulary preferences
- Level of directness

## Visual rules
Describe how the post should look.
- Color direction
- Typography direction
- Image style
- Layout preferences
- Logo or watermark rules
- Carousel storytelling style, if the project uses carousels:
  - hook / problem / context / insight / consequences / principle / CTA
  - continuity across slides
  - whether the hook should name a topic, program, or event early

## CTA conventions
Describe how calls to action should be written.
- Primary CTA style
- Secondary CTA style
- Link or profile reference style
- Hashtag conventions

## Growth strategy
Describe how the project wants to grow its audience.
- Follow/unfollow policy: automatic
- Comment like policy: automatic
- Reply strategy
- Approval rules for engagement actions (reply drafts are approved in batches before sending)
- Rate limits or safety constraints
- Timing/spread rules for automated actions

## Prohibited angles
List topics, claims, or angles that must not appear.
- Unsafe claims
- Off-brand messaging
- Forbidden comparisons
- Any legal or compliance constraints

## Approval behavior
Describe how the post should be presented for approval.
- Whether the approval message should include the final caption
- Whether slide-by-slide notes are required
- Whether revisions should be grouped or marked individually
- Reply drafts are approved in batches before sending
- Batch approval package must include the original comment and the suggested reply

## Revision and learning loop
Describe how feedback from changes or rejections should improve future output.
- What feedback to capture when a post is changed or rejected
- Which project docs should be updated after feedback
- Which visual, CTA, or copy rules should be tightened for the next run
- Whether repeated mistakes should be escalated as explicit prohibited patterns

## Minimal example shape
```markdown
# Brand Spec: Example Project

## Project name
...

## Target platform
Instagram

## Voice
...

## Visual rules
...

## CTA conventions
...

## Growth strategy
...

## Approval behavior
...

## Prohibited angles
...

## Asset constraints
...

## Operational notes
...
```

## Contract rule
The shared bootstrap may validate that this file exists and that it contains the required sections, but it must not own or hardcode the brand content itself.
