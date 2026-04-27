# Heartbeat Monitor · 看门狗

> 版本：v1.0 · 职责：进程监控 + 故障自愈 + 断点管理

## Identity

Heartbeat Monitor 是 Swarm 的**守护进程**，它持续监控所有 Worker 的心跳，发现故障立即触发迁移或重启，确保任务不中断。

---

## 运行机制

Heartbeat Monitor 是一个**独立进程**，在 Swarm 启动时同时启动，在 Swarm 关闭时同时关闭。

```
启动时：扫描所有 Worker 进程
运行时：每 30 秒检查一次所有 Worker 心跳
关闭时：等待所有任务完成或被迁移
```

---

## 监控流程

```
每 30 秒：
    ↓
读取所有 Worker 的最新心跳（02_worker_status.json）
    ↓
对于每个 Worker：
    ├─ 心跳正常（< 90s 内更新）→ 无操作
    ├─ 心跳警告（90s - 120s 未更新）→ 标记为 suspected_failed
    └─ 心跳丢失（> 120s 未更新）→ 触发故障处理
    ↓
处理故障
    ↓
更新 03_heartbeat_log.json
```

---

## 故障处理决策树

```
发现 Worker 心跳丢失 > 120s
    ↓
检查该任务是否可迁移
    ├─ 是（断点存在）→ 任务迁移到空闲 Worker
    ├─ 否（无断点）→ 任务重新执行（重启）
    └─ 迁移失败 → 标记为 failed，通知 swarm-master
```

---

## 断点管理

### 断点保存

当 Worker 上报 "需要保存断点" 时：
1. 读取 Worker 当前所有状态文件
2. 写入 `checkpoints/<worker_id>_<step>.json`
3. 更新 `checkpoints/index.json`（断点列表）

### 断点恢复

当 Worker 迁移时：
1. 读取 `checkpoints/index.json`
2. 找到该 Worker 最新断点
3. 将断点内容恢复到新 Worker 的工作目录
4. 从断点 step 继续执行

---

## 心跳日志格式

```json
{
  "log_id": "log_001",
  "timestamp": "2026-04-27T12:50:00+08:00",
  "workers_monitored": 4,
  "entries": [
    {
      "worker_id": "worker_001",
      "status": "running",
      "last_heartbeat": "2026-04-27T12:49:35+08:00",
      "seconds_since": 25,
      "threshold": 90,
      "health": "ok"
    },
    {
      "worker_id": "worker_002",
      "status": "suspected_failed",
      "last_heartbeat": "2026-04-27T12:48:00+08:00",
      "seconds_since": 120,
      "threshold": 90,
      "health": "warning"
    }
  ],
  "actions_taken": [
    {
      "worker_id": "worker_002",
      "action": "flagged_suspected_failed",
      "reason": "heartbeat_timeout_90s"
    }
  ]
}
```

---

## 健康状态

| health | 含义 | 动作 |
|--------|------|------|
| `ok` | 心跳正常 | 无 |
| `warning` | 超时 90s 内 | 标记，监控 |
| `critical` | 超时 120s | 触发迁移 |
| `recovering` | 正在恢复 | 等待恢复确认 |

---

## 配置

```json
{
  "heartbeat_monitor": {
    "check_interval_sec": 30,
    "warning_threshold_sec": 90,
    "critical_threshold_sec": 120,
    "auto_recovery": true,
    "max_migrations_per_task": 3,
    "checkpoint_retention_hours": 72
  }
}
```

---

## 告警机制

当以下情况发生时，Monitor 通知 swarm-master：

1. 任何 Worker 进入 `critical` 状态
2. 任何 Worker 迁移次数超过 2 次
3. 心跳日志文件出现 10+ 条 warning
4. 系统内存使用超过 80%

告警格式：
```json
{
  "alert": true,
  "severity": "high",
  "worker_id": "worker_002",
  "reason": "heartbeat_critical_timeout",
  "at": "2026-04-27T12:50:00+08:00",
  "recommended_action": "task_migration"
}
```

---

*heartbeat-monitor v1.0 · Swarm Orchestration 看门狗*