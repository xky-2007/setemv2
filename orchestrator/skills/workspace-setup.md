# Workspace Setup Guide

> 用途：orchestrator 编排工作区时的标准流程
> 版本：v1.0

## 使用方法

1. 接收 designer 的团队设计方案（05_designed.json）
2. 读取每个 Agent 的职责配置
3. 按本指南创建工作区目录和配置文件

## 标准目录结构

每个项目必须包含：

```
projects/
└── <project_id>/
    ├── state/                      # 状态文件
    │   ├── 00_mission.json        # 任务书
    │   ├── 01_clarified.json     # clarifier 产出
    │   ├── 02_analyzed.json      # analyzer 产出
    │   ├── 03_matched.json       # matcher 产出
    │   ├── 04_planned.json       # planner 产出
    │   ├── 05_designed.json      # designer 产出（含团队配置）
    │   ├── 06_orchestrated.json  # orchestrator 产出
    │   ├── 07_executed.json      # supervisor 产出
    │   ├── 08_reviewed.json      # reviewer 产出
    │   └── 09_lessons.json        # archivist 产出
    │
    ├── shared/                    # 共享资源
    │   ├── inputs/                # 外部输入
    │   ├── outputs/               # 最终产出（所有Agent共享）
    │   ├── discussions/           # 主流程讨论
    │   │   ├── inner_circle/     # 内圈讨论
    │   │   └── inner_draft.md   # 内圈收敛草案
    │   └── cache/                # 临时缓存
    │
    └── agents/                    # Agent 工作目录
        └── <agent_id>/
            ├── SOUL.md            # Agent 角色定义
            ├── config.json        # Agent 配置
            ├── memory/            # Agent 记忆
            └── outputs/           # Agent 私有产出
```

## 目录创建检查清单

- [ ] `state/` 已创建
- [ ] `shared/inputs/` 已创建
- [ ] `shared/outputs/` 已创建
- [ ] `shared/discussions/` 已创建
- [ ] `shared/discussions/inner_circle/` 已创建
- [ ] 每个 Agent 的 `agents/<agent_id>/` 已创建
- [ ] 每个 Agent 的 `SOUL.md` 已写入
- [ ] 每个 Agent 的 `config.json` 已写入

## config.json 模板

```json
{
  "agent_id": "<agent_id>",
  "role": "<role_name>",
  "model": {
    "provider": "minimax",
    "model_id": "MiniMax-M2",
    "temperature": 0.7
  },
  "workspace_dir": "projects/<project_id>/agents/<agent_id>",
  "input_schema": "<输入格式说明>",
  "output_schema": "<输出格式说明>",
  "dependencies": ["<前置Agent列表>"],
  "output_dir": "shared/outputs/"
}
```

## 路径冲突检查

创建目录时，必须检查：

1. **同名文件冲突**：检查 `shared/outputs/` 下是否有重名文件
2. **路径长度限制**：Windows 最大 260 字符，需注意
3. **中文目录**：避免使用中文目录名（可能导致编码问题）
4. **权限问题**：确保目录可写

## 环境验证

创建工作区后，必须验证：

1. 每个 Agent 可读自己的 `SOUL.md`
2. 每个 Agent 可写自己的 `outputs/`
3. 所有 Agent 可写 `shared/outputs/`
4. 所有 Agent 可读 `state/` 下的前置状态文件

## 产出清单

```markdown
## 工作区创建清单

### 目录结构
- [ ] state/ 已创建
- [ ] shared/inputs/ 已创建
- [ ] shared/outputs/ 已创建
- [ ] shared/discussions/ 已创建
- [ ] agents/ 已创建

### Agent 配置
- [ ] clarifier SOUL.md + config.json
- [ ] analyzer SOUL.md + config.json
- [ ] matcher SOUL.md + config.json
- [ ] planner SOUL.md + config.json
- [ ] designer SOUL.md + config.json
- [ ] orchestrator SOUL.md + config.json
- [ ] supervisor SOUL.md + config.json
- [ ] reviewer SOUL.md + config.json
- [ ] archivist SOUL.md + config.json

### 环境验证
- [ ] 所有 Agent 可读可写自己的目录
- [ ] shared/ 目录所有 Agent 可读写
- [ ] 无路径冲突
```
