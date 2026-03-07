# Roadmap

## Phase 1 Goal

Build the first usable version of the engineering knowledge visualization workflow for HVAC.

Phase 1 should prove that the system can turn a topic into a structured outline, storyboard, animated scenes, and a final narrated video while preserving inspectability and reusable assets.

---

## Phase 1A — Foundation and Scope Lock

### Objectives

- lock project philosophy
- lock boundaries
- define engine vs domain split
- define initial schemas
- establish repo structure

### Deliverables

- README
- philosophy.md
- boundaries.md
- roadmap.md
- architecture draft
- schema draft
- initial monorepo scaffold
- ADR documents for key scope decisions

### Exit criteria

- repository can be bootstrapped
- core docs exist
- engine/domain boundary is explicit
- semantic layer draft is documented

---

## Phase 1B — Semantic Core

### Objectives

- define the initial intermediate representations
- make the workflow inspectable
- ensure artifacts can be saved, edited, and re-run

### Deliverables

- concept schema
- entity schema
- process schema
- control loop schema
- scene schema
- narration intent schema
- visual intent schema
- timing schema
- JSON examples for all schemas

### Exit criteria

- at least 3 example topics can be represented with the schemas
- schemas are versioned
- examples are stored in the repo

---

## Phase 1C — HVAC Domain Pack v0

### Objectives

- create the first domain pack
- establish HVAC-specific reusable assets

### Deliverables

- HVAC glossary
- HVAC entity catalog
- HVAC process definitions
- HVAC teaching patterns
- HVAC review rules
- visual conventions for HVAC diagrams

### Initial focus

- chiller
- chilled water loop
- AHU
- PID basics

### Exit criteria

- domain pack can support the first three sample lessons
- domain review rules can be applied during review

---

## Phase 1D — Outline and Storyboard Pipeline

### Objectives

- turn topics into structured outlines
- turn outlines into storyboard artifacts

### Deliverables

- topic-to-outline pipeline
- outline-to-storyboard pipeline
- planner prompts
- storyboarder prompts
- artifact persistence format
- first review pass hooks

### Exit criteria

- sample topic can generate outline
- outline can generate storyboard
- storyboard is editable and saved as structured artifact

---

## Phase 1E — Scene Generation

### Objectives

- generate technical scenes from storyboard artifacts

### Deliverables

- Manim scene generator for algorithm/technical visuals
- asset-based scene generator for simple principle visuals
- scene render manifest
- local render scripts

### Exit criteria

- at least 3 representative scenes can be rendered
- scene generation is linked to structured scene definitions
- failed scenes are debuggable and re-runnable

---

## Phase 1F — Composition and Narration

### Objectives

- assemble scenes into a final explanatory video

### Deliverables

- narration generation
- TTS integration
- subtitle generation
- Remotion composition templates
- final video assembly workflow

### Exit criteria

- one complete lesson video can be rendered end-to-end
- subtitles and narration are aligned to scene timing
- composition is template-based, not hardcoded per lesson

---

## Phase 1G — Evaluation and Sample Lessons

### Objectives

- validate quality on representative lessons
- create reusable sample assets

### Deliverables

- quality checklist
- review prompts
- sample outputs for:
  - chiller basics
  - chilled water loop
  - PID intro
- issue list for Phase 2

### Exit criteria

- all three sample lessons can run through the pipeline
- review process can identify major clarity/correctness issues
- reusable assets are committed into examples and domain pack

---

## Phase 1 success criteria

Phase 1 is successful if:

1. The project has a stable engine/domain structure.
2. Intermediate semantic artifacts are explicit and inspectable.
3. At least three HVAC sample lessons can be produced end-to-end.
4. Reusable domain assets exist.
5. The workflow proves that the system is an engineering knowledge visualization engine rather than a generic video generator.
