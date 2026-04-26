# 讨论能力扩展 · 所有Agent共享规范

> 当某个Agent在 `common/discussions/` 发起或收到讨论消息时，按本规范执行。

---

## 讨论参与规则

### 1. 收到讨论消息时

当自己的 `inbox` 里收到讨论通知，必须：
- 阅读涉及自己视角的问题
- 在 `common/discussions/` 写回复（用自己视角的立场）
- 标注 `status: resolved` 或 `status: open`

### 2. 发起讨论时

当自己发现以下情况，必须主动发起讨论：
- 自己的视角发现其他 Agent 忽视的风险
- 对其他 Agent 的方案有质疑
- 需要其他视角补充信息

### 3. 讨论消息格式

```json
{
  "id": "disc_XXX",
  "from": "agent_id",
  "to": "target_agent_id 或 all",
  "topic": "讨论议题",
  "type": "question | objection | agreement | suggestion | warning",
  "message": "具体内容",
  "timestamp": "2026-04-26T19:00:00Z",
  "status": "open",
  "my_viewpoint": "你的视角是什么"
}
```

### 4. 讨论轮次

- 第1轮：各方发表观点
- 第2轮：回应质疑，形成初步共识
- 第3轮：投票或designer裁判强制收敛

### 5. 收敛写入

收敛后，designer 写入 `common/discussions/round_<N>_summary.md`：
```
## 结论
- [结论1]
- [结论2]

## 未解决（可选）
- [遗留问题]
```

---

## 各Agent讨论视角速查

| Agent | 视角 | 讨论时必问 |
|-------|------|-----------|
| requirement_clarifier | 用户意图 | "用户真正想要的是什么？有哪些没说出口的？" |
| requirement_analyzer | 需求结构 | "这个需求完整吗？验收标准清晰吗？" |
| experience_matcher | 历史经验 | "有没有类似案例可以借鉴？" |
| planner | 任务可行 | "这个计划能完成吗？风险在哪里？" |
| designer | 团队设计 | "这个团队设计合理吗？" |
| orchestrator | 执行落地 | "工作区准备好了吗？" |
| supervisor | 质量门控 | "质量达标了吗？" |
| reviewer | 评分公正 | "评分标准一致吗？" |
| archivist | 知识沉淀 | "这次学到了什么？" |
