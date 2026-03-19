"""Integration tests for POST /notes/{id}/extract."""

NOTE_CONTENT = (
    "Planning session #project #backend\n"
    "- [ ] Set up CI pipeline\n"
    "- [ ] Write integration tests\n"
    "- [x] Initialise repo\n"
)


def _create_note(client, content=NOTE_CONTENT):
    r = client.post("/notes/", json={"title": "Test Note", "content": content})
    assert r.status_code == 201, r.text
    return r.json()["id"]


# ---------------------------------------------------------------------------
# Dry-run (apply omitted / apply=false)
# ---------------------------------------------------------------------------


def test_extract_returns_structured_result(client):
    note_id = _create_note(client)
    r = client.post(f"/notes/{note_id}/extract")
    assert r.status_code == 200, r.text
    data = r.json()
    assert set(data.keys()) == {"tags", "action_items"}
    assert data["tags"] == ["project", "backend"]
    assert data["action_items"] == ["Set up CI pipeline", "Write integration tests"]


def test_extract_dry_run_does_not_persist(client):
    note_id = _create_note(client)
    client.post(f"/notes/{note_id}/extract")  # no apply param

    r = client.get("/action-items/")
    assert r.status_code == 200
    assert r.json()["items"] == []


def test_extract_apply_false_does_not_persist(client):
    note_id = _create_note(client)
    client.post(f"/notes/{note_id}/extract", params={"apply": "false"})

    r = client.get("/action-items/")
    assert r.status_code == 200
    assert r.json()["items"] == []


# ---------------------------------------------------------------------------
# apply=true — persistence path
# ---------------------------------------------------------------------------


def test_extract_apply_true_persists_action_items(client):
    note_id = _create_note(client)
    r = client.post(f"/notes/{note_id}/extract", params={"apply": "true"})
    assert r.status_code == 200, r.text

    data = r.json()
    assert data["action_items"] == ["Set up CI pipeline", "Write integration tests"]

    items_r = client.get("/action-items/")
    assert items_r.status_code == 200
    descriptions = [i["description"] for i in items_r.json()["items"]]
    assert "Set up CI pipeline" in descriptions
    assert "Write integration tests" in descriptions
    # Completed checkbox should NOT be persisted
    assert "Initialise repo" not in descriptions


def test_extract_apply_true_new_items_are_not_completed(client):
    note_id = _create_note(client)
    client.post(f"/notes/{note_id}/extract", params={"apply": "true"})

    items_r = client.get("/action-items/")
    for item in items_r.json()["items"]:
        assert item["completed"] is False


def test_extract_apply_true_returns_tags(client):
    note_id = _create_note(client)
    r = client.post(f"/notes/{note_id}/extract", params={"apply": "true"})
    assert r.json()["tags"] == ["project", "backend"]


def test_extract_apply_true_no_tasks_in_note(client):
    note_id = _create_note(client, content="Just a plain note #simple")
    r = client.post(f"/notes/{note_id}/extract", params={"apply": "true"})
    assert r.status_code == 200
    assert r.json()["action_items"] == []
    assert r.json()["tags"] == ["simple"]

    items_r = client.get("/action-items/")
    assert items_r.json()["items"] == []


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------


def test_extract_note_not_found(client):
    r = client.post("/notes/9999/extract")
    assert r.status_code == 404
