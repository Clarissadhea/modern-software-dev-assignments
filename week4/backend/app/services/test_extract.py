from backend.app.services.extract import extract_action_items

def test_extract_action_items_basic():
    text = """
    - Ship it!
    - TODO: Refactor
    - Not actionable
    """
    assert extract_action_items(text) == ["Ship it!", "TODO: Refactor"]

def test_extract_action_items_tags():
    text = """
    - #urgent Ship it!
    - TODO: Refactor #refactor
    - #ignore Not actionable
    """
    items = extract_action_items(text)
    assert "#urgent Ship it!" in items
    assert "TODO: Refactor #refactor" in items
    assert "#ignore Not actionable" not in items


def test_extract_action_items_tag_parsing():
    text = """
    - #tag1 Do this!
    - #tag2 TODO: Something
    - Just a note
    """
    items = extract_action_items(text)
    assert any("#tag1" in item for item in items)
    assert any("#tag2" in item for item in items)
