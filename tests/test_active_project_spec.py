from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowContractDocsTests(unittest.TestCase):
    def test_content_workflow_contract_preserves_hidden_orchestration(self) -> None:
        contract = (ROOT / "docs" / "content-workflow-contract.md").read_text(encoding="utf-8").lower()
        carousel_contract = (ROOT / "docs" / "carousel-workflow-contract.md").read_text(encoding="utf-8").lower()
        story_contract = (ROOT / "docs" / "story-workflow-contract.md").read_text(encoding="utf-8").lower()
        visual_contract = (ROOT / "docs" / "visual-template-contract.md").read_text(encoding="utf-8").lower()
        self.assertIn("the user is not the orchestrator", contract)
        self.assertIn("carousel-workflow-contract.md", contract)
        self.assertIn("story-workflow-contract.md", contract)
        self.assertIn("validate the brief with a checklist", contract)
        self.assertIn("validate the narrative with a checklist", contract)
        self.assertIn("selected visual template", contract)
        self.assertIn("caption + rendered card images", contract)
        self.assertIn("swipeable value asset", carousel_contract)
        self.assertIn("save/share reason", carousel_contract)
        self.assertIn("primary engagement cta", carousel_contract)
        self.assertIn("single 9:16 interaction unit", story_contract)
        self.assertIn("sticker placement note rule", story_contract)
        self.assertIn("no slide counter", visual_contract)
        self.assertIn("generic rendering rules", visual_contract)


if __name__ == "__main__":
    unittest.main()
