# AI Agent 与 Harness 完整解释基准

这是独立于 54 秒短样片 `ai-agent-harness-benchmark` 的长片基准。目标不是逐镜复制参考视频，而是在内容内核、可检查流程、角色融合、证据和生产质量上达到或超过它。

## 验收对象

- `storyboard/story.json`：10 章、29 个音频优先镜头；用“制作观众正在看的这条视频”作为同一端到端案例。
- `sources/citations.json`：一手资料与参考片清单。
- `evaluation/coverage.json`：15 项 Agent/Harness 核心知识映射。
- `evaluation/rubric.json`：冻结的硬门槛、100 分量表和盲评协议。
- `audio/*.timeline.json`：MiMo 女声真实时长、视频节拍、统一字幕 cue，以及 129 个语义动画事件逐一人工绑定旁白的视觉事件契约；不允许按时长比例回退。
- `audio/sfx.timeline.json`：跨 10 章的 19 个 cue-locked 事件音效；最终混音另含旁白侧链压低的 ambient bed。
- `evaluation/asr-report.json`、`layout-qa.json`、`technical-qa.json`：逐段盲 ASR、角色图片比例、400 个文本容器、Card System V2、Scene Grammar V2、Character Performance V2 的 cue-bound 姿态节拍、Character Stage V3 的真实 alpha 与语义目标绑定，以及音画/黑帧/冻结段/字幕同步门槛。
- `evaluation/judge-scorecard.json`：四位独立评委对固定成片 SHA 的最终评分、硬门槛和仍未超过参考片的差距记录。
- `final/trace.json`、`trace-viewer.html`：29 个镜头事件的机器可读制作叙事 Trace 与交互查看器；文件明确声明它不是原始模型/工具遥测。
- `final/*.mp4`：最终渲染，默认不进入 Git；生成源、字幕、Trace 与 QA 报告进入 Git。

## 内容范围

完整长片覆盖单次模型调用、Workflow/Agent 边界、工具协议、ReAct 与停止条件、Plan-and-Execute、Context/Memory/Compaction、多 Agent、结构化输出、Retry/Idempotency、Checkpoint、安全审批、反馈评测，以及一条包含失败恢复和人工批准的制作叙事 Trace。

## 女声

主讲人固定为小兰，生产配置为 MiMo `mimo-v2.5-tts` 的女声 `茉莉`。故事板保存非敏感的音色与风格，凭证只从 `MIMO_API_KEY` 环境变量读取。

## 命令

```bash
pnpm benchmark:complete:validate
pnpm benchmark:complete:audio
pnpm benchmark:complete:subtitles
pnpm benchmark:complete:visual-cues
pnpm benchmark:complete:asr
pnpm benchmark:complete:trace
pnpm benchmark:complete:render
pnpm benchmark:complete:qa
```

只有 `evaluation/rubric.json` 的全部硬门槛通过、盲评总分达到要求，才允许把目标标记为完成。
