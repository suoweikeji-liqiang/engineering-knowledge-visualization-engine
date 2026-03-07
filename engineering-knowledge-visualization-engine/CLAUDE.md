# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Engineering Knowledge Visualization Engine focused on transforming complex engineering knowledge into structured explanations, visual animations, and reusable teaching assets. Phase 1 targets HVAC principle animation.

## Core Architecture

The system is organized into three layers:

1. **Knowledge Layer** - Represents concepts, entities, processes, control loops, and domain relationships
2. **Pedagogy Layer** - Converts knowledge into outlines, storyboards, narration intent, visual intent, and timing
3. **Rendering Layer** - Converts pedagogical artifacts into technical scenes, animations, narration audio, and final video

### Engine vs Domain Pack Separation

- **Engine** (domain-agnostic): schemas, transformation pipelines, orchestration, scene composition abstractions, evaluation hooks
- **HVAC Domain Pack** (domain-specific): glossary, entity definitions, process definitions, teaching patterns, review rules, visual conventions

Domain knowledge must never be hardcoded into the engine. New domains should arrive as separate domain packs.

### Rendering Split

- **Manim**: Technical/algorithmic animation, curves, signals, control logic, abstract principle visuals
- **Remotion**: Composition, chapter cards, subtitles, narration sync, final assembly

## Commands

```bash
# Development
pnpm dev

# Build
pnpm build

# Bootstrap
pnpm bootstrap

# Type checking
pnpm typecheck
```

## Repository Structure

- `apps/` - Application entry points (studio, cli)
- `packages/core/` - Engine core with knowledge, pedagogy, storyboard, visualization, rendering, evaluation modules
- `packages/schemas/` - Semantic schemas (concept, entity, process, control-loop, scene, narration-intent, visual-intent, timing)
- `packages/domain-hvac/` - HVAC domain pack
- `packages/generator-manim/` - Technical scene generation
- `packages/composer-remotion/` - Video composition
- `packages/voice/` - Narration/TTS integration
- `packages/utils/` - Shared utilities
- `examples/` - Sample lessons (chiller-basics, chilled-water-loop, pid-intro)
- `pipelines/` - Transformation pipelines (topic-to-outline, outline-to-storyboard, storyboard-to-scenes, scenes-to-video)
- `prompts/` - AI agent prompts (planner, storyboarder, reviewer, narrator)
- `docs/` - Philosophy, boundaries, roadmap, architecture, schemas, ADRs

## Key Principles

1. **Intermediate artifacts must be inspectable** - No black-box generation
2. **Schemas must be explicit and versionable** - Stable semantic layer independent of tools
3. **Pipelines must support partial re-run** - Workflows remain editable at each stage
4. **Domain knowledge stays in domain packs** - Engine remains generic
5. **Renderers plug into semantic artifacts** - Not freeform prompts alone

## Workflow

The logical flow is: `topic → outline → storyboard → scenes → composition → output`

Each stage produces structured, inspectable artifacts defined by schemas.

## Tech Stack

- pnpm workspace monorepo
- TypeScript (ES2022, ESNext modules, strict mode)
- Manim (Python) for technical animations
- Remotion (React) for composition

## What This Project Is NOT

- Not a movie-style video generation system
- Not a generic video editing platform
- Not a one-click black-box generator
- Not focused on visual spectacle over clarity and correctness
- Not attempting to support every content type or domain immediately

## Phase 1 Focus

Validate the architecture through three representative HVAC lessons:
1. Chiller Basics
2. Chilled Water Loop
3. PID Intro for HVAC
