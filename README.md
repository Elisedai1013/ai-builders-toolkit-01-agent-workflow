# AI Builders 工具箱 01｜设计可控的 Agent 工作流

这套工具帮助你在 Agent 动手前找盲点、对齐需求和探索方案，在执行中记录偏差，完成后检查人是否仍理解关键决策。它从第一期《A Field Guide to Fable》解读中整理而来，包含：

1. 6 组可直接复制的 Agent 提示词；
2. 3 个用于持续制作 AI Builders 解读内容的 Codex Skills；
3. 清晰的来源、归属与公开边界说明。

原分享来自 Anthropic Claude Code 开发者 Thariq Shihipar 在 AI Engineer World’s Fair 2026 的演讲 [A Field Guide to Fable](https://www.youtube.com/watch?v=9fubhllmsBU)。

> 重要说明：6 组中文提示词由「Elisedai在创造」根据原演讲观点重新整理，是本系列的编辑性工具，不是 Thariq Shihipar 或 Anthropic 发布的官方提示词。

## 先从工具箱开始

打开 [Agent 工作流六组提示词](toolkits/agent-workflow-prompts.md)，可以直接使用：

| 工具 | 适合解决的问题 |
| --- | --- |
| 盲点扫描 | 执行前找出需求中没有出现、但会改变方案的问题 |
| 差异化原型 | 不知道自己想要什么时，先比较真正不同的方向 |
| AI 逐题访谈 | 通过一次一个问题补全关键决策 |
| 参考实现 | 让 AI 理解已有实现的语义，而不是机械照抄 |
| 执行偏差记录 | Agent 自主推进时保留可复盘的决策记录 |
| 完成后反向测验 | 确保人仍然理解关键修改并能对结果负责 |

## 随仓库提供的 Skills

| Skill | 作用 |
| --- | --- |
| [ai-builder-talk-to-script](skills/ai-builder-talk-to-script/) | 把一线 Builder 的逐字稿、PPT 和元数据转成有证据、有画面映射、有方法论交付的中文解读口播稿 |
| [archive-ai-builders-episode](skills/archive-ai-builders-episode/) | 扫描候选材料、统一命名、确认版本并审计单期正式归档 |
| [create-ai-builders-promo-covers](skills/create-ai-builders-promo-covers/) | 按统一信息层级生成 3:4 与 4:3 的 AI Builders 解读宣传封面 |

这些 Skills 是 AI Builders 解读系列的生产方法沉淀，不属于原演讲内容，也不代表原分享人的官方工作流。

## 相关的独立工具

以下项目已经有自己的维护入口，因此不在本仓库重复复制：

- [Builder Radar](https://github.com/Elisedai1013/builder-radar)：追踪全球 AI Builders 的一线发布、研究、工程文章与演讲。
- [YouTube Learning — 视频逐字稿提取与双语整理](https://skillhub.cn/skills/youtube-learning-elisedai)：提取 YouTube 字幕、生成双语文档并记录播放量快照。

## 安装一个 Skill

先克隆仓库：

~~~bash
git clone https://github.com/Elisedai1013/ai-builders-toolkit-01-agent-workflow.git
cd ai-builders-toolkit-01-agent-workflow
~~~

再把需要的 Skill 文件夹复制到 Codex Skills 目录：

~~~bash
mkdir -p "$HOME/.codex/skills"
cp -R skills/ai-builder-talk-to-script "$HOME/.codex/skills/"
~~~

也可以把复制命令中的 Skill 名称替换为：

- archive-ai-builders-episode
- create-ai-builders-promo-covers

安装后可以这样调用：

~~~text
使用 $ai-builder-talk-to-script，根据这份 AI Builder 逐字稿和 PPT，生成中文解读口播稿与配套工具箱。
~~~

## 仓库结构

~~~text
ai-builders-toolkit-01-agent-workflow/
├── README.md
├── LICENSE
├── NOTICE.md
├── toolkits/
│   └── agent-workflow-prompts.md
└── skills/
    ├── ai-builder-talk-to-script/
    ├── archive-ai-builders-episode/
    └── create-ai-builders-promo-covers/
~~~

## 没有上传的内容

本仓库不包含：

- 第一期解读视频、解读 PPT 和宣传图；
- 原演讲 PPT、完整英文逐字稿及中文翻译；
- 演讲截图、讲者照片和其他第三方媒体素材；
- SkillHub 平台元数据、本地路径、缓存、预览或过程文件。

这样可以让仓库保持轻量、可复用，也避免重新分发原演讲的完整版权内容。

## License

本仓库中由 Elisedai 创作的提示词、Skills、脚本和文字说明采用 [MIT License](LICENSE)。原演讲、人物、品牌与第三方材料的权利仍归各自权利人所有，详见 [NOTICE](NOTICE.md)。
