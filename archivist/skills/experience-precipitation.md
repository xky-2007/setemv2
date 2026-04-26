# Experience Precipitation Guide

> 用途：archivist 在任务结束后沉淀经验的标准流程
> 位置：archivist/skills/experience-precipitation.md

## 使用方法

每个任务执行完毕后，archivist 必须：

1. 读取任务的所有讨论记录和产出文件
2. 按本模板提炼经验
3. 写入 `knowledge/entries/YYYY-MM-DD-<task-type>.md`
4. 更新 `templates/` 中的可复用模板
5. 更新 `knowledge/index.json`

## 沉淀检查清单

任务完成后，必须确认：

- [ ] **成功要素** ≥ 2条
- [ ] **风险点** ≥ 1条
- [ ] **改进建议** ≥ 1条
- [ ] **可模板化的内容** 已识别
- [ ] **写入知识库**
- [ ] **更新 index.json**

## 经验文档模板

```markdown
# [任务类型] 经验沉淀

> 日期：YYYY-MM-DD
> 任务：<任务名称>
> 难度：低/中/高
> 评分：XX/100

## 任务概述

<用3-5句话描述这个任务是什么>

## 成功要素（≥2条）

1. **<要素名称>**
   <具体描述为什么这个要素有效>
   来源：讨论记录 disc_XXX.json

2. **<要素名称>**
   <具体描述>
   来源：讨论记录 disc_XXX.json

## 风险点（≥1条）

1. **<风险描述>**
   - 风险级别：高/中/低
   - 来源：讨论记录 disc_XXX.json
   - 预防措施：<如果有的话>

## 改进建议（≥1条）

1. **<建议描述>**
   <具体应该怎么做>
   来源：supervisor/reviewer 反馈

2. **<建议描述>**
   <具体应该怎么做>

## 可模板化的内容

| 内容 | 模板位置 | 适用场景 |
|------|---------|---------|
| <内容> | templates/...md | <场景> |

## 关键讨论记录

- disc_XXX.json：<描述>
- disc_XXX.json：<描述>

## 下次参考

下次遇到类似任务时，应该：
1. <action 1>
2. <action 2>
3. <action 3>
```

## index.json 更新规范

每次写入新经验后，必须更新：

```json
{
  "last_updated": "YYYY-MM-DD",
  "entries": [
    {
      "id": "YYYY-MM-DD-<task-type>",
      "title": "<任务类型>经验沉淀",
      "date": "YYYY-MM-DD",
      "task_type": "<类型>",
      "score": XX,
      "key_success": "<一句话成功要素>",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

## 模板更新规则

以下情况需要更新模板：

1. **成功的工作方式** → 提取为模板
   - 例：某次 WBS 分解特别有效 → 更新 `planner/skills/wbs-template.md`

2. **常见的错误模式** → 写入注意事项
   - 例：预算经常超支 → 在预算模板里加警告

3. **新的产出格式** → 创建新模板
   - 例：新的文档格式 → 写入 `templates/`

## 常见错误

- ❌ 只写总结不写具体细节（未来无法检索）
- ❌ 不更新 index.json（经验无法被找到）
- ❌ 把经验写成感想（要有可操作的建议）
- ❌ 任务失败但不写失败教训（教训比成功更有价值）
