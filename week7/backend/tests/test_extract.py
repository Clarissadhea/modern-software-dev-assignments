from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - TASK: implement feature
    - [ ] empty checkbox
    - [x] completed checkbox
    - Ship it!
    Not actionable
    Some other text
    """.strip()
    items = extract_action_items(text)
    
    # Test keyword patterns
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "TASK: implement feature" in items
    
    # Test Markdown checkboxes
    assert "[ ] empty checkbox" in items
    assert "[x] completed checkbox" in items
    
    # Test exclamation mark pattern
    assert "Ship it!" in items
    
    # Verify non-actionable text is not included
    assert "This is a note" not in items
    assert "Not actionable" not in items
    assert "Some other text" not in items
    
    # Verify correct number of items extracted
    assert len(items) == 6


