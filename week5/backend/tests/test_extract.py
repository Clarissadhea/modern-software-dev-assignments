import pytest
from backend.app.services.extract import (
    extract_action_items,
    extract_all,
    extract_tags,
    extract_tasks,
)

# ---------------------------------------------------------------------------
# Legacy extractor (backward-compat)
# ---------------------------------------------------------------------------


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


# ---------------------------------------------------------------------------
# extract_tags
# ---------------------------------------------------------------------------


def test_extract_tags_basic():
    text = "Check out #python and #fastapi for the backend."
    tags = extract_tags(text)
    assert tags == ["python", "fastapi"]


def test_extract_tags_deduplication():
    text = "#python is great. I love #python."
    tags = extract_tags(text)
    assert tags == ["python"]


def test_extract_tags_no_tags():
    assert extract_tags("No hashtags here.") == []


def test_extract_tags_ignores_mid_word():
    """A '#' embedded inside a word (e.g. a URL fragment) should NOT be extracted."""
    text = "Visit example.com/page#anchor but use #realtag"
    tags = extract_tags(text)
    assert "anchor" not in tags
    assert "realtag" in tags


# ---------------------------------------------------------------------------
# extract_tasks
# ---------------------------------------------------------------------------


def test_extract_tasks_basic():
    text = "- [ ] Write unit tests\n- [ ] Deploy to staging\n- [x] Already done"
    tasks = extract_tasks(text)
    assert tasks == ["Write unit tests", "Deploy to staging"]
    assert "Already done" not in tasks


def test_extract_tasks_with_leading_spaces():
    text = "  - [ ] Indented task"
    tasks = extract_tasks(text)
    assert tasks == ["Indented task"]


def test_extract_tasks_empty_text():
    assert extract_tasks("") == []


def test_extract_tasks_no_tasks():
    text = "Just a regular note without checkboxes."
    assert extract_tasks(text) == []


# ---------------------------------------------------------------------------
# extract_all
# ---------------------------------------------------------------------------


def test_extract_all_combined():
    text = (
        "Meeting notes #project #backend\n"
        "- [ ] Finish the API\n"
        "- [ ] Write docs\n"
        "- [x] Setup DB\n"
    )
    result = extract_all(text)
    assert result["tags"] == ["project", "backend"]
    assert result["action_items"] == ["Finish the API", "Write docs"]


@pytest.mark.parametrize(
    "text,expected_tags,expected_tasks",
    [
        ("No special content", [], []),
        ("#only tags #here", ["only", "here"], []),
        ("- [ ] only tasks", [], ["only tasks"]),
    ],
)
def test_extract_all_parametrized(text, expected_tags, expected_tasks):
    result = extract_all(text)
    assert result["tags"] == expected_tags
    assert result["action_items"] == expected_tasks
