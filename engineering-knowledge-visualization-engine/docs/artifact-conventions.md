# Artifact Conventions

## Purpose

This document defines how artifacts are organized, named, and managed throughout the pipeline.

---

## Artifact Lifecycle

The pipeline transforms a topic through these stages:

```
topic → outline → storyboard → scene manifest → rendered scenes → final video
```

Each stage produces inspectable, editable artifacts.

---

## Folder Layout

### Example Structure

```
examples/
  hvac-chiller-basics/
    outline/
      outline.json
    storyboard/
      storyboard.json
    scenes/
      scene-01-intro.json
      scene-02-components.json
      scene-03-cycle.json
    renders/
      scene-01-intro.mp4
      scene-02-components.mp4
      scene-03-cycle.mp4
    final/
      chiller-basics.mp4
      chiller-basics.srt
```

---

## Naming Conventions

### Topics
- Use kebab-case
- Prefix with domain: `hvac-chiller-basics`, `hvac-pid-intro`

### Outlines
- Single file: `outline.json`
- Contains lesson structure, learning objectives, section breakdown

### Storyboards
- Single file: `storyboard.json`
- Contains scene definitions, visual/narration intents, timing

### Scene Manifests
- Pattern: `scene-{number}-{slug}.json`
- Number with leading zeros: `scene-01`, `scene-02`
- Slug describes content: `intro`, `components`, `cycle`

### Rendered Scenes
- Match scene manifest names: `scene-01-intro.mp4`
- Keep intermediate renders for debugging

### Final Output
- Use topic name: `chiller-basics.mp4`
- Include subtitles: `chiller-basics.srt`

---

## Artifact Persistence

### Version Control
- Commit outlines and storyboards to git
- Do not commit large video files
- Use .gitignore for renders/ and final/ directories

### Editability
- All JSON artifacts must be human-readable
- Use 2-space indentation
- Include comments where schemas allow

### Re-runnability
- Each stage can be re-run independently
- Artifacts include enough context to regenerate downstream outputs
- Failed renders should not block inspection of scene manifests

---

## Stage Responsibilities

### topic-to-outline
- Input: topic description (text or structured input)
- Output: `outline.json`
- Defines learning objectives, section structure, key concepts

### outline-to-storyboard
- Input: `outline.json`
- Output: `storyboard.json`
- Defines scenes, visual/narration intents, timing estimates

### storyboard-to-scenes
- Input: `storyboard.json`
- Output: `scene-*.json` manifests
- Expands storyboard into detailed scene definitions

### scenes-to-video
- Input: `scene-*.json` manifests
- Output: rendered scene videos in `renders/`
- Generates technical animations and asset-based scenes

### final composition
- Input: rendered scenes, narration audio, subtitles
- Output: final video in `final/`
- Assembles scenes with narration, subtitles, chapter cards
