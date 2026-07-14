# AI Builders 解读封面视觉系统

## 系列不变项

- 气质：一线 Builder 观点的编辑封面，理性、大胆、有人的判断，不做套模板的“AI 蓝紫霓虹”。
- 配色策略：不设系列固定主色。每期优先从原演讲 PPT、活动视觉、产品界面或讲者画面中提取配色。
- 色彩结构：选择 1 个主色、1 个强对比色和 1 个中性色；两种比例必须使用同一组配色。
- 可读性：主标题与背景保持高对比，背景可以是深色或浅色，不默认黑底。
- 来源视觉过于杂乱时，从其中选一个最能代表当期的颜色，再配黑、白、灰之一建立干净的编辑层级。
- 排版：粗黑无衬线、紧凑标题、明显编辑层级，可加轻微纸张或半调纹理。
- 人物：黑白或暖色半调剪影，轮廓清楚，保留本人可识别特征。
- 系列标识：`AI Builders 解读 NN` 使用紧凑横条或框线承载，次于主标题。

## 每期变化项

- 讲者人像；
- 短标题；
- 从当期来源提取的主色与对比色；
- 原演讲中最能被记住的一个物件、画面或矛盾；
- 背景中与主题相关的产品界面或舞台意象；
- 人物与主题意象在横竖版中的位置。

不要机械复制任何上一期的视觉隐喻。每期都应从当期原演讲中选择自己的人物、物件、空间或矛盾关系。

## 提示词骨架

```text
Use case: ads-marketing
Asset type: Chinese AI Builders 解读 episode cover, <3:4 portrait | 4:3 landscape>
Primary request: Create a premium editorial cover for episode <NN> about <one-sentence tension>.
Input images: Image 1 is the verified speaker reference; Images 2–N are source-talk visual references.
Subject: Keep <speaker> recognizable; integrate <episode-specific visual metaphor>.
Style/medium: bold technology editorial poster, Swiss typography, subtle halftone print texture.
Composition/framing: <ratio-specific native composition and safe margins>.
Color palette: extract one dominant color, one contrasting color, and one neutral from the verified source-talk or event visuals; keep the same palette across both ratios.
Text (verbatim):
“<approved short title>”
“AI Builders 解读 <NN>”
“<Speaker Name> · <Event YYYY>”
Constraints: exact Chinese text; verified identity; only specified text; professional hierarchy.
Avoid: extra copy, fake logos, garbled Chinese, watermark, generic robot imagery, circuit-board clichés, excessive neon, duplicate people.
```

## 参考资产规则

公开 Skill 不附带真实讲者肖像或单期宣传图。执行任务时，从当期原演讲、活动官方页面或用户确认的资料中选择可核验的人物和视觉参考。只借鉴信息层级、编辑排版、人物处理和横竖版构图关系；不直接复制受版权保护的画面，也不虚构讲者面孔。
