# STDD Workflow 实践记录：Todo CRUD 功能

> 本文档记录使用 STDD（Spec/Test-Driven Development）workflow 实现 Todo List CRUD 功能的完整过程。
> STDD workflow 融合了 OpenSpec 的 spec-driven 流程和 Superpowers 的 TDD 技能。

## 项目背景

- **项目**: stdd-demo — 一个用于验证 STDD workflow 的 FastAPI REST API
- **技术栈**: Python 3, FastAPI, Pydantic, pytest, httpx
- **Schema**: 自定义 `stdd` schema (brainstorm → proposal → design/specs → tasks → plan)

## Workflow 概览

```
brainstorm → proposal → design ──┐
                    └→ specs ───┤→ tasks → plan → apply
```

---

## Phase 0: 创建 Change

```bash
openspec new change "add-todo-crud"
```

创建了 `openspec/changes/add-todo-crud/`，schema 为 `stdd`，需要完成 6 个 artifact 才能进入 apply 阶段。

---

## Phase 1: Brainstorm

> 目标：协作式设计探索，明确需求和方案

由于这是一个明确的需求（Todo CRUD），brainstorm 阶段简化为需求确认和方案选择。

**需求确认：**
- 提供 Todo List 的基础增删改查功能
- 作为 REST API 端点暴露
- 内存存储（验证 workflow 用，不需要数据库）

**方案选择：**
- 使用 FastAPI + Pydantic 模型
- 内存字典存储，Todo ID 自增
- 标准 RESTful 端点：POST/GET/PUT/DELETE

---

## Phase 2: Proposal

> 目标：定义 WHY 和 WHAT

提炼 brainstorm 成果，明确变更的动机、范围和影响。
创建了 `proposal.md`，定义了新增的 `todo-crud` capability。

---

## Phase 3: Design

> 目标：定义 HOW

技术设计决策：
- 内存字典存储 vs SQLite vs 文件 → 选择内存字典（最简单，适合验证 workflow）
- Pydantic model 做输入验证
- 标准 HTTP 状态码（201 Created, 404 Not Found 等）

---

## Phase 4: Specs

> 目标：定义可测试的需求规格

每个 Requirement 的 Scenario 直接映射为一个测试用例。
使用 SHALL/MUST 的规范化语言。

---

## Phase 5: Tasks

> 目标：拆分为可追踪的实施任务

按依赖顺序排列，使用 checkbox 格式追踪进度。

---

## Phase 6: Plan

> 目标：TDD 微任务计划（Red-Green-Refactor）

每个 task 拆分为：
1. 写失败测试 (RED)
2. 运行验证失败
3. 写最小实现 (GREEN)
4. 运行验证通过
5. 重构 (REFACTOR)
6. 提交

---

## Phase 7: Apply

> 目标：按 plan 逐步实施代码

（实施过程将在此阶段记录）

---

## Phase 8: 总结

（完成后填写）
