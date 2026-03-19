def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_notes_case_insensitive(client):
    payload = {"title": "CaseTest", "content": "MixedCaseContent"}
    client.post("/notes/", json=payload)
    r = client.get("/notes/search/", params={"q": "casetest"})
    assert r.status_code == 200
    items = r.json()
    assert any(item["title"] == "CaseTest" for item in items)
    r = client.get("/notes/search/", params={"q": "mixedcasecontent"})
    assert r.status_code == 200
    items = r.json()
    assert any(item["content"] == "MixedCaseContent" for item in items)


def test_edit_note(client):
    payload = {"title": "EditMe", "content": "EditContent"}
    r = client.post("/notes/", json=payload)
    note = r.json()
    r = client.put(f"/notes/{note['id']}", json={"title": "NewTitle", "content": "NewContent"})
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "NewTitle"
    assert updated["content"] == "NewContent"


def test_delete_note(client):
    payload = {"title": "DeleteMe", "content": "DeleteContent"}
    r = client.post("/notes/", json=payload)
    note = r.json()
    r = client.delete(f"/notes/{note['id']}")
    assert r.status_code == 204
    r = client.get(f"/notes/{note['id']}")
    assert r.status_code == 404


def test_validation_error(client):
    payload = {"title": "A", "content": "B"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    payload = {"title": "Valid", "content": "B"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    payload = {"title": "A", "content": "Valid"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
