# Visual Template Contract

This contract defines the reusable visual-rendering rules for Instagram card assets. It is generic: the rule names are shared, while concrete values come from the selected project spec and visual template.

## Purpose
A visual template prevents the renderer from inventing layout elements during post generation. It must be loaded alongside the selected `project_spec_path` before rendering `assets/*.png`.

## Required inputs
Every production run must resolve:
- `project_id`
- `project_spec_path`
- `visual_template_path`
- `post_id`
- `cards_json_path`
- `asset_output_dir`

## Generic rendering rules
These rules apply to every project unless the selected visual template explicitly overrides them.

### Slide chrome
- No slide counter unless the selected visual template explicitly enables one.
- No decorative metadata labels unless the selected visual template explicitly defines them.
- No random footer text, tags, keywords, dates, or category labels unless they are real content from `cards.json` and required by the template.

### Text containers
- Do not place the main headline/body inside a large box or panel unless the selected visual template explicitly requires it.
- Avoid generic card-within-card layouts by default.
- Text hierarchy should come from typography, whitespace, alignment, and color — not from boxing every block.

### Typography
- Headline minimum size comes from the selected project spec or visual template.
- Body maximum lines and body size come from the selected project spec or visual template.
- If text does not fit, reduce copy or split slides before shrinking below the minimum.
- Legibility on mobile has priority over fitting more copy.

### Logo / mark
- Logo/mark placement comes from the selected project spec or visual template.
- Logo/mark size comes from the selected project spec or visual template.
- Do not invent wordmarks, watermarks, or repeated branding placements.

### Margins and composition
- Margins come from the selected visual template.
- Keep safe areas explicit: top, sides, bottom.
- Respect the project’s alignment rule: left, centered, asymmetric, or mixed.
- Whitespace is part of the template and must not be filled with decorative noise.

### Background
- Background style comes from the selected project spec or visual template.
- Use only approved colors, gradients, textures, and visual motifs.
- Decorative effects must be subtle and specified.

### Prohibited examples
Each project template must list prohibited examples/anti-patterns. The renderer must check them before approval.

Generic anti-patterns:
- slide counters added by default
- main text inside a generic square/panel by default
- decorative labels like `Body`, `Insight`, `IPCA • orçamento • decisão` unless explicitly required
- dense grid/noise that competes with the copy
- tiny headline or body text used to cram too much content
- visual elements not traceable to the project spec/template

## Required visual template sections
A project visual template should define:
1. Canvas
2. Background
3. Margins and safe areas
4. Typography sizes and limits
5. Logo / mark placement
6. Layout patterns
7. CTA slide pattern
8. Decorative elements allowed
9. Decorative elements prohibited
10. Renderer fit rules
11. Visual audit checklist

## Visual audit checklist
- Was `visual_template_path` loaded?
- Does the output obey the selected project spec?
- Does the output obey the selected visual template?
- Are slide counters absent unless enabled?
- Are generic text boxes absent unless enabled?
- Are random metadata/footer labels absent unless enabled?
- Are headline/body sizes within the allowed ranges?
- Is logo placement correct?
- Are margins correct?
- Is the background on-brand and not noisy?
- Are all images present and free of cutoffs?
