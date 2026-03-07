# Engineering Knowledge Visualization Engine

Stage 1 alias: **hvac-principle-animation-studio**

An engine for transforming complex engineering knowledge into structured explanations, visual animations, and reusable teaching assets.

## Phase 1 Focus

- HVAC principle animation
- HVAC system flow explanation
- HVAC control algorithm visualization

## Non-Goals

- Movie-style video generation
- General-purpose video editing platform
- Full automatic black-box one-click generation
- External video reconstruction as the main workflow

## Core Layers

- Knowledge Layer
- Pedagogy Layer
- Rendering Layer

## Tech Direction

- Manim for technical / algorithmic animation
- Remotion for composition, subtitles, narration, and final rendering

## First Deliverables

- Chiller basics animation
- Chilled water loop animation
- PID intro animation

## Repository Structure

- `apps/` — app entry points
- `packages/core/` — engine core
- `packages/schemas/` — semantic schemas
- `packages/domain-hvac/` — HVAC domain pack
- `packages/generator-manim/` — technical scene generation
- `packages/composer-remotion/` — video composition
- `packages/voice/` — narration / TTS integration
- `examples/` — sample lessons
- `docs/` — philosophy, boundaries, roadmap, architecture, schemas

## Phase 1 Sample Lessons

1. Chiller Basics
2. Chilled Water Loop
3. PID Intro for HVAC
