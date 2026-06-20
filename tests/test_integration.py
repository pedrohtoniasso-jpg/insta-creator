from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from insta_creator_bootstrap.integration import (
    build_trace_context,
    build_workflow_continuation,
    load_project_spec,
    normalize_cron_intake,
    queue_growth_actions,
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
Approval channel: Telegram
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

    def test_load_project_spec_reads_sections(self) -> None:
        with TemporaryDirectory() as tmp:
            spec = load_project_spec(self._write_spec(Path(tmp)))
            self.assertEqual(spec.title, "Brand Spec: Example Project")
            self.assertEqual(spec.project_name, "Example Project")
            self.assertEqual(spec.target_platform, "Instagram")
            self.assertEqual(spec.approval_channel, "Telegram")
            self.assertIn("growth strategy", spec.sections)
            self.assertIn("reply drafts require approval", spec.sections["growth strategy"].lower())

    def test_normalize_cron_intake_preserves_traceable_fields(self) -> None:
        intake = normalize_cron_intake(
            {
                "idea_text": "Build a post about clean workflows",
                "priority": "high",
                "format": "carousel",
                "source_channel": "telegram:home",
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
        self.assertEqual(intake.content_format, "carousel")
        self.assertEqual(intake.source, "cron")
        self.assertEqual(intake.project_name, "Example Project")
        self.assertEqual(intake.source_channel, "telegram:home")
        self.assertNotIn("source_channel", intake.structured_fields)
        self.assertIn("extra_context", intake.structured_fields)
        self.assertTrue(intake.trace_id)

    def test_normalize_cron_intake_supports_story_format(self) -> None:
        with TemporaryDirectory() as tmp:
            spec = load_project_spec(self._write_spec(Path(tmp)))
            intake = normalize_cron_intake(
                {
                    "idea_text": "Tease the new launch in a story sequence",
                    "format": "stories",
                },
                project_name=spec.project_name,
                project_spec_path=spec.path,
            )
            self.assertEqual(intake.content_format, "story")
            self.assertEqual(intake.format_hint, "stories")
            trace = build_trace_context(spec, intake)
            self.assertEqual(trace["content_format"], "story")

    def test_workflow_continuation_uses_main_channel_and_hides_internal_stages(self) -> None:
        with TemporaryDirectory() as tmp:
            spec = load_project_spec(self._write_spec(Path(tmp)))
            intake = normalize_cron_intake(
                {
                    "idea_text": "Write a clean workflow post",
                    "source_channel": "telegram:home",
                },
                project_name=spec.project_name,
            )
            continuation = build_workflow_continuation(
                spec,
                intake,
                selected_theme="Pix parcelado vs cartão",
            )
            self.assertEqual(continuation.current_stage, "theme_selected")
            self.assertEqual(continuation.next_stage, "brief")
            self.assertTrue(continuation.approval_delivery.final_only)
            self.assertEqual(continuation.approval_delivery.channel, "Telegram")
            self.assertEqual(continuation.approval_delivery.visible_payload, ("images", "caption"))
            self.assertIn("brief", continuation.hidden_stages)

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

    def test_workflow_continuation_uses_story_frame_visibility(self) -> None:
        with TemporaryDirectory() as tmp:
            spec = load_project_spec(self._write_spec(Path(tmp)))
            intake = normalize_cron_intake(
                {
                    "idea_text": "Create a story teaser",
                    "format": "story",
                },
                project_name=spec.project_name,
            )
            continuation = build_workflow_continuation(
                spec,
                intake,
                selected_theme="Launch teaser",
            )
            self.assertEqual(continuation.approval_delivery.visible_payload, ("story_frames", "caption"))


if __name__ == "__main__":
    unittest.main()
