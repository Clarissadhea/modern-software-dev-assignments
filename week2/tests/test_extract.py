import os
import pytest

from ..app.services.extract import extract_action_items


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items

import sys
import types

import pytest

from ..app.services.extract import extract_action_items_llm

@pytest.mark.skipif(
    not os.environ.get("RUN_LLM_TESTS"),
    reason="extract_action_items_llm requires Ollama running and can be slow. Set RUN_LLM_TESTS=1 to enable.",
)
def test_extract_action_items_llm_with_bullets_and_checkboxes(monkeypatch):
    # We'll patch ollama.chat to avoid actually calling LLM for test determinism
    mocked_response = {
        "message": {
            "content": '["Set up database", "implement API extract endpoint", "Write tests"]'
        }
    }

    def mock_chat(*args, **kwargs):
        return mocked_response

    # Patch the ollama module imported within the function's scope
    import builtins

    # Patch imports inside function
    saved_import = builtins.__import__

    def mocked_import(name, *args, **kwargs):
        if name == "ollama":
            return types.SimpleNamespace(chat=mock_chat)
        return saved_import(name, *args, **kwargs)

    builtins.__import__ = mocked_import
    try:
        text = """
        Notes from meeting:
        - [ ] Set up database
        * implement API extract endpoint
        1. Write tests
        Some narrative sentence.
        """.strip()
        items = extract_action_items_llm(text)
        assert isinstance(items, list)
        assert set(items) == {
            "Set up database",
            "implement API extract endpoint",
            "Write tests",
        }
    finally:
        builtins.__import__ = saved_import

@pytest.mark.skipif(
    not os.environ.get("RUN_LLM_TESTS"),
    reason="extract_action_items_llm requires Ollama running and can be slow. Set RUN_LLM_TESTS=1 to enable.",
)
def test_extract_action_items_llm_with_paragraph_tasks(monkeypatch):
    mocked_response = {
        "message": {
            "content": '["Update documentation", "Check server logs"]'
        }
    }

    def mock_chat(*args, **kwargs):
        return mocked_response

    import builtins
    saved_import = builtins.__import__

    def mocked_import(name, *args, **kwargs):
        if name == "ollama":
            return types.SimpleNamespace(chat=mock_chat)
        return saved_import(name, *args, **kwargs)

    builtins.__import__ = mocked_import
    try:
        text = (
            "We need to update documentation for the new API release. "
            "Also, someone should check server logs for the last deployment."
        )
        items = extract_action_items_llm(text)
        assert isinstance(items, list)
        assert set(items) == {"Update documentation", "Check server logs"}
    finally:
        builtins.__import__ = saved_import

@pytest.mark.skipif(
    not os.environ.get("RUN_LLM_TESTS"),
    reason="extract_action_items_llm requires Ollama running and can be slow. Set RUN_LLM_TESTS=1 to enable.",
)
def test_extract_action_items_llm_empty_string(monkeypatch):
    mocked_response = {
        "message": {"content": '[]'}
    }

    def mock_chat(*args, **kwargs):
        return mocked_response

    import builtins
    saved_import = builtins.__import__

    def mocked_import(name, *args, **kwargs):
        if name == "ollama":
            return types.SimpleNamespace(chat=mock_chat)
        return saved_import(name, *args, **kwargs)

    builtins.__import__ = mocked_import
    try:
        items = extract_action_items_llm("")
        assert items == []
    finally:
        builtins.__import__ = saved_import