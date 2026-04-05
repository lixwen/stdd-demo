## 1. Data Models

- [x] 1.1 Create `src/models.py` with Pydantic models: TodoCreate, TodoUpdate, TodoResponse

## 2. Storage Layer

- [x] 2.1 Create `src/store.py` with TodoStore class (in-memory dict, auto-increment ID)

## 3. API Routes

- [ ] 3.1 Create `src/routes/__init__.py` and `src/routes/todos.py` with APIRouter
- [ ] 3.2 Implement POST /todos endpoint (create)
- [ ] 3.3 Implement GET /todos endpoint (list all)
- [ ] 3.4 Implement GET /todos/{id} endpoint (get single)
- [ ] 3.5 Implement PUT /todos/{id} endpoint (update)
- [ ] 3.6 Implement DELETE /todos/{id} endpoint (delete)

## 4. App Integration

- [ ] 4.1 Register todo router in `src/app.py`

## 5. Tests

- [ ] 5.1 Add store fixture in `tests/conftest.py` for test isolation
- [ ] 5.2 Write tests for POST /todos (success + validation error)
- [ ] 5.3 Write tests for GET /todos (empty + with items)
- [ ] 5.4 Write tests for GET /todos/{id} (found + not found)
- [ ] 5.5 Write tests for PUT /todos/{id} (update title + update completed + not found)
- [ ] 5.6 Write tests for DELETE /todos/{id} (success + not found)
