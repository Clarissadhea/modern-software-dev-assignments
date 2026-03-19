def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert "total" in body
    assert body["total"] >= 1
    assert len(body["items"]) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_notes_pagination_defaults(client):
    """Default page=1, page_size=10 returns items and total."""
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": "body"})

    r = client.get("/notes/")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 3


def test_notes_pagination_page_size(client):
    """page_size limits results; total reflects full count."""
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": "body"})

    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2

    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    body = r.json()
    assert len(body["items"]) == 2

    r = client.get("/notes/", params={"page": 3, "page_size": 2})
    body = r.json()
    assert len(body["items"]) == 1


def test_notes_empty_last_page(client):
    """A page beyond available data returns empty items but correct total."""
    client.post("/notes/", json={"title": "Only", "content": "one"})

    r = client.get("/notes/", params={"page": 99, "page_size": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"] == []


def test_notes_too_large_page_size(client):
    """page_size capped at 100; exceeding it returns 422."""
    r = client.get("/notes/", params={"page_size": 101})
    assert r.status_code == 422


def test_notes_invalid_page(client):
    """page < 1 returns 422."""
    r = client.get("/notes/", params={"page": 0})
    assert r.status_code == 422
