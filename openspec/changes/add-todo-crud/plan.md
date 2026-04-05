# Todo CRUD Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task.

**Goal:** Add Todo List CRUD functionality to the STDD Demo API

**Architecture:** FastAPI router with Pydantic models, in-memory dict storage via TodoStore class, dependency injection for test isolation

**Tech Stack:** Python 3, FastAPI, Pydantic, pytest, httpx

---

## Task 1: Pydantic Models

**Files:**
- Create: `src/models.py`
- Test: `tests/test_models.py`

- [ ] **Step 1: Write failing test for TodoCreate model**

```python
# tests/test_models.py
from src.models import TodoCreate

def test_todo_create_defaults():
    todo = TodoCreate(title="Buy milk")
    assert todo.title == "Buy milk"
    assert todo.completed is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.models'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/models.py
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/test_models.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/models.py tests/test_models.py
git commit -m "feat: add Pydantic models for Todo CRUD"
```

## Task 2: TodoStore

**Files:**
- Create: `src/store.py`
- Test: `tests/test_store.py`

- [ ] **Step 1: Write failing test for TodoStore.add**

```python
# tests/test_store.py
from src.store import TodoStore

def test_store_add():
    store = TodoStore()
    todo = store.add({"title": "Buy milk", "completed": False})
    assert todo["id"] == 1
    assert todo["title"] == "Buy milk"
    assert todo["completed"] is False

def test_store_add_auto_increment():
    store = TodoStore()
    t1 = store.add({"title": "First"})
    t2 = store.add({"title": "Second"})
    assert t1["id"] == 1
    assert t2["id"] == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_store.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.store'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/store.py
class TodoStore:
    def __init__(self):
        self._data: dict[int, dict] = {}
        self._next_id = 1

    def add(self, item: dict) -> dict:
        todo = {"id": self._next_id, **item}
        self._data[self._next_id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id: int) -> dict | None:
        return self._data.get(todo_id)

    def get_all(self) -> list[dict]:
        return list(self._data.values())

    def update(self, todo_id: int, updates: dict) -> dict | None:
        if todo_id not in self._data:
            return None
        self._data[todo_id].update(updates)
        return self._data[todo_id]

    def delete(self, todo_id: int) -> bool:
        if todo_id not in self._data:
            return False
        del self._data[todo_id]
        return True
```

- [ ] **Step 4: Write additional tests for get, get_all, update, delete**

```python
# append to tests/test_store.py
def test_store_get():
    store = TodoStore()
    store.add({"title": "Buy milk", "completed": False})
    assert store.get(1) is not None
    assert store.get(999) is None

def test_store_get_all_empty():
    store = TodoStore()
    assert store.get_all() == []

def test_store_update():
    store = TodoStore()
    store.add({"title": "Buy milk", "completed": False})
    updated = store.update(1, {"title": "Buy eggs"})
    assert updated["title"] == "Buy eggs"
    assert store.update(999, {"title": "X"}) is None

def test_store_delete():
    store = TodoStore()
    store.add({"title": "Buy milk", "completed": False})
    assert store.delete(1) is True
    assert store.delete(1) is False
    assert store.get_all() == []
```

- [ ] **Step 5: Run all store tests**

Run: `.venv/bin/pytest tests/test_store.py -v`
Expected: PASS (all tests)

- [ ] **Step 6: Commit**

```bash
git add src/store.py tests/test_store.py
git commit -m "feat: add TodoStore with in-memory dict storage"
```

## Task 3: API Routes + Integration Tests

**Files:**
- Create: `src/routes/__init__.py`, `src/routes/todos.py`
- Modify: `src/app.py`, `tests/conftest.py`
- Create: `tests/test_todos.py`

- [ ] **Step 1: Write failing test for POST /todos**

```python
# tests/test_todos.py
import pytest

@pytest.mark.asyncio
async def test_create_todo(client):
    resp = await client.post("/todos", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_todos.py::test_create_todo -v`
Expected: FAIL — 404 (route not registered)

- [ ] **Step 3: Create route module and register router**

```python
# src/routes/__init__.py
(empty file)
```

```python
# src/routes/todos.py
from fastapi import APIRouter, HTTPException
from src.models import TodoCreate, TodoUpdate, TodoResponse
from src.store import TodoStore

router = APIRouter(prefix="/todos", tags=["todos"])
store = TodoStore()

@router.post("", status_code=201, response_model=TodoResponse)
async def create_todo(body: TodoCreate):
    todo = store.add(body.dict())
    return todo
```

```python
# src/app.py — add router registration
from fastapi import FastAPI
from src.routes.todos import router as todos_router

app = FastAPI(title="STDD Demo API", version="0.1.0")
app.include_router(todos_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/test_todos.py::test_create_todo -v`
Expected: PASS

- [ ] **Step 5: Update conftest.py for store isolation, add remaining endpoint tests**

Update `tests/conftest.py` to reset store between tests.

Add tests in `tests/test_todos.py` for:
- POST /todos with missing title (422)
- GET /todos (empty list + with items)
- GET /todos/{id} (found + 404)
- PUT /todos/{id} (update title + update completed + 404)
- DELETE /todos/{id} (success 204 + 404)

- [ ] **Step 6: Implement remaining endpoints in src/routes/todos.py**

```python
@router.get("", response_model=list[TodoResponse])
async def list_todos():
    return store.get_all()

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    todo = store.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, body: TodoUpdate):
    updates = body.dict(exclude_unset=True)
    todo = store.update(todo_id, updates)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    if not store.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
```

- [ ] **Step 7: Run all tests**

Run: `.venv/bin/pytest -v`
Expected: ALL PASS

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: add Todo CRUD API routes with full test coverage"
```
