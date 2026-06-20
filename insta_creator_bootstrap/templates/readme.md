# Insta Creator Bootstrap

This scaffold was created by the reusable bootstrap package.

## What it includes
- a project spec template
- planning docs
- a deterministic post storage root
- a reusable bootstrap CLI
- audit and approval workflow references
- a documented `.env` contract for companion posting helpers

## Bootstrap commands
1. Inspect the available actions:
   ```bash
   python -m insta_creator_bootstrap --help
   ```
2. Plan the scaffold:
   ```bash
   python -m insta_creator_bootstrap plan --target <dir>
   ```
3. Apply the scaffold:
   ```bash
   python -m insta_creator_bootstrap apply --target <dir>
   ```
4. Validate the scaffold:
   ```bash
   python -m insta_creator_bootstrap validate --target <dir>
   ```

## Posting credentials
If your project uses a companion Instagram publishing helper, configure credentials in `.env`.

Recommended pattern:
```bash
cp .env.example .env
# or
ln -sf ~/.hermes/.env .env
```

Expected variables:
- `INSTAGRAM_ACCESS_TOKEN`
- `FACEBOOK_USER_ACCESS_TOKEN` (optional)
- `FACEBOOK_APP_ID` (optional)
- `FACEBOOK_APP_SECRET` (optional)

## Cron jobs
Typical queues to wire after bootstrap:
1. content idea intake
2. content creation
3. audit pass
4. growth actions

If you use Hermes cron, create the jobs from the project directory with `--workdir <project-path>` so the project context is available.

## Next steps
1. Fill in the project spec.
2. Review the typography, voice, visual rules, and CTA conventions.
3. Wire cron jobs for content intake, content creation, audit, and growth actions.
4. Configure the `.env` file or symlink it to `~/.hermes/.env`.
5. Use the bootstrap CLI to validate the scaffold.
