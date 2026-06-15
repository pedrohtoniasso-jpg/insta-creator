from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from insta_creator_bootstrap.integration import (
    build_trace_context,
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
        self.assertIn("source_channel", intake.structured_fields)
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


if __name__ == "__main__":
    unittest.main()
