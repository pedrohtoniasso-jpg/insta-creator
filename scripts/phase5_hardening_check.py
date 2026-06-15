#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from insta_creator_bootstrap.core import bootstrap_project, validate_bootstrap_environment

POST_FOLDER_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2} - .+$")
REQUIRED_POST_FILES = [
    "manifest.json",
    "brief.md",
    "cards.json",
    "caption.md",
    "approval.md",
    "assets",
]


def _make_sample_post_bundle(posts_root: Path) -> dict[str, Any]:
    post_dir = posts_root / "2026.06.15 - Hardening demo"
    assets_dir = post_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "post_id": "2026.06.15-hardening-demo",
        "folder_name": post_dir.name,
        "idea_source": "cron-fed demo input",
        "project_spec": "docs/project-spec.md",
        "verification_notes": [
            "bootstrap validated in a clean temp directory",
            "image verification audit trail recorded; no generated image supplied for this check",
        ],
        "artifacts": {
            "brief": "brief.md",
            "cards": "cards.json",
            "caption": "caption.md",
            "approval": "approval.md",
        },
    }
    cards = {
        "version": "1",
        "post_id": manifest["post_id"],
        "subject": "Hardening demo",
        "slide_count": 2,
        "cards": [
            {
                "slide": 1,
                "role": "hook",
                "headline": "Hardening makes the workflow safe to reuse",
                "body": "The bootstrap, workflow, and verification loops all agree on the same contract.",
                "visual_note": "Simple layout with strong contrast",
                "cta_note": "",
                "source_notes": ["phase 5 hardening checklist"],
            },
            {
                "slide": 2,
                "role": "proof",
                "headline": "Deterministic outputs make reuse easier",
                "body": "A clean temp run confirms the scaffold and the post bundle shape.",
                "visual_note": "Checklist-style proof slide",
                "cta_note": "",
                "source_notes": ["bootstrap validation run"],
            },
        ],
        "traceability": {
            "idea": "cron-fed demo input",
            "brief_source": "brief.md",
            "project_spec": "docs/project-spec.md",
            "content_root": "content/posts",
        },
    }
    files = {
        "brief.md": "# Brief\n\nHardening demo brief.\n",
        "cards.json": json.dumps(cards, indent=2, ensure_ascii=False) + "\n",
        "caption.md": "# Caption\n\nHardening demo caption.\n",
        "approval.md": "# Approval\n\nImage verification: recorded in manifest notes.\n",
        "manifest.json": json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    }
    for name, content in files.items():
        (post_dir / name).write_text(content, encoding="utf-8")
    (assets_dir / ".gitkeep").write_text("", encoding="utf-8")

    return {
        "post_dir": str(post_dir),
        "manifest": manifest,
        "cards": cards,
    }


def _validate_sample_post_bundle(post_dir: Path) -> None:
    assert POST_FOLDER_RE.match(post_dir.name), f"folder name not deterministic: {post_dir.name}"
    for rel in REQUIRED_POST_FILES:
        path = post_dir / rel
        assert path.exists(), f"missing expected post artifact: {rel}"

    manifest = json.loads((post_dir / "manifest.json").read_text(encoding="utf-8"))
    cards = json.loads((post_dir / "cards.json").read_text(encoding="utf-8"))

    assert manifest["folder_name"] == post_dir.name
    assert "verification_notes" in manifest and manifest["verification_notes"], "manifest missing verification trail"
    assert cards["slide_count"] == len(cards["cards"]), "slide_count mismatch"
    assert cards["traceability"]["project_spec"] == "docs/project-spec.md"



def run_check() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        apply = subprocess.run(
            [
                sys.executable,
                "-m",
                "insta_creator_bootstrap",
                "apply",
                "--target",
                str(tmp_path),
                "--project-name",
                "Hardening Demo",
            ],
            cwd=str(Path(__file__).resolve().parents[1]),
            capture_output=True,
            text=True,
            check=False,
        )
        if apply.returncode != 0:
            raise SystemExit(apply.stdout + apply.stderr)

        validate = subprocess.run(
            [sys.executable, "-m", "insta_creator_bootstrap", "validate", "--target", str(tmp_path)],
            cwd=str(Path(__file__).resolve().parents[1]),
            capture_output=True,
            text=True,
            check=False,
        )
        if validate.returncode != 0:
            raise SystemExit(validate.stdout + validate.stderr)

        bootstrap_project(tmp_path, project_name="Hardening Demo")
        validate_bootstrap_environment(tmp_path)

        sample = _make_sample_post_bundle(tmp_path / "content" / "posts")
        _validate_sample_post_bundle(Path(sample["post_dir"]))

        return {
            "bootstrap_apply_returncode": apply.returncode,
            "bootstrap_validate_returncode": validate.returncode,
            "bootstrap_validate_stdout": validate.stdout.strip(),
            "sample_post_dir": sample["post_dir"],
            "status": "pass",
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run phase 5 hardening checks.")
    parser.add_argument("--write-report", help="Optional path to write a JSON report")
    args = parser.parse_args()
    report = run_check()
    if args.write_report:
        Path(args.write_report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
