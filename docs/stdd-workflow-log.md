# STDD Workflow 实践记录：Todo CRUD 功能

> 本文档记录使用 STDD（Spec/Test-Driven Development）workflow 实现 Todo List CRUD 功能的完整过程。
> STDD workflow 融合了 OpenSpec 的 spec-driven 流程和 Superpowers 的 TDD 技能。

## 项目背景

- **项目**: stdd-demo — 一个用于验证 STDD workflow 的 FastAPI REST API
- **技术栈**: Python 3, FastAPI, Pydantic, pytest, httpx
- **Schema**: 自定义 `stdd` schema (brainstorm → proposal → design/specs → tasks → plan)

## Workflow 概览

```
brainstorm → proposal ─→ specs ──┐
         └→ design ──────────────┤→ tasks → plan → apply
```

**6 个 Artifact + 1 个 Apply 阶段：**

| 阶段 | 产出 | 作用 |
|------|------|------|
| brainstorm | brainstorm.md | 协作设计探索，确认需求和方案 |
| proposal | proposal.md | 定义 WHY 和 WHAT，列出 capabilities |
| design | design.md | 技术设计决策，定义 HOW |
| specs | specs/todo-crud/spec.md | 可测试的需求规格（WHEN/THEN） |
| tasks | tasks.md | 实施任务清单（checkbox 追踪） |
| plan | plan.md | TDD 微任务计划（Red-Green-Refactor） |
| apply | 代码实现 | 按 plan 逐步 TDD 实施 |

---

## Phase 0: 创建 Change

```bash
openspec new change "add-todo-crud"
# ✔ Created change 'add-todo-crud' at openspec/changes/add-todo-crud/ (schema: stdd)
```

`openspec status` 显示 6 个 artifact 的依赖关系：
- `brainstorm` → ready（无依赖）
- `proposal` / `design` → blocked on brainstorm
- `specs` → blocked on proposal
- `tasks` → blocked on design + specs
- `plan` → blocked on tasks

---

## Phase 1: Brainstorm

**输入**: "提供 todo list 的基础增删改查功能"

**产出**: `brainstorm.md`

由于需求明确，brainstorm 简化为方案选择：
- 评估了 3 个方案：SQLite+SQLAlchemy、文件存储、内存字典
- 选定内存字典：最简单，聚焦于验证 workflow
- 确定 API 端点设计（5 个 RESTful 端点）
- 确定数据模型（id + title + completed）

**状态变化**: brainstorm done → proposal 和 design 变为 ready

---

## Phase 2: Proposal

**输入**: brainstorm.md

**产出**: `proposal.md`

提炼 brainstorm 成果：
- **Why**: 需要第一个业务功能来驱动完整 STDD 流程
- **What**: 4 项变更（模型、存储、路由、测试）
- **Capabilities**: 新增 `todo-crud` capability
- **Impact**: 新增 3 个文件，修改 1 个文件

**状态变化**: proposal done → specs 变为 ready

---

## Phase 3: Design

**输入**: brainstorm.md

**产出**: `design.md`

5 项技术决策：
1. 文件结构 — models/store/routes 分离
2. 存储层 — TodoStore 类封装内存字典
3. Pydantic 模型 — 三层模型（Create/Update/Response）
4. HTTP 状态码 — 标准 RESTful 语义
5. 测试策略 — 依赖注入实现测试隔离

**状态变化**: design done → tasks 只差 specs

---

## Phase 4: Specs

**输入**: proposal.md（capabilities 列表）

**产出**: `specs/todo-crud/spec.md`

定义了 5 个 Requirement、11 个 Scenario：

| Requirement | Scenarios |
|-------------|-----------|
| Create a todo | 3 (成功默认值、成功带 completed、缺少 title) |
| List all todos | 2 (空列表、有数据) |
| Get a single todo | 2 (存在、不存在) |
| Update a todo | 3 (更新 title、更新 completed、不存在) |
| Delete a todo | 2 (成功、不存在) |

每个 Scenario 使用 WHEN/THEN 格式，直接映射为测试用例。

**状态变化**: specs done → tasks 变为 ready

---

## Phase 5: Tasks

**输入**: specs + design

**产出**: `tasks.md`

拆分为 5 组、14 个 task：

1. Data Models (1 task)
2. Storage Layer (1 task)
3. API Routes (6 tasks)
4. App Integration (1 task)
5. Tests (6 tasks)

所有 task 使用 `- [ ]` checkbox 格式，apply 阶段自动追踪进度。

**状态变化**: tasks done → plan 变为 ready

---

## Phase 6: Plan

**输入**: tasks.md + design.md

**产出**: `plan.md`

将 tasks 拆分为 3 个 TDD Task，每个包含 Red-Green-Refactor 微步骤：

- **Task 1**: Pydantic Models — 写测试 → 失败 → 实现 → 通过 → 提交
- **Task 2**: TodoStore — 写测试 → 失败 → 实现 → 通过 → 提交
- **Task 3**: API Routes + Integration — 写测试 → 失败 → 实现 → 通过 → 重构 → 提交

**状态变化**: plan done → 6/6 artifacts complete, ready for apply!

```
openspec status --change add-todo-crud
# Progress: 6/6 artifacts complete
# All artifacts complete!
```

---

## Phase 7: Apply

按 plan.md 的 TDD 节奏逐步实施。

### Task 1: Pydantic Models

**RED**: 写了 4 个测试（TodoCreate 默认值、带 completed、TodoUpdate 部分更新、TodoResponse）
```
.venv/bin/pytest tests/test_models.py -v
# FAIL — ModuleNotFoundError: No module named 'src.models'
```

**GREEN**: 创建 `src/models.py`，定义 TodoCreate、TodoUpdate、TodoResponse
```
.venv/bin/pytest tests/test_models.py -v
# 4 passed ✓
```

**Commit**: `feat: add Pydantic models for Todo CRUD`

### Task 2: TodoStore

**RED**: 写了 9 个测试（add、auto_increment、get、get_all_empty、get_all_with_items、update、update_not_found、delete、delete_not_found）
```
.venv/bin/pytest tests/test_store.py -v
# FAIL — ModuleNotFoundError: No module named 'src.store'
```

**GREEN**: 创建 `src/store.py`，实现 TodoStore 类
```
.venv/bin/pytest tests/test_store.py -v
# 9 passed ✓
```

**Commit**: `feat: add TodoStore with in-memory dict storage`

### Task 3: API Routes + Integration

**RED**: 写了 12 个 API 集成测试（覆盖所有 11 个 spec scenario + 1 个额外 case）
```
.venv/bin/pytest tests/test_todos.py -v
# 9 failed, 3 passed — 路由不存在，返回 404
```

**GREEN**: 创建 `src/routes/todos.py`（5 个端点 + 依赖注入），更新 `src/app.py`（注册路由），更新 `tests/conftest.py`（store 隔离 fixture）
```
.venv/bin/pytest -v
# 26 passed, 11 warnings (Pydantic V2 deprecation)
```

**REFACTOR**: 将 `.dict()` 替换为 `.model_dump()`，消除 deprecation warning
```
.venv/bin/pytest -v
# 26 passed, 0 warnings ✓
```

**Commit**: `feat: add Todo CRUD API routes with full test coverage`

---

## Phase 8: 总结

### 最终成果

| 指标 | 数值 |
|------|------|
| 测试总数 | 26 |
| 通过率 | 100% |
| 新增文件 | 7 (models, store, routes, tests) |
| 修改文件 | 2 (app.py, conftest.py) |
| Spec Scenarios | 11 |
| Commits | 5 (artifacts + 3 TDD commits) |

### 文件结构

```
src/
├── __init__.py
├── app.py              # FastAPI 实例 + 路由注册
├── models.py           # Pydantic: TodoCreate, TodoUpdate, TodoResponse
├── store.py            # TodoStore: 内存字典存储
└── routes/
    ├── __init__.py
    └── todos.py        # 5 个 CRUD 端点

tests/
├── __init__.py
├── conftest.py         # AsyncClient fixture + store 隔离
├── test_health.py      # Health check 测试 (1)
├── test_models.py      # 模型测试 (4)
├── test_store.py       # 存储层测试 (9)
└── test_todos.py       # API 集成测试 (12)
```

### Workflow 验证结论

STDD workflow 成功运行了完整的 8 个阶段：

1. **brainstorm** — 快速确认需求和方案（对于简单需求可以简化）
2. **proposal** — 提炼为结构化的变更描述
3. **design** — 技术决策记录（对未来维护有价值）
4. **specs** — WHEN/THEN 格式直接映射为测试用例（spec → test 的桥梁）
5. **tasks** — checkbox 追踪提供清晰的进度可见性
6. **plan** — TDD 微任务确保 Red-Green-Refactor 纪律
7. **apply** — 按 plan 逐步实施，每步都有测试验证

关键价值：**specs 中的 11 个 scenario 最终变成了 12 个 API 测试**，spec 驱动测试、测试驱动开发的理念得到了端到端验证。
