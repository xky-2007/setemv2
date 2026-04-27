# Swarm Orchestration · 蜂群集群调度层

> 位于 SETeam2 执行引擎之上的调度层
> 版本：v1.0 · 2026-04-27
> 依赖：SETeam2 v2.1 + PROTOCOL v1.0

---

## 架构总览

```
用户复杂任务
    ↓
┌─────────────────────────────────────┐
│  Swarm Orchestration 调度层         │
│                                     │
│  swarm-master ──→ 任务拆解 + 调度    │
│       ↓                             │
│  task-queue ───→ 状态追踪 + 排序   │
│       ↓                             │
│  heartbeat-monitor ──→ 故障自愈     │
│       ↓                             │
│  workers ────→ N个SETeam2执行单元  │
│       ↓                             │
│  swarm-collector ──→ 结果汇总      │
└─────────────────────────────────────┘
    ↓
最终交付物
```

---

## 组件说明

| 组件 | 文件 | 职责 |
|------|------|------|
| **swarm-master** | `swarm-master.md` | 任务拆解 + 调度分配 + 执行监控 |
| **swarm-worker** | `workers/swarm-worker.md` | SETeam2 包装 + 状态上报 + 断点自愈 |
| **swarm-collector** | `swarm-collector.md` | 产出验收 + 结果合并 + 交付报告 |
| **heartbeat-monitor** | `heartbeat-monitor.md` | 进程监控 + 故障迁移 + 看门狗 |
| **task-queue-manager** | `task-queue-manager.md` | 任务分发 + 状态追踪 + 依赖排序 |

---

## 核心能力

| 能力 | 参数 |
|------|------|
| 最大并行 Worker | 8 |
| 单任务最大步数 | 4000 |
| 单任务最大超时 | 5天（120小时）|
| 心跳检测间隔 | 30秒 |
| 故障自愈 | 自动（最多3次迁移）|
| 断点保存 | 每50步 |

---

## 与 SETeam2 的关系

```
SETeam2：执行引擎（如何做）
Swarm Orchestration：调度层（谁先做谁后做）

用户任务 → Swarm 拆解 → SETeam2 执行 → 结果汇总
```

SETeam2 是底层执行单元，Swarm 是上层调度层。两者互补，不是替代关系。

---

## 目录结构

```
swarm-orchestration/
├── SKILL.md                    # 整体说明
├── README.md                   # 本文件
├── swarm-master.md             # 主控 Agent
├── swarm-collector.md         # 汇总 Agent
├── heartbeat-monitor.md        # 看门狗
├── task-queue-manager.md      # 队列管理
├── task-queue.json            # 任务队列（运行时生成）
└── workers/
    └── swarm-worker.md       # 执行单元模板

seteam workspace/
├── common/
│   └── PROTOCOL.md v1.0      # 7阶段协议
├── SETeam2/                   # 执行引擎
└── swarm-orchestration/      # 蜂群调度层（本目录）
```

---

## 快速开始

### 触发 Swarm

当遇到以下情况时，触发 Swarm Orchestration：
- 任务太复杂，需要多个领域同时工作
- 需要长时无人值守（> 2小时）
- 用户明确说"并发执行"

### 启动流程

```
1. swarm-master 接收任务
2. 任务分析 + WBS 拆解
3. 分配 Worker（每个子任务一个 Worker）
4. 启动所有 Worker（并行执行）
5. heartbeat-monitor 持续监控
6. Worker 完成后通知 swarm-collector
7. collector 汇总结果 + 生成交付报告
```

### 查看状态

运行时查看：
- `state/02_worker_status.json` — 各 Worker 实时状态
- `state/03_heartbeat_log.json` — 心跳历史
- `outputs/<swarm_id>/06_final_delivery/` — 最终交付物

---

## 配置参数

```json
{
  "swarm": {
    "max_workers": 8,
    "parallelism": "adaptive",
    "heartbeat_interval": 30,
    "max_execution_steps": 4000,
    "timeout_per_task_hours": 120,
    "auto_recovery": true,
    "checkpoint_interval": 50
  }
}
```

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v1.0 | 2026-04-27 | 初始版本 |

---

*Swarm Orchestration v1.0 · SETeam2 v2.1 蜂群调度层*