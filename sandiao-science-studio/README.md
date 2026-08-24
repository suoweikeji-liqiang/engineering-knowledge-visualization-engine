# 沙雕科普动画工作室

一个可以直接交给 Codex 继续完善的 MVP：**Story JSON → 中文配音 → 角色/图解/字幕动画 → MP4**。

首条样片：`空调开到 16℃真的更省电吗？`。渲染样片随本次交付包单独提供，仓库保留可重复生成它的完整脚本与代码。

## 已实现

- 两套“小行星原理剧场”SVG 角色资产，支持动作帧、说话嘴型、镜像与锚点定位；程序化角色保留为回退后端。
- 8 个 JSON 分镜，包含对白、时长、角色状态、标题、图解、特效、转场和音效。
- MiMo 中文配音，支持 preset voice、Voice Design、Voice Clone、按角色风格和真实音频时长；未配置时回退到 `espeak`，没有 TTS 时仍可静音渲染。
- 误区卡片、机制流程、运行时间对比、温度计、节能建议等图解。
- 字幕烧录、片头标签、进度条、封面和 H.264 MP4。
- 151 个经过严格 manifest 校验的角色、背景、道具和图解 SVG；Story 语义不依赖具体绘图后端。
- 资产按 `brand`、`shared` 和领域包隔离；当前领域包括 `domain.hvac` 与
  `domain.ai-models`，每个包拥有独立 manifest，由 catalog 显式组合。

## 运行

要求：Python 3.11+、FFmpeg。项目已接入 MiMo 生产 TTS；未配置 MiMo 时可回退到 `espeak`/`espeak-ng`。

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .

sandiao validate stories/ac-16c.json
sandiao build stories/ac-16c.json --assets design/manifests/design-assets.json

# 只渲染前 10 秒设计样片
sandiao render stories/ac-16c.json \
  --assets design/manifests/design-assets.json \
  --duration 10 \
  --output output/ac-16c-observatory-voice-v2-10s.mp4
```

生产前检查与契约工具：

```bash
# 检查 Python、FFmpeg、字体、TTS、Story 和可选设计资产
sandiao doctor --story stories/ac-16c.json
sandiao doctor --story stories/ac-16c.json --assets design/manifests/design-assets.json --json

# 将旧 Story 确定性迁移为显式 schemaVersion 2.0，不覆盖源文件
sandiao migrate-story stories/ac-16c.json

# 单独严格校验设计资产
sandiao validate-assets design/manifests/design-assets.json

# 领域包也可单独校验
sandiao validate-assets design/assets/domains/hvac/manifest.json
sandiao validate-assets design/assets/domains/ai-models/manifest.json
```

首次使用先配置 MiMo：

```bash
cp .env.example .env
# 在 .env 中填写 MIMO_API_KEY；.env 已被 Git 忽略
```

`sandiao build` 和 `sandiao audio` 默认使用 `auto` 策略：存在 MiMo 凭证时使用 MiMo，否则回退到 espeak。也可以显式选择：

```bash
sandiao audio stories/ac-16c.json --tts-provider mimo
sandiao build stories/ac-16c.json --tts-provider espeak
```

## MiMo 多模态能力

```bash
# 生产级 TTS
sandiao mimo-tts "空调设定温度不是制冷功率旋钮。" output/probe.wav

# ASR / 音频理解
sandiao mimo-asr output/probe.wav

# 视频理解：支持本地小视频或 HTTPS URL
sandiao mimo-video output/ac-16c-sample.mp4 --fps 1
```

本地媒体通过 data URL 发送，默认上限约 27 MB；较大的视频应先压缩或放到可访问的 HTTPS 地址。调用失败会自动重试三次。分镜 TTS 缓存在 `build/audio/`，相同文本、模型和音色不会重复请求。

生成音频时会按真实配音时长扩展镜头，不再压缩或加速语音。解析结果写入与音频同名的 `*.timeline.json`（`schemaVersion: "1.0"`），渲染器会在 Story 指纹匹配时自动采用该时间线；Story 或角色声音配置变化后，旧时间线会自动失效。

输出：

```text
output/ac-16c-observatory.mp4
output/ac-16c-observatory-poster.png
output/ac-16c-voices-v2.wav
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

参见 `AGENTS.md` 与 `docs/UPGRADE_PLAN.md`。优先补：Story v2 显式资产引用、竖屏成片、文章到分镜 Agent、视觉回归 golden，以及全片 MiMo 发音评测。

MIT License。项目不打包或分发字体文件。
