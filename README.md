# AI Builders 工具箱 01｜《A Field Guide to Fable》

本仓库只围绕 Thariq Shihipar 的演讲《A Field Guide to Fable》展开，收录「Elisedai在创造」根据演讲观点整理的 6 组中文提示词，帮助你：

- 在 Agent 执行前找盲点、对齐需求和探索方案；
- 在执行中记录偏差；
- 在完成后确认人仍理解关键决策并能对结果负责。

原分享来自 Anthropic Claude Code 开发者 Thariq Shihipar 在 AI Engineer World’s Fair 2026 的演讲 [A Field Guide to Fable](https://www.youtube.com/watch?v=9fubhllmsBU)。

> 重要说明：6 组中文提示词由「Elisedai在创造」根据原演讲观点重新整理，是本系列的编辑性工具，不是 Thariq Shihipar 或 Anthropic 发布的官方提示词。

## 六组提示词

打开 [Agent 工作流六组提示词](toolkits/agent-workflow-prompts.md)，可以直接使用：

| 工具 | 适合解决的问题 |
| --- | --- |
| 盲点扫描 | 执行前找出需求中没有出现、但会改变方案的问题 |
| 差异化原型 | 不知道自己想要什么时，先比较真正不同的方向 |
| AI 逐题访谈 | 通过一次一个问题补全关键决策 |
| 参考实现 | 让 AI 理解已有实现的语义，而不是机械照抄 |
| 执行偏差记录 | Agent 自主推进时保留可复盘的决策记录 |
| 完成后反向测验 | 确保人仍然理解关键修改并能对结果负责 |

## 如何使用

可以直接打开 [Agent 工作流六组提示词](toolkits/agent-workflow-prompts.md) 复制使用，也可以克隆仓库：

~~~bash
git clone https://github.com/Elisedai1013/ai-builders-toolkit-01-agent-workflow.git
cd ai-builders-toolkit-01-agent-workflow
~~~

## 仓库结构

~~~text
ai-builders-toolkit-01-agent-workflow/
├── README.md
├── LICENSE
├── NOTICE.md
└── toolkits/
    └── agent-workflow-prompts.md
~~~

## 没有上传的内容

本仓库不包含：

- 第一期解读视频、解读 PPT 和宣传图；
- 原演讲 PPT、完整英文逐字稿及中文翻译；
- 演讲截图、讲者照片和其他第三方媒体素材；
- 本地路径、缓存、预览或过程文件。

这样可以让仓库始终只围绕《A Field Guide to Fable》，也避免重新分发原演讲的完整版权内容。

## License

本仓库中由 Elisedai 创作的中文提示词和文字说明采用 [MIT License](LICENSE)。原演讲、人物、品牌与第三方材料的权利仍归各自权利人所有，详见 [NOTICE](NOTICE.md)。
