from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from insta_creator_bootstrap.renderer import load_visual_template, render_cards


class RendererTests(unittest.TestCase):
    def _write_spec(self, root: Path) -> Path:
        spec = root / "project-spec.md"
        spec.write_text(
            """# Brand Spec: Demo Project

## Project name
Demo Project

## Target platform
Instagram

## Brand voice
Clear and helpful.

## Visual rules
Use high contrast and clean typography.

## CTA conventions
Use one clear CTA.

## Growth strategy
No automated replies without approval.

## Approval behavior
Approval channel: main channel
Send rendered assets and caption for approval.

## Prohibited angles
No exaggerated claims.

## Asset constraints
Use PNG assets.

## Operational notes
Keep traceability.
""",
            encoding="utf-8",
        )
        return spec

    def _write_template(self, root: Path, *, story: bool = False) -> Path:
        canvas = "1080×1920" if story else "1080×1350"
        path = root / ("story-template.md" if story else "carousel-template.md")
        path.write_text(
            f"""# Visual Template: Demo {'Story' if story else 'Carousel'}

## Template identity
- Template ID: `demo-{'story' if story else 'carousel'}-v1`

## Canvas
- Size: {canvas} px
- Safe area:
  - left: 88 px
  - right: 88 px
  - top: 76 px
  - bottom: 86 px

## Background
- Primary background: `#020817`
- Secondary background: `#0f172a`
- Accent primary: `#0066ff`

## Typography
- Headline:
  - minimum: 96 px
  - preferred: 124 px
  - max lines: 4
- Body:
  - minimum: 42 px
  - preferred: 52 px
  - max lines: 3

## Logo / mark
- Text: DEMO
- Position: top-left
- Size: 58 px

## Layout pattern
- Mobile-first hierarchy.
- Slide counters are prohibited.
- Main text boxes are prohibited.

## Decorative elements prohibited
- no slide counter
- no main text box
- no random metadata
- no fake interactive sticker UI

## Renderer fit rules
- Keep copy concise and mobile-readable.

## Visual audit checklist
- [ ] Canvas matches the selected format.
- [ ] No slide counter appears.
""",
            encoding="utf-8",
        )
        return path

    def _write_cards(self, root: Path, *, slide_count: int = 2, long: bool = False) -> Path:
        cards = {
            "version": "test",
            "post_id": "demo-post",
            "subject": "Demo",
            "slide_count": slide_count,
            "cards": [
                {
                    "slide": idx,
                    "role": "cover" if idx == 1 else "body",
                    "headline": " ".join(["palavra"] * 80) if long and idx == 1 else f"Demo headline {idx}",
                    "body": "Short readable body",
                    "visual_note": "test",
                }
                for idx in range(1, slide_count + 1)
            ],
            "traceability": {"idea": "test", "brief_source": "brief.md", "project_spec": "project-spec.md"},
        }
        cards_path = root / "cards.json"
        cards_path.write_text(json.dumps(cards), encoding="utf-8")
        return cards_path

    def test_visual_template_blocks_default_chrome(self) -> None:
        with TemporaryDirectory() as tmp:
            template = load_visual_template(self._write_template(Path(tmp)))
            self.assertEqual(template.canvas, (1080, 1350))
            self.assertFalse(template.allow_slide_counter)
            self.assertFalse(template.allow_main_text_box)
            self.assertFalse(template.allow_random_metadata)
            self.assertGreaterEqual(template.headline_min, 96)
            self.assertGreaterEqual(template.body_min, 42)
            self.assertEqual(template.logo_position, "top-left")
            self.assertEqual(template.accent_primary, "#0066ff")

    def test_story_template_uses_story_canvas(self) -> None:
        with TemporaryDirectory() as tmp:
            template = load_visual_template(self._write_template(Path(tmp), story=True))
            self.assertEqual(template.canvas, (1080, 1920))
            self.assertFalse(template.allow_slide_counter)
            self.assertFalse(template.allow_random_metadata)
            self.assertGreaterEqual(template.headline_min, 96)
            self.assertGreaterEqual(template.body_min, 42)

    def test_render_cards_outputs_expected_assets(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = render_cards(
                project_spec_path=self._write_spec(root),
                visual_template_path=self._write_template(root),
                cards_json_path=self._write_cards(root, slide_count=2),
                output_dir=root / "assets",
            )
            self.assertEqual(len(result.assets), 2)
            for idx, asset in enumerate(result.assets, start=1):
                self.assertEqual(asset.slide, idx)
                self.assertTrue(asset.path.exists())
                self.assertEqual((asset.width, asset.height), (1080, 1350))

    def test_render_rejects_copy_that_exceeds_template_limits(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(Exception):
                render_cards(
                    project_spec_path=self._write_spec(root),
                    visual_template_path=self._write_template(root),
                    cards_json_path=self._write_cards(root, slide_count=1, long=True),
                    output_dir=root / "assets",
                )


if __name__ == "__main__":
    unittest.main()
