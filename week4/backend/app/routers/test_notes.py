from fastapi.testclient import TestClient
from backend.app.routers.notes import router
from backend.app.schemas import NoteCreate

client = TestClient(router)

def test_put_note():
    # Create
    payload = {"title": "A", "content": "B"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note = r.json()
    # Update
    r = client.put(f"/notes/{note['id']}", json={"title": "Updated", "content": "Changed"})
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "Updated"
    assert updated["content"] == "Changed"

def test_delete_note():
    payload = {"title": "DeleteMe", "content": "Bye"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note = r.json()
    r = client.delete(f"/notes/{note['id']}")
    assert r.status_code == 204
    # Confirm gone
    r = client.get(f"/notes/{note['id']}")
    assert r.status_code == 404
