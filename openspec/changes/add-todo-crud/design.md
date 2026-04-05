## Context

STDD Demo API 是一个用于验证 STDD workflow 的 FastAPI 项目。当前只有一个 `/health` 端点。需要添加 Todo CRUD 作为第一个业务功能。

现有代码结构：
- `src/app.py` — FastAPI 应用实例 + health 端点
- `tests/conftest.py` — httpx AsyncClient fixture
- `tests/test_health.py` — health 端点测试

## Goals / Non-Goals

**Goals:**
- 实现标准的 Todo CRUD RESTful API
- 保持代码结构清晰，模型/存储/路由分离
- 测试覆盖所有端点及错误场景

**Non-Goals:**
- 不做持久化存储（不引入数据库）
- 不做用户认证/授权
- 不做分页、排序、过滤
- 不做 WebSocket 实时推送

## Decisions

**1. 文件结构 — 模块分离**

```
src/
├── app.py          # FastAPI 实例，注册路由
├── models.py       # Pydantic 模型：TodoCreate, TodoUpdate, TodoResponse
├── store.py        # TodoStore 类，内存字典存储
└── routes/
    └── todos.py    # APIRouter，5 个 CRUD 端点
```

理由：模型/存储/路由分离，每个文件职责单一，便于测试和未来替换存储层。

备选：全部写在 app.py — 更简单但不利于扩展，且验证不了真实项目结构。

**2. 存储层 — 内存字典 + 类封装**

使用 `TodoStore` 类封装 `dict[int, dict]`，提供 `add/get/get_all/update/delete` 方法。ID 使用 `_next_id` 自增计数器。

理由：类封装提供清晰的接口边界。未来替换为数据库只需实现相同接口。

**3. Pydantic 模型 — 三层模型**

- `TodoCreate`: 创建时的输入（title 必填，completed 可选默认 false）
- `TodoUpdate`: 更新时的输入（title 和 completed 都可选）
- `TodoResponse`: 响应输出（包含 id）

理由：分离输入/输出模型是 FastAPI 最佳实践，避免用户指定 id。

**4. HTTP 状态码**

| 操作 | 成功 | 失败 |
|------|------|------|
| POST /todos | 201 Created | 422 Validation Error |
| GET /todos | 200 OK | — |
| GET /todos/{id} | 200 OK | 404 Not Found |
| PUT /todos/{id} | 200 OK | 404 Not Found |
| DELETE /todos/{id} | 204 No Content | 404 Not Found |

**5. 测试策略**

每个端点至少一个成功和一个失败测试。使用 fixture 提供预置数据。
测试间状态隔离：每个测试使用独立的 store 实例。

## Risks / Trade-offs

- [内存存储重启丢失数据] → 可接受，项目目标是验证 workflow
- [并发写入不安全] → 可接受，测试项目不涉及并发场景
- [无分页] → 可接受，数据量小，后续需求可扩展

## Open Questions

无。
