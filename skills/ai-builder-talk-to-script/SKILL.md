---
name: ai-builder-talk-to-script
description: Transform first-party AI Builder conference or YouTube transcripts, bilingual transcripts, slide decks, extracted slide images, and video metadata into source-grounded Chinese self-media commentary scripts for the AI Builders 解读 series. Use when Codex needs to write, rewrite, or audit an AI Builder oral script; map narration to PPT pages and timestamps; turn a talk into an engaging Builder-led story; extract reusable prompts, templates, checklists, observation forms, or decision frameworks; create a companion toolkit; or fix scripts that feel stiff, abstract, overlong, poorly hooked, or weakly attributed.
---

# AI Builder Talk to Script

Turn a first-party Builder talk into an evidence-backed Chinese episode, not a translated summary or a list of homework.

Before drafting, read these references completely:

- [references/series-voice-and-structure.md](references/series-voice-and-structure.md)
- [references/artifact-templates.md](references/artifact-templates.md)

## Non-negotiable rules

1. Read the complete source transcript and the relevant slides. Do not write from a synopsis alone.
2. Distinguish three layers in working notes: `S` for source facts, cases, and claims; `I` for Elise's interpretation; `T` for tools derived by this series.
3. Put quotation marks only around wording verified against the original-language transcript. Label a paraphrase as a paraphrase.
4. Never attribute an Elise question, tool name, prompt, or framework to the speaker. Introduce a derived tool with wording such as “我把它整理成……”.
5. Start with the speaker, distinctive background, and sharing context before the fixed series identification line.
6. Use a concrete tension, failure, choice, or surprising case as the hook. Do not use a vague sentence that needs explanation before it becomes interesting.
7. Explain a concrete example before naming an abstract concept. Make the example understandable without specialist domain knowledge: remove nonessential jargon, and explain any essential term in plain Chinese before using it.
8. Deliver at least one reusable method. A one-time action such as “去问用户” is not a method.
9. Give every derived method a use case, inputs, steps, output, boundary, and provenance.
10. Write all generated artifacts as `_草稿` work files in the matching source folder under `【YouTube学习资料】/`. Use `output/` only for disposable previews and QA output. Never write directly into a formal episode folder under `【AI Builders解读】/` without the separate archive workflow and explicit confirmation.

## 1. Discover and verify inputs

Prefer, in order:

1. Files explicitly selected by the user.
2. Clean English transcript plus bilingual transcript.
3. Raw transcript only for recovering missing or disputed wording.
4. Official PPTX or PDF; otherwise `slides.json` plus ordered slide images from a video-projection reconstruction.
5. Metadata, source notes, event pages, and the existing episode README.

Run the inventory script when the source folder contains many candidates:

```bash
python3 scripts/inventory_inputs.py --source <working-source-folder> --format markdown
```

Treat identical hashes as one source. If plausible transcript or deck candidates differ, compare them and state the coverage gap; do not choose solely by modification time.

Treat filenames such as `_原PPT` as clues, not proof of official provenance. Check `SOURCE.md`, linked source pages, deck structure, and whether each page is a flattened image. If the verified official talk title conflicts with an existing episode prefix, report the difference and keep the current working identity until the user confirms a rename.

If only a YouTube URL exists, first use `youtube-learning-elisedai` when available. If the talk visibly contains a deck but no slide source exists, use `extract-youtube-slides` when available. If either prerequisite is unavailable, report the missing evidence before drafting.

Verify current job titles, event details, and other changeable speaker facts against primary sources. Prefer the official event page, employer profile, speaker site, or the speaker's own profile. Do not invent a biography from memory.

If slides came from the recording, state exactly:

> 画面页码均指视频投屏截图复原版，不是演讲者官方原始 PPT。

If a flattened PPTX has no `slides.json`, create a minimal page index in the working folder before mapping visuals:

```bash
python3 scripts/build_slide_index.py \
  --pptx <flattened-deck.pptx> \
  --official-original-deck false \
  --output <working-folder/slides.json>
```

Use `unknown` instead of `false` when provenance is unresolved. This index validates file-page ranges but does not invent slide topics or video timestamps.

## 2. Build an evidence map before prose

Create a temporary evidence table using the schema in `references/artifact-templates.md`. Map each candidate story to:

- transcript wording or timestamp;
- PPT page and video timestamp when available;
- evidence class `S`, `I`, or `T`;
- intended role in the episode;
- confidence or unresolved ambiguity.

Use slides to prove what appeared on screen, not to prove that the speaker said a sentence. Return to the English transcript before using a direct quote.

Do not save the evidence map in a formal archive. Save it as a working draft only when the content is complex, attribution is easy to confuse, or the user requests traceability.

## 3. Find the episode's editorial spine

Write one sentence for each item before outlining:

- the talk's central tension;
- why it matters specifically to people building AI or Agent products;
- the human judgment that AI does not remove;
- the reusable method the audience can keep using.

Select two to four source stories that best develop that tension. Do not force exactly three points. Prefer stories with a visible choice, failed attempt, unexpected result, or before-and-after contrast.

Reject a candidate section when it merely repeats the talk, cannot be traced to evidence, or does not change how a Builder would judge or build something.

## 4. Design the opening

Follow this order unless the user explicitly changes it:

1. Identify the speaker and the part of their background that creates useful tension with the topic.
2. Say where, when, and in what role they shared the talk.
3. Surface one concrete question or contradiction from the talk.
4. Use the fixed series identification line verbatim.
5. Promise concrete reusable takeaways using observable language.
6. Leave one clear question that the ending will answer.

Keep this sequence within roughly the first minute. Make the value understandable without terms that have not yet been explained. Promise tools by form or result—such as a five-second test, a trade-off template, or an observation sheet—not “三件很重要的事”.

## 5. Draft each body section as a story

Use this beat sequence:

1. Reconstruct a concrete source scene.
2. Show the choice, friction, or failed expectation.
3. State the speaker's actual point.
4. Explain what it changes for an AI Builder.
5. Deliver a reusable tool derived from that point when appropriate.
6. End with the question that naturally opens the next section.

Add a short visual cue before every major section:

```markdown
> 画面：原 PPT 第 7—11、13 页；三种椅子与对应界面。
```

Verify every cited page against the actual deck or `slides.json`. Use “讲者画面”“产品演示” or “自制工具卡” when no source slide exists. Keep screen directions outside the spoken copy.

Use short paragraphs and concrete verbs. Make the script understandable with eyes closed. Avoid consecutive abstract nouns, translated syntax, ceremonial transitions, and repeated summaries.

## 6. Convert advice into reusable methodology

Use prompts, fill-in templates, tests, checklists, observation forms, decision rules, or repeatable loops. A method must help the audience decide, not merely tell them to act.

For every tool, specify:

- source relationship: which speaker case or claim inspired it;
- use case;
- inputs;
- ordered steps;
- output;
- boundary and who owns the final decision.

Demonstrate the tool once with the current talk's example. Keep long prompts and tables out of the spoken narration. Put them in a linked companion toolkit and summarize only their purpose, use, and result in the script.

Preserve Builder ownership. AI may ask questions, create candidates, or find conflicts; the Builder must choose the principle, accept the trade-off, and remain responsible for the result.

## 7. Close the loop

Answer the opening question explicitly. Compress the episode into one Builder judgment, then remind viewers what reusable tool they can save. Do not introduce a new thesis in the ending.

Use a specific interaction question only when it helps the viewer apply the method. Avoid a generic “你怎么看”.

## 8. Write draft artifacts

Use the templates and naming rules in `references/artifact-templates.md`.

Default outputs:

1. a linked oral-script draft with verified visual cues;
2. a source/evidence map draft when attribution or slide mapping is complex;
3. a companion toolkit draft when a prompt, form, or table is too detailed to narrate.

Keep these in the matching source-material folder under `【YouTube学习资料】/` and retain `_草稿` in each filename. Put disposable renders, previews, and audit output in `output/`. Do not move, delete, overwrite, or rename source files. After the user approves the script, use the separate `archive-ai-builders-episode` workflow to propose formal names and request confirmation.

## 9. Run three QA passes

### Evidence pass

Check every biography claim, number, quote, product detail, causal claim, and tool attribution against the evidence map. Mark uncertainty instead of smoothing it over.

### Listener pass

Hide headings and visual cues, then read only the spoken text aloud. Rewrite anything that is hard to understand on first hearing. Check that each abstract term arrives after an example and is explained in plain Chinese.

### Promise-and-delivery pass

Check that the opening, body, toolkit, and ending use the same tool names, count, order, and result. Check that each promised method is actually usable without watching the talk again.

Run the deterministic audit:

```bash
python3 scripts/audit_oral_script.py \
  --script <oral-script-draft.md> \
  --toolkit <optional-toolkit-draft.md> \
  --slides-json <optional-slides.json>
```

Treat automated results as structural checks, not editorial approval. Fix all errors and review every warning. Report the spoken-character count and estimated duration. Respect the user's requested duration; otherwise target approximately 9–10 minutes and remove repetition before removing source evidence or the reusable method.

## 10. Revise from user feedback

Treat accepted fixed lines and rejected wording as editorial decisions, not isolated comments. When feedback identifies a category problem—too stiff, too abstract, weak hook, action list instead of methodology—revise the underlying structure across the whole draft.

Preserve approved source facts and visual mappings unless new evidence changes them. Re-run all three QA passes after a structural revision.
