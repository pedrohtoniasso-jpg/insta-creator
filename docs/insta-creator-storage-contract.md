# Storage Contract

## Goal
Store each post as a self-contained artifact bundle that can be reviewed, approved, and published without losing traceability. Story bundles use the same folder contract, but they should record the story format explicitly in the manifest and frame layout notes.

## Folder root
The post storage root is configurable per project, with a local default supplied by the bootstrap.

Default local root:
- `content/posts/`

Examples:
- `content/posts/`
- a project-specific root defined in the project config

## Folder naming
Use a deterministic folder name:

```text
YYYY.MM.DD - Short subject
```

Examples:
- `2026.06.14 - Receita simples`
- `2026.06.14 - Novo posicionamento`

## Required files
Each post folder must contain:
- `manifest.json`
- `brief.md`
- `cards.json`
- `caption.md`
- `approval.md`
- `assets/`

## `assets/` rules
- Store generated images or media files here.
- Use stable file names such as `01.png`, `02.png`, `03.png`.
- Do not mix unrelated assets from other posts.
- Generated images should be checked against the brief, cards, and project-spec visual rules before approval.
- If an image is changed, rejected, or re-generated, record the reason in the approval bundle or manifest notes.

## `manifest.json` minimum fields
The manifest should capture at least:
- Project name
- Post title / subject
- Date
- Source idea or prompt
- Content format
- Status
- Artifact list
- Approval state

## Traceability
The storage bundle must preserve the path from idea → brief → cards → caption → approval → publication.

## Validation rule
A later workflow skill should be able to confirm that a post is complete by checking only the folder contents and the manifest metadata.
