# AI Agent Harness Benchmark

This benchmark validates the upgraded explanatory-video direction against a
reference style built from a continuous technical canvas, animated diagrams,
and an inspectable product-like execution trace.

The source of truth is `storyboard/story.json`. MiMo TTS resolves the real
duration of every shot into `audio/ai-agent-harness-benchmark.timeline.json`.
The Web motion renderer consumes that timeline instead of relying on guessed
scene durations.

Generated WAV, MP4, frame extracts, and QA reports are local render artifacts
and are excluded from Git.

## Reproduce locally

From the workspace root:

```bash
pnpm benchmark:audio
pnpm benchmark:render
```

`benchmark:audio` uses the existing MiMo integration and credentials from the
adjacent studio package. `benchmark:render` derives a browser-compatible audio
proxy from the WAV master, renders at 1920×1080/30 fps, and writes the final
MP4 to `final/ai-agent-harness-benchmark.mp4`.

The renderer accepts `CHROME_PATH`, `FFMPEG_PATH`, and `FFPROBE_PATH` when the
executables are not available from their usual macOS locations or `PATH`.
