# EDGE_CASE.md

## Edge Case Documentation – Student Marks Manager

This document explains the edge cases identified during development and how they were handled in the implementation.

As required:

1) The edge case identified  
2) How it has been accounted for in the implementation  

---

## Edge Case 1 — Invalid Student Input

### Edge Case Identified
A user may submit invalid student data through the frontend form, including:

- Empty name field
- Missing course code
- Marks outside the valid range (0–100)
- Incorrect JSON payload structure

### Implementation Handling

The backend API validates incoming request data before inserting into the database.

If validation fails:

- The backend returns HTTP `400 Bad Request`
- A JSON error message is returned.

Example response:

```json
{
  "error": "Invalid student data"
}
```

### Result

Invalid data is prevented from entering the database, ensuring data integrity.

---

## Edge Case 2 — Non-existent Student Operations

### Edge Case Identified

A request may attempt to update or delete a student that does not exist in the database.

Example:

```
PUT /students/999
DELETE /students/999
```

### Implementation Handling

The backend checks whether the queried student exists:

* If no record is found → return `404 Not Found`.

Example response:

```json
{
  "error": "Student not found"
}
```

### Result

Prevents silent failures and maintains REST API correctness.

---

## Edge Case 3 — Database Not Ready During Startup

### Edge Case Identified

The backend container may start before PostgreSQL becomes available, causing connection errors.

### Implementation Handling

Docker Compose health checks are used:

```yaml
depends_on:
  db:
    condition: service_healthy
```

PostgreSQL exposes a health check using:

```bash
pg_isready -U grading -d grading
```

### Result

Backend only starts after the database is ready, preventing startup crashes.

---

## Edge Case 4 — Frontend Cannot Reach Backend API

### Edge Case Identified

The frontend may fail to fetch data if:

* Backend is down
* Incorrect API URL
* Network failure

### Implementation Handling

Frontend API calls check response status:

```javascript
if (!res.ok) {
  throw new Error("Failed to load students");
}
```

Errors are displayed in the UI as:

```
Failed to fetch
```

### Result

Users receive visible feedback instead of silent UI failure.

---

## Edge Case 5 — Docker Networking (localhost Issue)

### Edge Case Identified

Inside Docker containers, `localhost` refers to the container itself rather than another service.

Using:

```
http://localhost:5000
```

would fail inside the frontend container.

### Implementation Handling

Frontend API base URL priority:

```javascript
const API_BASE =
  import.meta.env.VITE_API_URL || "http://backend:5000";
```

Docker Compose provides:

```yaml
args:
  VITE_API_URL: http://backend:5000
```

### Result

Frontend communicates correctly with backend via Docker internal networking.

---

## Edge Case 6 — Merge Conflicts During Collaboration

### Edge Case Identified

Merging Eric’s feature branch introduced conflicts across multiple files.

### Implementation Handling

Conflicts were resolved manually by:

* Reviewing both versions of code
* Removing conflict markers:

```
<<<<<<<
=======
>>>>>>>
```

* Testing application functionality after resolution.

### Result

Ensures correct integration of collaborative work.

---

## Edge Case 7 — Accidental Commit of Sensitive `.env` File

### Edge Case Identified

A `.env` file containing secrets was accidentally staged.

### Implementation Handling

The file was removed from tracking:

```bash
git rm --cached .env
```

A `.gitignore` file was added:

```
.env
node_modules
```

### Result

Sensitive information is excluded from version control.

---

## Edge Case 8 — Empty Dataset Rendering

### Edge Case Identified

When no students exist, the frontend table could render incorrectly.

### Implementation Handling

Frontend displays a fallback message:

```
No students yet. Add one above.
```

### Result

Prevents UI crashes and improves user experience.

---

## Conclusion

The system accounts for edge cases across:

* Backend validation
* Database availability
* Docker networking
* Frontend error handling
* Git security practices
* Collaborative merge workflows

These measures ensure robustness, reliability, and safe deployment of the Student Marks Manager application.
