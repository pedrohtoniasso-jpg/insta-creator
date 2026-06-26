from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from insta_creator_bootstrap.integration import (
    build_trace_context,
    content_run_input_to_prompt,
    load_project_spec,
    normalize_content_run_input,
    normalize_cron_intake,
    queue_growth_actions,
)
from insta_creator_bootstrap.selection_state import (
    load_latest_shortlist,
    parse_selection_reply,
    resolve_selection_reply,
    save_latest_shortlist,
)


class IntegrationTests(unittest.TestCase):
    def _write_spec(self, root: Path) -> Path:
        spec = root / "docs" / "project-spec.md"
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_text(
            """# Brand Spec: Example Project

## Project name
Example Project

## Target platform
Instagram

## Brand voice
Friendly, concise, and helpful.

## Visual rules
High-contrast layouts with clean typography.

## CTA conventions
Use one direct CTA and one softer secondary CTA.

## Growth strategy
Follow/unfollow and likes are automatic; reply drafts require approval.

## Approval behavior
Approval channel: main channel
Reply drafts are approved in batches before sending.

## Prohibited angles
No exaggerated claims.

## Asset constraints
Keep images lightweight.

## Operational notes
Prefer dry runs for new workflows.
""",
            encoding="utf-8",
        )
        return spec

    def _write_project_spec(self, root: Path, project_id: str = "demo") -> Path:
        spec = root / "docs" / "projects" / project_id / "project-spec.md"
        spec.parent.mkdir(parents=True, exist_ok=True)
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
Use one direct CTA.

## Growth strategy
No automated replies without approval.

## Approval behavior
Approval channel: main channel
Send rendered assets plus copy for approval.

## Prohibited angles
No exaggerated claims.

## Asset constraints
Use lightweight PNG assets.

## Operational notes
Keep runs traceable.
""",
            encoding="utf-8",
        )
        return spec

    def _write_visual_template(self, root: Path, project_id: str = "demo", *, story: bool = False) -> Path:
        name = "story-visual-template.md" if story else "visual-template.md"
        canvas = "1080×1920" if story else "1080×1350"
        template = root / "docs" / "projects" / project_id / name
        template.parent.mkdir(parents=True, exist_ok=True)
        template.write_text(
            f"""# Visual Template: Demo {'Story' if story else 'Carousel'}

## Template identity
- Template ID: `demo-{'story' if story else 'carousel'}-v1`

## Canvas
- Size: {canvas} px
- Safe area:
  - left: 88 px
  - right: 88 px
  - top: 120 px
  - bottom: 140 px

## Background
- Primary background: `#020817`
- Secondary background: `#0f172a`
- Accent primary: `#0066ff`

## Typography
- Headline:
  - minimum: 96 px
  - preferred: 120 px
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
- Use clean mobile-first hierarchy.
- Do not enable slide counter.
- Do not allow a main text box.

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
        return template

    def test_load_project_spec_reads_sections(self) -> None:
        with TemporaryDirectory() as tmp:
            spec = load_project_spec(self._write_spec(Path(tmp)))
            self.assertEqual(spec.title, "Brand Spec: Example Project")
            self.assertEqual(spec.project_name, "Example Project")
            self.assertEqual(spec.target_platform, "Instagram")
            self.assertIn("growth strategy", spec.sections)
            self.assertIn("reply drafts require approval", spec.sections["growth strategy"].lower())

    def test_normalize_cron_intake_preserves_traceable_fields(self) -> None:
        intake = normalize_cron_intake(
            {
                "idea_text": "Build a post about clean workflows",
                "priority": "high",
                "format": "carousel",
                "source_channel": "cron:last30days",
                "campaign_id": "camp-123",
                "extra_context": "weekend trend",
            },
            source="cron",
            project_name="Example Project",
            project_spec_path="/tmp/project-spec.md",
        )
        self.assertEqual(intake.idea_text, "Build a post about clean workflows")
        self.assertEqual(intake.priority_hint, "high")
        self.assertEqual(intake.format_hint, "carousel")
        self.assertEqual(intake.source, "cron")
        self.assertEqual(intake.project_name, "Example Project")
        self.assertNotIn("source_channel", intake.structured_fields)
        self.assertIn("extra_context", intake.structured_fields)
        self.assertTrue(intake.trace_id)

    def test_queue_growth_actions_separates_approval_and_batches_replies(self) -> None:
        with TemporaryDirectory() as tmp:
            spec = load_project_spec(self._write_spec(Path(tmp)))
            intake = normalize_cron_intake("Write a clean workflow post", project_name=spec.project_name)
            trace = build_trace_context(spec, intake)
            queue = queue_growth_actions(
                [
                    "follow",
                    {"action_type": "comment_like", "post_id": "abc"},
                    {"action_type": "reply_draft", "body": "Thanks!", "batch_id": "batch-1"},
                    {"action_type": "reply_draft", "body": "Appreciate it!", "batch_id": "batch-1"},
                ],
                trace=trace,
            )
            self.assertEqual(len(queue.automatic), 2)
            self.assertEqual(len(queue.approval_required), 2)
            self.assertEqual(len(queue.reply_batches), 1)
            self.assertEqual(queue.reply_batches[0].action_type, "reply_batch")
            self.assertEqual(queue.reply_batches[0].payload["batch_id"], "batch-1")
            self.assertEqual(len(queue.reply_batches[0].payload["drafts"]), 2)
            self.assertEqual(queue.approval_required[0].trace["project_spec_path"], str(spec.path))

    def test_normalize_content_run_input_resolves_project_spec_and_visual_template(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_project_spec(root)
            self._write_visual_template(root)
            run_input = normalize_content_run_input(
                {
                    "project_id": "demo",
                    "theme": "Clean workflow checklist",
                    "source": "cron:demo",
                    "user_action": "select",
                },
                root=root,
            )
            self.assertTrue(run_input.project_spec_path.endswith("docs/projects/demo/project-spec.md"))
            self.assertTrue(run_input.visual_template_path.endswith("docs/projects/demo/visual-template.md"))
            self.assertEqual(run_input.user_action, "select")
            prompt = content_run_input_to_prompt(run_input)
            self.assertIn("project_spec_path", prompt)
            self.assertIn("visual_template_path", prompt)
            self.assertIn("Clean workflow", prompt)

    def test_normalize_content_run_input_accepts_nested_selection_envelope(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_spec = self._write_project_spec(root)
            visual_template = self._write_visual_template(root)
            run_input = normalize_content_run_input(
                {
                    "project_id": "demo",
                    "selection": {
                        "shortlist_id": "cron:demo",
                        "selected_option": 3,
                        "user_action": "select",
                    },
                    "shortlist": [
                        {"theme": "Tema 1"},
                        {"theme": "Tema 2"},
                        {"theme": "Inflação pressionando o carrinho de compras"},
                        {"theme": "Tema 4"},
                        {"theme": "Tema 5"},
                    ],
                    "project_spec_path": str(project_spec),
                    "visual_template_path": str(visual_template),
                },
                root=root,
            )
            self.assertEqual(run_input.theme, "Inflação pressionando o carrinho de compras")
            self.assertEqual(run_input.user_action, "select")
            self.assertEqual(run_input.structured_fields["selection"]["shortlist_id"], "cron:demo")
            self.assertEqual(run_input.structured_fields["selection"]["selected_option"], 3)

    def test_normalize_content_run_input_requires_change_request_for_revision(self) -> None:
        with self.assertRaises(Exception):
            normalize_content_run_input(
                {"project_id": "demo", "theme": "Tema", "user_action": "revise"},
                root=Path(__file__).resolve().parents[1],
            )

    def test_selection_reply_parser_accepts_one_digit_and_option_label(self) -> None:
        self.assertEqual(parse_selection_reply("5"), 5)
        self.assertEqual(parse_selection_reply("Opção 3"), 3)
        self.assertIsNone(parse_selection_reply("opção 7"))
        self.assertIsNone(parse_selection_reply("quero a terceira"))

    def test_latest_shortlist_state_resolves_one_digit_reply(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_spec = self._write_project_spec(root)
            visual_template = self._write_visual_template(root)
            save_latest_shortlist(
                project_id="demo",
                job_id="demo-job",
                root=tmp,
                project_spec_path=str(project_spec),
                visual_template_path=str(visual_template),
                shortlist=[
                    {"theme": "Tema 1"},
                    {"theme": "Tema 2"},
                    {"theme": "Tema 3"},
                    {"theme": "Tema 4"},
                    {"theme": "Controle financeiro simples: app ou planilha?"},
                ],
            )
            state = load_latest_shortlist("demo", root=tmp)
            self.assertEqual(state.shortlist[4]["theme"], "Controle financeiro simples: app ou planilha?")
            run_input = resolve_selection_reply("Opção 5", project_id="demo", root=tmp)
            self.assertEqual(run_input.theme, "Controle financeiro simples: app ou planilha?")
            self.assertEqual(run_input.source, "cron:demo-job")
            self.assertEqual(run_input.structured_fields["selection"]["selected_option"], 5)
            self.assertTrue(run_input.project_spec_path.endswith("docs/projects/demo/project-spec.md"))
            self.assertTrue(run_input.visual_template_path.endswith("docs/projects/demo/visual-template.md"))

    def test_carousel_shortlist_preserves_carousel_format_and_engagement_fields(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_spec = self._write_project_spec(root)
            visual_template = self._write_visual_template(root)
            save_latest_shortlist(
                project_id="demo",
                job_id="carousel-123",
                root=tmp,
                project_spec_path=str(project_spec),
                visual_template_path=str(visual_template),
                output_format="carousel",
                shortlist=[
                    {
                        "theme": "Limite por aproximação: quando vira risco",
                        "carousel_type": "trend_explainer",
                        "hook": "O detalhe que muda sua decisão",
                        "save_share_reason": "Regra prática para revisar limite antes de usar",
                        "primary_cta": "save",
                        "slide_arc": ["hook", "risco", "contexto", "decisão", "regra", "cta"],
                    },
                    {"theme": "Custo real", "carousel_type": "comparison"},
                    {"theme": "Checklist antes de comprar", "carousel_type": "checklist"},
                    {"theme": "Erro comum", "carousel_type": "mistakes"},
                    {"theme": "Regra simples", "carousel_type": "framework"},
                ],
            )
            run_input = resolve_selection_reply("1", project_id="demo", root=tmp)
            self.assertEqual(run_input.output_format, "carousel")
            self.assertEqual(run_input.structured_fields["shortlist"][0]["carousel_type"], "trend_explainer")
            self.assertEqual(run_input.structured_fields["shortlist"][0]["primary_cta"], "save")
            prompt = content_run_input_to_prompt(run_input)
            self.assertIn("docs/carousel-workflow-contract.md", prompt)
            self.assertIn('\"output_format\": \"carousel\"', prompt)

    def test_story_shortlist_preserves_story_format_and_template(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_spec = self._write_project_spec(root)
            visual_template = self._write_visual_template(root, story=True)
            save_latest_shortlist(
                project_id="demo",
                job_id="story-123",
                root=tmp,
                project_spec_path=str(project_spec),
                visual_template_path=str(visual_template),
                output_format="story",
                shortlist=[
                    {
                        "theme": "Which routine step do you forget?",
                        "story_type": "poll_preference",
                        "sticker": {"type": "poll", "prompt": "Which one?", "options": ["Hydrate", "Protect"]},
                    },
                    {"theme": "Myth or fact", "story_type": "quiz"},
                    {"theme": "Behind the scenes", "story_type": "question_box"},
                    {"theme": "Choose a finish", "story_type": "poll_this_or_that"},
                    {"theme": "Want a quick tip?", "story_type": "dm_prompt"},
                ],
            )
            run_input = resolve_selection_reply("1", project_id="demo", root=tmp)
            self.assertEqual(run_input.output_format, "story")
            self.assertEqual(run_input.theme, "Which routine step do you forget?")
            self.assertTrue(run_input.visual_template_path.endswith("docs/projects/demo/story-visual-template.md"))
            self.assertEqual(run_input.structured_fields["shortlist"][0]["story_type"], "poll_preference")
            prompt = content_run_input_to_prompt(run_input)
            self.assertIn("docs/story-workflow-contract.md", prompt)
            self.assertIn('\"output_format\": \"story\"', prompt)


if __name__ == "__main__":
    unittest.main()
