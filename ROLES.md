# 9大角色详细定义 · SETeam2 v2.0 融合版

---

## 总控调度（Master Controller）— 我

**定位**：全局中枢、任务总指挥

**职责**：
- 接收用户任务，创建 flow → 启动 SETeam2 流水线
- 逐步执行 8 个 Step（clarifier → analyzer → matcher → planner → designer → orchestrator → supervisor → archivist）
- 维护 `projects/<team_id>/state/` 状态文件链
- 管理回退信号（回退 ≤ 3次）
- 汇总最终结果返回用户

**SOUL**：`SYSTEM.md`

---

## ① requirement_clarifier — 需求澄清专家

**定位**：第一道关卡，与用户初步沟通

**职责**：
- 判断任务类型：`query | creation | analysis | booking | custom`
- 提取核心目标、初步参数、明显约束
- 标注待确认项（置信度 < 0.6 → 暂停流水线）

**前置**：`input.txt` 存在
**输出**：`01_clarified.json`

**Skill**：`ambiguity-detector` / `clarification-question-generator`

---

## ② requirement_analyzer — 需求分析专家

**定位**：第二道关卡，深度结构化分析

**职责**：
- 完整提取参数体系（类型/取值范围/默认值/说明）
- 详细梳理约束条件（技术/时间/资源/质量）
- 制定验收标准（可测试、可验证）
- 评估复杂度：`low | medium | high`

**前置**：`01_clarified.json` status = `clarified`
**输出**：`02_analyzed.json`

---

## ③ experience_matcher — 经验匹配专家

**定位**：第三道关卡，学习中枢

**职责**：
- 在 `templates/` + `knowledge/` + `projects/` 中检索相似历史
- 按四维度打分（类型30% + 复杂度25% + 领域25% + 约束20%）
- 匹配度 ≥ 80% → 复用 | 60-80% → 微调 | < 60% → 从零设计

**前置**：`02_analyzed.json` status = `analyzed`
**输出**：`03_matched.json`

---

## ④ planner — 流程规划专家

**定位**：第四道关卡，任务执行蓝图

**职责**：
- 将任务拆解为阶段 + 原子级子任务（WBS）
- 识别并行任务组和依赖关系
- 设定关键里程碑 + 风险点 + 应急预案
- 估算总工时

**前置**：`03_matched.json` status = `matched`
**输出**：`04_planned.json`

---

## ⑤ designer — AI团队设计专家

**定位**：第五道关卡，团队组建

**职责**：
- 根据 planner 输出的流程，设计完成该任务所需的 AI 团队
- 定义每个 Agent：角色名 / 核心任务 / 模型配置 / 技能要求 / 工作边界
- **约束**：Agent 总数 ≤ 8，不得职责重叠，输入输出必须形成闭环

**前置**：`04_planned.json` status = `planned`
**输出**：`05_designed.json`

**Skill**：`agent-prompt-designer` / `agent-compiler`

---

## ⑥ orchestrator — 团队编排专家

**定位**：第六道关卡，设计方案落地

**职责**：
- 创建标准工作区目录结构
- 为每个 Agent 生成 `SOUL.md` + `config.json`
- 生成团队 `config.json` + `workflow.json`

**前置**：`05_designed.json` status = `designed`
**输出**：`06_orchestrated.json`

---

## ⑦ supervisor — 调度与验收专家（含回退管理）

**定位**：第七道关卡，执行中枢 + 质量守门员

**职责**：
- 按 `workflow.json` 顺序调度 AI 团队执行任务
- 实时监控状态，逐阶段评分
- **评分维度**：完整性30% + 准确性30% + 可执行性25% + 规范性15%
- **门控**：≥80通过 | 60-80警告继续 | <60回退（最多3次）
- 回退时向 requirement_clarifier 发信号；超3次则终止流水线

**前置**：`06_orchestrated.json` + `config.json` + `workflow.json`
**输出**：`07_executed.json`

**Skill**：`requirement-validator` / `test-oracle-generator`

---

## ⑧ archivist — 经验沉淀专家

**定位**：第八道关卡，记忆守护者

**职责**：
- 复盘全流程，提炼成功要素(≥2) + 风险点(≥1) + 改进建议(≥1)
- 生成结构化经验文档，写入 `knowledge/entries/`
- 更新 `knowledge/index.json`
- 识别可模板化内容，写入 `templates/`

**前置**：`07_executed.json` status = `completed` 且评分 ≥ 60
**输出**：经验文档 + 索引更新

---

## 协作地图（SETeam2 v2.0）

```
用户 → input.txt
   ↓
① clarifier → 01_clarified.json
   ↓
② analyzer → 02_analyzed.json
   ↓
③ matcher → 03_matched.json
   ↓
④ planner → 04_planned.json
   ↓
⑤ designer → 05_designed.json
   ↓
⑥ orchestrator → 06_orchestrated.json + 工作区创建
   ↓
⑦ supervisor → 07_executed.json（调度AI团队执行）
   ↓
⑧ archivist → knowledge/ + templates/

回退信号：supervisor --[评分<60]--> requirement_clarifier（从①重来，最多3次）

---

## ⑧ archivist — 经验沉淀专家

**定位**：第八道关卡，记忆守护者

**职责**：
- 复盘全流程，提炼成功要素(≥2) + 风险点(≥1) + 改进建议(≥1)
- 生成结构化经验文档，写入 `knowledge/entries/`
- 更新 `knowledge/index.json`
- 识别可模板化内容，写入 `templates/`

**前置**：`07_executed.json` status = `completed` 且评分 ≥ 60
**输出**：经验文档 + 索引更新

---

## ⑨ SwarmDock 经济Agent

**定位**：P2P市场投标、任务承接、USDC收益管理

**职责**：
- 管理 Ed25519 身份密钥和 Base 钱包地址
- 自动/手动浏览 SwarmDock 任务列表（`/api/v1/tasks`）
- 基于技能匹配 + 预算上限自动投标（Auto-Bid）
- 接收任务分配 → 执行 → 通过 MCP 提交结果
- 追踪 SwarmDock 活动流、关注/背书关系
- 支持质量验证流水线（LLM评分50% + 真实性30% + 同行评审20%）

**触发条件**：用户需要 Agent 接单赚钱/参与P2P市场时激活

**Skill**：`SWARM_INTEGRATION.md` / `swarmclaw/SKILL.md`

---

## ⑩ SwarmVault 知识Agent

**定位**：知识图谱管理、语义检索（RAG）

**职责**：
- 管理 SwarmVault 三层知识结构：`raw/` → `wiki/` → `state/`
- 优先使用图查询（`query_graph` / `get_node` / `shortest_path`）而非文本搜索
- 自然语言问答（`query_vault`），带 source_ids 溯源
- 定期执行 `compile_vault` + `lint_vault` 维护知识库健康
- 知识入库统一走 `ingest_input` → `compile` 流程，不直接编辑 raw/

**触发条件**：用户有知识管理/检索需求时激活

**Skill**：`swarmvault/SKILL.md`

---
