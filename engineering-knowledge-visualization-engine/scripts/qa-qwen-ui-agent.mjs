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
const citations = JSON.parse(readFileSync(resolve(example, 'sources/citations.json'), 'utf8'));
const finalPath = resolve(example, 'final/qwen-ui-agent-hosted.mp4');
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
  return expected && rig.system === rigContract.system && rig.pose === expected.pose && rig.action === expected.action && rig.lipSync === 'none' && validPoses.has(rig.pose) && validActions.has(rig.action);
}), `${riggedHostShots.length} bound host shots`);
check('character-rig-coverage', riggedHostRatio >= rigContract.qualityGates.minimumRiggedHostRatio, `${riggedHostShots.length}/${hostShots.length} = ${(riggedHostRatio * 100).toFixed(1)}%`);
check('static-character-mouth', rigContract.lipSync.driver === 'none' && rigContract.qualityGates.requireStaticMouth === true && riggedHostShots.every(shot => shot.hostNarrative.rig.lipSync === 'none'), 'source illustration mouth is preserved without overlays or audio-driven deformation');
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

const report = {schemaVersion: '1.0', generatedAt: new Date().toISOString(), result: failures.length ? 'fail' : 'pass', metrics: {hostRatio, riggedHostRatio, riggedHostShots: riggedHostShots.length, lipSync: 'disabled', demoRatio, demoSeconds, duration: timeline.duration}, checks};
mkdirSync(resolve(example, 'qa'), {recursive: true});
writeFileSync(resolve(example, 'qa/qa-report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(report, null, 2));
if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
}
