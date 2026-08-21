# 沙雕科普动画工作室

一个可以直接交给 Codex 继续完善的 MVP：**Story JSON → 中文配音 → 角色/图解/字幕动画 → MP4**。

首条样片：`空调开到 16℃真的更省电吗？`。渲染样片随本次交付包单独提供，仓库保留可重复生成它的完整脚本与代码。

## 已实现

- 两个程序化卡通角色，支持说话口型、点指、震惊、思考、点头、发抖、庆祝。
- 8 个 JSON 分镜，包含对白、时长、角色状态、标题、图解、特效、转场和音效。
- 系统 `espeak` 中文配音；没有 TTS 时仍可静音渲染。
- 误区卡片、机制流程、运行时间对比、温度计、节能建议等图解。
- 字幕烧录、片头标签、进度条、封面和 H.264 MP4。
- 不依赖人物素材，所有画面由代码绘制，便于直接修改。

## 运行

要求：Python 3.11+、FFmpeg；建议安装 `espeak` 或 `espeak-ng`。

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .

sandiao validate stories/ac-16c.json
sandiao build stories/ac-16c.json
```

输出：

```text
output/ac-16c-sample.mp4
output/ac-16c-poster.png
output/ac-16c-master.wav
```

## 新建一条动画

复制 `stories/ac-16c.json`，修改 `shots`。每个镜头可配置：

```json
{
  "id": "runtime",
  "duration": 4.4,
  "speaker": "xiaoming",
  "dialogue": "温度设得更低，主要是让压缩机更晚停机。",
  "headline": "真正改变的是运行时间",
  "diagram": "runtime",
  "effect": "",
  "sfx": ["whoosh"],
  "states": [
    {
      "character": "xiaoming",
      "x": 0.87,
      "y": 0.60,
      "scale": 0.94,
      "facing": -1,
      "action": "point",
      "expression": "serious"
    }
  ]
}
```

当前动作：`idle`、`talk`、`point`、`shock`、`think`、`nod`、`shake`、`celebrate`。

当前表情：`neutral`、`confident`、`serious`、`puzzled`、`shocked`、`smile`、`tired`。

当前图解：`myth`、`not-faucet`、`compressor`、`no-super`、`runtime`、`never`、`tips`、`end`。

## 核心原则

```text
选题/资料 → LLM 写 Story JSON → 确定性组件渲染 → MP4
```

模型负责“导演”，组件负责稳定表现。相同 JSON、字体和版本应得到一致结果。

## 下一步

参见 `AGENTS.md` 与 `docs/ROADMAP.md`。优先补：自然中文 TTS、真实音频驱动时长、SVG/PNG 角色包、Revideo 适配器、文章到分镜 Agent、视觉回归测试。

MIT License。项目不打包或分发字体文件。
