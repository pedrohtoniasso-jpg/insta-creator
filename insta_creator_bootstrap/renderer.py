from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Any, Mapping, Sequence

from .core import BootstrapValidationError
from .integration import ProjectSpec, load_project_spec

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_HEX_RE = re.compile(r"`?(#[0-9a-fA-F]{6})`?")
_INT_RE = re.compile(r"(\d+)")


@dataclass(frozen=True)
class VisualTemplate:
    path: Path
    raw_text: str
    sections: dict[str, str]
    template_id: str | None
    canvas: tuple[int, int]
    background_primary: str
    background_secondary: str | None
    accent_primary: str
    accent_secondary: str | None
    text_primary: str
    text_muted: str
    headline_min: int
    headline_preferred: int
    headline_max_lines: int
    body_min: int
    body_preferred: int
    body_max_lines: int
    logo_text: str
    logo_position: str
    logo_size: int
    margin_left: int
    margin_right: int
    margin_top: int
    margin_bottom: int
    allow_slide_counter: bool
    allow_main_text_box: bool
    allow_random_metadata: bool


@dataclass(frozen=True)
class RenderedAsset:
    slide: int
    path: Path
    width: int
    height: int


@dataclass(frozen=True)
class RenderResult:
    project_spec: Path
    visual_template: Path
    cards_json: Path
    output_dir: Path
    assets: tuple[RenderedAsset, ...]


def _parse_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    lines: list[str] = []

    def flush() -> None:
        nonlocal current, lines
        if current is not None:
            sections[current] = "\n".join(lines).strip()
        current = None
        lines = []

    for line in markdown.splitlines():
        match = _HEADING_RE.match(line.strip())
        if match and len(match.group(1)) >= 2:
            flush()
            current = match.group(2).strip().lower()
            continue
        if current is not None:
            lines.append(line)
    flush()
    return {key: value for key, value in sections.items()}


def _section(sections: Mapping[str, str], name: str) -> str:
    return sections.get(name.lower(), "")


def _first_hex(text: str, default: str) -> str:
    match = _HEX_RE.search(text)
    return match.group(1).lower() if match else default


def _all_ints(text: str) -> list[int]:
    return [int(m.group(1)) for m in _INT_RE.finditer(text)]


def _accent_primary(raw: str, *, is_mary_kay: bool) -> str:
    default = "#c73b7a" if is_mary_kay else "#0066ff"
    explicit = re.search(r"(?:accent primary|primary accent|accent):\s*`?(#[0-9a-fA-F]{6})`?", raw, re.IGNORECASE)
    if explicit:
        return explicit.group(1).lower()
    if is_mary_kay:
        for candidate in ("#c73b7a", "#e88ab2"):
            if candidate in raw.lower():
                return candidate
    else:
        for candidate in ("#0066ff", "#38bdf8", "#2563eb"):
            if candidate in raw.lower():
                return candidate
    return default


def _contains_enabled(text: str, phrase: str) -> bool:
    lowered = text.lower()
    if phrase not in lowered:
        return False
    window_start = max(0, lowered.index(phrase) - 80)
    window_end = min(len(lowered), lowered.index(phrase) + len(phrase) + 80)
    window = lowered[window_start:window_end]
    return any(token in window for token in ["enable", "enabled", "allow", "allowed", "sim", "permit"])


def _parse_canvas(text: str) -> tuple[int, int]:
    match = re.search(r"(\d{3,5})\s*[×x]\s*(\d{3,5})", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 1080, 1350


def _parse_first_range_or_min(text: str, default: int) -> int:
    min_match = re.search(r"minimum:\s*(\d+)", text, re.IGNORECASE)
    if min_match:
        return int(min_match.group(1))
    px_values = [int(value) for value in re.findall(r"(\d+)\s*px", text, re.IGNORECASE)]
    if px_values:
        return min(px_values)
    ints = [value for value in _all_ints(text) if value >= 12]
    if not ints:
        return default
    return min(ints)


def _parse_preferred(text: str, default: int) -> int:
    preferred_match = re.search(r"preferred:\s*(\d+)(?:\s*[–-]\s*(\d+))?", text, re.IGNORECASE)
    if preferred_match:
        nums = [int(n) for n in preferred_match.groups() if n]
        return max(nums)
    px_values = [int(value) for value in re.findall(r"(\d+)\s*px", text, re.IGNORECASE)]
    if px_values:
        return max(px_values)
    ints = [value for value in _all_ints(text) if value >= 12]
    return max(ints) if ints else default


def load_visual_template(path: str | Path) -> VisualTemplate:
    template_path = Path(path).expanduser().resolve()
    raw = template_path.read_text(encoding="utf-8")
    sections = _parse_sections(raw)
    required = [
        "canvas",
        "background",
        "typography",
        "logo / mark",
        "layout pattern",
        "decorative elements prohibited",
        "renderer fit rules",
        "visual audit checklist",
    ]
    missing = [name for name in required if name not in sections]
    if missing:
        raise BootstrapValidationError(
            "Visual template is missing required sections: " + ", ".join(missing)
        )

    raw_lower = raw.lower()
    is_mary_kay = "mary kay" in raw_lower
    typography = _section(sections, "typography")
    logo = _section(sections, "logo / mark")
    margins = _section(sections, "canvas") + "\n" + _section(sections, "layout pattern")
    background = _section(sections, "background")

    template_id_match = re.search(r"Template ID:\s*`?([^`\n]+)`?", raw, re.IGNORECASE)
    canvas = _parse_canvas(_section(sections, "canvas"))
    margin_ints = _all_ints(margins)
    # Use explicit template margin order when available; otherwise safe defaults.
    margin_left = 88 if "left" not in margins.lower() else int(re.search(r"left:\s*(\d+)", margins, re.IGNORECASE).group(1))
    margin_right = 88 if "right" not in margins.lower() else int(re.search(r"right:\s*(\d+)", margins, re.IGNORECASE).group(1))
    margin_top = 76 if "top" not in margins.lower() else int(re.search(r"top:\s*(\d+)", margins, re.IGNORECASE).group(1))
    margin_bottom = 86 if "bottom" not in margins.lower() else int(re.search(r"bottom:\s*(\d+)", margins, re.IGNORECASE).group(1))
    logo_size_match = re.search(r"Size:\s*(\d+)(?:\s*[–-]\s*(\d+))?", logo, re.IGNORECASE)
    logo_size = 58
    if logo_size_match:
        logo_size = max(int(n) for n in logo_size_match.groups() if n)

    return VisualTemplate(
        path=template_path,
        raw_text=raw,
        sections=sections,
        template_id=template_id_match.group(1).strip() if template_id_match else None,
        canvas=canvas,
        background_primary=_first_hex(background, "#fff7fb" if is_mary_kay else "#020817"),
        background_secondary=_first_hex(background.split("Secondary", 1)[-1], "#fde7f1" if is_mary_kay else "#0f172a") if "secondary" in background.lower() else ("#fde7f1" if is_mary_kay else "#0f172a"),
        accent_primary=_accent_primary(raw, is_mary_kay=is_mary_kay),
        accent_secondary="#e88ab2" if is_mary_kay else ("#38bdf8" if "#38bdf8" in raw_lower else None),
        text_primary="#2b1f29" if is_mary_kay else "#f8fafc",
        text_muted="#5b4a55" if is_mary_kay else "#cbd5e1",
        headline_min=_parse_first_range_or_min(re.search(r"Headline:(.*?)(?:\n- Body:|$)", typography, re.S | re.I).group(1) if re.search(r"Headline:", typography, re.I) else typography, 104),
        headline_preferred=_parse_preferred(re.search(r"Headline:(.*?)(?:\n- Body:|$)", typography, re.S | re.I).group(1) if re.search(r"Headline:", typography, re.I) else typography, 124),
        headline_max_lines=4 if "max lines" not in typography.lower() else int(re.search(r"max lines:\s*(\d+)", typography, re.IGNORECASE).group(1)),
        body_min=_parse_first_range_or_min(re.search(r"Body:(.*?)(?:\n- Micro text:|$)", typography, re.S | re.I).group(1) if re.search(r"Body:", typography, re.I) else typography, 44),
        body_preferred=_parse_preferred(re.search(r"Body:(.*?)(?:\n- Micro text:|$)", typography, re.S | re.I).group(1) if re.search(r"Body:", typography, re.I) else typography, 52),
        body_max_lines=3 if "body" not in typography.lower() or not re.search(r"Body:.*?max lines:\s*(\d+)", typography, re.S | re.I) else int(re.search(r"Body:.*?max lines:\s*(\d+)", typography, re.S | re.I).group(1)),
        logo_text="GF" if "gf" in logo.lower() else "",
        logo_position="top-left" if "top-left" in logo.lower() else "top-left",
        logo_size=logo_size,
        margin_left=margin_left,
        margin_right=margin_right,
        margin_top=margin_top,
        margin_bottom=margin_bottom,
        allow_slide_counter=_contains_enabled(raw_lower, "slide counter"),
        allow_main_text_box=_contains_enabled(raw_lower, "main text box") or _contains_enabled(raw_lower, "large box"),
        allow_random_metadata=_contains_enabled(raw_lower, "random metadata") or _contains_enabled(raw_lower, "footer metadata"),
    )


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _font_path(prefer_bold: bool) -> str:
    candidates = [
        "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf" if prefer_bold else "/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if prefer_bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise BootstrapValidationError("No supported TrueType/OpenType font found for rendering.")


def _load_font(size: int, *, bold: bool):
    from PIL import ImageFont

    return ImageFont.truetype(_font_path(bold), size=size)


def _wrap(draw: Any, text: str, font: Any, max_width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def _has_orphan_line(lines: list[str]) -> bool:
    """Return True when wrapped text leaves a non-final line with a lonely word."""
    if len(lines) <= 1:
        return False
    for line in lines[:-1]:
        words = line.split()
        if len(words) == 1 and len(words[0]) <= 10:
            return True
    return False


def _fit_font(draw: Any, text: str, *, bold: bool, preferred: int, minimum: int, max_width: int, max_lines: int) -> tuple[Any, list[str]]:
    size = preferred
    while size >= minimum:
        font = _load_font(size, bold=bold)
        lines = _wrap(draw, text, font, max_width)
        if len(lines) <= max_lines and not _has_orphan_line(lines):
            return font, lines
        size -= 4
    font = _load_font(minimum, bold=bold)
    lines = _wrap(draw, text, font, max_width)
    if len(lines) > max_lines or _has_orphan_line(lines):
        raise BootstrapValidationError(
            f"Text does not fit visual template limits ({max_lines} lines at {minimum}px): {text}"
        )
    return font, lines


def _gradient_background(template: VisualTemplate):
    from PIL import Image, ImageDraw, ImageFilter

    width, height = template.canvas
    primary = _hex_to_rgb(template.background_primary)
    secondary = _hex_to_rgb(template.background_secondary or template.background_primary)
    img = Image.new("RGBA", (width, height), primary)
    px = img.load()
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(primary[i] + (secondary[i] - primary[i]) * t) for i in range(3))
        for x in range(width):
            px[x, y] = (*color, 255)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    accent = _hex_to_rgb(template.accent_primary)
    d.ellipse((width - 560, -260, width + 320, 620), fill=(*accent, 34))
    if template.accent_secondary:
        d.ellipse((-420, int(height * 0.56), 380, height + 190), fill=(*_hex_to_rgb(template.accent_secondary), 15))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    return Image.alpha_composite(img, glow)


def _draw_logo(draw: Any, template: VisualTemplate) -> None:
    if not template.logo_text:
        return
    x = template.margin_left
    y = template.margin_top
    size = template.logo_size
    accent = _hex_to_rgb(template.accent_primary)
    text = _hex_to_rgb(template.text_primary)
    draw.rounded_rectangle((x, y, x + size, y + size), radius=max(8, size // 4), fill=accent)
    font = _load_font(max(18, int(size * 0.46)), bold=True)
    bbox = draw.textbbox((0, 0), template.logo_text, font=font)
    draw.text(
        (x + (size - (bbox[2] - bbox[0])) / 2, y + (size - (bbox[3] - bbox[1])) / 2 - 3),
        template.logo_text,
        font=font,
        fill=text,
    )


def _render_card(card: Mapping[str, Any], *, template: VisualTemplate):
    from PIL import ImageDraw

    img = _gradient_background(template)
    draw = ImageDraw.Draw(img)
    _draw_logo(draw, template)
    width, height = template.canvas
    x = template.margin_left
    max_width = width - template.margin_left - template.margin_right
    role = str(card.get("role", "")).lower()
    y = int(height * (0.255 if role in {"cover", "cta"} else 0.235))
    accent = _hex_to_rgb(template.accent_primary)
    text_primary = _hex_to_rgb(template.text_primary)
    text_muted = _hex_to_rgb(template.text_muted)
    draw.rounded_rectangle((x, y - 48, x + 118, y - 38), radius=5, fill=accent)

    headline = str(card.get("headline", "")).strip()
    body = str(card.get("body", "")).strip()
    if not headline:
        raise BootstrapValidationError(f"Card {card.get('slide')} missing headline.")
    if not body and role != "cover":
        raise BootstrapValidationError(f"Card {card.get('slide')} missing body.")

    title_font, title_lines = _fit_font(
        draw,
        headline,
        bold=True,
        preferred=template.headline_preferred,
        minimum=template.headline_min,
        max_width=max_width,
        max_lines=template.headline_max_lines,
    )
    for line in title_lines:
        draw.text((x, y), line, font=title_font, fill=text_primary)
        y += int(title_font.size * 0.98)
    y += 44

    body_font, body_lines = _fit_font(
        draw,
        body,
        bold=False,
        preferred=template.body_preferred,
        minimum=template.body_min,
        max_width=max_width,
        max_lines=template.body_max_lines,
    )
    if body:
        for line in body_lines:
            draw.text((x, y), line, font=body_font, fill=text_muted)
            y += int(body_font.size * 1.18)

    cta = str(card.get("cta_note", "")).strip()
    if cta:
        cta_font = _load_font(max(template.body_min, 42 if role == "cta" else 38), bold=True)
        cta_y = height - template.margin_bottom - 150
        draw.rounded_rectangle((x, cta_y - 4, x + 126, cta_y + 6), radius=5, fill=accent)
        for line in _wrap(draw, cta, cta_font, max_width):
            draw.text((x, cta_y + 26), line, font=cta_font, fill=accent)
            cta_y += int(cta_font.size * 1.18)

    if template.allow_slide_counter:
        slide_label = str(card.get("slide", ""))
        counter_font = _load_font(28, bold=True)
        draw.text((width - template.margin_right - 50, template.margin_top), slide_label, font=counter_font, fill=text_muted)

    return img.convert("RGB")


def render_cards(
    *,
    project_spec_path: str | Path,
    visual_template_path: str | Path,
    cards_json_path: str | Path,
    output_dir: str | Path,
) -> RenderResult:
    # Import here so non-render commands do not require Pillow until rendering.
    try:
        from PIL import Image  # noqa: F401
    except ImportError as exc:
        raise BootstrapValidationError("Rendering requires Pillow (PIL). Install pillow first.") from exc

    project_spec = load_project_spec(project_spec_path)
    template = load_visual_template(visual_template_path)
    cards_path = Path(cards_json_path).expanduser().resolve()
    cards_data = json.loads(cards_path.read_text(encoding="utf-8"))
    cards = cards_data.get("cards")
    if not isinstance(cards, Sequence) or isinstance(cards, (str, bytes)):
        raise BootstrapValidationError("cards.json must contain a cards array.")
    slide_count = cards_data.get("slide_count")
    if slide_count != len(cards):
        raise BootstrapValidationError("cards.json slide_count does not match cards length.")

    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.glob("0*.png"):
        stale.unlink()

    assets: list[RenderedAsset] = []
    for expected, card in enumerate(cards, start=1):
        if not isinstance(card, Mapping):
            raise BootstrapValidationError(f"Card {expected} must be an object.")
        if card.get("slide") != expected:
            raise BootstrapValidationError(f"Card slide order mismatch at {expected}.")
        image = _render_card(card, template=template)
        out_path = out_dir / f"{expected:02d}.png"
        image.save(out_path, quality=96)
        assets.append(RenderedAsset(slide=expected, path=out_path, width=image.width, height=image.height))

    return RenderResult(
        project_spec=project_spec.path,
        visual_template=template.path,
        cards_json=cards_path,
        output_dir=out_dir,
        assets=tuple(assets),
    )


def render_result_to_dict(result: RenderResult) -> dict[str, Any]:
    return {
        "project_spec": str(result.project_spec),
        "visual_template": str(result.visual_template),
        "cards_json": str(result.cards_json),
        "output_dir": str(result.output_dir),
        "assets": [
            {"slide": asset.slide, "path": str(asset.path), "width": asset.width, "height": asset.height}
            for asset in result.assets
        ],
        "status": "rendered",
    }
