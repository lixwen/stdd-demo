from typing import Dict, List, Optional


class TodoStore:
    def __init__(self):
        self._data: Dict[int, dict] = {}
        self._next_id = 1

    def add(self, item: dict) -> dict:
        todo = {"id": self._next_id, **item}
        self._data[self._next_id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id: int) -> Optional[dict]:
        return self._data.get(todo_id)

    def get_all(self) -> List[dict]:
        return list(self._data.values())

    def update(self, todo_id: int, updates: dict) -> Optional[dict]:
        if todo_id not in self._data:
            return None
        self._data[todo_id].update(updates)
        return self._data[todo_id]

    def delete(self, todo_id: int) -> bool:
        if todo_id not in self._data:
            return False
        del self._data[todo_id]
        return True
