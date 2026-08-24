import {readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {
  CHARACTER_CONTAINED_SIZE,
  CHARACTER_SOURCE_SIZE,
  CHARACTER_VIEWPORT,
  CARD_SYSTEM_V2,
  SCENE_GRAMMAR_V2,
  XIAOLAN_PERFORMANCE_V1,
  detachedBadgeX,
  fitText,
  type TextFitOptions,
} from '../packages/renderer-revideo/src/layout-contracts';

type TextEntry = {shotId: string; role: string; text: string; width: number; height: number; options: TextFitOptions};
type Visual = Record<string, any> & {kind: string};
type Shot = {id: string; headline: string; visual: Visual};

const root = resolve(__dirname, '..');
const example = resolve(root, 'examples/ai-agent-harness-complete');

function entry(shotId: string, role: string, text: unknown, width: number, height: number, options: TextFitOptions): TextEntry | null {
  return typeof text === 'string' && text.length ? {shotId, role, text, width, height, options} : null;
}

function visualEntries(shot: Shot): TextEntry[] {
  const visual = shot.visual;
  const items: Array<TextEntry | null> = [entry(shot.id, 'headline', shot.headline, 1520, 82, {maxFontSize: 52, minFontSize: 30, maxLines: 2})];
  const addMany = (role: string, values: unknown[], width: number, height: number, options: TextFitOptions) => {
    values.forEach(value => items.push(entry(shot.id, role, typeof value === 'string' ? value : (value as any)?.label, width, height, options)));
  };
  switch (visual.kind) {
    case 'character': addMany('status', visual.status ?? [], 470, 64, {maxFontSize: 22, minFontSize: 15, maxLines: 2}); break;
    case 'compare':
      items.push(entry(shot.id, 'compare-title', visual.left?.title, 610, 60, {maxFontSize: 28, minFontSize: 18, maxLines: 2}));
      items.push(entry(shot.id, 'compare-title', visual.right?.title, 610, 60, {maxFontSize: 28, minFontSize: 18, maxLines: 2}));
      addMany('compare-item', [...(visual.left?.items ?? []), ...(visual.right?.items ?? [])], 530, 76, {maxFontSize: 27, minFontSize: 17, maxLines: 3});
      break;
    case 'evidence': addMany('evidence-callout', visual.callouts ?? [], 540, 108, {maxFontSize: 27, minFontSize: 17, maxLines: 3}); break;
    case 'topology':
      addMany('topology-node', visual.nodes ?? [], 252, 42, {maxFontSize: 22, minFontSize: 15, maxLines: 2});
      addMany('topology-meter', visual.meters ?? [], 400, 38, {maxFontSize: 18, minFontSize: 13, maxLines: 2});
      break;
    case 'stack': addMany('stack-layer', visual.layers ?? [], 520, 62, {maxFontSize: 22, minFontSize: 15, maxLines: 2}); break;
    case 'code': addMany('code-line', visual.lines ?? [], 1160, 46, {maxFontSize: 25, minFontSize: 15, maxLines: 1}); break;
    case 'gates': addMany('gate', visual.gates ?? [], 154, 118, {maxFontSize: 20, minFontSize: 13, maxLines: 4}); break;
    case 'swimlane': addMany('swimlane-event', visual.events ?? [], 328, 34, {maxFontSize: 17, minFontSize: 12, maxLines: 2}); break;
    case 'timeline': addMany('timeline-event', visual.events ?? [], 1080, 46, {maxFontSize: 22, minFontSize: 14, maxLines: 1}); break;
    case 'bars':
      addMany('bar-label', visual.bars ?? [], 160, 48, {maxFontSize: 20, minFontSize: 13, maxLines: 2});
      addMany('bar-after-label', visual.after ?? [], 160, 48, {maxFontSize: 20, minFontSize: 13, maxLines: 2});
      items.push(entry(shot.id, 'chart-note', visual.note, 660, 50, {maxFontSize: 21, minFontSize: 14, maxLines: 2}));
      break;
    case 'curve':
      addMany('axis-label', visual.x ?? [], 200, 42, {maxFontSize: 17, minFontSize: 12, maxLines: 2});
      addMany('series-label', visual.series ?? [], 300, 38, {maxFontSize: 18, minFontSize: 13, maxLines: 2});
      items.push(entry(shot.id, 'chart-note', visual.note, 710, 38, {maxFontSize: 18, minFontSize: 13, maxLines: 2}));
      break;
  }
  return items.filter((item): item is TextEntry => Boolean(item));
}

function pngSize(buffer: Buffer) {
  const signature = buffer.subarray(1, 4).toString('ascii');
  if (signature !== 'PNG') throw new Error('Character asset is not a PNG');
  return {width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20)};
}

async function main() {
  const story = JSON.parse(await readFile(resolve(example, 'storyboard/story.json'), 'utf8')) as {meta: {designSystem?: Record<string, string>}; shots: Shot[]};
  const captions = JSON.parse(await readFile(resolve(example, 'audio/captions.timeline.json'), 'utf8')) as {cues: Array<{shotId: string; text: string}>};
  const entries = [
    ...story.shots.flatMap(visualEntries),
    ...captions.cues.map(cue => ({shotId: cue.shotId, role: 'caption', text: cue.text, width: 1500, height: 88, options: {maxFontSize: 31, minFontSize: 23, maxLines: 2}})),
  ];
  const measured = entries.map(item => ({...item, fit: fitText(item.text, item.width, item.height, item.options)}));
  const overflowRisks = measured.filter(item => !item.fit.fits);
  const characterFiles = ['xiaolan-evidence-bridge.png', 'xiaolan-connect-modules.png', 'xiaolan-recover-path.png'];
  const characterSizes = await Promise.all(characterFiles.map(async file => ({file, ...pngSize(await readFile(resolve(example, 'assets/characters', file)))})));
  const sourceRatio = CHARACTER_SOURCE_SIZE.width / CHARACTER_SOURCE_SIZE.height;
  const renderedRatio = CHARACTER_CONTAINED_SIZE.width / CHARACTER_CONTAINED_SIZE.height;
  const characterAspectPreserved = characterSizes.every(size => Math.abs(size.width / size.height - sourceRatio) < 0.001)
    && Math.abs(sourceRatio - renderedRatio) < 0.001
    && CHARACTER_CONTAINED_SIZE.width <= CHARACTER_VIEWPORT.width
    && CHARACTER_CONTAINED_SIZE.height <= CHARACTER_VIEWPORT.height;
  const characterShotsDeclareContain = story.shots
    .filter(shot => shot.visual.kind === 'character')
    .every(shot => shot.visual.assetFit === 'contain');
  const cardSystemV2Declared = story.meta.designSystem?.cardSystem === CARD_SYSTEM_V2.id
    && story.meta.designSystem?.indexTreatment === CARD_SYSTEM_V2.indexTreatment
    && story.meta.designSystem?.contentAlignment === CARD_SYSTEM_V2.contentAlignment
    && story.meta.designSystem?.evidenceRelationship === CARD_SYSTEM_V2.evidenceRelationship;
  const detachedBadgeGap = -650 / 2 - (detachedBadgeX(650, 62) + 62 / 2);
  const detachedBadgeGapPasses = detachedBadgeGap >= CARD_SYSTEM_V2.indexGap;
  const topologyShots = story.shots.filter(shot => shot.visual.kind === 'topology');
  const topologyCompositions = topologyShots.map(shot => String(shot.visual.composition ?? ''));
  const validTopologyCompositions = new Set(SCENE_GRAMMAR_V2.topologyCompositions);
  const compositionCounts = Object.fromEntries([...new Set(topologyCompositions)].map(composition => [composition, topologyCompositions.filter(value => value === composition).length]));
  const distinctTopologyCompositions = Object.keys(compositionCounts).length;
  const maximumSingleCompositionShare = Math.max(...Object.values(compositionCounts), 0) / Math.max(1, topologyShots.length);
  const sceneGrammarV2Declared = story.meta.designSystem?.sceneGrammar === SCENE_GRAMMAR_V2.id
    && topologyCompositions.every(composition => validTopologyCompositions.has(composition as any))
    && distinctTopologyCompositions >= SCENE_GRAMMAR_V2.minimumDistinctTopologyCompositions
    && maximumSingleCompositionShare <= SCENE_GRAMMAR_V2.maximumSingleCompositionShare;
  const characterShots = story.shots.filter(shot => shot.visual.kind === 'character');
  const performanceStates = characterShots.map(shot => shot.visual.performance?.state).filter(Boolean);
  const performanceSystemDeclared = story.meta.designSystem?.performanceSystem === XIAOLAN_PERFORMANCE_V1.id
    && characterShots.every(shot => XIAOLAN_PERFORMANCE_V1.requiredFields.every(field => typeof shot.visual.performance?.[field] === 'string' && shot.visual.performance[field].length > 0))
    && XIAOLAN_PERFORMANCE_V1.states.every(state => performanceStates.includes(state));
  const report = {
    schemaVersion: '1.0',
    textContainers: measured.length,
    textOverflowRisks: overflowRisks.map(item => ({shotId: item.shotId, role: item.role, text: item.text, fit: item.fit})),
    minimumSelectedFontSize: Math.min(...measured.map(item => item.fit.fontSize)),
    characterAssets: characterSizes,
    characterViewport: CHARACTER_VIEWPORT,
    characterContainedSize: CHARACTER_CONTAINED_SIZE,
    characterAspectPreserved,
    characterShotsDeclareContain,
    cardSystem: CARD_SYSTEM_V2,
    cardSystemV2Declared,
    detachedBadgeGap,
    detachedBadgeGapPasses,
    sceneGrammar: SCENE_GRAMMAR_V2,
    topologyCompositionCounts: compositionCounts,
    distinctTopologyCompositions,
    maximumSingleCompositionShare,
    sceneGrammarV2Declared,
    performanceSystem: XIAOLAN_PERFORMANCE_V1,
    performanceStates,
    performanceSystemDeclared,
    pass: overflowRisks.length === 0
      && characterAspectPreserved
      && characterShotsDeclareContain
      && cardSystemV2Declared
      && detachedBadgeGapPasses
      && sceneGrammarV2Declared
      && performanceSystemDeclared,
  };
  await writeFile(resolve(example, 'evaluation/layout-qa.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(report, null, 2));
  if (!report.pass) process.exitCode = 1;
}

main().catch(error => {console.error(error); process.exitCode = 1;});
