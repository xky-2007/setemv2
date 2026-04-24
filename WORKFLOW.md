# 工作流协作机制 · SETeam2 v2.0

> 基于 SETeam2 八步流水线 + xky agent 原有经验体系融合

---

## 一、任务发起

用户向主控发送任务 → 创建 `projects/<team_id>/state/input.txt` + `flow.json`

```json
{
  "flowId": "<team_id>",
  "owner": "main-session",
  "goal": "用户需求描述",
  "status": "pending",
  "created": "ISO时间戳"
}
```

---

## 二、八步流水线详解

### Step ① · requirement_clarifier — 需求澄清

**输入**：`input.txt`（用户原始需求）
**输出**：`01_clarified.json`

**任务**：
- 判断任务类型：`query | creation | analysis | booking | custom`
- 提取核心目标、初步关键参数
- 识别明显约束
- 标注待确认项（置信度 < 0.6 时暂停流水线）

**状态**：`clarified`

---

### Step ② · requirement_analyzer — 需求分析

**前置**：`01_clarified.json` status = `clarified`
**输出**：`02_analyzed.json`

**任务**：
- 深度结构化分析：子目标 / 关键参数体系 / 约束条件 / 验收标准
- 评估复杂度：`low | medium | high`
- 验收标准必须可测试、可验证

**状态**：`analyzed`

---

### Step ③ · experience_matcher — 经验匹配

**前置**：`02_analyzed.json` status = `analyzed`
**输出**：`03_matched.json`

**匹配度计算**：

| 维度 | 权重 |
|------|------|
| 任务类型相似度 | 30% |
| 复杂度匹配 | 25% |
| 领域重叠度 | 25% |
| 约束条件重合度 | 20% |

**决策阈值**：

| 匹配度 | 决策 |
|--------|------|
| ≥ 80% | **复用 (reuse)** |
| 60%–80% | **微调 (adjust)** |
| < 60% | **从零设计 (new_design)** |

**状态**：`matched`

---

### Step ④ · planner — 流程规划

**前置**：`03_matched.json` status = `matched`
**输出**：`04_planned.json`

**新增：STEP 0 头脑风暴（强制）**：
- 每次任务规划前，必须先发散思考5个问题（不保存，仅内部参考）
- 解法路径 / 忽略的风险 / 与历史的差异 / 时间压缩时牺牲点 / 协作卡点

**任务**：
- 阶段划分 + 任务分解（WBS）
- 识别并行任务组
- 设定关键里程碑 + 风险点
- 估算总工时

**输出格式**：
```json
{
  "status": "planned",
  "流程图": "Mermaid格式",
  "阶段": [{"阶段ID": "PHASE_1", "任务": [...] }],
  "并行任务组": [["T1.1", "T1.2"]],
  "关键里程碑": [...],
  "风险点": [...]
}
```

---

### Step ⑤ · designer — AI团队设计

**前置**：`04_planned.json` status = `planned`
**输出**：`05_designed.json`

**任务**：
- 根据流程规划，设计完成该任务所需的AI团队
- 定义每个Agent的：角色名 / 核心任务 / 模型配置 / 技能要求 / 工作边界
- **约束**：Agent总数 ≤ 8，不得职责重叠

**状态**：`designed`

---

### Step ⑥ · orchestrator — 团队编排

**前置**：`05_designed.json` status = `designed`
**输出**：`06_orchestrated.json`

**新增：团队协作规范（强制）**：
- **Handoff 协议**：每个 Agent 完成后必须写 `shared/outputs/` + `memory/execution_log.md`
- **交接消息格式**：必须包含 from/to/task_id/input_summary/output_summary/confidence/issues/next_actions
- **Review 工作流**：子任务→supervisor评分 / 阶段→designer评审 / 全部→supervisor汇总

**任务**：
- 创建工作目录结构
- 为每个Agent生成 `SOUL.md` + `config.json`
- 填写 `config.json` + `workflow.json`

**状态**：`orchestrated`

---

### Step ⑦ · supervisor — 调度执行 + 验收

**前置**：`06_orchestrated.json` + `config.json` + `workflow.json`
**输出**：`07_executed.json`

**评分维度**：

| 维度 | 权重 |
|------|------|
| 完整性 | 30% |
| 准确性 | 30% |
| 可执行性 | 25% |
| 规范性 | 15% |

**门控规则**：

| 评分 | 决策 |
|--------|------|
| ≥ 80 | ✅ 直接通过 |
| 60–80 | ⚠️ 有改进空间，记录后继续 |
| < 60 | 🔄 回退（最多3次） |

**回退逻辑**：
```
评分 < 60 → 回退次数+1 → 
  回退次数 ≤ 3：发回退信号给 requirement_clarifier，从①重新开始
  回退次数 > 3：终止流水线，status = "failed"
```

**跨Agent经验传承（新增）**：
- 每次任务完成后，supervisor 必须写入 `teams/{team_id}/memory/execution_lessons.md`
- 记录成功要素(≥2) + 风险点(≥1) + 改进建议(≥1)
- matcher 下次运行时优先检索 lessons，避免重复踩坑

**状态**：`completed | partial | failed`

---

### Step ⑧ · archivist — 经验沉淀

**前置**：`07_executed.json` status = `completed` 且评分 ≥ 60
**输出**：写入 `xky agent/knowledge/` + `xky agent/templates/`

**任务**：
- 复盘全流程，提炼成功要素 + 风险点 + 改进建议
- 生成结构化经验文档
- 更新 `knowledge/index.json`
- **同时**：识别可模板化的流程，写入 `templates/`

**状态**：`completed`

---

## 三、经验匹配检索路径

Step③ 执行时，自动检索以下路径：

```
xky agent/templates/                   ← 模板库
xky agent/knowledge/entries/           ← 历史经验文档
xky agent/projects/<已完成项目>/      ← 历史项目归档
```

---

## 四、异常处理

| 情况 | 处理 |
|------|------|
| Step① 置信度 < 0.6 | 列出缺失信息，暂停流水线 |
| Step⑦ 评分 < 60 | 触发回退信号 |
| 回退次数 > 3 | 终止流水线 |
| 任意Step失败 | 停止流水线，标记 `failed` |

---

## 五、与原有体系的融合

| 原有组件 | 融合方式 |
|---------|---------|
| `agent-worker.js` | 作为 Tooler Agent 的执行引擎 |
| `templates/` | Step③ 经验匹配时自动检索 |
| `knowledge/` | Step⑧ 归档时写入；Step③ 匹配时检索 |
| `projects/` | 扩展为标准 SETeam2 工作区结构 |
