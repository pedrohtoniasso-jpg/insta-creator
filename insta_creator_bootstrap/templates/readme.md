# {{ project_name }}

This scaffold was created by the reusable Insta Creator bootstrap package.

## Next steps
1. Fill in `docs/project-spec.md` with the active project’s real brand rules.
2. Confirm visual identity, typography, logo/mark rules, CTA conventions, and approval behavior.
3. Wire discovery cron to return exactly 5 numbered ideas.
4. Let the user continue by replying with `1`-`5` or explicitly naming a theme.
5. Run content production through `skills/social-media/insta-creator-workflow/SKILL.md`.
6. Validate the scaffold:

```bash
python -m insta_creator_bootstrap validate --target .
```

## Production rule
The user should see only the shortlist/selection gate and the final approval payload. Internal brief, narrative, checklist, JSON, and rendering steps are orchestrator-owned.

## Approval payload
Final approval should include:
- final caption
- rendered card images already created for the post

The internal bundle still keeps:
- `manifest.json`
- `brief.md`
- `cards.json`
- `caption.md`
- `approval.md`
- `assets/`
