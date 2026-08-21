# Codex 工作说明

## 北极星

把中文科普脚本稳定地渲染为“人物对话 + 程序化图解”的短视频。核心资产是 Story JSON、角色动作库、图解组件库和评测闭环。

## 不可破坏的约束

1. Story JSON 是唯一内容契约；未来 Pillow、Revideo、Motion Canvas、Manim 都复用它。
2. 渲染必须确定性；LLM 不直接生成每一帧。
3. 后续必须改为“先生成真实音频，再解析镜头时长”。
4. 字体不进入仓库，自动发现系统中文字体。
5. schema 变更必须有版本和迁移说明。

## P0 任务

- 抽象 `TTSProvider`，保留 espeak，增加 Edge TTS 与本地 Kokoro。
- 新增 `ResolvedTimeline`，以真实音频时长自动扩展镜头。
- 增加 `doctor` 命令检查 FFmpeg、字体、TTS 与 Story。
- 覆盖 Windows、macOS、Linux 路径与进程调用。
- 生成关键帧 golden PNG，增加视觉回归测试。

## P1 任务

- `CharacterRenderer` 接口：procedural、SVG sprite、PNG pose pack。
- 新动作：walk、angry、laugh、cry、sweat、whisper、zoom。
- 新图解：流程图、时间线、折线图、架构图、代码卡片、公式卡片。
- 竖屏 9:16、自适应字幕、镜头推拉摇移。
- 新增 Revideo renderer，但不得改写 Story JSON 契约。

## P2 任务

- 主题/文章/PDF → Writer → Fact Checker → Storyboard Director → Story JSON。
- 连续性检查、字幕长度检查、视觉密度检查、镜头重复度检查。
- 样片评测：事实准确、字幕可读、音画同步、节奏、视觉重复度。

## Definition of Done

- `pytest` 通过。
- 示例 Story 可验证。
- 能生成封面。
- timeline/audio/render 改动必须人工检查至少一个 10 秒片段。
