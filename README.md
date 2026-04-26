# seteam workspace · SETeam2 多Agent协作工作区

> 每个 Agent 拥有独立 workspace，通过文件驱动协作

---

## 目录结构

```
seteam workspace/
│
├── README.md                    # 本文件
│
├── requirement_clarifier/       # ① 需求澄清专家
│   ├── SOUL.md                  # Agent灵魂
│   ├── memory/                  # Agent记忆
│   ├── skills/                  # Agent技能
│   ├── tasks/                  # 待处理任务
│   └── outputs/                # 产出文件
│
├── requirement_analyzer/        # ② 需求分析专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── experience_matcher/         # ③ 经验匹配专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── planner/                    # ④ 流程规划专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── designer/                   # ⑤ AI团队设计专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── orchestrator/               # ⑥ 团队编排专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── supervisor/                 # ⑦ 调度执行专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── reviewer/                   # ⑧ 独立评分专家 [v2.1新增]
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
├── archivist/                  # ⑨ 经验沉淀专家
│   ├── SOUL.md
│   ├── memory/
│   ├── skills/
│   ├── tasks/
│   └── outputs/
│
└── common/                     # 共享资源
    ├── templates/              # 模板库
    ├── knowledge/             # 知识库
    └── workflows/              # 工作流配置
```

---

## 流水线

```
用户需求
   │
   ▼
① requirement_clarifier  ──→ 01_clarified.json
   │
   ▼
② requirement_analyzer   ──→ 02_analyzed.json
   │
   ▼
③ experience_matcher     ──→ 03_matched.json
   │
   ▼
④ planner               ──→ 04_planned.json
   │
   ▼
⑤ designer              ──→ 05_designed.json
   │
   ▼
⑥ orchestrator         ──→ 06_orchestrated.json + 工作区
   │
   ▼
⑦ supervisor            ──→ 07_executed.json
   │
   ▼
⑧ reviewer             ──→ 08_reviewed.json + hints
   │
   ▼
⑨ archivist            ──→ knowledge/entries/
```

---

## 协作规则

1. **每个 Agent 独立 workspace**，通过状态文件交接
2. **依赖驱动**：下游 Agent 轮询等待上游 done 信号
3. **reviewer 独立评分**：每个 Agent 产出单独打分，不通过则回退
4. **回退 ≤ 3 次**：超过则升级人工
5. **经验传承**：archivist 沉淀 lessons 供 matcher 检索

---

## 版本

- SETeam2 v2.1
- 2026-04-26
