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


def test_store_get():
    store = TodoStore()
    store.add({"title": "Buy milk", "completed": False})
    assert store.get(1) is not None
    assert store.get(999) is None


def test_store_get_all_empty():
    store = TodoStore()
    assert store.get_all() == []


def test_store_get_all_with_items():
    store = TodoStore()
    store.add({"title": "First", "completed": False})
    store.add({"title": "Second", "completed": True})
    items = store.get_all()
    assert len(items) == 2


def test_store_update():
    store = TodoStore()
    store.add({"title": "Buy milk", "completed": False})
    updated = store.update(1, {"title": "Buy eggs"})
    assert updated["title"] == "Buy eggs"
    assert updated["completed"] is False


def test_store_update_not_found():
    store = TodoStore()
    assert store.update(999, {"title": "X"}) is None


def test_store_delete():
    store = TodoStore()
    store.add({"title": "Buy milk", "completed": False})
    assert store.delete(1) is True
    assert store.get_all() == []


def test_store_delete_not_found():
    store = TodoStore()
    assert store.delete(1) is False
