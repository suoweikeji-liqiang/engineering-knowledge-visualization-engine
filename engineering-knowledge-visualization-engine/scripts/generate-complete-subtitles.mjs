import {readFile, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/ai-agent-harness-complete');
const story = JSON.parse(await readFile(resolve(example, 'storyboard/story.json'), 'utf8'));
const sourceTimeline = JSON.parse(await readFile(resolve(example, 'audio/ai-agent-harness-complete.timeline.json'), 'utf8'));
const alignment = JSON.parse(await readFile(resolve(example, 'audio/forced-alignment.timeline.json'), 'utf8'));
const narrationMasterSha256 = createHash('sha256').update(await readFile(resolve(example, 'audio/ai-agent-harness-complete.wav'))).digest('hex');
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

function stamp(seconds) {
  const millis = Math.max(0, Math.round(seconds * 1000));
  const hours = Math.floor(millis / 3_600_000);
  const minutes = Math.floor((millis % 3_600_000) / 60_000);
  const secs = Math.floor((millis % 60_000) / 1000);
  const ms = millis % 1000;
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

const shots = new Map(story.shots.map(shot => [shot.id, shot]));
const alignedShots = new Map(alignment.shots.map(shot => [shot.id, shot]));
if (alignment.storyFingerprint !== sourceTimeline.storyFingerprint) {
  throw new Error(`Forced alignment fingerprint mismatch: ${alignment.storyFingerprint} / ${sourceTimeline.storyFingerprint}`);
}
if (alignment.narrationMasterSha256 !== narrationMasterSha256) {
  throw new Error(`Forced alignment audio hash mismatch: ${alignment.narrationMasterSha256} / ${narrationMasterSha256}`);
}
if (alignment.proportionalFallbackAllowed !== false) {
  throw new Error('Forced alignment must explicitly forbid proportional timing fallback.');
}
const cues = [];
let cursor = 0;
for (const timing of timeline.shots) {
  const shot = shots.get(timing.id);
  if (!shot) throw new Error(`Timeline references unknown shot: ${timing.id}`);
  const aligned = alignedShots.get(timing.id);
  if (!aligned?.cues?.length) throw new Error(`Missing forced-alignment cues for ${timing.id}`);
  aligned.cues.forEach(chunk => {
    const localStart = Math.min(timing.duration, Math.max(0, chunk.start / playbackRate));
    const localEnd = Math.min(timing.duration, Math.max(localStart + 0.05, chunk.end / playbackRate));
    cues.push({
      start: cursor + localStart,
      end: cursor + localEnd,
      localStart,
      localEnd,
      text: chunk.text,
      shotId: timing.id,
      timingSource: 'forced-alignment',
    });
  });
  cursor += timing.duration;
}

const srt = cues.flatMap((cue, index) => [
  String(index + 1),
  `${stamp(cue.start)} --> ${stamp(cue.end)}`,
  cue.text,
  '',
]).join('\n');

const chapters = story.chapters.map(chapter => {
  const first = timeline.shots.findIndex(shot => chapter.shotIds.includes(shot.id));
  if (first < 0) throw new Error(`Chapter has no timed shots: ${chapter.id}`);
  const start = timeline.shots.slice(0, first).reduce((sum, shot) => sum + shot.duration, 0);
  return {id: chapter.id, title: chapter.title, start};
});

await writeFile(resolve(example, 'final/subtitles.srt'), srt, 'utf8');
await writeFile(resolve(example, 'final/chapters.json'), `${JSON.stringify(chapters, null, 2)}\n`, 'utf8');
await writeFile(resolve(example, 'audio/captions.timeline.json'), `${JSON.stringify({schemaVersion: '1.0', storySlug: story.meta.slug, alignment: {method: alignment.method, model: alignment.model, storyFingerprint: alignment.storyFingerprint}, cues}, null, 2)}\n`, 'utf8');
await writeFile(resolve(example, 'audio/video.timeline.json'), `${JSON.stringify(timeline, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({cues: cues.length, chapters: chapters.length, duration: timeline.duration}, null, 2));
