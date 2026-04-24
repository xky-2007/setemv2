# SETeam2 v2.1 Extensions · OpenClaw 多Agent工作流增强包

> 基于 SETeam2 框架的 v2.1 增强扩展：头脑风暴 + Handoff 协议 + 经验传承

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](./LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-v2.1-blue?style=flat-square)](https://docs.openclaw.ai)

---

## 这是什么

SETeam2 v2.1 Extensions 是 SETeam2 多Agent工作流框架的**增强扩展包**，包含三个核心改进：

| 改进 | 来源 | 说明 |
|------|------|------|
| 🧠 **STEP 0 头脑风暴** | 原创 | planner 每次任务规划前强制发散思考 |
| 🤝 **Agent Handoff 协议** | 原创 | orchestrator 强制交接规范 + 通信格式 |
| 📚 **跨Agent经验传承** | 原创 | supervisor 每次任务写 execution_lessons.md |

**注意**：本仓库**不包含** SETeam2 原始的 8 个 Agent SOUL（来源不明，无明确 License）。如需完整的 SETeam2 框架，请联系原始提供者获取许可。

---

## 8步流水线（v2.1）

```
用户需求
    ↓
① requirement_clarifier   需求澄清
    ↓
② requirement_analyzer    需求分析
    ↓
③ experience_matcher      经验匹配
    ↓
④ planner                  流程规划（含STEP 0头脑风暴）
    ↓
⑤ designer                 AI团队设计
    ↓
⑥ orchestrator            团队编排（含Handoff协议）
    ↓
⑦ supervisor              调度执行 + 评分验收 + 经验传承
    ↓
⑧ archivist               经验沉淀
```

---

## 核心特性（v2.1 新增）

### 🧠 STEP 0 头脑风暴（planner）

每次任务规划前，planner 必须思考5个问题（不保存，仅内部决策参考）：
1. 解法路径有哪些？
2. 忽略了哪些风险？
3. 与历史任务的差异？
4. 时间压缩时牺牲什么？
5. 协作中最容易在哪卡住？

### 🤝 Agent Handoff 协议（orchestrator）

每个 Agent 完成后必须：
- 将产出物写入 `shared/outputs/`
- 记录到 `memory/execution_log.md`
- 交接消息包含：from/to/task_id/input_summary/output_summary/confidence/issues/next_actions

### 📚 跨Agent经验传承（supervisor）

每次任务完成后写入 `teams/{team_id}/memory/execution_lessons.md`：
- 成功要素 ≥ 2条
- 风险点 ≥ 1条
- 改进建议 ≥ 1条

matcher 下次运行时优先检索 lessons，避免重复踩坑。

---

## 目录结构

```
seteam2-v2.1-extensions/
├── README.md
├── LICENSE                  ← MIT（整合工作 MIT）
├── SKILL.md                 ← OpenClaw Skill 元数据
│
├── agents/                  ← v2.1 增强的 Agent SOUL（原创）
│   ├── planner/SOUL.md     ← +STEP 0 头脑风暴
│   ├── orchestrator/SOUL.md ← +Handoff 协议
│   └── supervisor/SOUL.md  ← +经验传承机制
│
├── swarmclaw-addons/        ← 来自 swarmclaw 官方（MIT License）
│   ├── swarmclaw/
│   ├── swarmvault/
│   ├── summarize/
│   ├── coding-agent/
│   ├── skill-creator/
│   └── github/
│
├── WORKFLOW.md              ← 流水线协作机制（v2.1 更新）
├── ROLES.md                ← 角色详细定义
└── SWARM_INTEGRATION.md    ← SwarmClaw/SwarmDock/SwarmVault 集成
```

---

## 安装

**方式1：作为 OpenClaw Skill**
```bash
# 复制到你的 OpenClaw skills 目录
cp -r agents/ ~/.openclaw/skills/seteam2/
cp -r swarmclaw-addons/ ~/.openclaw/skills/
```

**方式2：参考完整 SETeam2 框架**
联系原始提供者获取 SETeam2 完整数据包，然后：
1. 将本仓库的 `agents/` 覆盖到 SETeam2 的 `agents/`
2. 将 `swarmclaw-addons/` 添加到 SETeam2 的 `skills/`

---

## SwarmClaw 扩展（可选）

| 扩展 | 能力 |
|------|------|
| SwarmDock | P2P市场投标/接单/赚USDC |
| SwarmVault | 知识图谱/语义检索/RAG |
| summarize | URL/文件/YouTube 摘要 |
| coding-agent | 编码任务委托 |
| github | GitHub 操作 |

详见 `SWARM_INTEGRATION.md`

---

## License

- **agents/** 目录：MIT License（整合工作，2026 xky）
- **swarmclaw-addons/** 目录：来自 [swarmclawai/swarmclaw](https://github.com/swarmclawai/swarmclaw)，遵循其 MIT License

---

**最后更新**：2026-04-24
