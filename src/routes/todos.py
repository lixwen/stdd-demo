from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.models import TodoCreate, TodoResponse, TodoUpdate
from src.store import TodoStore

router = APIRouter(prefix="/todos", tags=["todos"])

_default_store = TodoStore()


def get_store() -> TodoStore:
    return _default_store


@router.post("", status_code=201, response_model=TodoResponse)
async def create_todo(body: TodoCreate, store: TodoStore = Depends(get_store)):
    todo = store.add(body.model_dump())
    return todo


@router.get("", response_model=List[TodoResponse])
async def list_todos(store: TodoStore = Depends(get_store)):
    return store.get_all()


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, store: TodoStore = Depends(get_store)):
    todo = store.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, body: TodoUpdate, store: TodoStore = Depends(get_store)):
    updates = body.model_dump(exclude_unset=True)
    todo = store.update(todo_id, updates)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, store: TodoStore = Depends(get_store)):
    if not store.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
