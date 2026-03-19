# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create(client, title: str, content: str) -> dict:
    r = client.post("/notes/", json={"title": title, "content": content})
    assert r.status_code == 201, r.text
    return r.json()


def _search(client, **params) -> dict:
    r = client.get("/notes/search/", params=params)
    assert r.status_code == 200, r.text
    return r.json()


# ---------------------------------------------------------------------------
# Basic CRUD + list
# ---------------------------------------------------------------------------


def test_create_and_list_notes(client):
    _create(client, "Test", "Hello world")

    r = client.get("/notes/")
    assert r.status_code == 200
    assert len(r.json()) >= 1


# ---------------------------------------------------------------------------
# Search: response shape
# ---------------------------------------------------------------------------


def test_search_response_shape(client):
    _create(client, "Alpha", "some content")
    result = _search(client)
    assert "items" in result
    assert "total" in result
    assert "page" in result
    assert "page_size" in result


# ---------------------------------------------------------------------------
# Search: empty query returns all notes
# ---------------------------------------------------------------------------


def test_search_no_query_returns_all(client):
    _create(client, "Note One", "foo")
    _create(client, "Note Two", "bar")
    result = _search(client)
    assert result["total"] == 2
    assert len(result["items"]) == 2


# ---------------------------------------------------------------------------
# Search: whitespace-only query treated as empty
# ---------------------------------------------------------------------------


def test_search_whitespace_query_returns_all(client):
    _create(client, "A", "alpha")
    _create(client, "B", "beta")
    result = _search(client, q="   ")
    assert result["total"] == 2


# ---------------------------------------------------------------------------
# Search: match on title
# ---------------------------------------------------------------------------


def test_search_matches_title(client):
    _create(client, "Hello World", "irrelevant content")
    _create(client, "Goodbye", "other content")
    result = _search(client, q="Hello")
    assert result["total"] == 1
    assert result["items"][0]["title"] == "Hello World"


# ---------------------------------------------------------------------------
# Search: match on content
# ---------------------------------------------------------------------------


def test_search_matches_content(client):
    _create(client, "Unrelated", "Python is great")
    _create(client, "Unrelated2", "Nothing special")
    result = _search(client, q="Python")
    assert result["total"] == 1
    assert result["items"][0]["content"] == "Python is great"


# ---------------------------------------------------------------------------
# Search: case-insensitive
# ---------------------------------------------------------------------------


def test_search_case_insensitive(client):
    _create(client, "FastAPI Tutorial", "learn fastapi today")
    # Uppercase query against mixed-case title
    result = _search(client, q="FASTAPI")
    assert result["total"] == 1
    # Lowercase query against uppercase title
    result2 = _search(client, q="tutorial")
    assert result2["total"] == 1


# ---------------------------------------------------------------------------
# Search: no results
# ---------------------------------------------------------------------------


def test_search_no_results(client):
    _create(client, "Alpha", "alpha content")
    result = _search(client, q="zzz_nonexistent_zzz")
    assert result["total"] == 0
    assert result["items"] == []


# ---------------------------------------------------------------------------
# Pagination: page and page_size
# ---------------------------------------------------------------------------


def test_pagination_basic(client):
    for i in range(5):
        _create(client, f"Note {i}", f"content {i}")

    result = _search(client, page=1, page_size=3)
    assert result["total"] == 5
    assert result["page"] == 1
    assert result["page_size"] == 3
    assert len(result["items"]) == 3

    result2 = _search(client, page=2, page_size=3)
    assert result2["total"] == 5
    assert len(result2["items"]) == 2  # last page has 2 remaining


def test_pagination_page_size_one(client):
    _create(client, "A", "a")
    _create(client, "B", "b")
    result = _search(client, page=1, page_size=1)
    assert result["total"] == 2
    assert len(result["items"]) == 1


def test_pagination_beyond_last_page(client):
    _create(client, "Only Note", "lonely")
    result = _search(client, page=999, page_size=10)
    assert result["total"] == 1
    assert result["items"] == []


def test_pagination_with_query(client):
    for i in range(4):
        _create(client, f"Needle {i}", "haystack")
    _create(client, "Haystack", "no match here")

    result = _search(client, q="Needle", page=1, page_size=2)
    assert result["total"] == 4
    assert len(result["items"]) == 2

    result2 = _search(client, q="Needle", page=2, page_size=2)
    assert len(result2["items"]) == 2


# ---------------------------------------------------------------------------
# Sorting: created_desc (default) and title_asc
# ---------------------------------------------------------------------------


def test_sort_title_asc(client):
    _create(client, "Zebra", "z")
    _create(client, "Apple", "a")
    _create(client, "Mango", "m")
    result = _search(client, sort="title_asc")
    titles = [item["title"] for item in result["items"]]
    assert titles == sorted(titles)


def test_sort_created_desc(client):
    first = _create(client, "First Note", "1")
    second = _create(client, "Second Note", "2")
    result = _search(client, sort="created_desc")
    ids = [item["id"] for item in result["items"]]
    # Most recently created (highest id) should come first
    assert ids[0] == second["id"]
    assert ids[-1] == first["id"]


# ---------------------------------------------------------------------------
# Invalid sort value returns 422
# ---------------------------------------------------------------------------


def test_invalid_sort_value(client):
    r = client.get("/notes/search/", params={"sort": "invalid_sort"})
    assert r.status_code == 422
