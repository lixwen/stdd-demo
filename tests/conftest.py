import pytest
from httpx import ASGITransport, AsyncClient

from src.app import app
from src.routes.todos import get_store
from src.store import TodoStore


@pytest.fixture
async def client():
    store = TodoStore()
    app.dependency_overrides[get_store] = lambda: store
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
