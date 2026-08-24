import {createHash} from 'node:crypto';
import {existsSync, mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/qwen-ui-agent-hosted');
const story = JSON.parse(readFileSync(resolve(example, 'storyboard/story.json'), 'utf8'));
const timeline = JSON.parse(readFileSync(resolve(example, 'audio/video.timeline.json'), 'utf8'));
const evaluation = JSON.parse(readFileSync(resolve(example, 'evaluation/priority-and-gates.json'), 'utf8'));
const rigContract = JSON.parse(readFileSync(resolve(example, 'evaluation/rig-contract.json'), 'utf8'));
const rigV2Contract = JSON.parse(readFileSync(resolve(example, 'evaluation/rig-v2-contract.json'), 'utf8'));
const rigV2Root = resolve(example, 'assets/characters-v2');
const rigV2Manifest = JSON.parse(readFileSync(resolve(rigV2Root, 'manifest.json'), 'utf8'));
const lipSync = JSON.parse(readFileSync(resolve(example, 'audio/lip-sync.timeline.json'), 'utf8'));
const citations = JSON.parse(readFileSync(resolve(example, 'sources/citations.json'), 'utf8'));
const finalPath = resolve(example, 'final/qwen-ui-agent-hosted.mp4');
const finalV2Path = resolve(example, 'final/qwen-ui-agent-hosted-v2.mp4');
const asrPath = resolve(example, 'evaluation/asr-report.json');
const failures = [];
const checks = [];

function check(id, pass, detail) {
  checks.push({id, pass, detail});
  if (!pass) failures.push(`${id}: ${detail}`);
}

const hostShots = story.shots.filter(shot => shot.hostNarrative?.hostOnScreen);
const hostRatio = hostShots.length / story.shots.length;
check('host-presence', hostRatio >= evaluation.gates.hostPresenceRatio.min && hostRatio <= evaluation.gates.hostPresenceRatio.max, `${hostShots.length}/${story.shots.length} = ${(hostRatio * 100).toFixed(1)}%`);

const timingById = new Map(timeline.shots.map(shot => [shot.id, shot.duration]));
const demoKinds = new Set(['demo', 'demo-channels', 'host-result']);
const demoSeconds = story.shots.filter(shot => demoKinds.has(shot.visual?.kind)).reduce((sum, shot) => sum + (timingById.get(shot.id) ?? 0), 0);
const demoRatio = demoSeconds / timeline.duration;
check('official-demo-time', demoRatio >= evaluation.gates.officialDemoTimeRatio.min, `${demoSeconds.toFixed(1)}s/${timeline.duration.toFixed(1)}s = ${(demoRatio * 100).toFixed(1)}%`);

const citedSourceIds = new Set(story.shots.flatMap(shot => shot.citations ?? []));
const primarySources = citations.sources.filter(source => citedSourceIds.has(source.id) && ['official-repository', 'technical-report', 'official-demo'].includes(source.type));
check('primary-sources', primarySources.length >= evaluation.gates.primarySourceCount.min, `${primarySources.length} primary sources`);
check('case-callback', Boolean(story.shots.at(-1)?.hostNarrative?.role === 'resolve' && story.narrativeCase?.callback), story.narrativeCase?.callback ?? 'missing');
check('visual-cadence-contract', story.shots.every(shot => (shot.visual?.cueIndexes?.length ?? 0) >= 3), 'every shot has at least three semantic visual cues plus continuous ambient motion');
check('template-is-additive', story.meta.template === 'xiaolan-hosted-case-study-v1' && story.meta.slug !== 'ai-agent-harness-complete', story.meta.template);

const validPoses = new Set(rigContract.sourcePoses.map(pose => pose.pose));
const validActions = new Set(rigContract.actions);
const riggedHostShots = hostShots.filter(shot => shot.hostNarrative?.rig);
const riggedHostRatio = riggedHostShots.length / hostShots.length;
check('character-rig-system', story.meta.characterRig === rigContract.system && rigContract.system === 'xiaolan-rig-v1', `${story.meta.characterRig} / ${rigContract.system}`);
check('character-rig-bindings', riggedHostShots.length === rigContract.episodeBindings.length && riggedHostShots.every(shot => {
  const expected = rigContract.episodeBindings.find(binding => binding.shotId === shot.id);
  const rig = shot.hostNarrative.rig;
  return expected && rig.system === rigContract.system && rig.pose === expected.pose && rig.action === expected.action && rig.lipSync === 'voice-rms' && validPoses.has(rig.pose) && validActions.has(rig.action);
}), `${riggedHostShots.length} bound host shots`);
check('character-rig-coverage', riggedHostRatio >= rigContract.qualityGates.minimumRiggedHostRatio, `${riggedHostShots.length}/${hostShots.length} = ${(riggedHostRatio * 100).toFixed(1)}%`);

const rigV2PartsValid = rigV2Manifest.parts.every(part => {
  const path = resolve(rigV2Root, part.path);
  return existsSync(path) && createHash('sha256').update(readFileSync(path)).digest('hex') === part.sha256;
});
const rigV2HeadPath = resolve(rigV2Root, rigV2Manifest.headBase.path);
const rigV2HeadValid = existsSync(rigV2HeadPath) && createHash('sha256').update(readFileSync(rigV2HeadPath)).digest('hex') === rigV2Manifest.headBase.sha256;
const alphaParts = [...rigV2Manifest.parts.map(part => resolve(rigV2Root, part.path)), rigV2HeadPath].filter(path => {
  const probe = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'stream=pix_fmt', '-of', 'default=nw=1:nk=1', path], {encoding: 'utf8'});
  return probe.status === 0 && probe.stdout.trim() === 'rgba';
});
const requiredJointChain = ['leftUpperArm', 'leftForearm', 'leftHand', 'rightUpperArm', 'rightForearm', 'rightHand'];
check('character-rig-v2-system', rigV2Manifest.id === rigV2Contract.system && rigV2Contract.technique === 'layered-cutout-skeleton', `${rigV2Manifest.id} / ${rigV2Contract.technique}`);
check('character-rig-v2-parts', rigV2Manifest.parts.length >= rigV2Contract.qualityGates.minimumTransparentParts && rigV2PartsValid && rigV2HeadValid && alphaParts.length === rigV2Manifest.parts.length + 1, `${rigV2Manifest.parts.length} hashed parts + head base, ${alphaParts.length} RGBA assets`);
check('character-rig-v2-joints', requiredJointChain.every(bone => rigV2Contract.bones.includes(bone)), requiredJointChain.join(' -> '));
check('character-rig-v2-face', rigV2Contract.face.noseMayAnimate === false && rigV2Contract.face.blinkSprites.length === 2 && rigV2Contract.face.mouthSprites.length === 3, `${rigV2Contract.face.blinkSprites.length} eye states, ${rigV2Contract.face.mouthSprites.length} mouth states, nose locked`);

const lipShots = Object.entries(lipSync.shots ?? {});
const lipValues = lipShots.flatMap(([, shot]) => shot.values ?? []);
const lipFrameCount = lipValues.length;
const lipCoverage = story.shots.every(shot => {
  const envelope = lipSync.shots?.[shot.id];
  const duration = timingById.get(shot.id) ?? 0;
  return envelope && envelope.frameRate >= rigContract.lipSync.minimumFrameRate && envelope.values.length >= Math.floor(duration * envelope.frameRate) && envelope.values.every(value => Number.isFinite(value) && value >= rigContract.lipSync.range[0] && value <= rigContract.lipSync.range[1]);
});
check('audio-driven-lip-sync', lipSync.source?.includes('MiMo') && lipShots.length === story.shots.length && lipCoverage, `${lipShots.length} shots, ${lipFrameCount} RMS frames`);
if (existsSync(asrPath)) {
  const asr = JSON.parse(readFileSync(asrPath, 'utf8'));
  check('mimo-blind-asr', asr.summary?.segments === story.shots.length && asr.summary?.below0_8 === 0 && asr.summary?.errors === 0, JSON.stringify(asr.summary));
}

for (const source of citations.sources.filter(source => source.sha256)) {
  const filename = source.id === 'qwen-ui-agent-report' ? 'Qwen-UI-Agent-Technical-Report.pdf' : 'proactive-flight-recovery-hd.mp4';
  const path = resolve(example, 'source-media', filename);
  const digest = existsSync(path) ? createHash('sha256').update(readFileSync(path)).digest('hex') : '';
  check(`source-sha-${source.id}`, digest === source.sha256, digest || 'missing source media');
}

check('final-exists', existsSync(finalPath), finalPath);
check('final-v2-exists', existsSync(finalV2Path), finalV2Path);
if (existsSync(finalV2Path)) {
  const probe = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', finalV2Path], {encoding: 'utf8'});
  const metadata = probe.status === 0 ? JSON.parse(probe.stdout) : {};
  const video = metadata.streams?.find(stream => stream.codec_type === 'video');
  const audio = metadata.streams?.find(stream => stream.codec_type === 'audio');
  const duration = Number(metadata.format?.duration ?? 0);
  check('video-v2-format', video?.width === 1920 && video?.height === 1080 && Boolean(audio), `${video?.width ?? 0}x${video?.height ?? 0}, audio=${Boolean(audio)}`);
  check('duration-v2-match', Math.abs(duration - timeline.duration) < 0.2, `${duration.toFixed(3)}s vs ${timeline.duration.toFixed(3)}s`);
  const detect = spawnSync('ffmpeg', ['-hide_banner', '-i', finalV2Path, '-vf', 'blackdetect=d=1:pix_th=0.08,freezedetect=n=-55dB:d=3', '-an', '-f', 'null', '-'], {encoding: 'utf8'});
  const diagnostic = `${detect.stdout}\n${detect.stderr}`;
  const blackSegments = [...diagnostic.matchAll(/black_duration:([0-9.]+)/g)].map(match => Number(match[1])).filter(value => value >= 1);
  const freezeSegments = [...diagnostic.matchAll(/freeze_duration: ([0-9.]+)/g)].map(match => Number(match[1]));
  const frozenSeconds = freezeSegments.reduce((sum, value) => sum + value, 0);
  const maximumFreezeSeconds = Math.max(...freezeSegments, 0);
  check('no-black-v2-segments', blackSegments.length === 0, JSON.stringify(blackSegments));
  check('no-long-v2-freezes', maximumFreezeSeconds < 8 && frozenSeconds / duration < 0.5, `max=${maximumFreezeSeconds.toFixed(3)}s, total=${frozenSeconds.toFixed(3)}s`);
}
if (existsSync(finalPath)) {
  const probe = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height', '-of', 'json', finalPath], {encoding: 'utf8'});
  const metadata = probe.status === 0 ? JSON.parse(probe.stdout) : {};
  const video = metadata.streams?.find(stream => stream.codec_type === 'video');
  const audio = metadata.streams?.find(stream => stream.codec_type === 'audio');
  const duration = Number(metadata.format?.duration ?? 0);
  check('video-format', video?.width === 1920 && video?.height === 1080 && Boolean(audio), `${video?.width ?? 0}x${video?.height ?? 0}, audio=${Boolean(audio)}`);
  check('duration-match', Math.abs(duration - timeline.duration) < 0.2, `${duration.toFixed(3)}s vs ${timeline.duration.toFixed(3)}s`);
  const detect = spawnSync('ffmpeg', ['-hide_banner', '-i', finalPath, '-vf', 'blackdetect=d=1:pix_th=0.08,freezedetect=n=-55dB:d=3', '-an', '-f', 'null', '-'], {encoding: 'utf8'});
  const diagnostic = `${detect.stdout}\n${detect.stderr}`;
  const blackSegments = [...diagnostic.matchAll(/black_duration:([0-9.]+)/g)].map(match => Number(match[1])).filter(value => value >= 1);
  const freezeSegments = [...diagnostic.matchAll(/freeze_duration: ([0-9.]+)/g)].map(match => Number(match[1]));
  const frozenSeconds = freezeSegments.reduce((sum, value) => sum + value, 0);
  const maximumFreezeSeconds = Math.max(...freezeSegments, 0);
  check('no-black-segments', blackSegments.length === 0, JSON.stringify(blackSegments));
  check('no-long-freezes', maximumFreezeSeconds < 8 && frozenSeconds / duration < 0.5, `max=${maximumFreezeSeconds.toFixed(3)}s, total=${frozenSeconds.toFixed(3)}s`);
}

const report = {schemaVersion: '1.0', generatedAt: new Date().toISOString(), result: failures.length ? 'fail' : 'pass', metrics: {hostRatio, riggedHostRatio, riggedHostShots: riggedHostShots.length, lipSyncFrames: lipFrameCount, demoRatio, demoSeconds, duration: timeline.duration}, checks};
mkdirSync(resolve(example, 'qa'), {recursive: true});
writeFileSync(resolve(example, 'qa/qa-report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(report, null, 2));
if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
}
