import fs from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const example = path.join(root, 'examples', 'ai-agent-harness-complete');
const [story, citations, coverage, rubric, visualTimeline] = await Promise.all([
  fs.readFile(path.join(example, 'storyboard', 'story.json'), 'utf8').then(JSON.parse),
  fs.readFile(path.join(example, 'sources', 'citations.json'), 'utf8').then(JSON.parse),
  fs.readFile(path.join(example, 'evaluation', 'coverage.json'), 'utf8').then(JSON.parse),
  fs.readFile(path.join(example, 'evaluation', 'rubric.json'), 'utf8').then(JSON.parse),
  fs.readFile(path.join(example, 'audio', 'visual-events.timeline.json'), 'utf8').then(JSON.parse),
]);

const errors = [];
const shots = story.shots ?? [];
const shotIds = new Set(shots.map(shot => shot.id));
const citationIds = new Set((citations.sources ?? []).map(source => source.id));

if (shots.length < 25) errors.push(`expected at least 25 shots, got ${shots.length}`);
if ((story.chapters ?? []).length < 8) errors.push('expected at least 8 chapters');

const chapterShotIds = (story.chapters ?? []).flatMap(chapter => chapter.shotIds ?? []);
for (const id of shotIds) {
  const count = chapterShotIds.filter(item => item === id).length;
  if (count !== 1) errors.push(`shot ${id} must appear in exactly one chapter, got ${count}`);
}
for (const id of chapterShotIds) if (!shotIds.has(id)) errors.push(`chapter references unknown shot ${id}`);

for (const shot of shots) {
  if (!shot.dialogue?.trim()) errors.push(`shot ${shot.id} has no narration`);
  if (!shot.visual?.kind) errors.push(`shot ${shot.id} has no visual.kind`);
  for (const citation of shot.citations ?? []) {
    if (!citationIds.has(citation)) errors.push(`shot ${shot.id} references unknown citation ${citation}`);
  }
  if (shot.visual?.kind === 'swimlane') {
    const lanes = new Set(shot.visual.lanes ?? []);
    for (const event of shot.visual.events ?? []) {
      if (!event || typeof event !== 'object') errors.push(`swimlane ${shot.id} must use explicit event objects`);
      else if (!lanes.has(event.from) || !lanes.has(event.to) || event.from === event.to || !event.label) errors.push(`swimlane ${shot.id} has invalid event ${JSON.stringify(event)}`);
    }
    if ((shot.visual.events ?? []).some(event => event.label === 'next model call' && event.from === 'MODEL')) {
      errors.push(`swimlane ${shot.id} labels a MODEL response as next model call`);
    }
  }
  if (shot.visual?.kind === 'code') {
    const jsonLines = (shot.visual.lines ?? []).filter(line => !String(line).startsWith('validator:'));
    try { JSON.parse(jsonLines.join('\n')); } catch { errors.push(`code shot ${shot.id} must show valid JSON before validator output`); }
  }
}

const allowedTopologyCompositions = new Set(['orbit', 'branch', 'quadrants', 'constellation', 'dashboard', 'hero-map']);
const topologyShots = shots.filter(shot => shot.visual?.kind === 'topology');
const topologyCompositions = topologyShots.map(shot => shot.visual?.composition).filter(Boolean);
const topologyCompositionCounts = Object.fromEntries([...new Set(topologyCompositions)].map(composition => [composition, topologyCompositions.filter(value => value === composition).length]));
const maximumSingleCompositionShare = Math.max(...Object.values(topologyCompositionCounts), 0) / Math.max(1, topologyShots.length);
if (story.meta?.designSystem?.sceneGrammar !== 'scene-grammar-v2') errors.push('story must declare scene-grammar-v2');
if (topologyCompositions.length !== topologyShots.length) errors.push('every topology shot must declare a composition');
if (topologyCompositions.some(composition => !allowedTopologyCompositions.has(composition))) errors.push('topology shot declares an unknown composition');
if (Object.keys(topologyCompositionCounts).length < 5) errors.push('topology shots must use at least five distinct compositions');
if (maximumSingleCompositionShare > 0.34) errors.push(`one topology composition dominates ${(maximumSingleCompositionShare * 100).toFixed(1)}% of topology shots`);

const requiredPerformanceFields = ['state', 'emotion', 'gesture', 'motionProfile', 'focusTarget'];
const requiredPerformanceBeatFields = ['id', 'cueIndex', 'pose', 'gaze', 'gesture', 'expression', 'asset', 'transition'];
const requiredPerformanceStates = ['investigate', 'recover', 'synthesize'];
const characterShots = shots.filter(shot => shot.visual?.kind === 'character');
const performanceStates = characterShots.map(shot => shot.visual?.performance?.state);
const performancePoseAssets = new Set();
if (story.meta?.designSystem?.performanceSystem !== 'xiaolan-performance-v2') errors.push('story must declare xiaolan-performance-v2');
for (const shot of characterShots) {
  if (requiredPerformanceFields.some(field => !String(shot.visual?.performance?.[field] ?? '').trim())) errors.push(`character shot ${shot.id} must declare a complete performance state`);
  const beats = shot.visual?.performance?.beats ?? [];
  if (beats.length < 3) errors.push(`character shot ${shot.id} must declare at least three performance beats`);
  beats.forEach((beat, index) => {
    if (requiredPerformanceBeatFields.some(field => beat[field] === undefined || !String(beat[field]).trim())) errors.push(`character shot ${shot.id} has an incomplete performance beat`);
    if (!Number.isInteger(beat.cueIndex) || beat.cueIndex < 0 || beat.cueIndex >= shot.visual.cueIndexes.length) errors.push(`character shot ${shot.id} beat ${beat.id} has an invalid cueIndex`);
    if (index > 0 && beat.cueIndex <= beats[index - 1].cueIndex) errors.push(`character shot ${shot.id} performance beats must advance in cue order`);
    performancePoseAssets.add(beat.asset);
  });
}
for (const state of requiredPerformanceStates) if (!performanceStates.includes(state)) errors.push(`character performance state ${state} is not represented`);
if (performancePoseAssets.size < 5) errors.push(`character performance must use at least five distinct pose assets, got ${performancePoseAssets.size}`);

const stopReasons = shots.find(shot => shot.id === 'stop-reasons');
if (stopReasons?.visual?.edgeDirection !== 'outbound') errors.push('stop-reasons must direct arrows outward from RUNNING');
for (const shot of shots) {
  if (!Array.isArray(shot?.visual?.cueIndexes)) errors.push(`${shot.id} must declare explicit semantic cue indexes`);
}
const timedVisualEvents = (visualTimeline.shots ?? []).flatMap(shot => shot.events ?? []);
if (visualTimeline.mappingPolicy?.mode !== 'explicit-human-semantic') errors.push('visual timing must use explicit human semantic mapping');
if (visualTimeline.mappingPolicy?.proportionalFallbackAllowed !== false) errors.push('proportional visual cue fallback must be forbidden');
if (!timedVisualEvents.length || timedVisualEvents.some(event => event.strategy !== 'explicit')) {
  errors.push('every timed semantic visual event must use an explicit cue index');
}

const core = coverage.requirements ?? [];
if (core.length !== 15) errors.push(`expected exactly 15 core requirements, got ${core.length}`);
for (const requirement of [...core, ...(coverage.additionalRequirements ?? [])]) {
  if (!(requirement.shotIds ?? []).length) errors.push(`${requirement.id} has no evidence shots`);
  for (const id of requirement.shotIds ?? []) {
    if (!shotIds.has(id)) errors.push(`${requirement.id} references unknown shot ${id}`);
  }
}

const voice = story.characters?.[0]?.voice ?? {};
if (voice.mimo_model !== 'mimo-v2.5-tts') errors.push('production TTS model must be mimo-v2.5-tts');
if (voice.mimo_voice !== '茉莉') errors.push('primary narration must use female voice 茉莉');
if (!String(voice.style ?? '').includes('女性')) errors.push('voice style must explicitly require a female narrator');
if (Number(story.meta?.playbackRate ?? 1) < 1 || Number(story.meta?.playbackRate ?? 1) > 1.1) errors.push('playbackRate must remain in the natural 1.0–1.1 range');

const visualKinds = new Set(shots.map(shot => shot.visual?.kind).filter(Boolean));
if (visualKinds.size < 8) errors.push(`expected at least 8 semantic visual families, got ${visualKinds.size}`);
const dialogue = shots.map(shot => shot.dialogue).join('');
const cjkCount = (dialogue.match(/[\u3400-\u9fff]/g) ?? []).length;
if (cjkCount < 2500) errors.push(`narration is too short for a complete longform benchmark: ${cjkCount} CJK chars`);
if (/verified excerpt/i.test(JSON.stringify(story))) errors.push('unverifiable "verified excerpt" label is forbidden');

const dimensionTotal = (rubric.dimensions ?? []).reduce((sum, item) => sum + Number(item.weight || 0), 0);
if (dimensionTotal !== 100) errors.push(`rubric weights must total 100, got ${dimensionTotal}`);
if ((rubric.hardGates ?? []).length < 8) errors.push('rubric must include at least 8 hard gates');

const report = {
  schemaVersion: story.schemaVersion,
  shots: shots.length,
  chapters: story.chapters?.length ?? 0,
  cjkNarrationCharacters: cjkCount,
  plannedDurationSeconds: Number(shots.reduce((sum, shot) => sum + Number(shot.duration || 0), 0).toFixed(3)),
  semanticVisualFamilies: [...visualKinds].sort(),
  semanticVisualEvents: timedVisualEvents.length,
  semanticVisualMapping: visualTimeline.mappingPolicy?.mode,
  topologyCompositionCounts,
  maximumSingleCompositionShare,
  performanceStates,
  performancePoseAssets: [...performancePoseAssets],
  coreCoverage: core.length,
  femaleVoice: voice.mimo_voice,
  errors,
};

console.log(JSON.stringify(report, null, 2));
if (errors.length) process.exitCode = 1;
