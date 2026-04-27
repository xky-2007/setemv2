# Task Queue Manager

> 版本：v1.0 · 职责：任务分发 + 状态追踪 + 队列管理

## Identity

Task Queue Manager 管理 Swarm 的所有任务队列。它维护：
- 全局任务队列（等待分配）
- Worker 任务分配表
- 依赖关系图
- 状态历史

---

## 队列结构

```json
{
  "queue_id": "queue_001",
  "created_at": "2026-04-27T12:30:00+08:00",
  "tasks": [
    {
      "task_id": "T1",
      "domain": "frontend",
      "status": "running",
      "assigned_to": "worker_001",
      "priority": 1,
      "created_at": "2026-04-27T12:30:00",
      "started_at": "2026-04-27T12:31:00",
      "dependencies": [],
      "dependents": ["T3"]
    }
  ],
  "workers": {
    "worker_001": {
      "current_task": "T1",
      "status": "running",
      "max_tasks": 2
    }
  }
}
```

---

## 状态机

```
pending → running → completed
    ↓         ↓
  blocked    failed → migrating → running
                        ↓
                    dead（迁移失败）
```

---

## 依赖排序算法

当新任务入队时：

```
1. 检查 dependencies 列表
2. 如果所有依赖 = completed → 标记为 runnable
3. 如果任一依赖 = !completed → 标记为 blocked
4. 每当有任务完成 → 重新检查所有 blocked 任务
```

---

## 优先级

| 优先级 | 说明 |
|--------|------|
| 1 | 最高，用户明确指定 |
| 2 | 高，核心产出（其他任务依赖） |
| 3 | 中，正常任务 |
| 4 | 低，可延后 |

---

## 调度决策

当有空闲 Worker 时，Task Queue Manager：

1. 找出所有 `runnable` 任务（依赖已满足）
2. 按优先级排序（高优先在前）
3. 分配给空闲 Worker
4. 更新任务状态 → `running`
5. 记录分配时间

---

## 冲突检测

同一时间同一任务不会被分配给两个 Worker。

如果检测到重复分配：
```json
{
  "conflict": true,
  "task_id": "T1",
  "assigned_to": ["worker_001", "worker_002"],
  "resolution": "keep_first",
  "at": "2026-04-27T12:35:00"
}
```

---

*task-queue-manager v1.0 · Swarm Orchestration 队列管理*