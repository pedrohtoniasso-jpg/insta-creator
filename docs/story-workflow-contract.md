# Instagram Story Workflow Contract

This document defines how Insta Creator should treat **Instagram Stories** so a story request does not become a carousel, feed post, or multi-post sequence.

## Research-backed premise

Current Instagram guidance and social-media playbooks consistently point to Stories as a proximity and interaction format, not as a long-form publishing format:

- Instagram creator/community guidance highlights Q&A, polls, DMs, and feedback loops as ways to listen to the audience and build community.
- Story marketing references emphasize interactive stickers — polls, quizzes, questions, sliders, links — because they turn passive viewers into active participants.
- Brand playbooks position Stories as a direct line to audience conversation, not a substitute for a carousel.

Operational implication: a Story idea should usually be a **single 9:16 interaction unit** with one question, one visual cue, and one next action.

## Default Story unit

A Story unit is one full-screen frame with:

1. **Hook:** one short phrase that makes the viewer stop.
2. **Context:** optional supporting line; keep it short.
3. **Interactive sticker directive:** the exact sticker type and prompt to add natively in Instagram.
4. **CTA:** one next action, usually vote, answer, send a DM, or tap a link when permitted.
5. **Visual direction:** one simple background/product/face/bastidor cue.

Default dimensions: `1080×1920` PNG.

## Allowed Story formats

Use these as canonical story types in briefs, shortlists, and cards/story JSON:

- `poll_this_or_that`: two-choice poll, lowest-friction engagement.
- `poll_preference`: audience chooses preference, routine, concern, or product angle.
- `question_box`: open answer, good for objections, doubts, and consultation prompts.
- `quiz`: one right answer or playful myth/fact question.
- `emoji_slider`: intensity/feeling/relevance check.
- `dm_prompt`: direct-message invitation with a soft trigger phrase.
- `behind_the_scenes`: proximity/bastidores; can include a question sticker.
- `quick_tip`: one useful tip, not a mini article.
- `myth_fact`: one misconception compressed into a quiz or poll.
- `social_proof_prompt`: ask viewers if they want to see/use/learn more; avoid unverified claims.

## Hard boundary: not a sequence of posts

For Story intake, reject or rewrite ideas that require:

- a sequence of educational slides;
- multiple post topics in one suggestion;
- carousel-style arcs such as problem → context → consequence → CTA;
- long explanations, numbered lists, or several tips;
- feed-copy captions as the primary deliverable.

If an incoming idea is a sequence, compress it into **one interactive Story unit** by choosing the strongest audience action.

Example compression:

- Incoming sequence: “3 posts about skincare routine: cleanse, moisturize, protect, then CTA.”
- Story unit: `poll_preference` — “Qual etapa você mais esquece na rotina?” Options: “Hidratar” / “Proteger”. CTA: “Responde aqui que eu te mando uma dica simples no direct.”

## Shortlist requirements for Stories

When a discovery/intake job is generating Story ideas, every item must include:

- `theme`: short topic, not a post series title;
- `output_format`: `story`;
- `story_type`: one allowed Story format;
- `hook`: short on-screen text;
- `sticker`: object with `type`, `prompt`, and optional `options`;
- `cta`: one next action;
- `visual_direction`: one 9:16 visual cue;
- `why_it_engages`: why this prompts a reply, tap, vote, or DM.

The user-facing shortlist should still be exactly 5 numbered ideas, but each idea should read like a Story execution, not like a content-calendar sequence.

## Story narrative standard

A Story is not a carousel. Use this micro-arc:

1. Stop: hook.
2. Invite: question/sticker.
3. Move: CTA or DM prompt.

Do not use slide-count logic, long evidence sections, or multi-step educational arcs unless the explicit output format is a carousel.

## Approval package for Stories

A Story approval package should contain:

- the rendered 9:16 PNG frame;
- a short operator note listing the native Instagram sticker to add manually/API-side, because interactive stickers are platform-native elements and should not be baked into the static image as fake UI;
- optional copy-ready DM response if the Story asks people to DM.

Do not deliver a feed caption unless the user explicitly asks for a feed post.

## Sticker placement note rule

The static Story image may include a small placement guide inside the reserved sticker frame, but it must be short and fully contained. Prefer:

- `Coloque o sticker ENQUETE aqui`
- `Coloque o sticker PERGUNTAS aqui`
- `Sticker: QUIZ`

Never render long internal guidance such as “deixe livre o terço inferior para o sticker nativo do Instagram”. If the placement text clips or extends outside the sticker frame, rerender before approval.

## Validation checklist

- [ ] Is this executable as one 9:16 Story unit?
- [ ] Does it avoid becoming a carousel or sequence of posts?
- [ ] Is there exactly one primary audience action?
- [ ] Is the interactive sticker specified with prompt and options?
- [ ] If a placement note appears in the image, is it short and fully inside the sticker frame?
- [ ] Is the hook short enough for mobile?
- [ ] Does the CTA move to reply/vote/DM/link without public sales pressure?
- [ ] Does the visual direction fit the project spec and compliance rules?
