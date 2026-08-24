import {readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/ai-agent-harness-complete');
const story = JSON.parse(await readFile(resolve(example, 'storyboard/story.json'), 'utf8'));
const timeline = JSON.parse(await readFile(resolve(example, 'audio/video.timeline.json'), 'utf8'));
const captions = JSON.parse(await readFile(resolve(example, 'audio/captions.timeline.json'), 'utf8'));
const entryOffset = 0.46;

function eventLabels(shot) {
  const visual = shot.visual;
  switch (visual.kind) {
    case 'character': return visual.status ?? [];
    case 'compare': return [visual.left?.title, visual.right?.title].filter(Boolean);
    case 'evidence': return visual.callouts ?? [];
    case 'topology': return visual.nodes ?? [];
    case 'stack': return [...(visual.layers ?? []), visual.output].filter(Boolean);
    case 'code': {
      const focus = visual.focus ?? [];
      return focus.length ? focus.map(index => visual.lines?.[index - 1]).filter(Boolean) : (visual.lines ?? []);
    }
    case 'gates': return [...(visual.gates ?? []), visual.output].filter(Boolean);
    case 'swimlane': return (visual.events ?? [])
      .filter(event => typeof event === 'string' || event.semanticType !== 'prior-context')
      .map(event => typeof event === 'string' ? event : event.label);
    case 'loop': return visual.nodes ?? [];
    case 'timeline': return (visual.events ?? []).map(event => typeof event === 'string' ? event : event.label);
    case 'bars': return [...(visual.bars ?? []).map(item => item.label), ...(visual.after?.length ? ['after / compacted'] : [])];
    case 'curve': return (visual.series ?? []).map(item => item.label);
    default: return [visual.kind];
  }
}

let shotStart = 0;
const shots = timeline.shots.map(timing => {
  const shot = story.shots.find(item => item.id === timing.id);
  if (!shot) throw new Error(`Unknown timed shot: ${timing.id}`);
  const shotCues = captions.cues.filter(cue => cue.shotId === shot.id);
  if (!shotCues.length) throw new Error(`No narration cues for ${shot.id}`);
  const labels = eventLabels(shot);
  const explicit = shot.visual.cueIndexes;
  if (!Array.isArray(explicit)) {
    throw new Error(`${shot.id} must declare cueIndexes for every semantic event`);
  }
  if (explicit.length !== labels.length) {
    throw new Error(`${shot.id} cueIndexes has ${explicit.length} entries for ${labels.length} semantic events`);
  }
  const events = labels.map((label, index) => {
    const cueIndex = explicit[index];
    const cue = shotCues[cueIndex];
    if (!cue) throw new Error(`${shot.id} visual event ${index} references missing cue ${cueIndex}`);
    const activeStart = Math.max(0, cue.localStart - entryOffset);
    const renderedStart = shotStart + entryOffset + activeStart;
    return {
      id: `${shot.id}:visual:${String(index + 1).padStart(2, '0')}`,
      label,
      cueIndex,
      cueText: cue.text,
      narrationStart: Number(cue.start.toFixed(3)),
      activeStart: Number(activeStart.toFixed(3)),
      renderedStart: Number(renderedStart.toFixed(3)),
      deltaSeconds: Number(Math.abs(renderedStart - cue.start).toFixed(3)),
      strategy: 'explicit-forced-alignment',
    };
  });
  const result = {shotId: shot.id, visualKind: shot.visual.kind, shotStart: Number(shotStart.toFixed(3)), events};
  shotStart += timing.duration;
  return result;
});

const allEvents = shots.flatMap(shot => shot.events);
const within500ms = allEvents.filter(event => event.deltaSeconds <= 0.5).length / Math.max(1, allEvents.length);
const manifest = {
  schemaVersion: '1.0',
  contract: 'semantic-visual-events-are-triggered-from-this-manifest',
  mappingPolicy: {
    mode: 'explicit-human-semantic',
    timingSource: 'forced-alignment-word-timestamps',
    requiresCueIndexForEveryEvent: true,
    proportionalFallbackAllowed: false,
    excludedStaticContextEvents: [
      'boundary:primary-source-document',
      'tool-result:tool_call-prior-context',
    ],
  },
  entryOffset,
  events: allEvents.length,
  within500ms,
  maximumDeltaSeconds: Math.max(...allEvents.map(event => event.deltaSeconds), 0),
  shots,
};

await writeFile(resolve(example, 'audio/visual-events.timeline.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({events: manifest.events, within500ms, maximumDeltaSeconds: manifest.maximumDeltaSeconds}, null, 2));
if (within500ms < 0.95) process.exitCode = 1;
