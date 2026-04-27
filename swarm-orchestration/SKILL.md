# Swarm Orchestration Skill

> 蜂群集群调度层 · 基于 SETeam2 v2.1 · 与 PROTCOL v1.0 协同工作
> 版本：v1.0 · 2026-04-27

## Identity

Swarm Orchestration 是 OpenClaw 的**蜂群调度层**，位于 SETeam2 执行引擎之上。

它的核心职责：
1. 接收复杂任务，拆解为可并行的子任务
2. 调度多个 SETeam2 执行单元并行工作
3. 监控子任务状态，处理故障自愈
4. 汇总所有子任务产出，输出最终交付物

**与 SETeam2 的关系：**
- SETeam2 是执行引擎（如何做）
- Swarm Orchestration 是调度层（谁先做谁后做）
- 两者互补：Swarm → SETeam2 → 结果 → Swarm汇总

---

## Architecture

```
用户复杂任务
    ↓
【swarm-master】主控 Agent
    ↓ 任务拆解 + WBS
【swarm-workers】N个执行单元（每个都是 SETeam2）
    ↓ 并行执行各自的子任务
【swarm-collector】结果汇总 Agent
    ↓
最终交付物
```

---

## 核心组件

| 组件 | 文件 | 职责 |
|------|------|------|
| 主控 | `swarm-master.md` | 任务拆解、调度、监控 |
| 执行单元 | `workers/swarm-worker.md` | SETeam2 包装、状态上报 |
| 汇总 | `swarm-collector.md` | 结果验收、合并、输出 |
| 看门狗 | `heartbeat-monitor.md` | 进程监控、故障自愈 |
| 任务队列 | `task-queue.json` | 任务分发、状态追踪 |

---

## 触发条件

以下情况触发 Swarm Orchestration：

- 用户任务**无法由单一 SETeam2 完成**（太复杂/范围太广）
- 用户明确说"并发执行"、"多个任务同时做"
- 任务涉及**多个领域**（前端+后端+设计+文案同时需要）
- 任务需要**长时无人值守**（> 2小时）

---

## 不适用场景

- 单一清晰任务（直接用 SETeam2，不需要 Swarm）
- 实时对话/简单问答（Swarm 启动开销不划算）
- 用户要求逐个确认每一步（Swarm 是无人值守模式）

---

## 工作流程

### Phase 1：任务分析（swarm-master）

```
输入：用户复杂任务描述
输出：任务拆解方案 + worker 数量 + 并行策略
```

1. 读取任务，理解目标和约束
2. WBS 分解为独立的子任务
3. 分析子任务间的依赖关系
4. 决定并行度（多少 worker 同时启动）
5. 生成任务分配方案

### Phase 2：任务分发（swarm-master → workers）

```
输入：任务分配方案
输出：每个 worker 收到独立任务包
```

1. 为每个 worker 创建独立工作区
2. 分配任务 + 约束 + 验收标准
3. 启动 worker，开始执行
4. 监控心跳，发现故障立即迁移

### Phase 3：执行监控（heartbeat-monitor）

```
状态：持续监控所有 worker
故障：进程崩溃 → 任务迁移
超时：超过预估 → 告警/回收
完成：产出就绪 → 通知 collector
```

### Phase 4：结果汇总（swarm-collector）

```
输入：所有 worker 的产出
输出：最终交付物
```

1. 收集所有 worker 的产出
2. 验收每项产出（完整性/准确性）
3. 处理冲突（同一产出多个版本）
4. 合并为最终交付物
5. 生成交付报告

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

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_workers | 8 | 最多同时运行的 worker 数量 |
| heartbeat_interval | 30s | 心跳检测间隔 |
| max_execution_steps | 4000 | 单 worker 最大执行步数 |
| timeout_per_task_hours | 120 | 单任务最大超时（5天） |
| auto_recovery | true | 故障自动迁移 |
| checkpoint_interval | 50 | 断点保存间隔（每50步） |

---

## 输出格式

所有产出写入 `swarm-orchestration/outputs/<swarm_id>/`

```
swarm-orchestration/
└── outputs/
    └── <swarm_id>/
        ├── 00_swarm_manifest.json    # 整体任务描述
        ├── 01_task_breakdown.json    # 任务拆解方案
        ├── 02_worker_status.json    # 各 worker 状态
        ├── 03_heartbeat_log.json    # 心跳记录
        ├── 04_results/              # 各 worker 产出
        │   ├── worker_001/
        │   ├── worker_002/
        │   └── ...
        ├── 05_collector_report.md   # 汇总报告
        └── 06_final_delivery/       # 最终交付物
            └── <最终交付文件>
```

---

## 使用示例

用户：
> 帮我做一个完整的品牌官网，包含前端页面、后端API、运维部署脚本、宣传文案，一周内交付

swarm-master 分析：
- 前端页面 → worker_001 (SETeam2)
- 后端API → worker_002 (SETeam2)
- 运维脚本 → worker_003 (SETeam2)
- 宣传文案 → worker_004 (SETeam2)
- 并行度：4

swarm-collector 汇总：
- 前端页面（完成）
- 后端API（完成）
- 部署脚本（完成）
- 宣传文案（完成）
- 最终交付：`品牌官网完整项目.zip`

---

## 依赖关系

- 依赖 SETeam2 v2.1 执行单元
- 依赖 `common/PROTOCOL.md` v1.0
- 依赖各 Agent 的 skills（planner/wbs-task-decomposition.md 等）

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v1.0 | 2026-04-27 | 初始版本，支持8并行+故障自愈+断点续传 |

---

*Swarm Orchestration v1.0 · 需要配合 SETeam2 v2.1 + PROTOCOL v1.0 使用*