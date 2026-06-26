from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence

from .core import BootstrapValidationError, validate_project_spec

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

_SECTION_SYNONYMS = {
    "project name": "project name",
    "name": "project name",
    "target platform": "target platform",
    "platform": "target platform",
    "brand voice": "brand voice",
    "voice": "brand voice",
    "visual rules": "visual rules",
    "cta conventions": "cta conventions",
    "growth strategy": "growth strategy",
    "approval behavior": "approval behavior",
    "prohibited angles": "prohibited angles",
    "prohibited angles or topics": "prohibited angles",
    "asset constraints": "asset constraints",
    "operational notes": "operational notes",
    "revision and learning loop": "revision and learning loop",
    "story storytelling style": "story storytelling style",
    "story style": "story storytelling style",
    "story format": "story storytelling style",
    "stories": "story storytelling style",
}

_CONTENT_FORMAT_ALIASES = {
    "carousel": "carousel",
    "carousels": "carousel",
    "feed": "carousel",
    "post": "carousel",
    "posts": "carousel",
    "story": "story",
    "stories": "story",
    "story_sequence": "story",
    "story_sequence_post": "story",
}

AUTO_GROWTH_ACTIONS = {"follow", "unfollow", "comment_like"}
APPROVAL_GROWTH_ACTIONS = {"reply_draft", "reply", "public_reply", "comment_reply", "dm_reply"}
REPLY_DRAFT_ACTIONS = {"reply_draft", "reply", "public_reply", "comment_reply", "dm_reply"}


@dataclass(frozen=True)
class ProjectSpec:
    """Parsed project-specific spec loaded from Markdown."""

    path: Path
    title: str
    raw_text: str
    sections: dict[str, str]
    section_order: tuple[str, ...]
    project_name: str | None = None
    target_platform: str | None = None
    approval_channel: str | None = None


@dataclass(frozen=True)
class CronIdeaIntake:
    """Normalized cron-fed idea input."""

    source: str
    source_channel: str | None
    idea_text: str
    trace_id: str
    priority_hint: str | None
    format_hint: str | None
    content_format: str | None
    project_name: str | None
    project_spec_path: str | None
    structured_fields: dict[str, Any]
    raw_input: dict[str, Any]


@dataclass(frozen=True)
class ContentRunInput:
    """Concrete input passed from cron selection into the Insta Creator orchestrator."""

    project_id: str
    project_spec_path: str
    visual_template_path: str
    theme: str
    source: str
    trace_id: str
    user_action: str
    output_format: str | None
    change_request: str | None
    structured_fields: dict[str, Any]
    raw_input: dict[str, Any]


@dataclass(frozen=True)
class GrowthAction:
    """A normalized growth action with traceability metadata."""

    action_type: str
    payload: dict[str, Any]
    requires_approval: bool
    trace: dict[str, Any]


@dataclass(frozen=True)
class GrowthActionQueue:
    """Separated automatic vs approval-gated growth actions."""

    automatic: tuple[GrowthAction, ...]
    approval_required: tuple[GrowthAction, ...]
    reply_batches: tuple[GrowthAction, ...]
    trace: dict[str, Any]


@dataclass(frozen=True)
class ApprovalDeliveryContract:
    """Visible output contract for the main approval channel."""

    channel: str
    visible_payload: tuple[str, ...]
    final_only: bool = True


@dataclass(frozen=True)
class WorkflowContinuation:
    """State for resuming the content flow after the user selects a theme."""

    trace: dict[str, Any]
    selected_theme: str
    approval_delivery: ApprovalDeliveryContract
    current_stage: str
    next_stage: str
    hidden_stages: tuple[str, ...]


def _normalize_heading(heading: str) -> str:
    return _SECTION_SYNONYMS.get(heading.strip().lower(), heading.strip().lower())


def _parse_markdown_sections(markdown: str) -> tuple[str, dict[str, str], tuple[str, ...]]:
    title = "Project Spec"
    sections: dict[str, list[str]] = {}
    section_order: list[str] = []
    current_section: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_section, current_lines
        if current_section is not None:
            sections[current_section] = "\n".join(current_lines).strip()
            section_order.append(current_section)
        current_section = None
        current_lines = []

    for line in markdown.splitlines():
        match = _HEADING_RE.match(line.strip())
        if match:
            level = len(match.group(1))
            heading = match.group(2).strip()
            if level == 1 and title == "Project Spec":
                title = heading
                continue
            if level >= 2:
                flush()
                current_section = _normalize_heading(heading)
                current_lines = []
                continue
        if current_section is not None:
            current_lines.append(line)

    flush()
    return title, {key: value for key, value in sections.items()}, tuple(section_order)


def load_project_spec(path: str | Path) -> ProjectSpec:
    """Load and validate a project-specific Markdown spec."""

    spec_path = Path(path).expanduser().resolve()
    raw_text = spec_path.read_text(encoding="utf-8")
    validate_project_spec(raw_text)
    title, sections, section_order = _parse_markdown_sections(raw_text)
    approval_channel = _prefixed_value(
        sections.get("approval behavior"),
        "approval channel",
        "main channel",
        "delivery channel",
    )
    return ProjectSpec(
        path=spec_path,
        title=title,
        raw_text=raw_text,
        sections=sections,
        section_order=section_order,
        project_name=_first_line(sections.get("project name")),
        target_platform=_first_line(sections.get("target platform")),
        approval_channel=approval_channel,
    )


def _first_line(text: str | None) -> str | None:
    if text is None:
        return None
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned.lstrip("-•*").strip()
    return None


def _prefixed_value(text: str | None, *labels: str) -> str | None:
    if text is None:
        return None
    for line in text.splitlines():
        cleaned = line.strip().lstrip("-•*").strip()
        for label in labels:
            if not cleaned.lower().startswith(label.lower()):
                continue
            remainder = cleaned[len(label):].strip()
            if remainder.startswith(":") or remainder.startswith("-"):
                remainder = remainder[1:].strip()
            if remainder.startswith("(") and ")" in remainder:
                tail = remainder[remainder.index(")") + 1 :].strip()
                if tail.startswith(":") or tail.startswith("-"):
                    tail = tail[1:].strip()
                if tail:
                    remainder = tail
            if remainder:
                return remainder
    return None


def _pick_first(raw: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in raw and raw[key] not in (None, ""):
            return raw[key]
    return None


def _stringify_hint(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value).strip() or None


def normalize_content_format(value: Any) -> str | None:
    """Normalize a content format hint to the shared story/carousel vocabulary."""

    text = _stringify_hint(value)
    if text is None:
        return None
    normalized = text.replace("-", "_").replace(" ", "_").lower()
    return _CONTENT_FORMAT_ALIASES.get(normalized, normalized)


def _trace_id(seed: str) -> str:
    return sha256(seed.encode("utf-8")).hexdigest()[:12]


def normalize_cron_intake(
    payload: str | Mapping[str, Any],
    *,
    source: str = "cron",
    project_name: str | None = None,
    project_spec_path: str | Path | None = None,
) -> CronIdeaIntake:
    """Normalize noisy cron-fed input into a traceable shared shape."""

    if isinstance(payload, str):
        raw = {"idea_text": payload}
    else:
        raw = dict(payload)

    idea_text = _stringify_hint(
        _pick_first(raw, "idea_text", "idea", "text", "prompt", "summary", "note")
    )
    if not idea_text:
        raise BootstrapValidationError("Cron intake must include non-empty idea text.")

    priority_hint = _stringify_hint(_pick_first(raw, "priority_hint", "priority"))
    format_hint = _stringify_hint(_pick_first(raw, "format_hint", "format", "post_format"))
    content_format = normalize_content_format(format_hint)
    source_value = _stringify_hint(_pick_first(raw, "source", "source_name")) or source
    project_name_value = _stringify_hint(_pick_first(raw, "project_name")) or project_name
    project_spec_path_value = (
        str(Path(project_spec_path).expanduser().resolve()) if project_spec_path else None
    )
    source_channel = _stringify_hint(_pick_first(raw, "source_channel", "delivery_channel"))
    trace_id = _stringify_hint(_pick_first(raw, "trace_id", "idea_id", "campaign_id"))
    if not trace_id:
        seed = "|".join(
            [
                source_value,
                idea_text,
                project_name_value or "",
                project_spec_path_value or "",
            ]
        )
        trace_id = _trace_id(seed)

    recognized_keys = {
        "idea_text",
        "idea",
        "text",
        "prompt",
        "summary",
        "note",
        "priority_hint",
        "priority",
        "format_hint",
        "format",
        "post_format",
        "source",
        "source_name",
        "source_channel",
        "delivery_channel",
        "project_name",
        "project_spec_path",
        "trace_id",
        "idea_id",
        "campaign_id",
    }
    structured_fields = {
        key: value
        for key, value in raw.items()
        if key not in recognized_keys
    }

    return CronIdeaIntake(
        source=source_value,
        source_channel=source_channel,
        idea_text=idea_text,
        trace_id=trace_id,
        priority_hint=priority_hint,
        format_hint=format_hint,
        content_format=content_format,
        project_name=project_name_value,
        project_spec_path=project_spec_path_value,
        structured_fields=structured_fields,
        raw_input=raw,
    )


def build_trace_context(project_spec: ProjectSpec, intake: CronIdeaIntake) -> dict[str, Any]:
    """Create a traceability payload that can be attached to workflow artifacts."""

    return {
        "trace_id": intake.trace_id,
        "source": intake.source,
        "source_channel": intake.source_channel,
        "idea_text": intake.idea_text,
        "project_name": project_spec.project_name or intake.project_name,
        "project_spec_path": str(project_spec.path),
        "approval_channel": project_spec.approval_channel,
        "lineage": ["cron-intake", "project-spec", "growth-queue"],
        "priority_hint": intake.priority_hint,
        "format_hint": intake.format_hint,
        "content_format": intake.content_format,
    }



def build_workflow_continuation(
    project_spec: ProjectSpec,
    intake: CronIdeaIntake,
    *,
    selected_theme: str,
    approval_channel: str | None = None,
    visible_payload: Sequence[str] = ("images", "caption"),
) -> WorkflowContinuation:
    """Build the continuation state after the user selects a theme."""

    trace = build_trace_context(project_spec, intake)
    resolved_channel = (
        _stringify_hint(approval_channel)
        or project_spec.approval_channel
        or intake.source_channel
        or intake.source
        or "main channel"
    )
    resolved_payload = tuple(visible_payload)
    if resolved_payload == ("images", "caption") and intake.content_format == "story":
        resolved_payload = ("story_frames", "caption")
    return WorkflowContinuation(
        trace=trace,
        selected_theme=selected_theme.strip(),
        approval_delivery=ApprovalDeliveryContract(
            channel=resolved_channel,
            visible_payload=resolved_payload,
            final_only=True,
        ),
        current_stage="theme_selected",
        next_stage="brief",
        hidden_stages=("brief", "cards", "caption", "audit", "approval_package"),
    )


def default_project_paths(project_id: str, *, root: str | Path = ".") -> tuple[Path, Path]:
    """Return default spec/template paths for a project id under docs/projects/<id>."""

    slug = re.sub(r"[^a-z0-9]+", "-", project_id.strip().lower()).strip("-")
    if not slug:
        raise BootstrapValidationError("project_id is required.")
    base = Path(root).expanduser().resolve() / "docs" / "projects" / slug
    return base / "project-spec.md", base / "visual-template.md"


def normalize_content_run_input(
    payload: Mapping[str, Any],
    *,
    root: str | Path = ".",
    source: str = "cron-selection",
) -> ContentRunInput:
    """Normalize the handoff created after the user selects or revises a cron idea."""

    raw = dict(payload)
    selection = raw.get("selection") if isinstance(raw.get("selection"), Mapping) else {}
    if selection:
        for key, value in dict(selection).items():
            raw.setdefault(key, value)
    shortlist_value = raw.get("shortlist")
    shortlist = shortlist_value if isinstance(shortlist_value, Sequence) and not isinstance(shortlist_value, (str, bytes)) else []

    project_id = _stringify_hint(_pick_first(raw, "project_id", "project", "brand", "page"))
    if not project_id:
        raise BootstrapValidationError("Content run input must include project_id.")
    theme = _stringify_hint(_pick_first(raw, "theme", "selected_theme", "idea_text", "idea", "topic"))
    selected_item: Mapping[str, Any] | None = None
    if shortlist:
        selected_option = _stringify_hint(_pick_first(raw, "selected_option", "choice", "selection_option"))
        if selected_option and selected_option.isdigit():
            index = int(selected_option) - 1
            if 0 <= index < len(shortlist):
                candidate_item = shortlist[index]
                if isinstance(candidate_item, Mapping):
                    selected_item = candidate_item
                    if not theme:
                        theme = _stringify_hint(
                            _pick_first(selected_item, "theme", "selected_theme", "idea_text", "idea", "topic")
                        )
    if not theme:
        raise BootstrapValidationError("Content run input must include selected theme/topic.")

    default_spec, default_template = default_project_paths(project_id, root=root)
    spec_path = Path(_stringify_hint(_pick_first(raw, "project_spec_path", "project_spec")) or default_spec).expanduser()
    template_path = Path(_stringify_hint(_pick_first(raw, "visual_template_path", "visual_template")) or default_template).expanduser()
    if not spec_path.is_absolute():
        spec_path = Path(root).expanduser().resolve() / spec_path
    if not template_path.is_absolute():
        template_path = Path(root).expanduser().resolve() / template_path
    if not spec_path.exists():
        raise BootstrapValidationError(f"Selected project spec does not exist: {spec_path}")
    if not template_path.exists():
        raise BootstrapValidationError(f"Selected visual template does not exist: {template_path}")

    action = (_stringify_hint(_pick_first(raw, "user_action", "action")) or "select").lower()
    if action not in {"select", "revise"}:
        raise BootstrapValidationError("user_action must be 'select' or 'revise'.")
    change_request = _stringify_hint(_pick_first(raw, "change_request", "revision", "alteration", "feedback"))
    if action == "revise" and not change_request:
        raise BootstrapValidationError("change_request is required when user_action is 'revise'.")

    output_format = _stringify_hint(
        _pick_first(raw, "output_format", "content_format", "format", "post_format")
    )
    if not output_format and selected_item:
        output_format = _stringify_hint(
            _pick_first(selected_item, "output_format", "content_format", "format", "post_format")
        )
    output_format = normalize_content_format(output_format) if output_format else None

    source_value = _stringify_hint(_pick_first(raw, "source", "source_name")) or source
    trace_id = _stringify_hint(_pick_first(raw, "trace_id", "selection_id", "idea_id"))
    if not trace_id:
        trace_id = _trace_id("|".join([source_value, project_id, theme, str(spec_path), str(template_path), action, change_request or ""]))

    recognized = {
        "project_id", "project", "brand", "page", "theme", "selected_theme", "idea_text", "idea", "topic",
        "user_action", "action", "change_request", "revision", "alteration", "feedback",
        "source", "source_name", "trace_id", "selection_id", "idea_id", "project_spec_path", "project_spec",
        "visual_template_path", "visual_template", "output_format", "content_format", "format", "post_format",
    }
    structured = {key: value for key, value in raw.items() if key not in recognized}
    return ContentRunInput(
        project_id=project_id,
        project_spec_path=str(spec_path.resolve()),
        visual_template_path=str(template_path.resolve()),
        theme=theme,
        source=source_value,
        trace_id=trace_id,
        user_action=action,
        output_format=output_format,
        change_request=change_request,
        structured_fields=structured,
        raw_input=raw,
    )


def content_run_input_to_prompt(run_input: ContentRunInput) -> str:
    """Build a self-contained prompt for calling the Insta Creator orchestrator after selection."""

    lines = [
        "Execute o insta-creator usando o input normalizado abaixo.",
        "Use o project_spec_path e o visual_template_path informados; não use a spec genérica como marca.",
        "Respeite output_format quando informado: carousel deve seguir docs/carousel-workflow-contract.md e virar um ativo de valor com hook específico, motivo de save/share, CTA único e arco de slides justificado.",
        "Respeite output_format quando informado: story deve seguir docs/story-workflow-contract.md e virar um único Story 9:16 interativo, não uma sequência/carrossel.",
        "Se user_action for revise, aplique o change_request antes de produzir o pacote final.",
        "",
        "```json",
        json_like(run_input),
        "```",
    ]
    return "\n".join(lines)


def json_like(run_input: ContentRunInput) -> str:
    import json

    return json.dumps(
        {
            "project_id": run_input.project_id,
            "project_spec_path": run_input.project_spec_path,
            "visual_template_path": run_input.visual_template_path,
            "theme": run_input.theme,
            "source": run_input.source,
            "trace_id": run_input.trace_id,
            "user_action": run_input.user_action,
            "output_format": run_input.output_format,
            "change_request": run_input.change_request,
            "structured_fields": run_input.structured_fields,
        },
        indent=2,
        ensure_ascii=False,
    )


def classify_growth_action(action_type: str, *, requires_approval: bool | None = None) -> bool:
    """Return whether a growth action must go through approval."""

    if requires_approval is not None:
        return requires_approval
    normalized = action_type.strip().lower()
    if normalized in AUTO_GROWTH_ACTIONS:
        return False
    if normalized in APPROVAL_GROWTH_ACTIONS:
        return True
    return True


def _normalize_action_payload(action: str | Mapping[str, Any]) -> tuple[str, dict[str, Any], bool | None]:
    if isinstance(action, str):
        return action, {}, None
    data = dict(action)
    action_type = _stringify_hint(_pick_first(data, "action_type", "type", "name"))
    if not action_type:
        raise BootstrapValidationError("Growth actions must define an action type.")
    payload = dict(data.get("payload", {})) if isinstance(data.get("payload", {}), Mapping) else {}
    for key, value in data.items():
        if key not in {"action_type", "type", "name", "payload", "requires_approval"}:
            payload.setdefault(key, value)
    requires_approval = data.get("requires_approval")
    if requires_approval is not None:
        requires_approval = bool(requires_approval)
    return action_type, payload, requires_approval


def normalize_growth_action(
    action: str | Mapping[str, Any],
    *,
    trace: Mapping[str, Any],
) -> GrowthAction:
    action_type, payload, explicit_requires_approval = _normalize_action_payload(action)
    requires_approval = classify_growth_action(action_type, requires_approval=explicit_requires_approval)
    normalized_trace = dict(trace)
    normalized_trace["action_type"] = action_type
    return GrowthAction(
        action_type=action_type,
        payload=payload,
        requires_approval=requires_approval,
        trace=normalized_trace,
    )


def build_reply_batches(
    approval_required: Sequence[GrowthAction],
    *,
    trace: Mapping[str, Any],
) -> tuple[GrowthAction, ...]:
    reply_groups: dict[str, list[GrowthAction]] = {}
    for action in approval_required:
        if action.action_type.strip().lower() not in REPLY_DRAFT_ACTIONS:
            continue
        batch_id = _stringify_hint(action.payload.get("batch_id")) or "default"
        reply_groups.setdefault(batch_id, []).append(action)

    batches: list[GrowthAction] = []
    for batch_id, actions in sorted(reply_groups.items()):
        batches.append(
            GrowthAction(
                action_type="reply_batch",
                payload={
                    "batch_id": batch_id,
                    "drafts": [action.payload for action in actions],
                },
                requires_approval=True,
                trace={**dict(trace), "action_type": "reply_batch", "batch_id": batch_id},
            )
        )
    return tuple(batches)


def queue_growth_actions(
    actions: Iterable[str | Mapping[str, Any]],
    *,
    trace: Mapping[str, Any],
) -> GrowthActionQueue:
    normalized = tuple(normalize_growth_action(action, trace=trace) for action in actions)
    automatic = tuple(action for action in normalized if not action.requires_approval)
    approval_required = tuple(action for action in normalized if action.requires_approval)
    reply_batches = build_reply_batches(approval_required, trace=trace)
    return GrowthActionQueue(
        automatic=automatic,
        approval_required=approval_required,
        reply_batches=reply_batches,
        trace=dict(trace),
    )
