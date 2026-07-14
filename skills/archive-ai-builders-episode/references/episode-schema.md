# AI Builders episode archive schema

## Canonical identity

Use this folder and file prefix:

```text
【AI Builders解读NN】YYYYMMDD_OriginalSpeaker_OriginalTalkTitle
```

- `NN`: two-digit episode number, such as `01` or `02`.
- `YYYYMMDD`: first publication date of the interpretation video, not the original talk date.
- `OriginalSpeaker`: original speaker, with spaces removed for filenames.
- `OriginalTalkTitle`: exact source talk title, normalized only by removing filename-invalid punctuation and spaces.

Do not replace the original talk title with a separate interpretation headline.

Keep the reusable skill and project-wide documentation outside every episode folder. An episode folder contains only its structured `README.md` and confirmed formal artifacts for that episode; it must not contain infrastructure directories. Keep single-file artifacts flat, but allow a canonical self-contained bundle directory when a formal artifact cannot run without dependencies.

## Canonical artifact names

Append one of these suffixes to the shared prefix:

| Artifact | Canonical suffix | Notes |
| --- | --- | --- |
| Interpretation video | `_解读视频_<quality>.<ext>` | Example: `_解读视频_2K.mov` |
| Interpretation PPT | `_解读PPT.pptx` | Editable production deck |
| Interpretation transcript | `_解读视频逐字稿.md` | Markdown master |
| Interpretation transcript PDF | `_解读视频逐字稿.pdf` | Only when actually generated and verified |
| Interpretation HTML bundle | `_解读HTML_<format>/` | Self-contained directory with `index.html`, bundle `README.md`, and runtime assets only |
| Publication information | `_解读视频发布信息.md` | Platform, time, short title, description, tags |
| Portrait promo | `_解读视频宣传图_竖版3比4.png` | Include actual ratio in the name |
| Landscape promo | `_解读视频宣传图_横版4比3.png` | Include actual ratio in the name |
| Original video | `_原视频.<ext>` | Only if the user confirms local archival |
| Original PPT | `_原PPT.pptx` | May be image-based when only ordered screenshots exist |
| Original transcript | `_原文内容.<ext>` | Preserve useful source format |
| Bilingual transcript | `_原文内容及中文翻译.md` | English and Chinese aligned |

Do not use `最终`, `最新版`, `V19`, `final`, or similar workflow state in canonical names.

## Default interpreter profile

Use these values unless the user updates them:

| Field | Value |
| --- | --- |
| 解读人 | Elisedai在创造 |
| 解读人介绍 | 大厂 AI 产品经理，Agent 大赛冠军。关注全球 AI Builders，分享我的思考，以及正在创造的产品。 |

## README structure

Use this order.

### 1. 项目概览

Include:

- 系列
- 期数
- 分享主题
- 原分享人
- 解读人
- 解读人介绍
- 首次发布日期
- 首发渠道
- 核心问题

The `分享主题` must equal the original talk title used in the filenames.

### 2. 原始分享来源

Include original speaker, identity, exact talk title, event, original talk date, duration when known, official video URL, and speaker profile URL when useful.

### 3. 内容结构

Summarize the source talk's logical parts and explain what the interpretation adds. Do not copy a long transcript into README.

### 4. 文件结构

Group the formal files and delivery bundles in README tables:

- `4.1 解读成品`
- `4.2 宣传图片`
- `4.3 原始分享材料`

Do not list files that do not exist. Record genuinely missing source artifacts as `尚未取得` only when that status is useful.

### 5. 渠道发布记录

Create one subsection per channel, such as `5.1 微信视频号`. Include platform, exact publication time, short title, published duration, tags, and a pointer to the publication-information file.

### 6. 命名规范

Record the common prefix and allowed artifact suffixes. State that the archive excludes drafts and intermediate outputs.

## Confirmation manifest

Use a decision table before the first archive write:

```markdown
| Content type | Recommended source | Why | Canonical destination | Save? |
| --- | --- | --- | --- | --- |
| 解读PPT | `/path/to/V19.pptx` | Latest version aligned with the approved script | `..._解读PPT.pptx` | 请确认 |
| 用户上传双语稿 | `/path/to/upload.md` | User-provided source and translation | `..._原文内容及中文翻译.md` | 请确认 |
```

After confirmation, preserve the decision in the conversation; do not add a separate approval-log file to the clean archive unless the user asks.

## Exclusion patterns

Treat these as non-archival by default:

- versioned drafts: `V1`, `V2`, `draft`, `草稿`, `候选`, `旧版`;
- generated previews: `预览`, `preview`, `contact-sheet`, `montage`;
- slide renders and extracted frames: `slide-*.png`, timestamp crops, render folders;
- validation artifacts: `*.inspect.ndjson`, layout JSON, QA reports;
- caches and temporary content: `tmp`, `temp`, `.cache`, hidden system files;
- duplicates and backups: `copy`, `副本`, `(1)`, `(2)` unless the user selects one explicitly.

A versioned source may be chosen as the official content, but archive it only after confirmation and rename it to the stable canonical name.

## Formal delivery bundles

Use a bundle directory only when separating the files would break the formal artifact. HTML presentations and small static sites qualify; ordinary PPTX, PDF, Markdown, images, and videos do not.

A formal bundle must:

- use the complete episode prefix plus a stable content suffix;
- contain `index.html` as its entry point and a short `README.md` explaining how to open it;
- contain only files required to run or understand the final artifact;
- keep dependencies in clearly named subdirectories such as `assets/`;
- exclude drafts, prototypes, rejected concepts, previews, validation output, caches, source maps, and hidden system files;
- resolve every local static `src` and `href` reference.

The episode README lists the bundle once as a formal artifact. The bundle README lists its entry point and dependency directories; it does not need to enumerate every image asset.
