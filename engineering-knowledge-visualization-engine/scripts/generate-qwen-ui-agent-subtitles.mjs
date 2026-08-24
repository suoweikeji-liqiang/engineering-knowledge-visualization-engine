import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/qwen-ui-agent-hosted');
const story = JSON.parse(await readFile(resolve(example, 'storyboard/story.json'), 'utf8'));
const sourceTimeline = JSON.parse(await readFile(resolve(example, 'audio/qwen-ui-agent-hosted.timeline.json'), 'utf8'));
const playbackRate = Number(story.meta.playbackRate ?? 1);
const timeline = {
  ...sourceTimeline,
  duration: sourceTimeline.duration / playbackRate,
  playbackRate,
  shots: sourceTimeline.shots.map(shot => ({
    ...shot,
    speechDuration: shot.speechDuration / playbackRate,
    duration: shot.duration / playbackRate,
  })),
};

function splitCaption(text, maxChars = 22) {
  const clauses = text.split(/(?<=[。！？；，、：])/u).map(item => item.trim()).filter(Boolean);
  const result = [];
  let current = '';
  for (const clause of clauses) {
    if (current && [...current, ...clause].length > maxChars) {
      result.push(current);
      current = clause;
    } else current += clause;
  }
  if (current) result.push(current);
  return result.length ? result : [text];
}

function stamp(seconds) {
  const millis = Math.max(0, Math.round(seconds * 1000));
  const hours = Math.floor(millis / 3_600_000);
  const minutes = Math.floor((millis % 3_600_000) / 60_000);
  const secs = Math.floor((millis % 60_000) / 1000);
  const ms = millis % 1000;
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

const shots = new Map(story.shots.map(shot => [shot.id, shot]));
const cues = [];
let cursor = 0;
for (const timing of timeline.shots) {
  const shot = shots.get(timing.id);
  if (!shot) throw new Error(`Timeline references unknown shot: ${timing.id}`);
  const chunks = splitCaption(shot.dialogue);
  const weights = chunks.map(chunk => Math.max(1, [...chunk].length));
  const totalWeight = weights.reduce((sum, value) => sum + value, 0);
  const speechStart = cursor + 0.25;
  const speechSpan = Math.min(timing.speechDuration, Math.max(0, timing.duration - 0.25));
  let local = speechStart;
  chunks.forEach((chunk, index) => {
    const duration = speechSpan * (weights[index] / totalWeight);
    cues.push({start: local, end: local + duration, localStart: local - cursor, localEnd: local + duration - cursor, text: chunk, shotId: timing.id});
    local += duration;
  });
  cursor += timing.duration;
}

const srt = cues.flatMap((cue, index) => [String(index + 1), `${stamp(cue.start)} --> ${stamp(cue.end)}`, cue.text, '']).join('\n');
await mkdir(resolve(example, 'final'), {recursive: true});
await writeFile(resolve(example, 'final/subtitles.srt'), srt, 'utf8');
await writeFile(resolve(example, 'audio/captions.timeline.json'), `${JSON.stringify({schemaVersion: '1.0', storySlug: story.meta.slug, cues}, null, 2)}\n`, 'utf8');
await writeFile(resolve(example, 'audio/video.timeline.json'), `${JSON.stringify(timeline, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({cues: cues.length, duration: timeline.duration}, null, 2));
