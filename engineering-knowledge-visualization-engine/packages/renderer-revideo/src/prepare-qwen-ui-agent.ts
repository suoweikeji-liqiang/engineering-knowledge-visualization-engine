import {copyFileSync, cpSync, createWriteStream, existsSync, mkdirSync, readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {get} from 'node:https';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const packageRoot = process.cwd();
const exampleRoot = resolve(packageRoot, '../../examples/qwen-ui-agent-hosted');
const publicRoot = resolve(packageRoot, 'public/qwen-ui-agent');
const examplePublicRoot = resolve(exampleRoot, 'public/qwen-ui-agent');
const sourceRoot = resolve(exampleRoot, 'source-media');
const citations = JSON.parse(readFileSync(resolve(exampleRoot, 'sources/citations.json'), 'utf8')) as {sources: Array<{id: string; url: string; sha256?: string}>};
const sourceById = new Map(citations.sources.map(source => [source.id, source]));
const cacheRoot = process.env.QWEN_UI_AGENT_CACHE || '/tmp/qwen-ui-agent-audit';

mkdirSync(publicRoot, {recursive: true});
mkdirSync(examplePublicRoot, {recursive: true});
mkdirSync(sourceRoot, {recursive: true});
mkdirSync(resolve(publicRoot, 'characters'), {recursive: true});
mkdirSync(resolve(publicRoot, 'characters-v2'), {recursive: true});
mkdirSync(resolve(publicRoot, 'evidence'), {recursive: true});

function sha256(path: string): string {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

async function download(url: string, target: string): Promise<void> {
  await new Promise<void>((resolveDownload, reject) => {
    const request = get(url, response => {
      if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        response.resume();
        download(response.headers.location, target).then(resolveDownload, reject);
        return;
      }
      if (response.statusCode !== 200) {
        reject(new Error(`Download failed (${response.statusCode}): ${url}`));
        return;
      }
      const file = createWriteStream(target);
      response.pipe(file);
      file.on('finish', () => file.close(() => resolveDownload()));
      file.on('error', reject);
    });
    request.on('error', reject);
  });
}

async function materialize(sourceId: string, filename: string): Promise<string> {
  const source = sourceById.get(sourceId);
  if (!source) throw new Error(`Unknown source: ${sourceId}`);
  const target = resolve(sourceRoot, filename);
  const cached = resolve(cacheRoot, filename);
  if (!existsSync(target) && existsSync(cached)) copyFileSync(cached, target);
  if (!existsSync(target)) await download(source.url, target);
  const digest = sha256(target);
  if (source.sha256 && digest !== source.sha256) throw new Error(`SHA-256 mismatch for ${sourceId}: ${digest}`);
  return target;
}

const demo = await materialize('qwen-ui-agent-flight-demo', 'proactive-flight-recovery-hd.mp4');
const report = await materialize('qwen-ui-agent-report', 'Qwen-UI-Agent-Technical-Report.pdf');
copyFileSync(demo, resolve(publicRoot, 'proactive-flight-recovery-hd.mp4'));

const pagePrefix = resolve(publicRoot, 'evidence/qwen-report-page-05');
const raster = spawnSync('pdftoppm', ['-f', '5', '-l', '5', '-singlefile', '-png', '-r', '144', report, pagePrefix], {stdio: 'inherit'});
if (raster.status !== 0) throw new Error('pdftoppm failed while extracting Qwen report page 5.');

const aiDailyRoot = process.env.AI_DAILY_REPO || resolve(packageRoot, '../../../../ai_daily_brief_factory_v3');
const avatarRoot = resolve(aiDailyRoot, 'templates/cinematic_context_deck/assets/avatar');
const stageRoot = resolve(aiDailyRoot, 'templates/cinematic_context_deck/assets/character-stage');
for (const filename of ['char_surprised.jpg', 'char_outro.jpg']) {
  const input = resolve(avatarRoot, filename);
  if (!existsSync(input)) throw new Error(`Missing host asset: ${input}`);
  copyFileSync(input, resolve(publicRoot, 'characters', filename));
}
for (const filename of ['xiaolan-pointing.png', 'xiaolan-presenting.png', 'xiaolan-thinking.png']) {
  const input = resolve(stageRoot, filename);
  if (!existsSync(input)) throw new Error(`Missing stage actor: ${input}`);
  copyFileSync(input, resolve(publicRoot, 'characters', filename));
}
const v2CharacterRoot = resolve(exampleRoot, 'assets/characters-v2');
if (!existsSync(resolve(v2CharacterRoot, 'manifest.json'))) throw new Error(`Missing Xiaolan V2 rig assets: ${v2CharacterRoot}`);
cpSync(v2CharacterRoot, resolve(publicRoot, 'characters-v2'), {recursive: true});

const voice = resolve(exampleRoot, 'audio/qwen-ui-agent-hosted.wav');
const timelinePath = resolve(exampleRoot, 'audio/video.timeline.json');
if (!existsSync(voice) || !existsSync(timelinePath)) throw new Error('Narration is missing. Run "pnpm qwen-ui-agent:audio" first.');
const timeline = JSON.parse(readFileSync(timelinePath, 'utf8')) as {duration: number; playbackRate: number};
const mixedAudio = resolve(publicRoot, 'qwen-ui-agent-hosted.mp3');
const bedSeconds = Math.ceil(timeline.duration + 1);
const ffmpeg = process.env.FFMPEG_PATH || 'ffmpeg';
const mix = spawnSync(ffmpeg, [
  '-hide_banner', '-loglevel', 'error', '-y', '-i', voice,
  '-f', 'lavfi', '-i', `sine=frequency=82.41:duration=${bedSeconds}`,
  '-f', 'lavfi', '-i', `sine=frequency=164.81:duration=${bedSeconds}`,
  '-filter_complex',
  `[0:a]atempo=${timeline.playbackRate}[voice];` +
    `[1:a]volume=0.018,tremolo=f=0.10:d=0.45[low];[2:a]volume=0.010,tremolo=f=0.13:d=0.35[high];` +
    `[low][high]amix=inputs=2:normalize=0,afade=t=in:st=0:d=2,afade=t=out:st=${Math.max(0, bedSeconds - 4)}:d=4[bed];` +
    '[bed][voice]sidechaincompress=threshold=0.02:ratio=8:attack=80:release=600[duck];' +
    '[voice][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=10,alimiter=limit=0.97[a]',
  '-map', '[a]', '-t', String(timeline.duration), '-ac', '2', '-codec:a', 'libmp3lame', '-b:a', '192k', mixedAudio,
], {stdio: 'inherit'});
if (mix.status !== 0) throw new Error('ffmpeg failed while preparing narration mix.');
mkdirSync(resolve(examplePublicRoot, 'characters'), {recursive: true});
mkdirSync(resolve(examplePublicRoot, 'evidence'), {recursive: true});
for (const filename of ['proactive-flight-recovery-hd.mp4', 'qwen-ui-agent-hosted.mp3']) {
  copyFileSync(resolve(publicRoot, filename), resolve(examplePublicRoot, filename));
}
for (const filename of ['char_surprised.jpg', 'char_outro.jpg', 'xiaolan-pointing.png', 'xiaolan-presenting.png', 'xiaolan-thinking.png']) {
  copyFileSync(resolve(publicRoot, 'characters', filename), resolve(examplePublicRoot, 'characters', filename));
}
copyFileSync(resolve(publicRoot, 'evidence/qwen-report-page-05.png'), resolve(examplePublicRoot, 'evidence/qwen-report-page-05.png'));
console.log(`Prepared Qwen UI Agent media in ${publicRoot}`);
