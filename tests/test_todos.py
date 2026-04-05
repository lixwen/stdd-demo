import pytest


@pytest.mark.asyncio
async def test_create_todo(client):
    resp = await client.post("/todos", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_create_todo_with_completed(client):
    resp = await client.post("/todos", json={"title": "Buy milk", "completed": True})
    assert resp.status_code == 201
    assert resp.json()["completed"] is True


@pytest.mark.asyncio
async def test_create_todo_missing_title(client):
    resp = await client.post("/todos", json={})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_list_todos_empty(client):
    resp = await client.get("/todos")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_todos_with_items(client):
    await client.post("/todos", json={"title": "First"})
    await client.post("/todos", json={"title": "Second"})
    resp = await client.get("/todos")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_todo(client):
    create_resp = await client.post("/todos", json={"title": "Buy milk"})
    todo_id = create_resp.json()["id"]
    resp = await client.get(f"/todos/{todo_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Buy milk"


@pytest.mark.asyncio
async def test_get_todo_not_found(client):
    resp = await client.get("/todos/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_todo_title(client):
    create_resp = await client.post("/todos", json={"title": "Buy milk"})
    todo_id = create_resp.json()["id"]
    resp = await client.put(f"/todos/{todo_id}", json={"title": "Buy eggs"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Buy eggs"
    assert resp.json()["completed"] is False


@pytest.mark.asyncio
async def test_update_todo_completed(client):
    create_resp = await client.post("/todos", json={"title": "Buy milk"})
    todo_id = create_resp.json()["id"]
    resp = await client.put(f"/todos/{todo_id}", json={"completed": True})
    assert resp.status_code == 200
    assert resp.json()["completed"] is True
    assert resp.json()["title"] == "Buy milk"


@pytest.mark.asyncio
async def test_update_todo_not_found(client):
    resp = await client.put("/todos/999", json={"title": "X"})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_todo(client):
    create_resp = await client.post("/todos", json={"title": "Buy milk"})
    todo_id = create_resp.json()["id"]
    resp = await client.delete(f"/todos/{todo_id}")
    assert resp.status_code == 204

    list_resp = await client.get("/todos")
    assert len(list_resp.json()) == 0


@pytest.mark.asyncio
async def test_delete_todo_not_found(client):
    resp = await client.delete("/todos/999")
    assert resp.status_code == 404
