# Personal IP animation language

This note turns the useful directing pattern in liliMozi's Bilibili work into a
reusable rule for Asteroid AI Observatory videos. It borrows the narrative
structure, not the referenced character design or individual shots.

## References

- [HanaAgent introduction](https://www.bilibili.com/video/BV11q8J6CEZS/)
- [DeepSeek Harness explainer](https://www.bilibili.com/video/BV14cgp6TEBQ/)

## Three character roles

1. **Home-base host** — opens the subject in a recognizable room or desk scene.
2. **Narrative actor** — reacts to failure, enters a metaphor, or creates a
   chapter turn. The pose must add meaning instead of decorating a layout.
3. **Explainer** — points to the final model, comparison, or decision and closes
   the loop with the audience.

Technical evidence, diagrams, code, screenshots, and timelines remain separate
visual modes. The character returns between them to restore continuity and
intimacy.

## Production rules

- Character-led frames should occupy roughly 20–30% of a technical explainer.
- Use at least two poses and two narrative roles; never pin one portrait to the
  corner for the whole video.
- Preserve identity anchors across every pose: purple-black hair, gold planet
  hair clip, round glasses, warm studio light, and notebook materials.
- Bridge the warm character art and dark technical canvas with a consistent
  paper frame, tape, caption treatment, and Asteroid brand mark.
- A character frame must coincide with a hook, emotional turn, analogy, or
  synthesis. If removing it changes nothing, the frame is not doing a job.
- Keep narration subtitles in the bottom safe zone and keep character labels
  inside their own paper frame.

## Brand palette

Use a `70 / 20 / 10` distribution instead of a full-screen cyber-dark theme:

- **70% warm paper** — parchment background, cream cards, warm gray grid;
- **20% technical ink** — terminal, code, trace header, and high-contrast inset;
- **10% semantic accents** — planet purple, marker gold, observation red,
  teal, and success green.

The canonical renderer tokens live in
`packages/renderer-revideo/src/theme.ts`. Domain packs may select a dominant
accent, but should not replace the shared paper, ink, and character colors.

## Benchmark application

The `ai-agent-harness-benchmark` uses three Xiaolan frames:

- desk host for the opening question;
- surprised reaction beside the failed execution trace;
- pointing explainer beside `AGENT = MODEL × RUNTIME`.

The loop, tool, Harness, and execution sections stay diagram-led so the personal
IP strengthens the explanation without replacing it.
