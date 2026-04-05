# STDD Demo

一个用于探索和验证 **STDD（Spec/Test-Driven Development）** 工作流的示例项目。

STDD 将 [OpenSpec](https://github.com/fission-ai/openspec) 的 spec-driven 流程与 [Superpowers](https://github.com/cursor-public/superpowers) 的 TDD 技能融合，形成从需求到代码的完整闭环：**spec 驱动测试，测试驱动开发**。

## 核心理念

```
需求 → Spec（WHEN/THEN 场景） → 测试用例 → 最小实现 → 重构
```

传统开发中，需求文档和代码之间往往存在断层。STDD 的目标是让每一层产出都可以直接驱动下一层：

- **Spec 的每个 Scenario** 直接映射为一个测试用例
- **每个测试** 先写并看到失败（RED），再写最小实现（GREEN），再清理（REFACTOR）
- **整个过程** 通过 OpenSpec 的 artifact 依赖图自动编排

## STDD Workflow

自定义的 `stdd` schema 定义了 6 个 artifact 阶段 + 1 个 apply 阶段：

```
brainstorm ─→ proposal ─→ specs ──┐
          └─→ design ─────────────┤─→ tasks ─→ plan ─→ apply
```

| 阶段 | 产出 | 解决什么问题 |
|------|------|-------------|
| **brainstorm** | brainstorm.md | 协作探索，确认需求和方案 |
| **proposal** | proposal.md | 定义 WHY 和 WHAT，列出 capabilities |
| **design** | design.md | 技术决策，定义 HOW |
| **specs** | specs/\*/spec.md | 可测试的需求规格（WHEN/THEN） |
| **tasks** | tasks.md | 实施任务清单（checkbox 追踪） |
| **plan** | plan.md | TDD 微任务（Red-Green-Refactor 节奏） |
| **apply** | 代码 | 按 plan 逐步 TDD 实施 |

每个 artifact 有明确的依赖关系，OpenSpec CLI 自动管理状态流转：当前置 artifact 完成后，下游 artifact 自动变为 ready。

## 探索过程

本项目通过实现一个 **Todo List CRUD API** 来验证完整的 STDD 流程。

### 第一步：搭建基础设施

- 创建自定义 `stdd` schema（fork 自 [sdd-plus-superpowers](https://github.com/JiangWay/OpenSpec/tree/main/schemas/sdd-plus-superpowers)）
- 搭建 FastAPI + pytest 项目骨架
- 配置 OpenSpec + Cursor skills/commands

### 第二步：走完一个真实需求

用 "Todo CRUD" 作为第一个需求，走完 8 个阶段：

**Brainstorm** → 评估 3 个存储方案，选定内存字典

**Proposal** → 定义新增 `todo-crud` capability

**Design** → 5 项技术决策（模型分离、存储封装、依赖注入等）

**Specs** → 5 个 Requirement、11 个 WHEN/THEN Scenario：

```markdown
### Requirement: Create a todo

#### Scenario: Create todo with title only
- **WHEN** POST /todos with body {"title": "Buy milk"}
- **THEN** response status is 201 and body contains {"id": 1, "title": "Buy milk", "completed": false}
```

**Tasks** → 14 个 checkbox task，按依赖排序

**Plan** → 3 个 TDD Task，每个包含 RED/GREEN/REFACTOR 微步骤

**Apply** → 严格 TDD 实施：

```bash
# RED: 写测试，看它失败
.venv/bin/pytest tests/test_todos.py -v
# 9 failed — 路由不存在

# GREEN: 写最小实现
# ... 创建路由、注册到 app ...

.venv/bin/pytest -v
# 26 passed ✓
```

完整过程记录见 [docs/stdd-workflow-log.md](docs/stdd-workflow-log.md)。

### 最终成果

| 指标 | 数值 |
|------|------|
| 测试总数 | 26 |
| Spec Scenarios | 11 |
| API 端点 | 5 (POST/GET/GET/PUT/DELETE) |
| TDD Commits | 3 (models → store → routes) |

## 项目结构

```
stdd-demo/
├── src/                          # 应用代码
│   ├── app.py                    #   FastAPI 实例
│   ├── models.py                 #   Pydantic 数据模型
│   ├── store.py                  #   内存存储层
│   └── routes/todos.py           #   CRUD 端点
├── tests/                        # 测试
│   ├── conftest.py               #   Fixtures（AsyncClient + store 隔离）
│   ├── test_models.py            #   模型测试 (4)
│   ├── test_store.py             #   存储层测试 (9)
│   └── test_todos.py             #   API 集成测试 (12)
├── openspec/
│   ├── config.yaml               # OpenSpec 配置（schema: stdd）
│   ├── schemas/stdd/             # 自定义 STDD workflow schema
│   │   ├── schema.yaml           #   6 artifact 定义 + apply 指令
│   │   └── templates/            #   artifact 模板文件
│   └── changes/add-todo-crud/    # 第一个需求的完整 artifact
│       ├── brainstorm.md
│       ├── proposal.md
│       ├── design.md
│       ├── specs/todo-crud/spec.md
│       ├── tasks.md
│       └── plan.md
├── docs/
│   └── stdd-workflow-log.md      # 完整过程记录
└── pyproject.toml
```

## 快速开始

```bash
# 克隆项目
git clone git@github.com:lixwen/stdd-demo.git
cd stdd-demo

# 创建虚拟环境并安装依赖
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"

# 运行测试
.venv/bin/pytest -v

# 启动开发服务器
.venv/bin/uvicorn src.app:app --reload
```

## 使用 STDD Workflow

需要安装 [OpenSpec CLI](https://github.com/fission-ai/openspec) 和 Cursor IDE。

```bash
# 安装 openspec
npm install -g @fission-ai/openspec

# 查看可用 schema
openspec schemas

# 发起一个新需求
openspec new change "your-feature-name"

# 查看 artifact 进度
openspec status --change "your-feature-name"
```

在 Cursor 中可以使用以下命令：

| 命令 | 作用 |
|------|------|
| `/opsx-propose` | 提出新 change，自动生成所有 artifact |
| `/opsx-apply` | 按 plan 实施代码 |
| `/opsx-explore` | 探索模式，自由讨论和调研 |
| `/opsx-archive` | 归档已完成的 change |

## 技术栈

- **Python 3** + **FastAPI** + **Pydantic** — Web API
- **pytest** + **httpx** — 测试
- **OpenSpec** — Spec-driven workflow 编排
- **Superpowers** — TDD / brainstorming / planning 技能
