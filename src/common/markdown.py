from __future__ import annotations

from typing import Iterable


# YAML / markdown formatting constants
FRONTMATTER_DELIMITER = "---"
YAML_LIST_PREFIX = "  - "
BULLET_PREFIX = "- "


def yaml_quote(value: str) -> str:
    """Quote a string for safe inclusion in a YAML double-quoted scalar."""
    escaped = (
        value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    )
    return f'"{escaped}"'


def format_field(name: str, value) -> str:
    """Render a single YAML scalar field, coercing by Python type."""
    if value is None:
        return f"{name}:"
    if isinstance(value, bool):
        return f"{name}: {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{name}: {value}"
    return f"{name}: {yaml_quote(str(value))}"


def wikilink(target: str) -> str:
    """Return an Obsidian wikilink: ``[[target]]``."""
    return f"[[{target}]]"


def quoted_wikilink(target: str) -> str:
    """Return a YAML-safe wikilink scalar: ``"[[target]]"``."""
    return f'"{wikilink(target)}"'


def heading(level: int, text: str) -> str:
    """Render a markdown heading at ``level`` (1-based)."""
    return f"{'#' * level} {text}"


def bullet_link(target: str) -> str:
    """Render a single markdown bullet that wraps a wikilink."""
    return f"{BULLET_PREFIX}{wikilink(target)}"


def bullet_links(targets: Iterable[str]) -> list[str]:
    """Render a list of markdown bullets, each wrapping a wikilink."""
    return [bullet_link(t) for t in targets]


def section(title: str, body_lines: Iterable[str]) -> list[str]:
    """Render a body section: blank, ``## title``, blank, then ``body_lines``.

    The heading is always emitted, even when ``body_lines`` is empty.
    """
    return ["", heading(2, title), "", *body_lines]


def yaml_link_field(name: str, target: str) -> str:
    """Render a single YAML field whose value is a wikilink scalar."""
    return f"{name}: {quoted_wikilink(target)}"


def yaml_list(name: str, values: Iterable[str]) -> list[str]:
    """Render a YAML list field of quoted string scalars."""
    lines = [f"{name}:"]
    for value in values:
        lines.append(f"{YAML_LIST_PREFIX}{yaml_quote(value)}")
    return lines


def yaml_link_list(name: str, targets: Iterable[str]) -> list[str]:
    """Render a YAML list field of quoted wikilink scalars."""
    lines = [f"{name}:"]
    for target in targets:
        lines.append(f"{YAML_LIST_PREFIX}{quoted_wikilink(target)}")
    return lines


def frontmatter(blocks: Iterable[str]) -> list[str]:
    """Wrap pre-rendered YAML lines with ``---`` delimiters."""
    return [FRONTMATTER_DELIMITER, *blocks, FRONTMATTER_DELIMITER]


def render_note(lines: Iterable[str]) -> str:
    """Join markdown ``lines`` into a single string with a trailing newline."""
    return "\n".join(lines).rstrip() + "\n"
