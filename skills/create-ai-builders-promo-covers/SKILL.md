---
name: create-ai-builders-promo-covers
description: "Create a consistent pair of promotional cover images for the Chinese AI Builders 解读 series: one portrait 3:4 cover and one landscape 4:3 cover. Use when Codex needs to make, remake, update, or audit an episode cover, thumbnail, publicity image, social-media poster, or episode promo visual that must contain an approved short title, the current episode's speaker, and the AI Builders 解读 series identity."
---

# AI Builders 解读宣传封面

为每期解读生成同一视觉系统下的两张封面：1 张 3:4 竖版和 1 张 4:3 横版。系列识别由信息层级、编辑排版、人物处理和横竖版构图保持稳定；讲者、标题、配色和主题意象随当期内容替换。

生成前完整阅读 [references/visual-system.md](references/visual-system.md)。同时加载并遵循系统 `imagegen` Skill；正常情况使用内置图片生成工具。

## 1. 确认输入

在生成前确认：

- 期数 `NN`；
- 用户已确认的中文短标题，默认不超过 16 个字符；
- 当期讲者英文姓名；
- 讲者可核验的原始照片或视频截图；
- 原演讲主题、活动名或年份，供辅助信息使用；
- 一到三张能代表本期内容的原演讲画面。

优先从当期正式资料夹和对应的 `【YouTube学习资料】/` 工作夹查找。只有在讲者身份可确认时才使用人像；不用 AI 虚构一张“像讲者”的脸。

如果短标题尚未确认，先提供 3 个不超过 16 字符的候选，暂停生成，等用户选定。不擅自修改已确认的标题。

## 2. 固定信息层级

每张封面都必须出现：

1. 短标题：画面中最大的文字，必须逐字正确；
2. 当期讲者：使用真实来源人像，保持可识别；
3. 系列标识：`AI Builders 解读 NN`；
4. 讲者信息：`Speaker Name · Event YYYY`，仅在资料可核验时使用。

不默认添加 OpenAI、Figma、YouTube 或讲者公司 Logo。除非用户明确要求，不添加标签、介绍、口号或额外文案。

## 3. 生成两个原生构图

### 3:4 竖版

- 目标尺寸：1086×1448 或其他精确 3:4 尺寸。
- 上半部优先保留给短标题。
- 中部放主题意象，下部或下三分之一放讲者人像。
- 保留平台裁切安全边距。

### 4:3 横版

- 目标尺寸：1448×1086 或其他精确 4:3 尺寸。
- 必须重新构图，不得把竖版直接居中裁切。
- 优先使用“左标题、中主题意象、右人物”的横向阅读顺序；主题需要时可镜像调整。
- 使用竖版成品作为风格参考，但重新安排标题、人物和主题意象。

先生成并确认 3:4，再以其为系列风格参考生成 4:3。对两张图分别下达任务，不在同一张大图中并排输出。

## 4. 逐项验收

生成后必须使用视觉检查和尺寸检查，不只信任提示词。

检查：

- 短标题与用户确认版逐字一致，不少字、多字或乱码；
- `AI Builders 解读 NN` 的大小写、空格和期数正确；
- 讲者是当期人物，脸部没有被明显改换；
- 讲者英文名和活动信息拼写正确；
- 画面没有未授权 Logo、水印、多余文字或重复人物；
- 3:4 和 4:3 是两个完整原生构图；
- 标题在缩略图尺寸下仍然清楚。

如果只有文字错误，优先对当张图做局部编辑，要求仅替换文字并保留其他元素。错字封面不得作为成品交付。

## 5. 保存与交付

未获得正式归档确认前，保存到：

```text
output/AI Builders解读NN封面/
【AI Builders解读NN】<短标题>_宣传图_竖版3比4.png
【AI Builders解读NN】<短标题>_宣传图_横版4比3.png
```

不直接写入或覆盖当期正式资料夹。用户确认成品后，使用 `archive-ai-builders-episode` Skill 提案归档。

交付时直接展示两张图，并提供工作区绝对路径。报告实际像素尺寸，说明使用了内置图片生成工具。
