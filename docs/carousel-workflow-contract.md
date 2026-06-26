# Instagram Carousel Workflow Contract

This document defines how Insta Creator should treat **Instagram feed carousels** so a carousel is engineered for attention, swipes, saves, shares, and comments — not just as a deck of pretty slides.

## Research-backed premise

Current Instagram/creator guidance and social-media research point to a few durable carousel principles:

- Instagram Creator guidance defines engagement as interactions such as likes, comments, saves, and shares, and points creators toward content that earns those actions.
- Instagram Creator best-practices guidance calls out the need to capture attention through photos and improve creation, engagement, and reach.
- Instagram's ranking explanation says Feed includes videos, photos, and carousels, and that ranking predicts likely user actions. For Explore, Instagram explicitly names likes, saves, and shares as important predicted actions.
- Market playbooks repeatedly find carousels useful for saves/shares because they hold attention through swipe depth and deliver reusable information.

Operational implication: a carousel should be designed as a **swipeable value asset**. It must create curiosity on slide 1, keep momentum slide-to-slide, name the save/share reason, and end with one primary engagement CTA — save, share, comment, or DM — that fits the content.

## Default carousel unit

A carousel unit is a 4:5 feed asset set with:

1. **Thumb-stopping cover:** one clear promise, tension, or useful outcome.
2. **Swipe loop:** each slide creates a reason to continue to the next.
3. **Value payload:** practical insight, decision rule, checklist, comparison, mistake, myth, or framework.
4. **Save/share trigger:** the content is useful enough to revisit or send.
5. **Conversation trigger:** one simple prompt that invites comment or DM without feeling like engagement bait.
6. **Caption support:** caption reinforces the carousel and adds search/context, but the carousel must stand on its own visually.

Default dimensions: `1080×1350` PNG per slide.

## Allowed carousel formats

Use these as canonical carousel types in briefs, shortlists, and cards JSON:

- `checklist`: step-by-step list worth saving.
- `mistakes`: common errors + correction.
- `myth_fact`: misconception → truth → what to do.
- `comparison`: option A vs B, before/after, do/don't.
- `framework`: named mental model, rule, or decision tree.
- `how_to`: practical tutorial compressed into slides.
- `case_breakdown`: concrete example dissected into lesson.
- `trend_explainer`: current news/signal → why it matters → action.
- `objection_handler`: audience doubt → clear answer → next step.
- `resource_list`: tools, products, routines, or references worth saving.
- `story_lesson`: short relatable situation → lesson → CTA.

## Hook patterns that attract swipes

Prefer one of these cover shapes:

- **Specific promise:** “Como escolher X sem cair em Y”.
- **Mistake warning:** “O erro que faz você gastar mais com X”.
- **Contrarian truth:** “Nem sempre X é a melhor escolha”.
- **Checklist/save cue:** “Salva isso antes de fazer X”.
- **Comparison tension:** “X ou Y: quando cada um faz sentido”.
- **Curiosity gap, sem clickbait:** “O detalhe que muda sua decisão sobre X”.
- **Audience mirror:** “Se você faz X, olha isso antes de Y”.

Avoid vague covers such as “Dicas sobre skincare” or “Entenda finanças”. The first slide must tell the viewer why swiping is worth it.

## Slide architecture

Default 6-slide structure:

1. **Cover / promise:** clear tension or benefit.
2. **Problem / stakes:** what people get wrong or why it matters.
3. **Mechanism / context:** what is actually happening.
4. **Practical rule / example:** turn the idea into a decision.
5. **Checklist / takeaway:** compress into a saveable rule.
6. **CTA:** save, share, comment, or DM tied to the same topic.

Allowed shorter version: 4–5 slides when the idea is simple.
Allowed longer version: 7–8 slides only when each slide adds a new necessary step.

Hard rule: each slide must either increase curiosity, clarify the decision, or make the asset more saveable. If a slide only repeats the premise, remove it.

## Engagement CTA rules

Choose one primary action, based on objective:

- **Save CTA:** for checklists, routines, rules, frameworks, product selection, finance decisions.
  - Example: “Salva para consultar antes de escolher.”
- **Share CTA:** for audience identity, warnings, comparisons, or useful reminders.
  - Example: “Envia para quem sempre fica em dúvida nisso.”
- **Comment CTA:** for preference, experience, or objection discovery.
  - Example: “Qual parte mais pega para você?”
- **DM CTA:** for private/commercial/sensitive follow-up.
  - Example: “Se quiser, me chama no direct com ‘rotina’.”

Do not stack multiple CTAs. Do not ask for meaningless comments such as “comenta SIM”. The CTA must be a natural next action.

## Caption and SEO support

The caption should:

- restate the hook in natural language;
- add 1–3 short context paragraphs;
- include the same CTA as the final slide;
- use natural keywords people might search for;
- keep hashtags relevant and limited.

The caption must not compensate for weak cards. A viewer should understand the core value by swiping only.

## Visual and readability rules

- One idea per slide.
- Large mobile-first headline.
- Minimal body text.
- Strong contrast.
- Clear slide-to-slide continuity.
- No clutter, no generic templates, no “wall of text”.
- No orphan/single-word wrapped lines.
- Do not add slide counters unless the project spec explicitly allows them.

## Shortlist requirements for carousels

When a discovery/intake job is generating carousel ideas, every item should include:

- `theme`: short topic;
- `output_format`: `carousel`;
- `carousel_type`: one allowed carousel format;
- `hook`: proposed cover promise;
- `save_share_reason`: why someone would save or send it;
- `primary_cta`: `save`, `share`, `comment`, or `dm`;
- `slide_arc`: compact 4–8 step arc;
- `why_it_engages`: why the topic creates swipes, saves, shares, comments, or DMs.

The user-facing shortlist should still be exactly 5 numbered ideas, but each idea should read like a carousel execution, not just a broad topic.

## Anti-patterns

Reject or rewrite carousel ideas that are:

- generic tips with no audience tension;
- long article paragraphs split across slides;
- isolated facts without continuity;
- too promotional too early;
- unsupported statistics or claims;
- vague hooks that do not promise a useful outcome;
- multiple unrelated topics in one deck;
- final CTAs disconnected from the content.

## Validation checklist

- [ ] Is the cover specific enough to earn a swipe?
- [ ] Does every slide add new value or curiosity?
- [ ] Is the deck useful enough to save or send?
- [ ] Is there one primary CTA matched to the content objective?
- [ ] Is the slide count justified by the idea?
- [ ] Are claims supported or conservatively framed?
- [ ] Are cards readable on mobile with no orphan lines?
- [ ] Does the caption support the same promise and CTA?
- [ ] Does the visual direction fit the project spec and template?
