import {createHash} from 'node:crypto';
import {existsSync, mkdirSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const root = resolve(import.meta.dirname, '..');
const candidate = resolve(root, 'examples/ai-agent-harness-complete/final/ai-agent-harness-complete.mp4');
const referenceA = process.env.REFERENCE_A;
const referenceB = process.env.REFERENCE_B;
const output = resolve(process.env.BLIND_OUTPUT ?? '/tmp/ai-agent-harness-blind-study');
const keyPath = resolve(process.env.BLIND_KEY ?? '/tmp/ai-agent-harness-blind-key.json');
const seed = process.env.BLIND_SEED ?? 'xiaolan-reference-blind-2026-08-24';

if (!referenceA || !existsSync(referenceA)) throw new Error('Set REFERENCE_A to the downloaded reference-a video.');
if (!referenceB || !existsSync(referenceB)) throw new Error('Set REFERENCE_B to the downloaded reference-b video.');
if (!existsSync(candidate)) throw new Error(`Candidate video is missing: ${candidate}`);
mkdirSync(output, {recursive: true});

const sources = [
  {id: 'reference-a', path: referenceA, segments: [30, 135, 190, 355, 470, 630]},
  {id: 'reference-b', path: referenceB, segments: [0, 55, 115, 180, 245, 320]},
  {id: 'candidate', path: candidate, segments: [0, 68, 180, 407, 589, 687]},
];
const labels = ['X', 'Y', 'Z'];
const randomized = [...sources].sort((a, b) => createHash('sha256').update(seed + a.id).digest('hex').localeCompare(createHash('sha256').update(seed + b.id).digest('hex')));

function buildReel(source, label) {
  const filters = [];
  const concatInputs = [];
  source.segments.forEach((start, index) => {
    const end = start + 10;
    filters.push(`[0:v]trim=start=${start}:end=${end},setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30[v${index}]`);
    filters.push(`[0:a]atrim=start=${start}:end=${end},asetpts=PTS-STARTPTS[a${index}]`);
    concatInputs.push(`[v${index}][a${index}]`);
  });
  filters.push(`${concatInputs.join('')}concat=n=${source.segments.length}:v=1:a=1[vcat][acat]`);
  filters.push('[acat]loudnorm=I=-16:TP=-1.5:LRA=11[aout]');
  const target = resolve(output, `${label}.mp4`);
  const result = spawnSync('ffmpeg', [
    '-hide_banner', '-loglevel', 'error', '-y', '-i', source.path,
    '-filter_complex', filters.join(';'), '-map', '[vcat]', '-map', '[aout]',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', target,
  ], {stdio: 'inherit'});
  if (result.status !== 0) throw new Error(`Failed to build blind reel ${label}.`);
  return target;
}

const mapping = randomized.map((source, index) => ({label: labels[index], sourceId: source.id, sourcePath: source.path, segments: source.segments}));
for (const item of mapping) buildReel(sources.find(source => source.id === item.sourceId), item.label);

const protocol = {
  schemaVersion: '1.0',
  labels,
  resolution: '1920x1080',
  frameRate: 30,
  integratedLufsTarget: -16,
  durationSecondsPerCandidate: 60,
  construction: 'six ten-second stratified best-work samples per source',
  scoreBeforeDiscussion: true,
  dimensions: ['clarity', 'animation', 'character', 'sound', 'brand', 'evidence'],
  instruction: 'Review X, Y, and Z without attempting to identify their source. Score each dimension from 0 to 10 and give one observable reason.',
};
writeFileSync(resolve(output, 'protocol.json'), `${JSON.stringify(protocol, null, 2)}\n`, 'utf8');
writeFileSync(keyPath, `${JSON.stringify({schemaVersion: '1.0', seed, mapping}, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({output, keyPath, files: labels.map(label => resolve(output, `${label}.mp4`))}, null, 2));
