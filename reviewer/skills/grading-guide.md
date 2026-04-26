# Independent Grading Guide

> 用途：reviewer 对每个Agent独立评分时的标准流程
> 版本：v1.0

## 评分维度（各25分，满分100）

| 维度 | 考核内容 |
|------|---------|
| 任务理解 | 是否准确理解需求；clarity 和 confidence 是否达标 |
| 产出完整性 | 产出文件是否完整；handoff 8字段是否齐全 |
| 流程规范性 | 是否遵循状态机；交接消息格式是否合规 |
| 交接质量 | next_actions 是否明确；接收方能否直接上手 |

## 评分标准

### 任务理解（25分）

| 分数 | 等级 | 描述 |
|------|------|------|
| 23-25 | 优秀 | 完全理解需求，confidence ≥ 0.85，无误解 |
| 19-22 | 良好 | 基本理解，confidence 0.7-0.85，有小遗漏但不影响 |
| 15-18 | 边缘 | 有部分误解，confidence 0.6-0.7，需要澄清 |
| < 15 | 不及格 | 误解需求，confidence < 0.6，产出与需求不符 |

### 产出完整性（25分）

| 分数 | 等级 | 描述 |
|------|------|------|
| 23-25 | 优秀 | 所有产出文件完整，handoff 8字段齐全 |
| 19-22 | 良好 | 文件完整，handoff 字段缺失 < 2 |
| 15-18 | 边缘 | 缺少部分文件或字段（2-3个） |
| < 15 | 不及格 | 核心产出缺失或格式错误 |

### 流程规范性（25分）

| 分数 | 等级 | 描述 |
|------|------|------|
| 23-25 | 优秀 | 完全遵循状态机，交接消息格式完全合规 |
| 19-22 | 良好 | 基本遵循，小格式问题（1-2处） |
| 15-18 | 边缘 | 有1-2处违反状态机的情况 |
| < 15 | 不及格 | 完全不遵循状态机流程 |

### 交接质量（25分）

| 分数 | 等级 | 描述 |
|------|------|------|
| 23-25 | 优秀 | next_actions 明确具体，接收方可立即执行 |
| 19-22 | 良好 | next_actions 基本清晰，有1-2处模糊 |
| 15-18 | 边缘 | next_actions 模糊，需要大量补充说明 |
| < 15 | 不及格 | 无交接或交接内容完全无法执行 |

## 评分输出格式

```json
{
  "agent": "<agent_id>",
  "score": <总分>,
  "breakdown": {
    "task_understanding": <分>,
    "output_completeness": <分>,
    "process_compliance": <分>,
    "handover_quality": <分>
  },
  "batna_check": {
    "status": "passed|violated",
    "details": "<BATNA检查详情>"
  },
  "hint": "<如果总分<80，需要生成改进hint>"
}
```

## Hint 生成规范（总分 < 80 时必须生成）

```markdown
## 改进 Hint

### 问题1：<具体问题描述>
- 来源：<哪个字段/哪个文件>
- 原因：<为什么出问题>
- 改进建议：<具体应该怎么做>

### 问题2：...
```

## BATNA 最低标准

| Agent | BATNA |
|-------|-------|
| clarifier | confidence ≥ 0.8，task_type 必填 |
| analyzer | parameters 结构完整，constraints 不为空 |
| matcher | 检索路径覆盖 templates/knowledge/projects/ |
| planner | workflow ≥ 2 phases，关键里程碑必填 |
| designer | team.roles ≥ 2，状态机必填 |
| orchestrator | shared/outputs/ 存在，scripts 语法正确 |
| supervisor | scores 4维度完整，加权计算正确 |
| reviewer | 每个Agent单独打分，hint 格式正确 |

## 评分决策

| 总分 | 决策 | 动作 |
|------|------|------|
| ≥ 90 | 优秀 | 通过，写入正面案例 |
| 80-89 | 通过 | 直接通过 |
| 75-79 | 边缘 | 通过，附改进建议（可选执行） |
| 60-74 | 警告 | 记录，不阻断 |
| < 60 | 回退 | 必须生成 hint，回退该 Agent（最多3次） |

## 升级人工条件

以下情况立即触发人工介入：

1. 同一 Agent 回退 ≥ 3 次仍 < 60 分
2. 任意 Agent 评分 < 30 分（严重误解需求）
3. reviewer 与 supervisor 评分差距 > 40 分
4. 流水线执行时间超过预期工时 3 倍
