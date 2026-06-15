from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .core import (
    BootstrapValidationError,
    bootstrap_project,
    result_to_dict,
    validate_bootstrap_environment,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="insta_creator_bootstrap",
        description="Bootstrap the shared Insta Creator workflow scaffold.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--target", required=True, help="Target directory to bootstrap")
        subparser.add_argument("--project-name", help="Project name to use in templates")
        subparser.add_argument(
            "--project-spec",
            help="Override path to the project spec Markdown file",
        )
        subparser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")

    plan = subparsers.add_parser("plan", help="Show the actions the bootstrap would take")
    add_common(plan)

    apply = subparsers.add_parser("apply", help="Create or refresh the shared scaffold")
    add_common(apply)
    apply.add_argument("--dry-run", action="store_true", help="Show actions without writing files")

    validate = subparsers.add_parser("validate", help="Validate an existing bootstrap scaffold")
    validate.add_argument("--target", required=True, help="Target directory to validate")
    validate.add_argument("--project-spec", help="Override path to the project spec Markdown file")

    return parser


def _print_actions(data: dict[str, object]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"plan", "apply"}:
        result = bootstrap_project(
            target=Path(args.target),
            project_name=args.project_name,
            project_spec_path=args.project_spec,
            dry_run=(args.command == "plan") or args.dry_run,
            force=args.force,
        )
        _print_actions(result_to_dict(result))
        return 0

    if args.command == "validate":
        try:
            status = validate_bootstrap_environment(args.target, project_spec_path=args.project_spec)
        except BootstrapValidationError as exc:
            print(str(exc))
            return 1
        _print_actions(status)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
