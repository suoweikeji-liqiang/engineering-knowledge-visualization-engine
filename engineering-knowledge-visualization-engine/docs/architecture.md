# Architecture

## 1. High-level architecture

The system is split into three major layers:

- Knowledge Layer
- Pedagogy Layer
- Rendering Layer

A separate HVAC domain pack supplies domain knowledge without polluting the generic engine.

---

## 2. Layers

### 2.1 Knowledge Layer

Responsible for representing:

- concepts
- entities
- processes
- control loops
- terminology
- domain relationships

### 2.2 Pedagogy Layer

Responsible for converting knowledge into:

- outlines
- lesson structure
- storyboard artifacts
- narration intent
- visual intent
- timing suggestions

### 2.3 Rendering Layer

Responsible for converting structured pedagogical artifacts into:

- technical scenes
- animation assets
- narration audio
- subtitles
- final composed video

---

## 3. Engine vs domain pack

### Engine

The engine should remain domain-agnostic and own:

- schema definitions
- transformation pipelines
- orchestration
- scene composition abstractions
- evaluation hooks

### HVAC domain pack

The HVAC pack should own:

- glossary
- entity definitions
- process definitions
- teaching patterns
- review rules
- visual conventions

---

## 4. Tool split

### Manim

Used for:

- algorithm explanation
- curves
- signals
- control logic
- abstract principle visuals

### Remotion

Used for:

- composition
- chapter cards
- subtitles
- narration sync
- final assembly
- template-driven packaging

---

## 5. Design constraints

- Intermediate artifacts must be inspectable.
- Schemas must be explicit and versionable.
- Pipelines must support partial re-run.
- Domain knowledge must not be hardcoded into the engine.
- Renderers must plug into structured semantic artifacts rather than freeform prompts alone.

---

## 6. Initial sample lessons

The initial architecture is validated through three representative lessons:

1. Chiller Basics
2. Chilled Water Loop
3. PID Intro for HVAC
