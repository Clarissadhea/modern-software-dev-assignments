def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert "total" in body
    assert body["total"] == 1
    assert len(body["items"]) == 1


def test_action_items_pagination_page_size(client):
    """page_size limits results; total reflects full count."""
    for i in range(5):
        client.post("/action-items/", json={"description": f"Task {i}"})

    r = client.get("/action-items/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2

    r = client.get("/action-items/", params={"page": 3, "page_size": 2})
    body = r.json()
    assert len(body["items"]) == 1


def test_action_items_empty_last_page(client):
    """A page beyond available data returns empty items but correct total."""
    client.post("/action-items/", json={"description": "Only one"})

    r = client.get("/action-items/", params={"page": 99, "page_size": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"] == []


def test_action_items_too_large_page_size(client):
    """page_size > 100 returns 422."""
    r = client.get("/action-items/", params={"page_size": 101})
    assert r.status_code == 422


def test_action_items_invalid_page(client):
    """page < 1 returns 422."""
    r = client.get("/action-items/", params={"page": 0})
    assert r.status_code == 422
