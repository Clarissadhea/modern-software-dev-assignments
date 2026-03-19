# API Documentation

This document describes the available endpoints for Notes, Action Items, and Search functionality in the backend.

## Notes Endpoints

- **GET /notes/**
  - List notes with optional search (`q`), pagination (`skip`, `limit`), and sorting (`sort`).
  - Query params:
    - `q`: Search term for title/content
    - `skip`: Offset for pagination
    - `limit`: Max results (default 50, max 200)
    - `sort`: Field to sort by (prefix with '-' for descending)

- **POST /notes/**
  - Create a new note.
  - Body: `{ title, content }`

- **PATCH /notes/{note_id}**
  - Update note fields (title/content).
  - Body: `{ title?, content? }`

- **GET /notes/{note_id}**
  - Retrieve a single note by ID.

## Action Items Endpoints

- **GET /action-items/**
  - List action items with optional filter (`completed`), pagination (`skip`, `limit`), and sorting (`sort`).
  - Query params:
    - `completed`: Filter by completion status
    - `skip`: Offset for pagination
    - `limit`: Max results (default 50, max 200)
    - `sort`: Field to sort by (prefix with '-' for descending)

- **POST /action-items/**
  - Create a new action item.
  - Body: `{ description }`

- **PUT /action-items/{item_id}/complete**
  - Mark an action item as complete.

- **PATCH /action-items/{item_id}**
  - Update action item fields (description/completed).
  - Body: `{ description?, completed? }`

## Search

- Notes endpoint supports search via the `q` query parameter in `GET /notes/`.

---

For detailed request/response schemas, see the backend code in `week7/backend/app/schemas.py`.
