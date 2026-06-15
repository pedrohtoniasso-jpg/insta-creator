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


@dataclass(frozen=True)
class CronIdeaIntake:
    """Normalized cron-fed idea input."""

    source: str
    idea_text: str
    trace_id: str
    priority_hint: str | None
    format_hint: str | None
    project_name: str | None
    project_spec_path: str | None
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
    return ProjectSpec(
        path=spec_path,
        title=title,
        raw_text=raw_text,
        sections=sections,
        section_order=section_order,
        project_name=_first_line(sections.get("project name")),
        target_platform=_first_line(sections.get("target platform")),
    )


def _first_line(text: str | None) -> str | None:
    if text is None:
        return None
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned.lstrip("-•*").strip()
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
    source_value = _stringify_hint(_pick_first(raw, "source", "source_name")) or source
    project_name_value = _stringify_hint(_pick_first(raw, "project_name")) or project_name
    project_spec_path_value = (
        str(Path(project_spec_path).expanduser().resolve()) if project_spec_path else None
    )
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
        idea_text=idea_text,
        trace_id=trace_id,
        priority_hint=priority_hint,
        format_hint=format_hint,
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
        "idea_text": intake.idea_text,
        "project_name": project_spec.project_name or intake.project_name,
        "project_spec_path": str(project_spec.path),
        "lineage": ["cron-intake", "project-spec", "growth-queue"],
        "priority_hint": intake.priority_hint,
        "format_hint": intake.format_hint,
    }


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
