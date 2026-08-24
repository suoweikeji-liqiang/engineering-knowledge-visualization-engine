import {readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/qwen-ui-agent-hosted');
const wav = await readFile(resolve(example, 'audio/qwen-ui-agent-hosted.wav'));
const sourceTimeline = JSON.parse(await readFile(resolve(example, 'audio/qwen-ui-agent-hosted.timeline.json'), 'utf8'));
const videoTimeline = JSON.parse(await readFile(resolve(example, 'audio/video.timeline.json'), 'utf8'));
const frameRate = 20;

function findChunk(id) {
  let offset = 12;
  while (offset + 8 <= wav.length) {
    const name = wav.toString('ascii', offset, offset + 4);
    const size = wav.readUInt32LE(offset + 4);
    if (name === id) return {offset: offset + 8, size};
    offset += 8 + size + (size % 2);
  }
  throw new Error(`WAV chunk not found: ${id}`);
}

const fmt = findChunk('fmt ');
const data = findChunk('data');
const audioFormat = wav.readUInt16LE(fmt.offset);
const channels = wav.readUInt16LE(fmt.offset + 2);
const sampleRate = wav.readUInt32LE(fmt.offset + 4);
const bitsPerSample = wav.readUInt16LE(fmt.offset + 14);
if (audioFormat !== 1 || channels !== 1 || bitsPerSample !== 16) throw new Error(`Unsupported WAV format: pcm=${audioFormat}, channels=${channels}, bits=${bitsPerSample}`);

function sampleRms(startSeconds, durationSeconds = 0.055) {
  const first = Math.max(0, Math.floor(startSeconds * sampleRate));
  const last = Math.min(data.size / 2, Math.ceil((startSeconds + durationSeconds) * sampleRate));
  if (last <= first) return 0;
  let energy = 0;
  for (let index = first; index < last; index += 1) {
    const value = wav.readInt16LE(data.offset + index * 2) / 32768;
    energy += value * value;
  }
  return Math.sqrt(energy / (last - first));
}

function percentile(values, ratio) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(sorted.length * ratio)))] ?? 1;
}

const shots = {};
let sourceCursor = 0;
for (let index = 0; index < sourceTimeline.shots.length; index += 1) {
  const sourceShot = sourceTimeline.shots[index];
  const videoShot = videoTimeline.shots[index];
  if (sourceShot.id !== videoShot.id) throw new Error(`Timeline mismatch at ${index}: ${sourceShot.id} / ${videoShot.id}`);
  const frameCount = Math.ceil(videoShot.duration * frameRate);
  const raw = Array.from({length: frameCount}, (_, frame) => sampleRms(sourceCursor + (frame / frameRate) * videoTimeline.playbackRate));
  const ceiling = Math.max(0.006, percentile(raw, 0.9));
  const gated = raw.map(value => Math.max(0, Math.min(1, (value - 0.0025) / Math.max(0.001, ceiling - 0.0025))));
  const smoothed = gated.map((value, frame) => {
    const previous = gated[frame - 1] ?? value;
    const next = gated[frame + 1] ?? value;
    return Number((previous * 0.2 + value * 0.6 + next * 0.2).toFixed(3));
  });
  shots[sourceShot.id] = {frameRate, values: smoothed};
  sourceCursor += sourceShot.duration;
}

const output = {
  schemaVersion: '1.0',
  storySlug: 'qwen-ui-agent-hosted',
  source: 'authored MiMo narration RMS envelope',
  playbackRate: videoTimeline.playbackRate,
  shots,
};
await writeFile(resolve(example, 'audio/lip-sync.timeline.json'), `${JSON.stringify(output)}\n`, 'utf8');
console.log(JSON.stringify({shots: Object.keys(shots).length, frameRate, frames: Object.values(shots).reduce((sum, shot) => sum + shot.values.length, 0)}, null, 2));
