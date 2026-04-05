from src.models import TodoCreate, TodoUpdate, TodoResponse


def test_todo_create_defaults():
    todo = TodoCreate(title="Buy milk")
    assert todo.title == "Buy milk"
    assert todo.completed is False


def test_todo_create_with_completed():
    todo = TodoCreate(title="Buy milk", completed=True)
    assert todo.completed is True


def test_todo_update_partial():
    update = TodoUpdate(title="Buy eggs")
    assert update.title == "Buy eggs"
    assert update.completed is None


def test_todo_response():
    resp = TodoResponse(id=1, title="Buy milk", completed=False)
    assert resp.id == 1
    assert resp.title == "Buy milk"
