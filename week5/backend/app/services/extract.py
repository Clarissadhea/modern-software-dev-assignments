import re


def extract_action_items(text: str) -> list[str]:
    """Legacy extractor: lines ending in '!' or starting with 'todo:'."""
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    return [line for line in lines if line.endswith("!") or line.lower().startswith("todo:")]


def extract_tags(text: str) -> list[str]:
    """Extract unique #hashtags from text, returning the tag name without '#'."""
    return list(dict.fromkeys(re.findall(r"(?<!\w)#(\w+)", text)))


def extract_tasks(text: str) -> list[str]:
    """Extract unchecked task items matching '- [ ] task text' (GitHub checkbox style)."""
    return re.findall(r"^\s*-\s*\[\s*\]\s*(.+)$", text, re.MULTILINE)


def extract_all(text: str) -> dict[str, list[str]]:
    """Return a structured dict with both tags and action_items extracted from text."""
    return {
        "tags": extract_tags(text),
        "action_items": extract_tasks(text),
    }
