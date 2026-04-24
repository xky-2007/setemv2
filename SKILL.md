---
name: seteam2-v2.1-extensions
description: SETeam2 v2.1 multi-agent workflow enhancements for OpenClaw. Includes brainstorming (STEP 0), Agent Handoff protocol, and cross-agent experience inheritance. Requires the base SETeam2 framework (8-agent pipeline). Use when handling complex multi-step tasks that need structured agent collaboration.
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: []
    install: []
version: "2.1.0"
author: "xky"
homepage: "https://github.com/xky/seteam2-v2.1-extensions"
tags: [multi-agent, workflow, pipeline, orchestration, seteam2, brainstorming, handoff]
---

# SETeam2 v2.1 Extensions

> 头脑风暴 + Handoff协议 + 经验传承

## v2.1 新增特性

| 特性 | Agent | 说明 |
|------|-------|------|
| STEP 0 头脑风暴 | planner | 每次任务规划前强制发散思考5问 |
| Agent Handoff 协议 | orchestrator | 强制交接规范 + 通信格式 |
| 跨Agent经验传承 | supervisor | 每次任务写 execution_lessons.md |

## 使用前提

本扩展**依赖 SETeam2 基础框架**（8个Agent）。请先获取 SETeam2 完整数据包，然后将本扩展的 `agents/` 覆盖到对应位置。

## 加载路径

- 头脑风暴规范：`agents/planner/SOUL.md` → 第5节 STEP 0
- Handoff 协议：`agents/orchestrator/SOUL.md` → 第4节
- 经验传承：`agents/supervisor/SOUL.md` → 第9节
- 完整流水线：`WORKFLOW.md`

## SwarmClaw 扩展

- **SwarmDock**：P2P投标/接单/赚USDC
- **SwarmVault**：知识图谱/检索
- **summarize**：URL/文件/YouTube 摘要
- **coding-agent**：编码委托
- **github**：GitHub 操作

详见 `SWARM_INTEGRATION.md`
