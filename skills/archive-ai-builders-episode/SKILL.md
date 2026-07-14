---
name: archive-ai-builders-episode
description: Archive, clean, audit, or update an AI Builders interpretation episode in its canonical formal folder. Use when preparing episode 02 or later, consolidating PPT/script/video/image/HTML versions, deciding what belongs in a formal episode folder, cleaning an existing archive, handling user-uploaded sources, or checking whether drafts and intermediate outputs leaked into the archive. Inventory candidates, require confirmation before ambiguous writes, support self-contained HTML delivery bundles, and keep only confirmed formal materials.
---

# Archive an AI Builders Episode

Create a clean, flat, traceable episode archive. Automate discovery and naming, but keep the user in control of what becomes official.

Read [references/episode-schema.md](references/episode-schema.md) completely before proposing names, creating the episode folder, or writing its README.

## Non-negotiable rules

1. Treat the archive as a published record, not a workbench.
2. Do not copy, move, rename, or replace a candidate until the confirmation gate is satisfied.
3. Require confirmation for:
   - every inferred “best” version when multiple versions exist;
   - every user-uploaded file unless the user explicitly said to save that exact file;
   - any replacement of an already archived file;
   - uncertain metadata that changes the folder prefix.
4. An explicit instruction such as “把这个文件保存进去” for one exact file counts as confirmation for that file only.
5. Never archive drafts, rejected alternatives, old versions, slide renders, preview images, contact sheets, inspection files, caches, temporary files, or duplicate exports.
6. Copy confirmed source files; do not move or delete the user's originals.
7. Keep single-file deliverables flat. Allow a nested directory only when it is one confirmed self-contained delivery bundle, such as an HTML presentation that requires assets. Name the bundle with the full episode prefix and list it in the episode README.
8. Treat the existing workspace as three zones: `【YouTube学习资料】/` for source and working drafts, `output/` for temporary generation and QA outputs, and the canonical episode folder under `【AI Builders解读】/` for confirmed formal artifacts only. Do not work iteratively inside the formal zone.

## Workflow

### 1. Establish the episode identity

Confirm or infer, then verify before writing:

- episode number;
- interpretation video's first publication date;
- original speaker's name;
- exact original talk title;
- interpreter name and profile;
- original source link and event metadata;
- first publication channel.

Use the interpretation video's first publication date in the canonical prefix. Record the original talk date separately in README.

### 2. Inventory candidates without mutating files

Run:

```bash
python3 scripts/inventory_candidates.py \
  --source <search-root> \
  --episode <NN> \
  --date <YYYYMMDD> \
  --speaker <OriginalSpeaker> \
  --topic <OriginalTalkTitle> \
  --output <candidate-inventory.md>
```

Write the inventory to operating-system scratch space outside both the source tree and the canonical episode folder. Delete it after the decisions are captured in the conversation and always before final handoff; it is not a deliverable.

Add chat attachments and files outside the scan root to the inventory manually. Treat attachments as candidates, not automatic archive members.

### 3. Recommend, but do not silently decide

Evaluate candidates using all available evidence:

1. explicit user selection;
2. alignment between PPT page order and transcript;
3. completeness and successful rendering/playback;
4. meaningful version labels and conversation decisions;
5. modification time only as supporting evidence, never as the sole reason.

Mark one recommended candidate per artifact type when evidence supports it. If evidence is weak, say so.

### 4. Apply the confirmation gate

Before any archive write, show a compact table with:

| Content type | Recommended source | Why | Canonical destination | Save? |
| --- | --- | --- | --- | --- |

Ask the user to confirm the rows. Explicitly call out uploaded files. Do not proceed on ambiguous replies such as “use the latest” when more than one candidate plausibly qualifies.

If the user rejects a row, leave it out; do not keep it as a backup in the archive.

### 5. Create the canonical archive

After confirmation:

1. Create the episode folder using the schema reference.
2. Copy only approved artifacts under canonical stable names.
3. Normalize versioned filenames such as `V19`, `final-final`, or `最新版`; keep the versioned original outside the archive.
4. Preserve meaningful delivery qualifiers only, such as `_2K`, `_1080p`, `_竖版3比4`, or `_横版4比3`.
5. Verify copied files by SHA-256 when practical; always verify size and existence.
6. Validate presentations, PDFs, videos, and images in proportion to risk using their applicable artifact skills.
7. For a compound HTML deliverable, copy the complete runnable bundle under a canonical bundle directory. Keep only runtime dependencies, use `index.html` as the entry point, add a short bundle `README.md`, and remove prototypes, alternative concepts, source maps, inspection output, caches, and drafts.

When the original deck exists only as ordered screenshots, create a multi-page `.pptx` with one source slide image per page. Do not substitute a montage or contact sheet. Note in README that text inside the screenshots is not separately editable.

### 6. Write a structured README

Use the schema reference. Separate:

- project overview;
- original source;
- content structure;
- file map grouped by role;
- channel-specific publication records;
- naming rules and any material limitations.

Use `首次发布日期` once in the overview. Put exact timestamps and platform-specific copy in the channel record. Do not add a verbose technical-spec section unless the user asks.

### 7. Perform the clean-archive audit

Run:

```bash
python3 scripts/audit_archive.py --episode-dir <canonical-episode-folder>
```

Before handoff, verify:

- every archived file appears in README;
- every README file link exists;
- every archived artifact was confirmed;
- no unconfirmed upload was copied;
- no draft or intermediate artifact remains;
- names share the exact canonical prefix;
- the original source URL is present;
- missing materials are labeled missing rather than fabricated.
- every formal bundle has a canonical directory name, `index.html`, a bundle `README.md`, and no broken local `src` or `href` dependency;
- the audit passes after every add, replace, rename, or deletion in the formal folder.

Report what was archived and list anything still awaiting confirmation. Do not say the archive is complete while required rows remain undecided.
