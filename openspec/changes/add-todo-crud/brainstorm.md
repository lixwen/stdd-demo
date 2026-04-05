## Design Summary

为 STDD Demo API 添加 Todo List 的基础增删改查（CRUD）功能。通过 RESTful API 端点暴露，使用内存存储，专注于验证 STDD workflow 的完整流程。

## Agreed Approach

**方案：FastAPI + Pydantic + 内存字典存储**

选择理由：
- 项目目标是验证 STDD workflow，不需要持久化存储的复杂性
- 内存字典最简单，足以承载 CRUD 语义
- Pydantic 提供输入验证和序列化
- FastAPI 的依赖注入可以在未来方便地替换存储层

备选方案评估：
1. **SQLite + SQLAlchemy** — 过重，引入 ORM 和迁移的复杂性，不适合 workflow 验证目标
2. **文件存储（JSON）** — 比内存稍复杂，但没有额外收益
3. **内存字典**（选定）— 最简单，聚焦于业务逻辑和 API 设计

## Key Decisions

| 决策 | 选择 | 理由 |
|------|------|------|
| 存储方式 | 内存字典 | 最简单，验证 workflow 用 |
| ID 生成 | 自增整数 | 简单明确 |
| API 风格 | RESTful | 标准的 CRUD 映射 |
| 数据模型 | title (必填) + completed (默认 false) | 最小可用的 todo 模型 |
| 错误处理 | 404 for 不存在的 todo | 标准 HTTP 语义 |
| 测试方式 | httpx AsyncClient + pytest | 已有基础设施 |

**API 端点设计：**

| 方法 | 路径 | 功能 | 响应码 |
|------|------|------|--------|
| POST | /todos | 创建 todo | 201 |
| GET | /todos | 列出所有 todos | 200 |
| GET | /todos/{id} | 获取单个 todo | 200 / 404 |
| PUT | /todos/{id} | 更新 todo | 200 / 404 |
| DELETE | /todos/{id} | 删除 todo | 204 / 404 |

**数据模型：**

```
Todo:
  id: int (自动生成)
  title: str (必填，非空)
  completed: bool (默认 false)
```

## Open Questions

无。需求明确，方案简单直接。
