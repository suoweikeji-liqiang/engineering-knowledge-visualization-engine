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
