# Bootstrap Package

## Purpose
The bootstrap package prepares a new environment for the shared Instagram content workflow without hardcoding brand-specific logic.

## CLI
- `python -m insta_creator_bootstrap plan --target <dir>`
- `python -m insta_creator_bootstrap apply --target <dir>`
- `python -m insta_creator_bootstrap validate --target <dir>`

## Behavior
- Uses a hybrid onboarding model: defaults first, prompts can be added later if needed.
- Generates only the essential scaffold.
- Validates a project spec if one exists.
- Supports dry-run output.
- Keeps brand rules outside the shared bootstrap.
