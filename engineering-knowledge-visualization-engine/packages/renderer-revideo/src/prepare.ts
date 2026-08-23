import {copyFileSync, existsSync, mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const packageRoot = process.cwd();
const exampleRoot = resolve(packageRoot, '../../examples/ai-agent-harness-benchmark');
const source = resolve(exampleRoot, 'audio/ai-agent-harness-benchmark.wav');
const examplePublic = resolve(exampleRoot, 'public/benchmark-audio.mp3');
const rendererPublic = resolve(packageRoot, 'public/benchmark-audio.mp3');

if (!existsSync(source)) {
  throw new Error(
    `MiMo narration master is missing: ${source}\nRun \"pnpm benchmark:audio\" first.`,
  );
}

mkdirSync(resolve(exampleRoot, 'public'), {recursive: true});
mkdirSync(resolve(packageRoot, 'public'), {recursive: true});

const ffmpeg = process.env.FFMPEG_PATH || 'ffmpeg';
const result = spawnSync(
  ffmpeg,
  [
    '-hide_banner',
    '-loglevel',
    'error',
    '-y',
    '-i',
    source,
    '-codec:a',
    'libmp3lame',
    '-b:a',
    '192k',
    examplePublic,
  ],
  {stdio: 'inherit'},
);

if (result.status !== 0) {
  throw new Error(`Failed to prepare browser audio with ${ffmpeg}`);
}

// Revideo 0.11 serves browser assets from the package public directory but
// resolves server-side audio mixing from the example output's sibling public
// directory. Keep both generated copies until that upstream split is removed.
copyFileSync(examplePublic, rendererPublic);
console.log(`Prepared browser narration: ${examplePublic}`);
