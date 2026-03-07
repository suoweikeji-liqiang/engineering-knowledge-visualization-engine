# Boundaries

## 1. Purpose of this document

This document defines the current scope of the project so that implementation remains focused and does not drift into unrelated product directions.

---

## 2. In-scope for Phase 1

Phase 1 focuses on engineering explanation for HVAC.

### 2.1 Content types

The system should support:

- equipment principle explanation
- system flow explanation
- control algorithm explanation

### 2.2 Representative examples

Examples include:

- chiller basics
- chilled water loop
- cooling water loop
- AHU principle
- PID introduction
- differential pressure control
- basic MPC explanation

### 2.3 Output forms

Phase 1 may produce:

- animation scenes
- narrated explanatory videos
- subtitles
- chapter cards
- reusable scene assets
- structured teaching artifacts

### 2.4 Core workflow

Phase 1 should support the following logical flow:

topic -> outline -> storyboard -> scenes -> composition -> output

### 2.5 Technical direction

Phase 1 will primarily use:

- Manim for technical and algorithmic scenes
- Remotion for composition and final assembly
- TTS for narration
- structured schemas for intermediate representations

---

## 3. Explicit non-goals for Phase 1

### 3.1 Not a movie-style generation system

The project does not target:

- realistic character animation
- lip sync
- cinematic storytelling
- film-style camera movement
- photorealistic scene generation

### 3.2 Not a generic video editing platform

The project does not aim to replace professional editing tools.

### 3.3 Not a one-click black-box generator

Intermediate artifacts must remain inspectable and editable.

### 3.4 Not external video reconstruction as the main workflow

External videos may be used as references, inspiration sources, or teaching analysis material.  
However, automatic reconstruction of external videos is not a core Phase 1 workflow.

### 3.5 Not a multi-tenant product platform

Phase 1 does not include:

- permissions
- collaboration systems
- tenant management
- workflow dashboards for multiple teams
- large-scale production orchestration

### 3.6 Not a full knowledge base product

This project may connect to a knowledge base in the future, but Phase 1 does not attempt to build the full knowledge platform.

---

## 4. Engine vs domain boundaries

### 4.1 Engine responsibilities

The engine owns:

- semantic schemas
- pipeline orchestration
- pedagogy and storyboard flow
- render pipeline abstraction
- evaluation hooks
- reusable composition logic

### 4.2 HVAC domain pack responsibilities

The HVAC domain pack owns:

- glossary
- entities and components
- process definitions
- teaching patterns
- visual conventions
- domain review rules

---

## 5. Quality boundaries

Phase 1 should optimize for:

- clarity
- correctness
- consistency
- inspectability
- reusability

Phase 1 should not optimize for:

- extreme visual richness
- maximal automation at any cost
- supporting every content type
- supporting every engineering domain immediately

---

## 6. Expansion boundaries

Future expansion is allowed only if it preserves the engine architecture.

This means:

- new domains should arrive as domain packs
- new renderers should plug into existing semantic layers
- new workflows should not bypass schemas and intermediate artifacts

Any major expansion that weakens the semantic layer or merges engine and domain concerns should be rejected.
