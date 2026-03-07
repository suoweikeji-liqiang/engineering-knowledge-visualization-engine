#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-engineering-knowledge-visualization-engine}"
STAGE1_ALIAS="hvac-principle-animation-studio"

echo "==> Initializing repository: ${PROJECT_NAME}"

mkdir -p "${PROJECT_NAME}"
cd "${PROJECT_NAME}"

# ------------------------------------------------------------------------------
# Directory structure
# ------------------------------------------------------------------------------
mkdir -p \
  docs/decisions \
  apps/studio/src \
  apps/cli/src \
  packages/core/src/knowledge \
  packages/core/src/pedagogy \
  packages/core/src/storyboard \
  packages/core/src/visualization \
  packages/core/src/rendering \
  packages/core/src/evaluation \
  packages/schemas/src \
  packages/domain-hvac/src/glossary \
  packages/domain-hvac/src/entities \
  packages/domain-hvac/src/processes \
  packages/domain-hvac/src/teaching-patterns \
  packages/domain-hvac/src/review-rules \
  packages/generator-manim/src \
  packages/composer-remotion/src \
  packages/voice/src \
  packages/utils/src \
  assets/svg \
  assets/icons \
  assets/audio \
  assets/subtitles \
  assets/templates \
  examples/hvac-chiller-basics/input \
  examples/hvac-chiller-basics/outline \
  examples/hvac-chiller-basics/storyboard \
  examples/hvac-chiller-basics/render \
  examples/hvac-chilled-water-loop/input \
  examples/hvac-chilled-water-loop/outline \
  examples/hvac-chilled-water-loop/storyboard \
  examples/hvac-chilled-water-loop/render \
  examples/hvac-pid-intro/input \
  examples/hvac-pid-intro/outline \
  examples/hvac-pid-intro/storyboard \
  examples/hvac-pid-intro/render \
  pipelines/topic-to-outline \
  pipelines/outline-to-storyboard \
  pipelines/storyboard-to-scenes \
  pipelines/scenes-to-video \
  scripts \
  prompts/planner \
  prompts/storyboarder \
  prompts/reviewer \
  prompts/narrator

# ------------------------------------------------------------------------------
# Root files
# ------------------------------------------------------------------------------
cat > .gitignore <<'EOF'
node_modules/
dist/
build/
coverage/
.pnpm-store/
.env
.env.local
.DS_Store
*.log
*.tmp
*.swp
out/
tmp/
.cache/
EOF

cat > LICENSE <<'EOF'
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

cat > package.json <<EOF
{
  "name": "${PROJECT_NAME}",
  "version": "0.1.0",
  "private": true,
  "description": "Engineering Knowledge Visualization Engine",
  "packageManager": "pnpm@10.0.0",
  "scripts": {
    "dev": "node scripts/dev.ts",
    "build": "node scripts/build.ts",
    "bootstrap": "node scripts/bootstrap.ts",
    "lint": "echo 'lint not configured yet'",
    "typecheck": "tsc -p tsconfig.base.json --noEmit"
  }
}
EOF

cat > pnpm-workspace.yaml <<'EOF'
packages:
  - "apps/*"
  - "packages/*"
EOF

cat > tsconfig.base.json <<'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "declaration": false,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "baseUrl": "."
  },
  "exclude": ["node_modules", "dist", "build"]
}
EOF

cat > README.md <<EOF
# Engineering Knowledge Visualization Engine

Stage 1 alias: **${STAGE1_ALIAS}**

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

- \`apps/\` — app entry points
- \`packages/core/\` — engine core
- \`packages/schemas/\` — semantic schemas
- \`packages/domain-hvac/\` — HVAC domain pack
- \`packages/generator-manim/\` — technical scene generation
- \`packages/composer-remotion/\` — video composition
- \`packages/voice/\` — narration / TTS integration
- \`examples/\` — sample lessons
- \`docs/\` — philosophy, boundaries, roadmap, architecture, schemas

## Phase 1 Sample Lessons

1. Chiller Basics
2. Chilled Water Loop
3. PID Intro for HVAC
EOF

# ------------------------------------------------------------------------------
# Docs
# ------------------------------------------------------------------------------
cat > docs/philosophy.md <<'EOF'
# Philosophy

## 1. Why this project exists

Engineering knowledge is often difficult to explain, difficult to reuse, and difficult to transfer.

In many companies, the most valuable knowledge does not only live in documents or code. It lives in:

- system understanding
- engineering experience
- causal reasoning
- control logic
- practical explanation patterns

This project exists to make that knowledge easier to express, visualize, teach, and reuse.

Its purpose is not merely to generate videos.  
Its purpose is to transform complex engineering knowledge into structured explanatory assets.

---

## 2. What this project is

This project is an engineering knowledge visualization engine.

It converts engineering knowledge into:

- structured teaching outlines
- storyboards
- principle animations
- algorithm demonstrations
- narration scripts
- reusable teaching assets

Video is only one output form.  
The deeper goal is knowledge expression and reusable explanation.

---

## 3. What this project is not

This project is not:

- a movie-style video generation system
- a generic video editing platform
- a pure subtitle or dubbing tool
- a content farm for low-value mass generation
- a black-box system that hides all intermediate reasoning and artifacts

The project should not be driven by novelty or visual spectacle.  
It should be driven by clarity, correctness, and reusability.

---

## 4. Core beliefs

### 4.1 Expression over generation

The goal is not to generate more content.  
The goal is to explain complex knowledge clearly.

### 4.2 Assets over one-off outputs

The project should accumulate reusable assets, not just isolated mp4 files.

Important assets include:

- concept structures
- terminology systems
- domain rules
- teaching patterns
- storyboard patterns
- visual templates
- review rules

### 4.3 Stable semantics over tool dependence

Models, APIs, TTS engines, and renderers may change.  
The semantic layer should remain stable.

This project values:

- explicit schemas
- structured intermediate representations
- inspectable artifacts
- replaceable toolchains

### 4.4 Human-guided intelligence over black-box automation

AI should drive the workflow, but intermediate outputs must remain inspectable, editable, and re-runnable.

### 4.5 Domain grounding over generic fluency

Engineering content must be grounded in domain meaning, not just plausible language.

Correctness, causality, process logic, and control relationships matter more than fluent wording.

---

## 5. Long-term vision

The long-term goal is not limited to HVAC.

The long-term goal is to build a general engine that can be extended across engineering domains through domain packs.

Possible future domains include:

- industrial control
- electrical systems
- process engineering
- building automation
- energy systems

The engine remains generic.  
Domain knowledge is plugged in through structured domain packs.

---

## 6. Phase 1 mission

Phase 1 starts with HVAC.

The mission of Phase 1 is:

- to prove that complex HVAC knowledge can be transformed into high-quality visual teaching assets
- to establish the engine/domain-pack boundary
- to define the semantic schemas
- to validate the split between technical scene generation and final composition

The first phase is successful if it can reliably produce a small set of representative assets:

- equipment principle animation
- system flow animation
- control algorithm animation

---

## 7. Decision principle

When choosing features or directions, always ask:

1. Does this improve knowledge expression?
2. Does this create reusable assets?
3. Does this belong to the engine or to a domain pack?
4. Does this strengthen or weaken the semantic layer?
5. Does this keep the system focused on engineering explanation rather than generic video processing?
EOF

cat > docs/boundaries.md <<'EOF'
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
EOF

cat > docs/roadmap.md <<'EOF'
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
EOF

cat > docs/architecture.md <<'EOF'
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
EOF

cat > docs/schemas.md <<'EOF'
# Schemas

## 1. Purpose

Schemas define the stable semantic layer of the project.

They ensure that:

- workflows remain inspectable
- models can be swapped
- renderers can be replaced
- artifacts can be saved and re-run
- engine and domain responsibilities remain separated

---

## 2. Initial schema set

Phase 1 defines the following schema families:

### 2.1 Concept
Represents a knowledge concept.

Example fields:
- id
- name
- description
- prerequisites
- related_concepts

### 2.2 Entity
Represents a physical or logical engineering object.

Example fields:
- id
- name
- type
- attributes
- components
- domain_tags

### 2.3 Process
Represents a process or flow.

Example fields:
- id
- name
- steps
- inputs
- outputs
- causal_notes

### 2.4 Control Loop
Represents a control relationship.

Example fields:
- id
- controlled_variable
- manipulated_variable
- feedback_source
- constraints
- explanation_notes

### 2.5 Scene
Represents a renderable instructional unit.

Example fields:
- id
- title
- scene_type
- target_renderer
- visual_intent
- narration_intent
- timing

### 2.6 Narration Intent
Represents why narration exists for the scene.

Example fields:
- goal
- audience_level
- explanation_style
- emphasis_points

### 2.7 Visual Intent
Represents how the scene should communicate visually.

Example fields:
- primary_objects
- visual_pattern
- highlight_targets
- motion_type
- diagram_style

### 2.8 Timing
Represents temporal structure.

Example fields:
- estimated_duration_sec
- beat_points
- sync_targets

---

## 3. Principles

- Schemas should be explicit, small, and evolvable.
- Schemas should describe semantics, not renderer-specific implementation details.
- Renderer-specific details should be derived downstream where possible.
EOF

# ------------------------------------------------------------------------------
# ADRs
# ------------------------------------------------------------------------------
cat > docs/decisions/0001-project-scope.md <<'EOF'
# ADR 0001: Project Scope

## Status
Accepted

## Context
The project could easily drift into generic video generation, content production tooling, or external video reconstruction.

## Decision
Phase 1 will focus on HVAC engineering knowledge explanation through structured visual teaching assets.

## Consequences
- Better focus
- Faster validation
- Lower architectural drift
- Clearer quality criteria
EOF

cat > docs/decisions/0002-engine-vs-domain-pack.md <<'EOF'
# ADR 0002: Engine vs Domain Pack

## Status
Accepted

## Context
Engineering knowledge differs by domain, but the transformation pipeline should remain reusable.

## Decision
The repository will separate:
- domain-agnostic engine logic
- domain-specific knowledge packs

HVAC will be implemented as the first domain pack.

## Consequences
- Better long-term extensibility
- Cleaner ownership boundaries
- Lower coupling between content and engine
EOF

cat > docs/decisions/0003-manim-remotion-split.md <<'EOF'
# ADR 0003: Manim vs Remotion Split

## Status
Accepted

## Context
The project needs both technical animation and final composition.

## Decision
- Manim will be used for technical and algorithmic animation scenes.
- Remotion will be used for composition, subtitles, narration sync, and final packaging.

## Consequences
- Cleaner renderer roles
- Better specialization
- Easier future replacement or extension
EOF

# ------------------------------------------------------------------------------
# App/package READMEs
# ------------------------------------------------------------------------------
cat > apps/studio/README.md <<'EOF'
# Studio App

Future visual workbench for inspecting and editing outlines, storyboards, scenes, and outputs.
EOF

cat > apps/cli/README.md <<'EOF'
# CLI App

Command-line entry point for bootstrapping pipelines and running sample workflows.
EOF

cat > packages/core/README.md <<'EOF'
# Core

Domain-agnostic engine logic for transforming engineering knowledge into visual teaching artifacts.
EOF

cat > packages/schemas/README.md <<'EOF'
# Schemas

Stable semantic layer for concepts, entities, processes, control loops, scenes, narration intent, visual intent, and timing.
EOF

cat > packages/domain-hvac/README.md <<'EOF'
# HVAC Domain Pack

HVAC-specific glossary, entities, processes, teaching patterns, visual conventions, and review rules.
EOF

cat > packages/generator-manim/README.md <<'EOF'
# Generator Manim

Technical scene generation layer for algorithm and principle-focused animations.
EOF

cat > packages/composer-remotion/README.md <<'EOF'
# Composer Remotion

Composition layer for subtitles, narration sync, chapter cards, and final video assembly.
EOF

cat > packages/voice/README.md <<'EOF'
# Voice

Narration generation, TTS integration, and timing alignment.
EOF

cat > packages/utils/README.md <<'EOF'
# Utils

Shared utility functions used across packages.
EOF

# ------------------------------------------------------------------------------
# Minimal source stubs
# ------------------------------------------------------------------------------
cat > packages/core/src/index.ts <<'EOF'
export * from "./knowledge";
export * from "./pedagogy";
export * from "./storyboard";
export * from "./visualization";
export * from "./rendering";
export * from "./evaluation";
EOF

for d in knowledge pedagogy storyboard visualization rendering evaluation; do
  upper_name="$(printf '%s' "$d" | tr '[:lower:]' '[:upper:]')"
  cat > "packages/core/src/${d}/index.ts" <<EOF
export const ${upper_name}_MODULE = "${d}";
EOF
done

cat > packages/schemas/src/concept.ts <<'EOF'
export type Concept = {
  id: string;
  name: string;
  description?: string;
  prerequisites?: string[];
  relatedConcepts?: string[];
};
EOF

cat > packages/schemas/src/entity.ts <<'EOF'
export type Entity = {
  id: string;
  name: string;
  type: string;
  attributes?: Record<string, unknown>;
  components?: string[];
  domainTags?: string[];
};
EOF

cat > packages/schemas/src/process.ts <<'EOF'
export type Process = {
  id: string;
  name: string;
  steps: string[];
  inputs?: string[];
  outputs?: string[];
  causalNotes?: string[];
};
EOF

cat > packages/schemas/src/control-loop.ts <<'EOF'
export type ControlLoop = {
  id: string;
  controlledVariable: string;
  manipulatedVariable: string;
  feedbackSource: string;
  constraints?: string[];
  explanationNotes?: string[];
};
EOF

cat > packages/schemas/src/scene.ts <<'EOF'
export type Scene = {
  id: string;
  title: string;
  sceneType: string;
  targetRenderer: "manim" | "remotion" | "asset-based";
  visualIntentId?: string;
  narrationIntentId?: string;
  timingId?: string;
};
EOF

cat > packages/schemas/src/narration-intent.ts <<'EOF'
export type NarrationIntent = {
  id: string;
  goal: string;
  audienceLevel?: "beginner" | "intermediate" | "advanced";
  explanationStyle?: string;
  emphasisPoints?: string[];
};
EOF

cat > packages/schemas/src/visual-intent.ts <<'EOF'
export type VisualIntent = {
  id: string;
  primaryObjects: string[];
  visualPattern?: string;
  highlightTargets?: string[];
  motionType?: string;
  diagramStyle?: string;
};
EOF

cat > packages/schemas/src/timing.ts <<'EOF'
export type Timing = {
  id: string;
  estimatedDurationSec: number;
  beatPoints?: number[];
  syncTargets?: string[];
};
EOF

cat > packages/schemas/src/index.ts <<'EOF'
export * from "./concept";
export * from "./entity";
export * from "./process";
export * from "./control-loop";
export * from "./scene";
export * from "./narration-intent";
export * from "./visual-intent";
export * from "./timing";
EOF

cat > packages/domain-hvac/src/index.ts <<'EOF'
export const HVAC_DOMAIN_PACK = "hvac-domain-pack-v0";
EOF

cat > packages/generator-manim/src/index.ts <<'EOF'
export const MANIM_GENERATOR = "generator-manim";
EOF

cat > packages/composer-remotion/src/index.ts <<'EOF'
export const REMOTION_COMPOSER = "composer-remotion";
EOF

cat > packages/voice/src/index.ts <<'EOF'
export const VOICE_MODULE = "voice";
EOF

cat > packages/utils/src/index.ts <<'EOF'
export const UTILS_MODULE = "utils";
EOF

# ------------------------------------------------------------------------------
# Scripts
# ------------------------------------------------------------------------------
cat > scripts/bootstrap.ts <<'EOF'
console.log("Bootstrap placeholder: install dependencies and validate repo layout.");
EOF

cat > scripts/dev.ts <<'EOF'
console.log("Dev placeholder: run local development workflow.");
EOF

cat > scripts/build.ts <<'EOF'
console.log("Build placeholder: run package builds and validations.");
EOF

# ------------------------------------------------------------------------------
# Prompts
# ------------------------------------------------------------------------------
cat > prompts/planner/README.md <<'EOF'
# Planner Prompts

Prompts for converting topics into structured outlines.
EOF

cat > prompts/storyboarder/README.md <<'EOF'
# Storyboarder Prompts

Prompts for converting outlines into storyboard artifacts.
EOF

cat > prompts/reviewer/README.md <<'EOF'
# Reviewer Prompts

Prompts for checking clarity, correctness, and consistency.
EOF

cat > prompts/narrator/README.md <<'EOF'
# Narrator Prompts

Prompts for narration script generation and spoken style control.
EOF

# ------------------------------------------------------------------------------
# Example READMEs + placeholders
# ------------------------------------------------------------------------------
cat > examples/hvac-chiller-basics/README.md <<'EOF'
# Example: Chiller Basics

Representative sample for validating equipment principle explanation.
EOF

cat > examples/hvac-chilled-water-loop/README.md <<'EOF'
# Example: Chilled Water Loop

Representative sample for validating system flow explanation.
EOF

cat > examples/hvac-pid-intro/README.md <<'EOF'
# Example: PID Intro for HVAC

Representative sample for validating control algorithm explanation.
EOF

cat > examples/hvac-chiller-basics/outline/outline.json <<'EOF'
{
  "topic": "Chiller Basics",
  "status": "placeholder"
}
EOF

cat > examples/hvac-chilled-water-loop/outline/outline.json <<'EOF'
{
  "topic": "Chilled Water Loop",
  "status": "placeholder"
}
EOF

cat > examples/hvac-pid-intro/outline/outline.json <<'EOF'
{
  "topic": "PID Intro for HVAC",
  "status": "placeholder"
}
EOF

# ------------------------------------------------------------------------------
# Pipeline placeholders
# ------------------------------------------------------------------------------
cat > pipelines/topic-to-outline/README.md <<'EOF'
# topic-to-outline

Pipeline for converting a topic into a structured lesson outline.
EOF

cat > pipelines/outline-to-storyboard/README.md <<'EOF'
# outline-to-storyboard

Pipeline for converting a structured outline into storyboard artifacts.
EOF

cat > pipelines/storyboard-to-scenes/README.md <<'EOF'
# storyboard-to-scenes

Pipeline for converting storyboard artifacts into renderable scene manifests.
EOF

cat > pipelines/scenes-to-video/README.md <<'EOF'
# scenes-to-video

Pipeline for composing scenes, narration, subtitles, and final video output.
EOF

# ------------------------------------------------------------------------------
# Helpful marker file
# ------------------------------------------------------------------------------
cat > .repo-init-summary.txt <<EOF
Repository initialized successfully.

Project name: ${PROJECT_NAME}
Stage 1 alias: ${STAGE1_ALIAS}

Key docs:
- README.md
- docs/philosophy.md
- docs/boundaries.md
- docs/roadmap.md
- docs/architecture.md
- docs/schemas.md

Next recommended steps:
1. Initialize git: git init
2. Create first commit
3. Define schema JSON examples
4. Implement topic-to-outline stub
5. Implement outline-to-storyboard stub
6. Start HVAC domain pack v0
EOF

echo "==> Repository structure created."
echo "==> Next steps:"
echo "    cd ${PROJECT_NAME}"
echo "    git init"
echo "    git add ."
echo "    git commit -m 'chore: initialize engineering knowledge visualization engine'"

