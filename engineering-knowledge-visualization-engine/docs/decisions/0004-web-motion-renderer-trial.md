# ADR 0004: Trial a Web Motion Renderer for Continuous Technical Canvases

## Status

Trial

## Context

ADR 0003 assigns mathematical and algorithmic animation to Manim and final
packaging to Remotion. The benchmark references add a third visual need:
continuous technical canvases that mix diagrams, product-like UI, terminal
traces, camera focus, and narration-driven motion in one inspectable scene.

The existing Pillow prototype is useful for diagnostics and asset previews,
but it is too low-level to be the primary renderer for this visual language.

## Decision

- Trial Revideo 0.11 as an isolated TypeScript Web motion renderer.
- Keep Story and resolved narration timelines as the source of truth.
- Keep Manim for specialist mathematical or algorithmic shots.
- Keep the existing composition boundary; this trial does not make renderer
  details part of the semantic schemas.
- Keep Pillow as a diagnostic and fallback renderer, not the benchmark path.

The trial package is `packages/renderer-revideo`. Its first acceptance artifact
is `examples/ai-agent-harness-benchmark`.

## Consequences

- Technical diagrams and product UI can share a programmable scene graph.
- Real MiMo narration durations drive shot timing before frames are rendered.
- Browser, FFmpeg, and media-path behavior must be tested as runtime concerns.
- Revideo remains replaceable because the benchmark consumes Story artifacts,
  not Revideo-specific prompts or domain knowledge.
- A production adoption decision will follow evaluation of rendering stability,
  concurrency, licensing, and long-term maintenance.
