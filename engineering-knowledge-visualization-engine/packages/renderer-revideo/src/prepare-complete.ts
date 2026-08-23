import {copyFileSync, existsSync, mkdirSync, readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const packageRoot = process.cwd();
const exampleRoot = resolve(packageRoot, '../../examples/ai-agent-harness-complete');
const source = resolve(exampleRoot, 'audio/ai-agent-harness-complete.wav');
const timeline = JSON.parse(readFileSync(resolve(exampleRoot, 'audio/video.timeline.json'), 'utf8')) as {duration: number; playbackRate: number};
const ambientBed = resolve(exampleRoot, 'audio/ai-agent-harness-ambient.wav');
const examplePublic = resolve(exampleRoot, 'public/complete/complete-audio.mp3');
const rendererPublic = resolve(packageRoot, 'public/complete/complete-audio.mp3');
const characterSource = resolve(exampleRoot, 'assets/characters');
const characterPublic = resolve(packageRoot, 'public/complete/characters');
const evidenceSource = resolve(exampleRoot, 'assets/evidence');
const evidencePublic = resolve(packageRoot, 'public/complete/evidence');
const characterFiles = ['xiaolan-evidence-bridge.png', 'xiaolan-connect-modules.png', 'xiaolan-recover-path.png'] as const;
const evidenceFiles = ['openai-agent-guide-page-04.png'] as const;

if (!existsSync(source)) throw new Error(`MiMo female narration is missing: ${source}\nRun "pnpm benchmark:complete:audio" first.`);
mkdirSync(resolve(exampleRoot, 'public/complete'), {recursive: true});
mkdirSync(resolve(packageRoot, 'public/complete'), {recursive: true});
mkdirSync(characterPublic, {recursive: true});
mkdirSync(evidencePublic, {recursive: true});

for (const filename of characterFiles) {
  const input = resolve(characterSource, filename);
  if (!existsSync(input)) throw new Error(`Character asset is missing: ${input}`);
  copyFileSync(input, resolve(characterPublic, filename));
}
for (const filename of evidenceFiles) {
  const input = resolve(evidenceSource, filename);
  if (!existsSync(input)) throw new Error(`Evidence asset is missing: ${input}`);
  copyFileSync(input, resolve(evidencePublic, filename));
}

const ffmpeg = process.env.FFMPEG_PATH || 'ffmpeg';
if (!existsSync(ambientBed)) {
  const bedSeconds = Math.ceil(timeline.duration + 1);
  const bedInputs = [55, 110, 164.81, 220, 329.63].flatMap(frequency => ['-f', 'lavfi', '-i', `sine=frequency=${frequency}:duration=${bedSeconds}`]);
  const bedFilter = [
    '[0:a]volume=0.32,tremolo=f=0.10:d=0.6[a]',
    '[1:a]volume=0.18,tremolo=f=0.13:d=0.5[b]',
    '[2:a]volume=0.12,tremolo=f=0.11:d=0.42[c]',
    '[3:a]volume=0.08,tremolo=f=0.15:d=0.3[d]',
    '[4:a]volume=0.05,tremolo=f=0.17:d=0.5[e]',
    '[5:a]lowpass=f=320,volume=0.14[f]',
    `[a][b][c][d][e][f]amix=inputs=6:normalize=0,afade=t=in:st=0:d=3,afade=t=out:st=${Math.max(0, bedSeconds - 5)}:d=5[out]`,
  ].join(';');
  const bedResult = spawnSync(ffmpeg, [
    '-hide_banner', '-loglevel', 'error', '-y', ...bedInputs,
    '-f', 'lavfi', '-i', `anoisesrc=color=pink:duration=${bedSeconds}:amplitude=0.05`,
    '-filter_complex', bedFilter, '-map', '[out]', '-c:a', 'pcm_s16le', '-ar', '48000', ambientBed,
  ], {stdio: 'inherit'});
  if (bedResult.status !== 0) throw new Error(`Failed to generate ambient bed with ${ffmpeg}`);
}
const result = spawnSync(ffmpeg, [
  '-hide_banner', '-loglevel', 'error', '-y', '-i', source, '-i', ambientBed,
  '-filter_complex',
  `[0:a]atempo=${timeline.playbackRate}[voice];[1:a]atrim=duration=${timeline.duration},volume=0.16[bgm];` +
    '[bgm][voice]sidechaincompress=threshold=0.02:ratio=8:attack=90:release=650[duck];' +
    '[voice][duck]amix=inputs=2:duration=first:normalize=0,' +
    'loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.97,aresample=48000[a]',
  '-map', '[a]', '-t', String(timeline.duration), '-ac', '2', '-codec:a', 'libmp3lame', '-b:a', '192k', examplePublic,
], {stdio: 'inherit'});
if (result.status !== 0) throw new Error(`Failed to prepare browser audio with ${ffmpeg}`);
copyFileSync(examplePublic, rendererPublic);
console.log(`Prepared complete female narration: ${examplePublic}`);
console.log(`Prepared ${characterFiles.length} character assets and ${evidenceFiles.length} evidence assets.`);
