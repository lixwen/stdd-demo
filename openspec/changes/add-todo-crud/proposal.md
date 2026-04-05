## Why

STDD Demo API 目前仅有一个 health check 端点，缺乏实际的业务功能来验证完整的 STDD workflow。需要添加 Todo List 的 CRUD 功能作为第一个真实需求，驱动 brainstorm → specs → design → tasks → plan → apply 的完整流程。

## What Changes

- 新增 Todo 数据模型（Pydantic model），包含 id、title、completed 字段
- 新增内存存储层，使用字典管理 Todo 数据
- 新增 5 个 RESTful API 端点：创建、列出、获取、更新、删除
- 新增对应的 pytest 测试覆盖所有端点和错误场景

## Capabilities

### New Capabilities
- `todo-crud`: Todo List 的基础增删改查功能，包括 RESTful API 端点、数据模型和内存存储

### Modified Capabilities
（无）

## Impact

- **新增文件**: `src/models.py`（数据模型）、`src/store.py`（内存存储）、`src/routes/todos.py`（API 路由）
- **修改文件**: `src/app.py`（注册路由）
- **新增测试**: `tests/test_todos.py`
- **依赖**: 无新增依赖，现有 FastAPI + Pydantic 已满足需求
