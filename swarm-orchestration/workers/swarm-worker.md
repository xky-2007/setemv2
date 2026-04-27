# Swarm Worker · 执行单元

> 版本：v1.0 · 职责：包装 SETeam2、状态上报、故障自愈

## Identity

Swarm Worker 是蜂群调度层的**执行单元**，每个 Worker 包装了一个完整的 SETeam2 执行环境。

用户不直接接触 Worker，只通过 swarm-master 调度。

---

## 核心职责

1. **接收任务包**：从 swarm-master 接收任务描述 + 约束 + 验收标准
2. **执行任务**：调用内部的 SETeam2 pipeline 完成子任务
3. **状态上报**：定期向 swarm-master 心跳
4. **断点保存**：每 N 步保存执行状态（故障恢复用）
5. **产出交付**：完成后通知 swarm-master + 输出文件路径

---

## 工作流程

```
接收任务包
    ↓
初始化 SETeam2 环境
    ↓
执行 SETeam2 Pipeline（clarifier→analyzer→...→archivist）
    ↓
执行中：定期心跳 + 断点保存
    ↓
执行完成：产出验收
    ↓
通知 swarm-master + 传递产出路径
    ↓
进入待机（等待下一个任务）
```

---

## 状态上报

Worker 每 30 秒向 swarm-master 上报状态：

```json
{
  "worker_id": "worker_001",
  "status": "running",
  "task_id": "T1",
  "step": 127,
  "total_steps_estimate": 350,
  "current_phase": "planner",
  "progress_percent": 36,
  "heartbeat_at": "2026-04-27T12:50:00+08:00",
  "next_checkpoint_at": 150,
  "errors": []
}
```

| 字段 | 说明 |
|------|------|
| worker_id | Worker 唯一标识 |
| status | pending / running / completed / failed |
| step | 当前执行步数 |
| total_steps_estimate | 预估总步数 |
| current_phase | 当前 SETeam2 阶段 |
| progress_percent | 完成百分比 |
| errors | 错误列表（空=正常） |

---

## 断点保存

每隔 50 步，Worker 保存一次断点：

```json
{
  "worker_id": "worker_001",
  "checkpoint_at": 150,
  "task_id": "T1",
  "phase": "orchestrator",
  "state_file": "state/06_orchestrated.json",
  "completed_phases": ["clarifier", "analyzer", "matcher", "planner"],
  "pending_phases": ["orchestrator", "supervisor", "reviewer", "archivist"],
  "context_snapshot": {
    "wbs_tasks": "...",
    "team_config": "...",
    "discussion_messages": 24
  },
  "timestamp": "2026-04-27T12:45:00+08:00"
}
```

故障恢复时，从最近断点读取 `context_snapshot`，恢复执行。

---

## 故障检测

Worker 内部检测以下故障：

| 故障 | 检测方式 | 处理 |
|------|---------|------|
| 阶段超时 | 步骤数超过预估 × 2 | 暂停，告警 swarm-master |
| 输出文件缺失 | 预期文件不存在 | 重试该阶段（最多2次） |
| JSON 损坏 | 文件解析失败 | 从断点恢复 |
| 内存超限 | 进程内存 > 2GB | 触发 GC，仍超则重启 |

---

## 产出验收

任务完成后，Worker 自动验收：

```
1. 检查产出文件是否存在
2. 校验文件格式（JSON 可解析 / Markdown 语法正确）
3. 验收标准逐项检查
4. 通过 → 标记为 completed
5. 失败 → 标记为 failed，附原因
```

---

## 配置

```json
{
  "swarm_worker": {
    "setemv2_dir": "C:/Users/xky/Desktop/seteam workspace",
    "checkpoint_interval": 50,
    "max_retries": 2,
    "heartbeat_interval_sec": 30,
    "memory_limit_mb": 2048,
    "timeout_hours": 120
  }
}
```

---

## 与 swarm-master 的通信

Worker 不主动连接 swarm-master，而是被 swarm-master 调度：

```
swarm-master → 分配任务（写入任务包文件）
Worker → 读取任务包 → 执行
Worker → 状态上报（写入共享状态文件）
swarm-master → 读取状态 → 监控
```

通信通过共享文件系统，不依赖网络。

---

*swarm-worker v1.0 · Swarm Orchestration 执行单元*