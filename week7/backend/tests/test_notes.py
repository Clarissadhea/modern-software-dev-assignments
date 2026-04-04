def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_notes_pagination_and_sorting(client):
    # Create at least 5 sample notes with different titles
    sample_titles = ["Note A", "Note B", "Note C", "Note D", "Note E"]
    created_notes = []

    for title in sample_titles:
        payload = {"title": title, "content": f"Content for {title}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, r.text
        created_notes.append(r.json())

    # Test Pagination: limit=2 should return only 2 notes
    r = client.get("/notes/", params={"limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2, f"Expected 2 items with limit=2, got {len(items)}"

    # Test Pagination: skip=2 should skip the first 2 notes
    r = client.get("/notes/", params={"skip": 2, "limit": 10})
    assert r.status_code == 200
    items_after_skip = r.json()
    assert len(items_after_skip) >= 3, "Expected at least 3 items after skipping 2"

    # Verify skip returns different notes than the first request
    first_two = client.get("/notes/", params={"limit": 2}).json()
    assert first_two[0]["id"] != items_after_skip[0]["id"], "skip=2 should return different notes"

    # Test Sorting by title in ascending order
    r = client.get("/notes/", params={"sort": "title", "limit": 10})
    assert r.status_code == 200
    items_asc = r.json()
    
    # Extract titles from the response, filtering only the ones we created
    created_note_ids = {note["id"] for note in created_notes}
    asc_titles = [item["title"] for item in items_asc if item["id"] in created_note_ids]
    
    # Verify ascending order (at least for the notes we created)
    if len(asc_titles) >= 2:
        for i in range(len(asc_titles) - 1):
            assert asc_titles[i] <= asc_titles[i + 1], f"Titles not in ascending order: {asc_titles}"

    # Test Sorting by title in descending order
    r = client.get("/notes/", params={"sort": "-title", "limit": 10})
    assert r.status_code == 200
    items_desc = r.json()
    
    desc_titles = [item["title"] for item in items_desc if item["id"] in created_note_ids]
    
    # Verify descending order (at least for the notes we created)
    if len(desc_titles) >= 2:
        for i in range(len(desc_titles) - 1):
            assert desc_titles[i] >= desc_titles[i + 1], f"Titles not in descending order: {desc_titles}"

    # Verify that ascending and descending are opposites
    asc_response = client.get("/notes/", params={"sort": "title", "limit": 10}).json()
    desc_response = client.get("/notes/", params={"sort": "-title", "limit": 10}).json()
    
    asc_ids = [note["id"] for note in asc_response if note["id"] in created_note_ids]
    desc_ids = [note["id"] for note in desc_response if note["id"] in created_note_ids]
    
    # Last in ascending should be first in descending (for created notes)
    if asc_ids and desc_ids:
        assert asc_ids[-1] == desc_ids[0], "Reverse order verification failed"


