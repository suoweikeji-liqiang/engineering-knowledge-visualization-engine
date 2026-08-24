import {readFile, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/ai-agent-harness-complete');
const video = resolve(example, 'final/ai-agent-harness-complete.mp4');
const timeline = JSON.parse(await readFile(resolve(example, 'audio/video.timeline.json'), 'utf8'));
const asr = JSON.parse(await readFile(resolve(example, 'evaluation/asr-report.json'), 'utf8'));
const subtitles = await readFile(resolve(example, 'final/subtitles.srt'), 'utf8');
const captionTimeline = JSON.parse(await readFile(resolve(example, 'audio/captions.timeline.json'), 'utf8'));
const visualTimeline = JSON.parse(await readFile(resolve(example, 'audio/visual-events.timeline.json'), 'utf8'));
const alignment = JSON.parse(await readFile(resolve(example, 'audio/forced-alignment.timeline.json'), 'utf8'));
const narrationMasterSha256 = createHash('sha256').update(await readFile(resolve(example, 'audio/ai-agent-harness-complete.wav'))).digest('hex');
const trace = JSON.parse(await readFile(resolve(example, 'final/trace.json'), 'utf8'));
const layout = JSON.parse(await readFile(resolve(example, 'evaluation/layout-qa.json'), 'utf8'));

function run(command, args) {
  const result = spawnSync(command, args, {encoding: 'utf8'});
  if (result.status !== 0) throw new Error(`${command} failed: ${result.stderr}`);
  return `${result.stdout ?? ''}${result.stderr ?? ''}`;
}

const probe = JSON.parse(run('ffprobe', [
  '-v', 'error', '-show_entries',
  'format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels',
  '-of', 'json', video,
]));
const videoStream = probe.streams.find(stream => stream.codec_type === 'video');
const audioStream = probe.streams.find(stream => stream.codec_type === 'audio');
const blackOutput = run('ffmpeg', ['-hide_banner', '-nostats', '-i', video, '-vf', 'blackdetect=d=0.25:pix_th=0.10', '-an', '-f', 'null', '-']);
const blackSegments = [...blackOutput.matchAll(/black_start:([0-9.]+).*?black_end:([0-9.]+).*?black_duration:([0-9.]+)/g)].map(match => ({start: Number(match[1]), end: Number(match[2]), duration: Number(match[3])}));
const freezeOutput = run('ffmpeg', ['-hide_banner', '-nostats', '-i', video, '-vf', 'freezedetect=n=-55dB:d=3', '-an', '-f', 'null', '-']);
const freezeDurations = [...freezeOutput.matchAll(/freeze_duration:\s*([0-9.]+)/g)].map(match => Number(match[1]));
const loudnessOutput = run('ffmpeg', ['-hide_banner', '-nostats', '-i', video, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-vn', '-f', 'null', '-']);
const loudnessMatch = loudnessOutput.match(/\{\s*"input_i"[\s\S]*?\}/);
if (!loudnessMatch) throw new Error('Unable to parse loudness measurement.');
const loudness = JSON.parse(loudnessMatch[0]);
const duration = Number(probe.format.duration);
const frozenSeconds = freezeDurations.reduce((sum, value) => sum + value, 0);
const maximumFreezeSeconds = Math.max(...freezeDurations, 0);
const subtitleCues = (subtitles.match(/--> /g) ?? []).length;
const shotStarts = Object.fromEntries(timeline.shots.map((shot, index) => [shot.id, timeline.shots.slice(0, index).reduce((sum, item) => sum + item.duration, 0)]));
const captionSync = captionTimeline.cues.map(cue => {
  const expected = cue.start;
  const shotDuration = timeline.shots.find(shot => shot.id === cue.shotId).duration;
  const activeStart = Math.min(shotDuration - 0.74, Math.max(0, cue.localStart - 0.46));
  const rendered = shotStarts[cue.shotId] + 0.46 + activeStart;
  return {shotId: cue.shotId, delta: Math.abs(rendered - expected)};
});
const captionSyncWithin500ms = captionSync.filter(item => item.delta <= 0.5).length / captionSync.length;
const maximumCaptionSyncDelta = Math.max(...captionSync.map(item => item.delta), 0);
const visualEvents = visualTimeline.shots.flatMap(shot => shot.events);
const semanticVisualSyncWithin500ms = visualEvents.filter(event => event.deltaSeconds <= 0.5).length / visualEvents.length;
const maximumSemanticVisualDelta = Math.max(...visualEvents.map(event => event.deltaSeconds), 0);
const explicitSemanticVisualEvents = visualEvents.filter(event => event.strategy === 'explicit-forced-alignment').length;
const alignmentIntegrity = alignment.shots.every(shot => shot.cues?.length && shot.cues.every((cue, index) => cue.start >= 0 && cue.end > cue.start && cue.end <= shot.audioDuration + 0.1 && (index === 0 || cue.start >= shot.cues[index - 1].end)));

const checks = {
  durationMatchesTimeline: Math.abs(duration - timeline.duration) <= 0.1,
  fullHd: videoStream?.width === 1920 && videoStream?.height === 1080,
  frameRate30: videoStream?.r_frame_rate === '30/1',
  stereo48k: audioStream?.channels === 2 && audioStream?.sample_rate === '48000',
  noSustainedBlackFrames: blackSegments.length === 0,
  noLongVisualFreeze: maximumFreezeSeconds < 8 && frozenSeconds / duration < 0.5,
  loudnessInPlatformRange: Number(loudness.input_i) >= -18 && Number(loudness.input_i) <= -14,
  asrAllSegmentsPass: asr.summary.segments === timeline.shots.length && asr.summary.below0_8 === 0 && asr.summary.errors === 0,
  subtitleCoverage: subtitleCues >= timeline.shots.length,
  captionsUseForcedAlignment:
    captionTimeline.alignment?.storyFingerprint === alignment.storyFingerprint
    && captionTimeline.cues.every(cue => cue.timingSource === 'forced-alignment'),
  forcedAlignmentCoverage:
    alignment.proportionalFallbackAllowed === false
    && alignment.narrationMasterSha256 === narrationMasterSha256
    && alignment.metrics?.shots === timeline.shots.length
    && alignment.metrics?.meanTranscriptSimilarity >= 0.85
    && alignment.metrics?.minimumTranscriptSimilarity >= 0.55
    && alignment.metrics?.minimumMatchedTargetCharacterRatio >= 0.55,
  forcedAlignmentCueIntegrity: alignmentIntegrity,
  captionTimelineWithin500ms: captionSyncWithin500ms >= 0.95,
  semanticVisualEventsWithin500ms: semanticVisualSyncWithin500ms >= 0.95,
  semanticVisualEventsExplicitlyMapped:
    visualTimeline.mappingPolicy?.mode === 'explicit-human-semantic'
    && visualTimeline.mappingPolicy?.timingSource === 'forced-alignment-word-timestamps'
    && visualTimeline.mappingPolicy?.proportionalFallbackAllowed === false
    && explicitSemanticVisualEvents === visualEvents.length,
  noTextOverflowRisks: layout.pass === true && layout.textOverflowRisks.length === 0,
  characterAspectPreserved: layout.characterAspectPreserved === true && layout.characterShotsDeclareContain === true,
  cardSystemV2Declared: layout.cardSystemV2Declared === true && layout.detachedBadgeGapPasses === true,
  sceneGrammarV2Declared: layout.sceneGrammarV2Declared === true,
  performanceSystemDeclared: layout.performanceSystemDeclared === true && layout.performanceBeatsPass === true,
  performancePoseAspectPreserved: layout.performancePoseAspectPreserved === true,
  characterStageV3Declared: layout.actorStagePass === true,
  traceDelivered: trace.status === 'complete' && trace.traceKind === 'production-narrative' && trace.events.length === timeline.shots.length,
};

const report = {
  schemaVersion: '1.0',
  artifact: 'final/ai-agent-harness-complete.mp4',
  media: {
    duration,
    sizeBytes: Number(probe.format.size),
    bitRate: Number(probe.format.bit_rate),
    video: videoStream,
    audio: audioStream,
  },
  loudness: {
    integratedLufs: Number(loudness.input_i),
    truePeakDb: Number(loudness.input_tp),
    rangeLu: Number(loudness.input_lra),
  },
  blackSegments,
  motion: {freezeSegmentsOver3Seconds: freezeDurations.length, frozenSeconds, frozenFraction: frozenSeconds / duration, maximumFreezeSeconds},
  asr: asr.summary,
  subtitles: {cues: subtitleCues, within500ms: captionSyncWithin500ms, maximumDeltaSeconds: maximumCaptionSyncDelta},
  forcedAlignment: {method: alignment.method, model: alignment.model, metrics: alignment.metrics},
  visualEvents: {
    events: visualEvents.length,
    explicitlyMapped: explicitSemanticVisualEvents,
    mappingMode: visualTimeline.mappingPolicy?.mode,
    timingSource: visualTimeline.mappingPolicy?.timingSource,
    proportionalFallbackAllowed: visualTimeline.mappingPolicy?.proportionalFallbackAllowed,
    within500ms: semanticVisualSyncWithin500ms,
    maximumDeltaSeconds: maximumSemanticVisualDelta,
  },
  layout: {
    textContainers: layout.textContainers,
    textOverflowRisks: layout.textOverflowRisks.length,
    minimumSelectedFontSize: layout.minimumSelectedFontSize,
    characterAspectPreserved: layout.characterAspectPreserved,
    characterShotsDeclareContain: layout.characterShotsDeclareContain,
    characterContainedSize: layout.characterContainedSize,
    cardSystem: layout.cardSystem,
    cardSystemV2Declared: layout.cardSystemV2Declared,
    detachedBadgeGap: layout.detachedBadgeGap,
    detachedBadgeGapPasses: layout.detachedBadgeGapPasses,
    sceneGrammar: layout.sceneGrammar,
    topologyCompositionCounts: layout.topologyCompositionCounts,
    maximumSingleCompositionShare: layout.maximumSingleCompositionShare,
    sceneGrammarV2Declared: layout.sceneGrammarV2Declared,
    performanceSystem: layout.performanceSystem,
    performanceStates: layout.performanceStates,
    performanceBeatsPerShot: layout.performanceBeatsPerShot,
    performancePoseAssets: layout.performancePoseAssets,
    performancePoseSizes: layout.performancePoseSizes,
    performancePoseAspectPreserved: layout.performancePoseAspectPreserved,
    performanceBeatsPass: layout.performanceBeatsPass,
    performanceSystemDeclared: layout.performanceSystemDeclared,
    characterStage: layout.characterStage,
    actorStageVisualKinds: layout.actorStageVisualKinds,
    actorStageAssets: layout.actorStageAssets,
    actorStagePass: layout.actorStagePass,
  },
  trace: {runId: trace.runId, status: trace.status, kind: trace.traceKind, events: trace.events.length},
  checks,
  pass: Object.values(checks).every(Boolean),
};

await writeFile(resolve(example, 'evaluation/technical-qa.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(report, null, 2));
if (!report.pass) process.exitCode = 1;
