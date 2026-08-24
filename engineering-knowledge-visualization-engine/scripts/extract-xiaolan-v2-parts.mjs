import {createHash} from 'node:crypto';
import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const root = resolve(import.meta.dirname, '..');
const outputRoot = resolve(root, 'examples/qwen-ui-agent-hosted/assets/characters-v2');
const sheet = resolve(outputRoot, 'xiaolan-v2-parts-sheet.png');
const headBaseSource = resolve(outputRoot, 'xiaolan-v2-head-base-source.png');

const parts = [
  {id: 'head', crop: [320, 430, 45, 35], pivot: [0.5, 0.78]},
  {id: 'torso', crop: [260, 350, 430, 45], pivot: [0.5, 0.12]},
  {id: 'left-upper-arm', crop: [140, 300, 775, 70], pivot: [0.48, 0.05]},
  {id: 'left-forearm', crop: [115, 250, 1015, 105], pivot: [0.48, 0.04]},
  {id: 'left-open-hand', crop: [190, 220, 50, 500], pivot: [0.55, 0.96]},
  {id: 'right-upper-arm', crop: [120, 290, 555, 450], pivot: [0.52, 0.05]},
  {id: 'right-forearm', crop: [110, 240, 795, 490], pivot: [0.52, 0.04]},
  {id: 'right-pointing-hand', crop: [165, 250, 1015, 470], pivot: [0.3, 0.96]},
  {id: 'eyes-open', crop: [250, 130, 40, 825], pivot: [0.5, 0.5]},
  {id: 'eyes-closed', crop: [240, 130, 355, 825], pivot: [0.5, 0.5]},
  {id: 'mouth-closed', crop: [120, 55, 715, 875], pivot: [0.5, 0.5]},
  {id: 'mouth-mid', crop: [105, 65, 975, 865], pivot: [0.5, 0.5]},
  {id: 'mouth-open', crop: [125, 90, 110, 1035], pivot: [0.5, 0.5]},
  {id: 'brows-surprised', crop: [250, 100, 355, 1015], pivot: [0.5, 0.5]},
];

mkdirSync(outputRoot, {recursive: true});
const headBase = resolve(outputRoot, 'head-base.png');
const headRender = spawnSync('ffmpeg', [
  '-y', '-hide_banner', '-loglevel', 'error', '-i', headBaseSource,
  '-vf', 'crop=900:1160:180:20,colorkey=0x00FF00:0.30:0.04,despill=type=green:mix=0.9:expand=0.18,format=rgba',
  '-frames:v', '1', headBase,
], {encoding: 'utf8'});
if (headRender.status !== 0) throw new Error(headRender.stderr || 'Failed to extract head base');

for (const part of parts) {
  const [width, height, x, y] = part.crop;
  const output = resolve(outputRoot, `${part.id}.png`);
  const render = spawnSync('ffmpeg', [
    '-y', '-hide_banner', '-loglevel', 'error', '-i', sheet,
    '-vf', `crop=${width}:${height}:${x}:${y},colorkey=0x00FF00:0.30:0.04,despill=type=green:mix=0.9:expand=0.18,format=rgba`,
    '-frames:v', '1', output,
  ], {encoding: 'utf8'});
  if (render.status !== 0) throw new Error(render.stderr || `Failed to extract ${part.id}`);
  part.path = `${part.id}.png`;
  part.sha256 = createHash('sha256').update(readFileSync(output)).digest('hex');
}

const manifest = {
  schemaVersion: '2.0',
  id: 'xiaolan-rig-v2',
  sourceSheet: 'xiaolan-v2-parts-sheet.png',
  sourceSheetSha256: createHash('sha256').update(readFileSync(sheet)).digest('hex'),
  headBase: {
    path: 'head-base.png',
    source: 'xiaolan-v2-head-base-source.png',
    sha256: createHash('sha256').update(readFileSync(headBase)).digest('hex'),
  },
  chromaKey: {color: '#00FF00', similarity: 0.3, blend: 0.04, despill: {mix: 0.9, expand: 0.18}},
  parts,
};
writeFileSync(resolve(outputRoot, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({parts: parts.length, outputRoot}, null, 2));
