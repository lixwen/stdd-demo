## 1. Data Models

- [x] 1.1 Create `src/models.py` with Pydantic models: TodoCreate, TodoUpdate, TodoResponse

## 2. Storage Layer

- [x] 2.1 Create `src/store.py` with TodoStore class (in-memory dict, auto-increment ID)

## 3. API Routes

- [x] 3.1 Create `src/routes/__init__.py` and `src/routes/todos.py` with APIRouter
- [x] 3.2 Implement POST /todos endpoint (create)
- [x] 3.3 Implement GET /todos endpoint (list all)
- [x] 3.4 Implement GET /todos/{id} endpoint (get single)
- [x] 3.5 Implement PUT /todos/{id} endpoint (update)
- [x] 3.6 Implement DELETE /todos/{id} endpoint (delete)

## 4. App Integration

- [x] 4.1 Register todo router in `src/app.py`

## 5. Tests

- [x] 5.1 Add store fixture in `tests/conftest.py` for test isolation
- [x] 5.2 Write tests for POST /todos (success + validation error)
- [x] 5.3 Write tests for GET /todos (empty + with items)
- [x] 5.4 Write tests for GET /todos/{id} (found + not found)
- [x] 5.5 Write tests for PUT /todos/{id} (update title + update completed + not found)
- [x] 5.6 Write tests for DELETE /todos/{id} (success + not found)
