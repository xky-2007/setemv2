# 讨论型多Agent协作 · 首次实战记录

## 基本信息

- 日期: 2026-04-26
- 任务: 个人作品集页面（测试任务）
- 任务ID: mission-001
- 参与Agent: 5个（clarifier / analyzer / matcher / planner / designer）
- 讨论消息数: 8条
- 收敛轮次: 1轮
- 状态文件: 5个（01~05）

---

## 讨论流程分析

### 发起讨论的时机

| Agent | 发起讨论的时机 | 讨论话题 |
|-------|-------------|---------|
| requirement_clarifier | 发现confidence < 0.8 | 需求模糊是否继续 |
| experience_matcher | 找到历史可借鉴项目 | 复用jxnu设计系统 |
| planner | 任务拆解后确认团队规模 | Builder要几个 |
| designer | 检测到讨论话题 | 技术方案选择 |

### 讨论类型分布

| type | 数量 | 说明 |
|------|------|------|
| question | 3 | 发起讨论/提问 |
| agreement | 2 | 同意对方观点 |
| suggestion | 3 | 提供建议 |

### 收敛过程

```
planner 提出问题 → designer 主持 → 3个Agent各发表意见 → 收敛
```

讨论触发条件（designer检测到planner的团队规模问题）正确识别。

---

## 关键发现

### 1. 讨论的触发条件

不是所有任务都需要讨论。触发条件：
- 需求模糊（clarifier confidence < 0.8）
- 方案分歧（不同Agent对实现方式有不同看法）
- 风险争议（某个风险被部分Agent忽视）
- 优先级冲突（资源/时间竞争）

### 2. 讨论收敛方式

第1轮直接收敛（3个建议全部采纳）：
- 单页HTML+GSAP 方案无异议
- SEO和鼠标光效是新增建议，被接受

没有触发第2、3轮投票或designer强制裁判。

### 3. 讨论消息的时效性

8条消息在Pipeline执行过程中连续写入，说明**文件驱动讨论是同步的**（不是等Pipeline完成后再讨论）。

---

## 经验教训

### 成功要素

1. **讨论有明确主持人**: designer作为主持，引导讨论并收敛
2. **各Agent视角不重叠**: clarifier关注用户、analyzer关注结构、matcher关注历史、planner关注可行性，视角互补
3. **收敛条件明确**: 3个共识点清晰记录

### 风险点

1. **讨论可能发散**: 如果designer不主动收敛，讨论可能无限延续
2. **文件IO开销**: 每次讨论都写文件，高频讨论场景可能有性能问题
3. **中文乱码**: PowerShell中文件名和内容中文字符显示有问题（但文件内容正确）

### 改进建议

1. **加讨论超时机制**: 单轮讨论超过N条消息后强制收敛
2. **加讨论消息队列**: Agent不直接写文件，而是写队列，由主持人统一处理
3. **加消息类型优先级**: objection必须回复，suggestion可选

---

## 技术细节

### 文件结构

```
projects/mission-001/
├── state/
│   ├── 01_clarified.json
│   ├── 02_analyzed.json
│   ├── 03_matched.json
│   ├── 04_planned.json
│   └── 05_designed.json
└── shared/
    └── discussions/
        ├── disc_001.json      # 8条消息
        ├── disc_002.json
        ├── ...
        └── round_1_summary.md  # 收敛结论
```

### 消息格式（最终验证）

```json
{
  "id": "disc_<agent>_<timestamp>",
  "from": "agent_id",
  "to": "target_agent_id 或 all",
  "topic": "讨论议题",
  "type": "question | objection | agreement | suggestion | warning",
  "message": "具体内容",
  "timestamp": "2026-04-26T11:19:40Z",
  "status": "open | resolved"
}
```

---

## 下次验证计划

- [ ] 在真实任务中验证讨论触发（不是测试任务）
- [ ] 测试"方案分歧"场景（让两个Agent对同一问题有相反观点）
- [ ] 测试第2、3轮收敛机制（强制投票）
- [ ] 测试reviewer参与讨论（质量评分分歧场景）

---

*来源: SETeam2 workspace 首次讨论协作测试 · 2026-04-26*
