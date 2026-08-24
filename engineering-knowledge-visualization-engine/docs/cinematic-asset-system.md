# Cinematic asset system

The current benchmark improved brand consistency, evidence grounding, character continuity, and tactile motion. It still differs from the reference explainers in one important way: too many chapters are complete compositions that enter and leave as a unit. A mature explainer changes state inside the shot—numbers grow, a curve is traced, code advances through a call stack, and visual objects carry meaning across cuts.

This system therefore separates three asset layers.

## 1. Narrative scene assets

These answer “where are we in the story?”

- `host-home-base`: recurring location, host, prop, and central question.
- `evidence-to-abstraction`: source page → highlighted claim → semantic diagram.
- `character-metaphor`: character action → explicit concept mapping → mechanism diagram.
- `technical-trace`: task → state changes → observations → verified outcome.
- `character-synthesis`: host returns and turns facts into a bounded personal judgment.

## 2. Explanation animation assets

These answer “how does this technical fact change over time?”

| Family | Semantic input | Motion beats | Required review |
|---|---|---|---|
| Growth bars | labels, values, unit, baseline, source | baseline → staggered growth → value → insight | zero/non-zero baseline, source, precision |
| Trend curve | points, phases, unit, source | axes → traced path → nodes → phase explanation | measured vs conceptual curve |
| Number counter | value, unit, baseline, delta | baseline → count → comparison | final value and significant digits |
| Code walkthrough | source ref, lines, focus steps, call stack, output | file → focus line → call stack → result | source version and reproducibility |
| System trace | input, steps, state, failure branch, outcome | task injection → pulse → state update → exit | failure path and exit condition |
| Before/after morph | paired objects and invariant anchors | establish before → preserve anchors → morph → after | comparable scale and meaning |

Charts and code are not decorative inserts. Every motion beat must correspond to a narration beat or an observable event.

## 3. Character performance assets

These answer “what is the host doing for the story?”

- establish: desk, observatory, entry, look-to-camera;
- question: pause, inspect, point at an anomaly;
- react: surprise, doubt, failed attempt, recovery;
- demonstrate: walk, connect, sort, open, compare;
- synthesize: point to the final model, write a note, return to the opening prop.

Each performance has identity anchors, action, gaze target, emotional intensity, compatible locations, and transition hooks. A portrait with no narrative job is not a performance asset.

## Accumulation boundary

- `packages/schemas` owns stable scene and beat semantics.
- `packages/domain-ai` owns AI concept metaphors, scene catalog entries, and review rules.
- renderers own visual implementation and animation timing.
- episodes own claims, values, source excerpts, code references, and selected media.
- `ai_daily_brief_factory_v3/templates/cinematic_context_deck` is the production implementation that receives these assets.

Asset variants share an `accumulationKey`, for example `ai/explanation/chart/curve` or `ai/character-metaphor/agent-loop`. A new episode binds inputs to an existing key; it does not fork the renderer.

## Next reusable assets

1. dual-series curve with threshold crossing;
2. ranking bars that reorder while preserving identity;
3. code diff that morphs into an execution trace;
4. error branch with retry and recovery state;
5. character action sheets for inspect, connect, compare, and recover;
6. sound cues for marker draw, data pulse, terminal result, and chapter return.
