# API Documentation

## Base URL
`http://localhost:8000`

---

## Endpoints

### 1. **GET /notes**
Retrieve a list of all notes.

- **Response**:
    - `200 OK`: Returns a JSON array of notes.

---

### 2. **GET /notes/search**
Search for notes based on query parameters.

- **Query Parameters**:
    - `q` (string): The search term.
- **Response**:
    - `200 OK`: Returns a JSON array of matching notes.

---

### 3. **POST /notes**
Create a new note.

- **Request Body**:
    - `title` (string): The title of the note.
    - `content` (string): The content of the note.
- **Response**:
    - `201 Created`: Returns the created note object.

---

### 4. **PUT /notes**
Update an existing note.

- **Request Body**:
    - `id` (integer): The ID of the note to update.
    - `title` (string): The updated title.
    - `content` (string): The updated content.
- **Response**:
    - `200 OK`: Returns the updated note object.

---

### 5. **DELETE /notes**
Delete a note.

- **Request Body**:
    - `id` (integer): The ID of the note to delete.
- **Response**:
    - `204 No Content`: Indicates successful deletion.

---

### 6. **PUT /action-items/{id}/complete**
Mark an action item as complete.

- **Path Parameter**:
    - `id` (integer): The ID of the action item to mark as complete.
- **Response**:
    - `200 OK`: Returns the updated action item object.

---

## Notes
- Ensure to include appropriate headers for authentication if required.
- Use the provided base URL for all requests.
- Run `make format`, `make lint`, and `make test` after implementing any changes.