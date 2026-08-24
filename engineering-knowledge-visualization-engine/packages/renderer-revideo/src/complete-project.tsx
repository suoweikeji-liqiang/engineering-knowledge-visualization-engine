import {Audio, Circle, Grid, Img, Layout, Line, Rect, Txt, View2D, makeScene2D} from '@revideo/2d';
import {Reference, all, chain, createRef, easeInOutCubic, linear, makeProject, tween, waitFor} from '@revideo/core';
import storyDocument from '../../../examples/ai-agent-harness-complete/storyboard/story.json';
import timeline from '../../../examples/ai-agent-harness-complete/audio/video.timeline.json';
import captionTimeline from '../../../examples/ai-agent-harness-complete/audio/captions.timeline.json';
import visualTimeline from '../../../examples/ai-agent-harness-complete/audio/visual-events.timeline.json';
import {ASTEROID_WARM_THEME as C} from './theme';
import {CINEMATIC_FONT as FONT, CINEMATIC_MONO as MONO} from './cinematic-sketch';
import {
  CHARACTER_CONTAINED_SIZE,
  detachedBadgeX,
  fitText,
  type TopologyComposition,
  type XiaolanMotionProfile,
  type XiaolanPerformanceState,
} from './layout-contracts';

type Visual = {
  kind: string;
  asset?: string;
  characterAsset?: string;
  assetFit?: 'contain';
  performanceLabel?: string;
  performance?: {
    state: XiaolanPerformanceState;
    emotion: string;
    gesture: string;
    motionProfile: XiaolanMotionProfile;
    focusTarget: string;
    beats?: Array<{
      id: string;
      cueIndex: number;
      pose: string;
      gaze: 'viewer' | 'object' | 'path' | 'offscreen';
      gesture: string;
      expression: string;
      asset: string;
      transition: 'cut-in' | 'match-cut' | 'reaction-pop';
    }>;
  };
  status?: string[];
  left?: {title: string; items: string[]};
  right?: {title: string; items: string[]};
  center?: string;
  nodes?: string[];
  meters?: string[];
  layers?: string[];
  output?: string;
  filename?: string;
  lines?: string[];
  focus?: number[];
  input?: string;
  gates?: string[];
  lanes?: string[];
  events?: Array<string | {from: string; to: string; label: string; semanticType?: string}>;
  bars?: Array<{label: string; value: number}>;
  after?: Array<{label: string; value: number}>;
  series?: Array<{label: string; values: number[]}>;
  x?: string[];
  note?: string;
  callouts?: string[];
  edgeDirection?: 'inbound' | 'outbound';
  continuityKey?: string;
  composition?: TopologyComposition;
};

type CompleteShot = {
  id: string;
  headline: string;
  dialogue: string;
  visual: Visual;
};

const story = storyDocument as unknown as {shots: CompleteShot[]; chapters: Array<{id: string; shotIds: string[]}>};
const durations = Object.fromEntries(timeline.shots.map(shot => [shot.id, shot.duration]));
const captionsByShot = captionTimeline.cues.reduce<Record<string, (typeof captionTimeline.cues)[number][]>>((result, cue) => {
  (result[cue.shotId] ??= []).push(cue);
  return result;
}, {});
const visualEventsByShot = Object.fromEntries(visualTimeline.shots.map(shot => [shot.shotId, shot.events]));
const ACCENTS = [C.red, C.cyan, C.yellow, C.purple, C.green] as const;

type CompleteStage = {root: Reference<Layout>; body: Reference<Layout>; caption: Reference<Txt>; scan: Reference<Rect>; direction: number};

function continuityDirection(shot: CompleteShot, index: number): number {
  const key = shot.visual.continuityKey;
  if (!key) return index % 2 ? 1 : -1;
  const hash = [...key].reduce((total, character) => total + character.codePointAt(0)!, 0);
  return hash % 2 ? 1 : -1;
}

function splitCaption(text: string, maxChars = 34): string[] {
  const clauses = text.split(/(?<=[。！？；])/u).map(item => item.trim()).filter(Boolean);
  const result: string[] = [];
  let current = '';
  for (const clause of clauses) {
    if (current && current.length + clause.length > maxChars) {
      result.push(current);
      current = clause;
    } else {
      current += clause;
    }
  }
  if (current) result.push(current);
  return result.length ? result : [text];
}

function makeCompleteStage(view: View2D, index: number, shot: CompleteShot, accent: string): CompleteStage {
  const root = createRef<Layout>();
  const body = createRef<Layout>();
  const caption = createRef<Txt>();
  const scan = createRef<Rect>();
  view.add(
    <Layout ref={root} size={[1920, 1080]} opacity={0} scale={0.985}>
      <Layout position={[-760, -438]} layout direction={'row'} gap={16} alignItems={'center'}>
        <Rect width={48} height={7} radius={4} fill={accent} />
        <Txt fontFamily={MONO} fontSize={21} fontWeight={800} letterSpacing={2.4} fill={accent} text={`OBSERVATION ${String(index + 1).padStart(2, '0')}`} />
      </Layout>
      <Txt position={[0, -374]} width={1520} textAlign={'left'} fontFamily={FONT} fontSize={52} fontWeight={800} fill={C.primary} text={shot.headline} />
      <Rect position={[-570, -318]} width={390} height={16} radius={8} fill={`${accent}2A`} rotation={-0.7} />
      <Rect ref={scan} position={[-820, 18]} width={280} height={650} radius={140} fill={`${accent}0B`} rotation={-5} />
      <Layout ref={body} position={[0, 18]} size={[1640, 650]} />
      <Layout position={[0, 438]}>
        <Rect x={6} y={7} width={1638} height={102} radius={[20, 25, 22, 24]} fill={'#E4D6C5'} rotation={0.2} />
        <Rect width={1640} height={104} radius={[23, 20, 25, 21]} fill={'#FFF9F0F2'} stroke={C.line} lineWidth={2}>
          <Txt ref={caption} width={1500} fontFamily={FONT} fontSize={31} fontWeight={650} lineHeight={44} textAlign={'center'} fill={C.primary} text={''} />
        </Rect>
        <Rect x={-712} y={-53} width={112} height={22} radius={4} fill={`${C.tape}B8`} rotation={-2.5} />
        <Rect x={712} y={-53} width={112} height={22} radius={4} fill={`${accent}42`} rotation={2.5} />
      </Layout>
    </Layout>,
  );
  return {root, body, caption, scan, direction: continuityDirection(shot, index)};
}

function* ambientScan(stage: CompleteStage, duration: number) {
  yield* stage.scan().position.x(820, duration, linear);
}

function visualDelay(shotId: string, index: number): number {
  const event = visualEventsByShot[shotId]?.[index];
  if (!event) throw new Error(`Missing semantic visual cue ${shotId}:${index}`);
  return event.activeStart;
}

function* enter(stage: CompleteStage) {
  const direction = stage.direction;
  stage.root().position.x(34 * direction);
  stage.root().rotation(0.28 * direction);
  yield* all(
    stage.root().opacity(1, 0.32),
    stage.root().scale(1, 0.46, easeInOutCubic),
    stage.root().position.x(0, 0.46, easeInOutCubic),
    stage.root().rotation(0, 0.46, easeInOutCubic),
  );
}

function* exit(stage: CompleteStage) {
  const direction = stage.direction;
  yield* all(stage.root().opacity(0, 0.28), stage.root().scale(1.012, 0.28), stage.root().position.x(-24 * direction, 0.28));
  stage.root().remove();
}

function* captions(stage: CompleteStage, shotId: string, duration: number) {
  const cues = captionsByShot[shotId] ?? [];
  const entryOffset = 0.46;
  let elapsed = 0;
  for (const cue of cues) {
    const cueStart = Math.min(duration, Math.max(0, cue.localStart - entryOffset));
    const cueEnd = Math.min(duration, cue.localEnd - entryOffset);
    if (cueStart > elapsed) {
      yield* waitFor(cueStart - elapsed);
      elapsed = cueStart;
    }
    const transition = Math.min(0.12, Math.max(0, cueEnd - elapsed) * 0.18);
    yield* stage.caption().text(cue.text, transition);
    elapsed += transition;
    if (cueEnd > elapsed) {
      yield* waitFor(cueEnd - elapsed);
      elapsed = cueEnd;
    }
  }
  if (duration > elapsed) yield* waitFor(duration - elapsed);
}

function paperCard(title: string, detail: string, color: string, width = 300, height = 140) {
  const titleFit = fitText(title, width - 48, 42, {maxFontSize: 22, minFontSize: 15, maxLines: 2});
  const detailFit = fitText(detail, width - 48, 56, {maxFontSize: 19, minFontSize: 13, maxLines: 2});
  return (
    <Layout>
      <Rect x={8} y={10} width={width} height={height} radius={[20, 25, 18, 23]} fill={'#DCCFBE88'} />
      <Rect width={width} height={height} radius={[22, 18, 24, 20]} fill={'#FFFCF7'} stroke={C.line} lineWidth={1.5} shadowColor={'#6D594024'} shadowBlur={18}>
        <Rect x={-width / 2 + 6} width={10} height={height - 28} radius={5} fill={color} />
        <Layout x={12} width={width - 62} height={height - 30} layout direction={'column'} justifyContent={'center'} alignItems={'start'} gap={7}>
          <Txt width={width - 62} textWrap={true} textAlign={'left'} fontFamily={MONO} fontSize={titleFit.fontSize} lineHeight={titleFit.lineHeight} fontWeight={850} fill={C.primary} text={title} />
          <Txt width={width - 62} textWrap={true} textAlign={'left'} fontFamily={FONT} fontSize={detailFit.fontSize} lineHeight={detailFit.lineHeight} fill={C.soft} text={detail} />
        </Layout>
      </Rect>
    </Layout>
  );
}

function* characterShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const accent = ACCENTS[index % ACCENTS.length];
  const stage = makeCompleteStage(view, index, shot, accent);
  const image = createRef<Layout>();
  const portrait = createRef<Img>();
  const liveDot = createRef<Circle>();
  const statuses = shot.visual.status ?? [];
  const refs = statuses.map(() => createRef<Layout>());
  const statusGap = 17;
  const statusHeight = 86;
  const statusStep = statusHeight + statusGap;
  const statusStartY = -((statuses.length - 1) * statusStep) / 2;
  const asset = shot.visual.asset ?? shot.visual.characterAsset ?? 'xiaolan-evidence-bridge.png';
  const performanceLabel = shot.visual.performanceLabel ?? '现场讲解';
  const performance = shot.visual.performance ?? {
    state: 'investigate',
    emotion: 'focused',
    gesture: 'annotate',
    motionProfile: 'scan-and-mark',
    focusTarget: 'evidence',
    beats: [],
  };
  const performanceBeats = performance.beats ?? [];
  const poseRefs = performanceBeats.map(() => createRef<Layout>());
  stage.body().add(
    <>
      <Layout ref={image} x={-420} opacity={0} scale={0.94} rotation={-1.2}>
        <Rect x={9} y={12} width={860} height={600} radius={28} fill={'#DCCDBA'} />
        <Rect width={860} height={600} radius={26} fill={C.paper} stroke={C.line} lineWidth={3} shadowColor={'#6D594044'} shadowBlur={28} clip>
          <Img
            ref={portrait}
            y={-34}
            src={`/complete/characters/${asset}`}
            width={CHARACTER_CONTAINED_SIZE.width}
            height={CHARACTER_CONTAINED_SIZE.height}
            radius={18}
          />
          <Rect y={252} width={824} height={68} radius={16} fill={'#FFF9F0EE'} stroke={accent} lineWidth={2}>
            <Circle ref={liveDot} x={-365} width={13} height={13} fill={accent} shadowColor={accent} shadowBlur={18} />
            <Txt x={18} width={690} textAlign={'left'} fontFamily={MONO} fontSize={19} fontWeight={800} fill={C.primary} text={`XIAOLAN · ${performanceLabel}`} />
          </Rect>
        </Rect>
        <Rect y={-310} width={126} height={28} radius={5} fill={`${C.tape}D8`} rotation={3} />
        <Rect x={272} y={-260} width={268} height={42} radius={21} fill={C.night} stroke={`${accent}88`} lineWidth={2} shadowColor={'#2B253033'} shadowBlur={14}>
          <Circle x={-108} width={10} height={10} fill={accent} shadowColor={accent} shadowBlur={12} />
          <Txt x={10} width={208} textAlign={'left'} fontFamily={MONO} fontSize={15} fontWeight={850} fill={C.onDark} text={`${performance.state.toUpperCase()} · ${performance.emotion.toUpperCase()}`} />
        </Rect>
        {performanceBeats.map((beat, beatIndex) => (
          <Layout ref={poseRefs[beatIndex]} x={beat.transition === 'cut-in' ? 310 : 250} y={26} opacity={0} scale={beat.transition === 'reaction-pop' ? 0.82 : 0.94} rotation={beatIndex % 2 ? 1.1 : -1.1}>
            <Rect x={6} y={7} width={286} height={190} radius={[16, 20, 15, 18]} fill={'#DCCFBE88'} />
            <Rect width={286} height={190} radius={[16, 20, 15, 18]} fill={'#FFFCF7'} stroke={accent} lineWidth={2} shadowColor={'#6D594033'} shadowBlur={18}>
              <Img y={-14} src={`/complete/poses/${beat.asset}`} width={268} height={150} radius={11} />
              <Rect y={76} width={268} height={28} radius={[0, 0, 9, 9]} fill={C.night}>
                <Circle x={-116} width={8} height={8} fill={accent} />
                <Txt x={8} width={220} textAlign={'left'} fontFamily={MONO} fontSize={17} fontWeight={850} fill={C.onDark} text={beat.expression.toUpperCase()} />
              </Rect>
            </Rect>
          </Layout>
        ))}
      </Layout>
      <Layout x={480}>
        {statuses.map((item, idx) => {
          const statusFit = fitText(item, 490, 64, {maxFontSize: 22, minFontSize: 15, maxLines: 2});
          return (
            <Layout ref={refs[idx]} y={statusStartY + idx * statusStep} opacity={0} x={42} scale={0.94}>
              <Rect x={5} y={6} width={610} height={86} radius={[15, 20, 16, 18]} fill={'#DCCFBE66'} />
              <Rect width={610} height={86} radius={[15, 20, 16, 18]} fill={idx === statuses.length - 1 ? `${accent}10` : '#FFFCF7'} stroke={C.line} lineWidth={1.5}>
                <Rect x={-299} width={8} height={62} radius={4} fill={accent} />
                <Txt x={26} width={490} textWrap={true} textAlign={'left'} fontFamily={MONO} fontSize={statusFit.fontSize} lineHeight={statusFit.lineHeight} fontWeight={700} fill={C.primary} text={item} />
              </Rect>
              <Rect x={detachedBadgeX(610, 58)} width={58} height={36} radius={12} fill={accent} shadowColor={`${accent}44`} shadowBlur={12}>
                <Txt fontFamily={MONO} fontSize={17} fontWeight={900} fill={'#FFFFFF'} text={String(idx + 1).padStart(2, '0')} />
              </Rect>
            </Layout>
          );
        })}
      </Layout>
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  const poseAnimations = performanceBeats.map((beat, beatIndex) => {
    const start = visualDelay(shot.id, beat.cueIndex);
    const nextStart = performanceBeats[beatIndex + 1] ? visualDelay(shot.id, performanceBeats[beatIndex + 1].cueIndex) : active;
    const hasNextBeat = beatIndex < performanceBeats.length - 1;
    const transitionDuration = hasNextBeat ? 0.58 : 0.38;
    const hold = Math.max(0, nextStart - start - transitionDuration);
    return chain(
      waitFor(start),
      all(poseRefs[beatIndex]().opacity(1, 0.2), poseRefs[beatIndex]().scale(1.02, 0.26, easeInOutCubic), poseRefs[beatIndex]().position.x(250, 0.26, easeInOutCubic), poseRefs[beatIndex]().position.y(18, 0.26, easeInOutCubic)),
      poseRefs[beatIndex]().scale(1, 0.12, easeInOutCubic),
      waitFor(hold),
      hasNextBeat
        ? all(poseRefs[beatIndex]().opacity(0, 0.2), poseRefs[beatIndex]().scale(0.97, 0.2), poseRefs[beatIndex]().position.y(12, 0.2))
        : waitFor(0),
    );
  });
  yield* all(
    all(image().opacity(1, 0.4), image().scale(1, 0.55)),
    ...refs.map((ref, cueIndex) => chain(
      waitFor(visualDelay(shot.id, cueIndex)),
      all(ref().opacity(1, 0.24), ref().position.x(0, 0.34), ref().scale(1.035, 0.28, easeInOutCubic)),
      ref().scale(1, 0.16, easeInOutCubic),
    )),
    ...poseAnimations,
    image().position.x(-405, active, easeInOutCubic),
    tween(active, value => {
      const phase = value * Math.PI * 4;
      if (performance.motionProfile === 'error-to-success') {
        const damping = 1 - value;
        portrait().position.x(Math.sin(value * Math.PI * 18) * damping * 7);
        portrait().position.y(-34 + Math.cos(phase * 0.65) * 3);
        portrait().scale(1.008 + value * 0.008);
        portrait().rotation(Math.sin(value * Math.PI * 14) * damping * 0.32);
      } else if (performance.motionProfile === 'assemble-and-present') {
        portrait().position.x(Math.sin(phase * 0.5) * 3);
        portrait().position.y(-34 - value * 6 + Math.cos(phase * 0.5) * 2);
        portrait().scale(1.004 + value * 0.016);
        portrait().rotation(-0.18 + value * 0.18);
      } else {
        portrait().position.x(Math.sin(phase) * 6);
        portrait().position.y(-34 + Math.cos(phase * 0.7) * 4);
        portrait().scale(1.006 + Math.sin(phase * 0.5) * 0.006);
        portrait().rotation(Math.sin(phase * 0.35) * 0.12);
      }
      liveDot().scale(0.88 + Math.sin(phase * 1.4) * 0.16);
      liveDot().shadowBlur(12 + (Math.sin(phase * 1.4) + 1) * 8);
    }),
    ambientScan(stage, active),
    captions(stage, shot.id, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function compareBoard(title: string, items: string[], color: string) {
  const titleFit = fitText(title, 610, 60, {maxFontSize: 28, minFontSize: 18, maxLines: 2});
  const itemStep = items.length <= 3 ? 112 : items.length === 4 ? 90 : 72;
  const itemStartY = 45 - ((items.length - 1) * itemStep) / 2;
  return (
    <Layout>
      <Rect x={9} y={11} width={710} height={560} radius={[28, 22, 30, 24]} fill={'#DCCFBE77'} />
      <Rect width={710} height={560} radius={[28, 22, 30, 24]} fill={'#FFFCF7'} stroke={C.line} lineWidth={1.5} shadowColor={'#6D594024'} shadowBlur={24}>
        <Rect y={-274} width={650} height={12} radius={6} fill={color} />
        <Txt y={-224} width={610} textWrap={true} fontFamily={MONO} fontSize={titleFit.fontSize} lineHeight={titleFit.lineHeight} fontWeight={900} fill={color} text={title} />
        <Line y={-178} points={[[-300, 0], [300, 0]]} stroke={`${color}48`} lineWidth={2} />
        {items.map((item, idx) => (
          <Layout y={itemStartY + idx * itemStep}>
            <Rect x={-275} width={22} height={22} radius={7} fill={`${color}18`} stroke={color} lineWidth={2}>
              <Circle width={7} height={7} fill={color} />
            </Rect>
            <Txt x={25} width={530} textWrap={true} textAlign={'left'} fontFamily={FONT} fontSize={fitText(item, 530, 76, {maxFontSize: 27, minFontSize: 17, maxLines: 3}).fontSize} lineHeight={31} fontWeight={650} fill={C.primary} text={item} />
          </Layout>
        ))}
      </Rect>
    </Layout>
  );
}

function* compareShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, ACCENTS[index % ACCENTS.length]);
  const left = createRef<Layout>();
  const right = createRef<Layout>();
  const divider = createRef<Line>();
  stage.body().add(
    <>
      <Layout ref={left} x={-405} opacity={0} scale={0.94} rotation={-0.5}>{compareBoard(shot.visual.left?.title ?? 'A', shot.visual.left?.items ?? [], C.cyan)}</Layout>
      <Layout ref={right} x={405} opacity={0} scale={0.94} rotation={0.45}>{compareBoard(shot.visual.right?.title ?? 'B', shot.visual.right?.items ?? [], C.red)}</Layout>
      <Line ref={divider} points={[[0, -285], [0, 285]]} stroke={C.yellow} lineWidth={5} lineDash={[14, 12]} end={0} />
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    chain(waitFor(visualDelay(shot.id, 0)), all(left().opacity(1, 0.42), left().scale(1, 0.5))),
    chain(waitFor((visualDelay(shot.id, 0) + visualDelay(shot.id, 1)) / 2), divider().end(1, 0.55)),
    chain(waitFor(visualDelay(shot.id, 1)), all(right().opacity(1, 0.42), right().scale(1, 0.5))),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* evidenceShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.red);
  const document = createRef<Layout>();
  const sourceImage = createRef<Img>();
  const callouts = shot.visual.callouts ?? [];
  const refs = callouts.map(() => createRef<Layout>());
  const connectors = callouts.map(() => createRef<Line>());
  const calloutY = (idx: number) => -190 + idx * 190;
  stage.body().add(
    <>
      <Layout ref={document} x={-430} opacity={0} scale={0.94} rotation={-0.8}>
        <Rect x={8} y={10} width={460} height={610} radius={18} fill={'#DCCDBA'} />
        <Rect width={460} height={610} radius={18} fill={'#FFFFFF'} stroke={C.red} lineWidth={3} shadowColor={'#6D594044'} shadowBlur={28} clip>
          <Img ref={sourceImage} src={`/complete/evidence/${shot.visual.asset ?? 'openai-agent-guide-page-04.png'}`} width={460} height={598} />
          <Rect y={-38} width={420} height={48} radius={4} fill={'#D8556210'} stroke={C.red} lineWidth={2} />
          <Rect y={-6} width={460} height={598} fill={'#FFFFFF08'} />
        </Rect>
        <Rect y={-315} width={128} height={26} radius={5} fill={`${C.tape}D8`} rotation={3} />
      </Layout>
      {callouts.map((_, idx) => (
        <Line
          ref={connectors[idx]}
          points={[[-192, -72 + idx * 34], [32, calloutY(idx)]]}
          stroke={`${ACCENTS[idx % ACCENTS.length]}99`}
          lineWidth={3}
          radius={18}
          endArrow
          arrowSize={12}
          end={0}
        />
      ))}
      {callouts.map((item, idx) => {
        const color = ACCENTS[idx % ACCENTS.length];
        const textFit = fitText(item, 540, 108, {maxFontSize: 27, minFontSize: 17, maxLines: 3});
        return (
          <Layout ref={refs[idx]} x={430} y={calloutY(idx)} opacity={0} scale={0.96}>
            <Rect x={7} y={8} width={650} height={142} radius={[20, 24, 19, 22]} fill={'#DCCFBE66'} />
            <Rect width={650} height={142} radius={[20, 24, 19, 22]} fill={'#FFFCF7'} stroke={C.line} lineWidth={1.5} shadowColor={'#6D594024'} shadowBlur={18} clip>
              <Rect x={-319} width={10} height={112} radius={5} fill={color} />
              <Layout x={18} width={540} height={110} layout direction={'column'} justifyContent={'center'} alignItems={'start'}>
                <Txt width={540} textWrap={true} textAlign={'left'} fontFamily={FONT} fontSize={textFit.fontSize} lineHeight={textFit.lineHeight} fontWeight={750} fill={C.primary} text={item} />
              </Layout>
            </Rect>
            <Rect x={detachedBadgeX(650, 62)} y={-48} width={62} height={40} radius={13} fill={color} shadowColor={`${color}55`} shadowBlur={14}>
              <Txt fontFamily={MONO} fontSize={18} fontWeight={900} fill={'#FFFFFF'} text={String(idx + 1).padStart(2, '0')} />
            </Rect>
          </Layout>
        );
      })}
      <Rect x={430} y={286} width={650} height={56} radius={16} fill={'#FFF4C7'} stroke={'#D7B84A66'} lineWidth={1.5}>
        <Circle x={-286} width={10} height={10} fill={C.yellow} />
        <Txt x={12} width={560} textAlign={'left'} fontFamily={MONO} fontSize={17} fontWeight={750} fill={C.primary} text={'PRIMARY SOURCES · OpenAI p.4 + Anthropic'} />
      </Rect>
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    all(document().opacity(1, 0.4), document().scale(1, 0.52)),
    ...refs.map((ref, cueIndex) => chain(
      waitFor(visualDelay(shot.id, cueIndex)),
      all(connectors[cueIndex]().end(1, 0.34, easeInOutCubic), ref().opacity(1, 0.28), ref().scale(1, 0.34)),
    )),
    document().rotation(0.8, active, easeInOutCubic),
    sourceImage().scale(1.018, active, easeInOutCubic),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function splitNode(value: string): [string, string] {
  const [title, ...rest] = value.split(/\s*·\s*/u);
  return [title, rest.join(' · ') || ''];
}

type TopologyGeometry = {
  center: [number, number];
  nodes: Array<[number, number]>;
  nodeWidth: number;
  nodeHeight: number;
};

function evenlySpaced(count: number, start: number, end: number): number[] {
  if (count <= 1) return [(start + end) / 2];
  return Array.from({length: count}, (_, idx) => start + idx * ((end - start) / (count - 1)));
}

function topologyGeometry(composition: TopologyComposition, count: number): TopologyGeometry {
  if (composition === 'branch') {
    return {center: [-560, 0], nodes: evenlySpaced(count, -190, 190).map(y => [250, y]), nodeWidth: 390, nodeHeight: 96};
  }
  if (composition === 'quadrants') {
    const positions: Array<[number, number]> = [[-440, -165], [440, -165], [-440, 165], [440, 165]];
    return {center: [0, 0], nodes: Array.from({length: count}, (_, idx) => positions[idx % positions.length]), nodeWidth: 390, nodeHeight: 126};
  }
  if (composition === 'constellation') {
    const positions: Array<[number, number]> = [[-120, -225], [330, -145], [510, 155], [30, 220], [-310, 80]];
    return {center: [-560, -45], nodes: Array.from({length: count}, (_, idx) => positions[idx % positions.length]), nodeWidth: 310, nodeHeight: 104};
  }
  if (composition === 'dashboard') {
    const positions: Array<[number, number]> = [[-80, -190], [300, -190], [500, 35], [300, 220], [-80, 220]];
    return {center: [-560, 10], nodes: Array.from({length: count}, (_, idx) => positions[idx % positions.length]), nodeWidth: 330, nodeHeight: 104};
  }
  if (composition === 'hero-map') {
    return {center: [0, -150], nodes: evenlySpaced(count, -600, 600).map(x => [x, 165]), nodeWidth: 250, nodeHeight: 106};
  }
  const radiusX = 590;
  const radiusY = 220;
  return {
    center: [0, 0],
    nodes: Array.from({length: count}, (_, idx) => {
      const angle = -Math.PI / 2 + (idx / Math.max(1, count)) * Math.PI * 2;
      return [Math.cos(angle) * radiusX, Math.sin(angle) * radiusY] as [number, number];
    }),
    nodeWidth: 300,
    nodeHeight: 132,
  };
}

function topologyNodePlate(composition: TopologyComposition, title: string, detail: string, color: string, width: number, height: number) {
  const titleFit = fitText(title, width - 50, detail ? 40 : height - 32, {maxFontSize: 22, minFontSize: 15, maxLines: 2});
  const detailFit = fitText(detail, width - 50, 38, {maxFontSize: 17, minFontSize: 13, maxLines: 2});
  const dark = composition === 'dashboard';
  const pill = composition === 'constellation';
  const fill = dark ? C.night : pill ? `${color}16` : composition === 'quadrants' ? `${color}0E` : '#FFFCF7';
  const stroke = dark ? `${color}AA` : pill ? color : C.line;
  return (
    <Layout>
      {composition === 'orbit' ? <Rect x={7} y={8} width={width} height={height} radius={[20, 24, 18, 22]} fill={'#DCCFBE66'} /> : null}
      <Rect width={width} height={height} radius={pill ? height / 2 : composition === 'hero-map' ? 12 : [18, 22, 17, 20]} fill={fill} stroke={stroke} lineWidth={dark || pill ? 2.5 : 1.5} shadowColor={composition === 'orbit' ? '#6D594024' : '#00000000'} shadowBlur={composition === 'orbit' ? 18 : 0}>
        {composition === 'branch' ? <Rect x={-width / 2 + 5} width={10} height={height - 22} radius={5} fill={color} /> : null}
        {composition === 'quadrants' ? <Rect x={-width / 2 + 18} y={-height / 2 + 13} width={36} height={5} radius={3} fill={color} /> : null}
        {composition === 'dashboard' ? <Rect y={-height / 2 + 5} width={width - 34} height={8} radius={4} fill={color} /> : null}
        {composition === 'hero-map' ? <Rect y={height / 2 - 5} width={width - 28} height={8} radius={4} fill={color} /> : null}
        <Layout width={width - 50} height={height - 24} layout direction={'column'} justifyContent={'center'} alignItems={'start'} gap={5}>
          <Txt width={width - 50} textWrap={true} textAlign={pill ? 'center' : 'left'} fontFamily={MONO} fontSize={titleFit.fontSize} lineHeight={titleFit.lineHeight} fontWeight={900} fill={dark ? C.onDark : C.primary} text={title} />
          {detail ? <Txt width={width - 50} textWrap={true} textAlign={pill ? 'center' : 'left'} fontFamily={FONT} fontSize={detailFit.fontSize} lineHeight={detailFit.lineHeight} fill={dark ? C.mutedOnDark : C.soft} text={detail} /> : null}
        </Layout>
      </Rect>
    </Layout>
  );
}

function topologyCenterPlate(composition: TopologyComposition, label: string, accent: string) {
  if (composition === 'branch') {
    return <Rect width={250} height={250} radius={32} fill={C.night} stroke={`${accent}99`} lineWidth={3}><Rect x={-112} width={10} height={190} radius={5} fill={accent} /><Txt width={190} textWrap={true} fontFamily={MONO} fontSize={30} fontWeight={950} fill={C.onDark} text={label} /></Rect>;
  }
  if (composition === 'constellation') {
    return <Rect width={176} height={176} radius={28} rotation={45} fill={C.night} stroke={accent} lineWidth={4} shadowColor={`${accent}44`} shadowBlur={30}><Txt rotation={-45} width={150} textWrap={true} fontFamily={MONO} fontSize={28} fontWeight={950} fill={C.onDark} text={label} /></Rect>;
  }
  if (composition === 'dashboard') {
    return <Rect width={330} height={184} radius={28} fill={'#FFF4C7'} stroke={`${accent}88`} lineWidth={3}><Txt y={-52} fontFamily={MONO} fontSize={15} fontWeight={850} fill={accent} text={'EVALUATION CORE'} /><Line y={-25} points={[[-118, 0], [118, 0]]} stroke={`${accent}55`} lineWidth={2} /><Txt y={24} width={270} fontFamily={MONO} fontSize={30} fontWeight={950} fill={C.primary} text={label} /></Rect>;
  }
  if (composition === 'hero-map') {
    return <Rect width={390} height={136} radius={68} fill={C.night} stroke={accent} lineWidth={4} shadowColor={`${accent}44`} shadowBlur={34}><Circle x={-154} width={16} height={16} fill={accent} shadowColor={accent} shadowBlur={18} /><Txt x={14} width={300} fontFamily={MONO} fontSize={34} fontWeight={950} fill={C.onDark} text={label} /></Rect>;
  }
  const size = composition === 'quadrants' ? 206 : 250;
  return <Circle width={size} height={size} fill={'#FFF9F0'} stroke={accent} lineWidth={6} shadowColor={`${accent}44`} shadowBlur={36}><Txt width={size - 40} fontFamily={MONO} fontSize={composition === 'quadrants' ? 28 : 34} fontWeight={950} fill={C.primary} text={label} /></Circle>;
}

function* topologyShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const accent = ACCENTS[index % ACCENTS.length];
  const stage = makeCompleteStage(view, index, shot, accent);
  const nodes = shot.visual.nodes ?? [];
  const refs = nodes.map(() => createRef<Layout>());
  const center = createRef<Layout>();
  const composition = shot.visual.composition ?? 'orbit';
  const geometry = topologyGeometry(composition, nodes.length);
  stage.body().add(
    <>
      {nodes.map((item, idx) => {
        const [x, y] = geometry.nodes[idx];
        const [centerX, centerY] = geometry.center;
        const deltaX = centerX - x;
        const deltaY = centerY - y;
        const [title, detail] = splitNode(item);
        const outbound = shot.visual.edgeDirection === 'outbound';
        return (
          <Layout ref={refs[idx]} x={x} y={y} opacity={0} scale={0.76}>
            <Line
              points={outbound
                ? [[deltaX * 0.78, deltaY * 0.78], [deltaX * 0.24, deltaY * 0.24]]
                : [[deltaX * 0.24, deltaY * 0.24], [deltaX * 0.78, deltaY * 0.78]]}
              stroke={`${ACCENTS[idx % ACCENTS.length]}88`}
              lineWidth={composition === 'constellation' ? 3 : 5}
              lineDash={composition === 'constellation' ? [12, 10] : undefined}
              endArrow
              arrowSize={18}
            />
            {topologyNodePlate(composition, title, detail, ACCENTS[idx % ACCENTS.length], geometry.nodeWidth, geometry.nodeHeight)}
          </Layout>
        );
      })}
      <Layout ref={center} x={geometry.center[0]} y={geometry.center[1]} opacity={0} scale={0.6}>
        {topologyCenterPlate(composition, shot.visual.center ?? 'SYSTEM', accent)}
      </Layout>
      {(shot.visual.meters ?? []).map((meter, idx) => (
        <Rect x={-510 + idx * 510} y={292} width={440} height={52} radius={26} fill={'#EEE3D5'} stroke={ACCENTS[idx % ACCENTS.length]} lineWidth={2}>
          <Txt width={400} height={38} textWrap={true} fontFamily={MONO} fontSize={fitText(meter, 400, 38, {maxFontSize: 18, minFontSize: 13, maxLines: 2}).fontSize} lineHeight={22} fontWeight={750} fill={C.primary} text={meter} />
        </Rect>
      ))}
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    chain(
      all(center().opacity(1, 0.4), center().scale(1, 0.55)),
      tween(Math.max(0, active - 0.55), value => center().scale(1 + Math.sin(value * Math.PI * 2) * 0.012)),
    ),
    ...refs.map((ref, cueIndex) => chain(waitFor(visualDelay(shot.id, cueIndex)), all(ref().opacity(1, 0.3), ref().scale(1, 0.4)))),
    ambientScan(stage, active),
    captions(stage, shot.id, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* stackShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, ACCENTS[index % ACCENTS.length]);
  const layers = shot.visual.layers ?? [];
  const refs = layers.map(() => createRef<Layout>());
  const output = createRef<Layout>();
  stage.body().add(
    <>
      <Layout x={-330}>
        {layers.map((layer, idx) => {
          const cardWidth = 760 - idx * 24;
          const textWidth = cardWidth - 92;
          const color = ACCENTS[idx % ACCENTS.length];
          const layerFit = fitText(layer, textWidth, 62, {maxFontSize: 22, minFontSize: 15, maxLines: 2});
          return (
            <Layout ref={refs[idx]} y={-245 + idx * (480 / Math.max(1, layers.length - 1))} x={idx * 18} opacity={0} scale={0.92}>
              <Rect x={5} y={6} width={cardWidth} height={82} radius={[14, 18, 15, 17]} fill={'#DCCFBE66'} />
              <Rect width={cardWidth} height={82} radius={[14, 18, 15, 17]} fill={'#FFFCF7'} stroke={C.line} lineWidth={1.5}>
                <Rect x={-cardWidth / 2 + 6} width={8} height={60} radius={4} fill={color} />
                <Rect x={detachedBadgeX(cardWidth, 52)} width={52} height={34} radius={11} fill={color} shadowColor={`${color}44`} shadowBlur={10}>
                  <Txt fontFamily={MONO} fontSize={16} fontWeight={900} fill={'#FFFFFF'} text={String(idx + 1).padStart(2, '0')} />
                </Rect>
                <Txt x={22} width={textWidth} textWrap={true} textAlign={'left'} fontFamily={MONO} fontSize={layerFit.fontSize} lineHeight={layerFit.lineHeight} fontWeight={700} fill={C.primary} text={layer} />
              </Rect>
            </Layout>
          );
        })}
      </Layout>
      <Line points={[[100, 0], [310, 0]]} stroke={C.cyan} lineWidth={5} endArrow arrowSize={16} />
      <Layout ref={output} x={520} opacity={0} scale={0.7}>{paperCard(shot.visual.output ?? 'OUTPUT', 'assembled by harness', C.red, 430, 210)}</Layout>
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    ...refs.map((ref, cueIndex) => chain(waitFor(visualDelay(shot.id, cueIndex)), all(ref().opacity(1, 0.25), ref().scale(1, 0.32)))),
    chain(waitFor(visualDelay(shot.id, refs.length)), all(output().opacity(1, 0.38), output().scale(1, 0.48))),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* codeShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.purple);
  const lines = shot.visual.lines ?? [];
  const refs = lines.map(() => createRef<Rect>());
  const editor = createRef<Layout>();
  stage.body().add(
    <Layout ref={editor} opacity={0} scale={0.96}>
      <Rect width={1420} height={590} radius={24} fill={C.night} stroke={C.line} lineWidth={3} shadowColor={'#00000044'} shadowBlur={30}>
        <Rect y={-260} width={1420} height={70} radius={[24, 24, 0, 0]} fill={C.night2}>
          <Circle x={-655} width={14} height={14} fill={C.red} /><Circle x={-625} width={14} height={14} fill={C.yellow} /><Circle x={-595} width={14} height={14} fill={C.green} />
          <Txt x={0} width={1140} textAlign={'left'} fontFamily={MONO} fontSize={19} fill={C.mutedOnDark} text={shot.visual.filename ?? 'trace.json'} />
        </Rect>
        {lines.map((line, idx) => (
          <Rect ref={refs[idx]} y={-195 + idx * 72} width={1320} height={58} radius={8} fill={'#FFFFFF00'}>
            <Txt x={-610} width={54} textAlign={'right'} fontFamily={MONO} fontSize={19} fill={'#71697A'} text={String(idx + 1).padStart(2, '0')} />
            <Txt x={25} width={1160} height={46} textWrap={false} textAlign={'left'} fontFamily={MONO} fontSize={fitText(line, 1160, 46, {maxFontSize: 25, minFontSize: 15, maxLines: 1}).fontSize} fill={shot.visual.focus?.includes(idx + 1) ? '#F1CF72' : C.onDark} text={line} />
          </Rect>
        ))}
      </Rect>
    </Layout>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  const focusIndexes = (shot.visual.focus?.length ? shot.visual.focus : refs.map((_, idx) => idx + 1)).map(value => value - 1);
  const scanLines = focusIndexes.map((lineIndex, cueIndex) => chain(
    waitFor(visualDelay(shot.id, cueIndex)),
    refs[lineIndex]().fill('#D5A42D2E', 0.16),
    waitFor(0.24),
    refs[lineIndex]().fill('#D5A42D22', 0.16),
  ));
  yield* all(
    all(editor().opacity(1, 0.35), editor().scale(1, 0.45)),
    ...scanLines,
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* gatesShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.red);
  const gates = shot.visual.gates ?? [];
  const refs = gates.map(() => createRef<Layout>());
  const pulse = createRef<Circle>();
  const output = createRef<Layout>();
  const startX = -430;
  const step = gates.length > 1 ? 860 / (gates.length - 1) : 0;
  stage.body().add(
    <>
      <Line points={[[-680, 55], [680, 55]]} stroke={C.line} lineWidth={8} radius={18} />
      <Layout x={-680} y={55}>{paperCard(shot.visual.input ?? 'INPUT', 'untrusted request', C.yellow, 240, 120)}</Layout>
      {gates.map((gate, idx) => (
        <Layout ref={refs[idx]} x={startX + idx * step} y={55} opacity={0} scale={0.8}>
          <Rect x={6} y={8} width={190} height={190} radius={28} fill={'#DCCFBE66'} />
          <Rect width={190} height={190} radius={28} fill={'#FFFCF7'} stroke={C.line} lineWidth={1.5} shadowColor={'#6D594024'} shadowBlur={16}>
            <Rect y={-90} width={150} height={10} radius={5} fill={ACCENTS[idx % ACCENTS.length]} />
            <Txt width={154} textWrap={true} fontFamily={MONO} fontSize={fitText(gate, 154, 118, {maxFontSize: 20, minFontSize: 13, maxLines: 4}).fontSize} lineHeight={24} fontWeight={850} fill={C.primary} text={gate} />
            <Rect y={78} width={84} height={16} radius={4} fill={`${ACCENTS[idx % ACCENTS.length]}33`} rotation={3} />
          </Rect>
        </Layout>
      ))}
      <Layout ref={output} x={680} y={55} opacity={0}>{paperCard(shot.visual.output ?? 'OUTPUT', 'allowed action', C.green, 260, 120)}</Layout>
      <Circle ref={pulse} x={-680} y={55} width={28} height={28} fill={C.red} shadowColor={C.red} shadowBlur={25} />
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  const moves = refs.map((_, idx) => pulse().position.x(startX + idx * step, Math.max(0.42, active * 0.72 / Math.max(1, refs.length + 1)), linear));
  yield* all(
    chain(
      ...moves,
      pulse().position.x(520, 0.38, linear),
      all(pulse().scale(0, 0.18), pulse().opacity(0, 0.18)),
    ),
    ...refs.map((ref, cueIndex) => chain(waitFor(visualDelay(shot.id, cueIndex)), all(ref().opacity(1, 0.24), ref().scale(1, 0.3)))),
    chain(waitFor(visualDelay(shot.id, refs.length)), output().opacity(1, 0.3)),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* swimlaneShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.cyan);
  const lanes = shot.visual.lanes ?? ['MODEL', 'HARNESS', 'TOOLS'];
  const events = shot.visual.events ?? [];
  const refs = events.map(() => createRef<Layout>());
  let semanticCueIndex = 0;
  const cueIndexByEvent = events.map(event => typeof event !== 'string' && event.semanticType === 'prior-context' ? -1 : semanticCueIndex++);
  const laneX = lanes.map((_, idx) => -560 + idx * (1120 / Math.max(1, lanes.length - 1)));
  stage.body().add(
    <>
      {lanes.map((lane, idx) => (
        <Layout x={laneX[idx]}>
          <Rect y={-255} width={300} height={58} radius={29} fill={`${ACCENTS[idx % ACCENTS.length]}22`} stroke={ACCENTS[idx % ACCENTS.length]} lineWidth={2.5}>
            <Txt fontFamily={MONO} fontSize={23} fontWeight={900} fill={C.primary} text={lane} />
          </Rect>
          <Line points={[[0, -215], [0, 292]]} stroke={`${ACCENTS[idx % ACCENTS.length]}70`} lineWidth={3} lineDash={[10, 9]} />
        </Layout>
      ))}
      {events.map((event, idx) => {
        const from = typeof event === 'string' ? idx % lanes.length : lanes.indexOf(event.from);
        const to = typeof event === 'string' ? (idx + 1) % lanes.length : lanes.indexOf(event.to);
        if (from < 0 || to < 0 || from === to) throw new Error(`Invalid swimlane event in ${shot.id}: ${JSON.stringify(event)}`);
        const label = typeof event === 'string' ? event : event.label;
        const y = -170 + idx * (430 / Math.max(1, events.length - 1));
        return (
          <Layout ref={refs[idx]} opacity={0}>
            <Line points={[[laneX[from], y], [laneX[to], y]]} stroke={ACCENTS[idx % ACCENTS.length]} lineWidth={4} endArrow arrowSize={13} />
            <Rect x={(laneX[from] + laneX[to]) / 2} y={y - 25} width={360} height={46} radius={14} fill={C.panel} stroke={C.line} lineWidth={2}>
              <Txt width={328} height={34} textWrap={true} fontFamily={MONO} fontSize={fitText(label, 328, 34, {maxFontSize: 17, minFontSize: 12, maxLines: 2}).fontSize} lineHeight={19} fontWeight={700} fill={C.primary} text={label} />
            </Rect>
          </Layout>
        );
      })}
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    ...refs.map((ref, eventIndex) => cueIndexByEvent[eventIndex] < 0
      ? ref().opacity(1, 0.01)
      : chain(waitFor(visualDelay(shot.id, cueIndexByEvent[eventIndex])), ref().opacity(1, 0.28))),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* loopShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.cyan);
  const nodes = shot.visual.nodes ?? [];
  const positions: [number, number][] = [[-600, 80], [-300, -190], [120, -190], [510, 70], [90, 245]];
  const refs = nodes.map(() => createRef<Layout>());
  const path = createRef<Line>();
  const pulse = createRef<Circle>();
  const route = [...positions.slice(0, nodes.length), positions[0]];
  stage.body().add(
    <>
      <Line ref={path} points={route} stroke={C.cyan} lineWidth={5} radius={38} endArrow arrowSize={15} end={0} />
      {nodes.map((node, idx) => <Layout ref={refs[idx]} x={positions[idx][0]} y={positions[idx][1]} opacity={0} scale={0.8}>{paperCard(node, idx === 0 ? 'task objective' : 'state transition', ACCENTS[idx % ACCENTS.length], 260, 126)}</Layout>)}
      <Circle ref={pulse} position={positions[0]} width={30} height={30} fill={C.red} shadowColor={C.red} shadowBlur={24} opacity={0} />
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  const pathPoints = positions.slice(1, nodes.length);
  const moveDuration = Math.max(0.42, (active * 0.62) / Math.max(1, pathPoints.length * 2 + 1));
  const moves = [...pathPoints, positions[0], ...pathPoints, positions[0]].map(point => pulse().position(point, moveDuration, linear));
  yield* all(
    chain(path().end(1, 1.35, easeInOutCubic), pulse().opacity(1, 0.2), ...moves, pulse().position(positions[0], 0.5, linear)),
    ...refs.map((ref, cueIndex) => chain(waitFor(visualDelay(shot.id, cueIndex)), all(ref().opacity(1, 0.22), ref().scale(1, 0.3)))),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* timelineShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.purple);
  const events = shot.visual.events ?? [];
  const refs = events.map(() => createRef<Layout>());
  const scan = createRef<Line>();
  stage.body().add(
    <>
      <Rect width={1460} height={590} radius={25} fill={C.night} stroke={C.line} lineWidth={3}>
        <Rect y={-260} width={1460} height={70} radius={[25, 25, 0, 0]} fill={C.night2}>
          <Txt width={1320} textAlign={'left'} fontFamily={MONO} fontSize={19} fill={C.mutedOnDark} text={`agent-run / ${shot.id}`} />
        </Rect>
        {events.map((event, idx) => (
          <Layout ref={refs[idx]} y={-190 + idx * (405 / Math.max(1, events.length - 1))} opacity={0} x={30}>
            <Circle x={-620} width={18} height={18} fill={ACCENTS[idx % ACCENTS.length]} />
            <Txt x={-560} width={72} textAlign={'left'} fontFamily={MONO} fontSize={18} fill={C.mutedOnDark} text={String(idx + 1).padStart(2, '0')} />
            <Txt x={30} width={1080} height={46} textWrap={false} textAlign={'left'} fontFamily={MONO} fontSize={fitText(typeof event === 'string' ? event : event.label, 1080, 46, {maxFontSize: 22, minFontSize: 14, maxLines: 1}).fontSize} fill={C.onDark} text={typeof event === 'string' ? event : event.label} />
            <Rect x={600} width={130} height={38} radius={19} fill={`${ACCENTS[idx % ACCENTS.length]}2A`} stroke={ACCENTS[idx % ACCENTS.length]} lineWidth={1.5}>
              <Txt fontFamily={MONO} fontSize={15} fontWeight={800} fill={ACCENTS[idx % ACCENTS.length]} text={idx === events.length - 1 ? 'DONE' : 'EVENT'} />
            </Rect>
          </Layout>
        ))}
        <Line ref={scan} points={[[-680, 0], [680, 0]]} stroke={'#73C5C544'} lineWidth={3} y={-220} />
      </Rect>
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    ...refs.map((ref, cueIndex) => chain(waitFor(visualDelay(shot.id, cueIndex)), all(ref().opacity(1, 0.22), ref().position.x(0, 0.3)))),
    scan().position.y(230, active, linear),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* barsShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.yellow);
  const bars = shot.visual.bars ?? [];
  const max = Math.max(...bars.map(item => item.value), 1);
  const groups = bars.map(() => createRef<Layout>());
  const refs = bars.map(() => createRef<Rect>());
  const values = bars.map(() => createRef<Txt>());
  const labels = bars.map(() => createRef<Txt>());
  const available = 1220;
  const gap = available / Math.max(1, bars.length);
  stage.body().add(
    <>
      <Line points={[[-680, 250], [680, 250]]} stroke={C.primary} lineWidth={4} />
      {bars.map((bar, idx) => {
        const x = -610 + idx * gap;
        const height = 390 * (bar.value / max);
        return (
          <Layout ref={groups[idx]} x={x}>
            <Rect ref={refs[idx]} y={250} width={Math.min(190, gap - 30)} height={0} offset={[0, 1]} radius={[14, 14, 0, 0]} fill={ACCENTS[idx % ACCENTS.length]} stroke={C.primary} lineWidth={3} />
            <Txt ref={labels[idx]} y={282} width={Math.min(190, gap - 30)} height={48} textWrap={true} fontFamily={FONT} fontSize={fitText(bar.label, Math.min(190, gap - 30), 48, {maxFontSize: 20, minFontSize: 13, maxLines: 2}).fontSize} lineHeight={23} fontWeight={750} fill={C.primary} text={bar.label} />
            <Txt ref={values[idx]} y={210 - height} width={180} fontFamily={MONO} fontSize={23} fontWeight={900} fill={ACCENTS[idx % ACCENTS.length]} text={String(bar.value)} />
          </Layout>
        );
      })}
      {shot.visual.note ? <Rect x={350} y={-255} width={720} height={68} radius={18} fill={'#FFF4C7'} stroke={C.yellow} lineWidth={2} clip><Txt width={660} height={50} textWrap={true} fontFamily={FONT} fontSize={fitText(shot.visual.note, 660, 50, {maxFontSize: 21, minFontSize: 14, maxLines: 2}).fontSize} lineHeight={25} fill={C.primary} text={shot.visual.note} /></Rect> : null}
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  const after = shot.visual.after;
  const grow = all(...refs.map((ref, idx) => chain(
    waitFor(visualDelay(shot.id, idx)),
    ref().height(390 * (bars[idx].value / max), 0.5, easeInOutCubic),
  )));
  const update = after?.length
    ? chain(
        waitFor(visualDelay(shot.id, refs.length)),
        all(...refs.map((ref, idx) => {
          const next = after[idx];
          if (!next) return all(ref().height(0, 0.5, easeInOutCubic), groups[idx]().opacity(0, 0.42));
          const nextHeight = 390 * (next.value / Math.max(max, ...after.map(item => item.value)));
          const afterGap = available / after.length;
          const afterX = -afterGap * (after.length - 1) / 2 + idx * afterGap;
          return all(
            groups[idx]().position.x(afterX, 0.62, easeInOutCubic),
            ref().height(nextHeight, 0.62, easeInOutCubic),
            values[idx]().position.y(210 - nextHeight, 0.62, easeInOutCubic),
            values[idx]().text(String(next.value), 0.36),
            labels[idx]().text(next.label, 0.36),
          );
        })),
      )
    : waitFor(0);
  yield* all(grow, update, captions(stage, shot.id, active), ambientScan(stage, active), waitFor(active));
  yield* exit(stage);
}

function* curveShot(view: View2D, shot: CompleteShot, duration: number, index: number) {
  const stage = makeCompleteStage(view, index, shot, C.cyan);
  const series = shot.visual.series ?? [];
  const labels = shot.visual.x ?? [];
  const max = Math.max(...series.flatMap(item => item.values), 1);
  const paths = series.map(() => createRef<Line>());
  const points = (values: number[]) => values.map((value, idx) => [-560 + idx * (1120 / Math.max(1, values.length - 1)), 220 - (value / max) * 420] as [number, number]);
  stage.body().add(
    <>
      <Rect width={1400} height={590} radius={24} fill={C.panel} stroke={C.line} lineWidth={3}>
        <Line points={[[-610, 240], [610, 240]]} stroke={C.primary} lineWidth={3} />
        <Line points={[[-610, 240], [-610, -240]]} stroke={C.primary} lineWidth={3} />
        {series.map((item, idx) => <Line ref={paths[idx]} points={points(item.values)} stroke={ACCENTS[idx % ACCENTS.length]} lineWidth={7} radius={18} end={0} />)}
        {labels.map((label, idx) => <Txt x={-560 + idx * (1120 / Math.max(1, labels.length - 1))} y={276} width={200} height={42} textWrap={true} fontFamily={MONO} fontSize={fitText(label, 200, 42, {maxFontSize: 17, minFontSize: 12, maxLines: 2}).fontSize} lineHeight={20} fill={C.soft} text={label} />)}
        {series.map((item, idx) => <Layout x={360} y={-235 + idx * 48}><Line points={[[-190, 0], [-130, 0]]} stroke={ACCENTS[idx % ACCENTS.length]} lineWidth={7} /><Txt x={50} width={300} height={38} textWrap={true} textAlign={'left'} fontFamily={MONO} fontSize={fitText(item.label, 300, 38, {maxFontSize: 18, minFontSize: 13, maxLines: 2}).fontSize} lineHeight={21} fontWeight={800} fill={C.primary} text={item.label} /></Layout>)}
      </Rect>
      {shot.visual.note ? <Rect y={-285} width={760} height={52} radius={18} fill={'#FFF4C7'} clip><Txt width={710} height={38} textWrap={true} fontFamily={FONT} fontSize={fitText(shot.visual.note, 710, 38, {maxFontSize: 18, minFontSize: 13, maxLines: 2}).fontSize} lineHeight={21} fill={C.primary} text={shot.visual.note} /></Rect> : null}
    </>,
  );
  yield* enter(stage);
  const active = duration - 0.74;
  yield* all(
    ...paths.map((ref, cueIndex) => chain(waitFor(visualDelay(shot.id, cueIndex)), ref().end(1, 0.9, easeInOutCubic))),
    captions(stage, shot.id, active),
    ambientScan(stage, active),
    waitFor(active),
  );
  yield* exit(stage);
}

function* runShot(view: View2D, shot: CompleteShot, index: number) {
  const duration = durations[shot.id];
  switch (shot.visual.kind) {
    case 'character': return yield* characterShot(view, shot, duration, index);
    case 'compare': return yield* compareShot(view, shot, duration, index);
    case 'evidence': return yield* evidenceShot(view, shot, duration, index);
    case 'topology': return yield* topologyShot(view, shot, duration, index);
    case 'stack': return yield* stackShot(view, shot, duration, index);
    case 'code': return yield* codeShot(view, shot, duration, index);
    case 'gates': return yield* gatesShot(view, shot, duration, index);
    case 'swimlane': return yield* swimlaneShot(view, shot, duration, index);
    case 'loop': return yield* loopShot(view, shot, duration, index);
    case 'timeline': return yield* timelineShot(view, shot, duration, index);
    case 'bars': return yield* barsShot(view, shot, duration, index);
    case 'curve': return yield* curveShot(view, shot, duration, index);
    default: return yield* topologyShot(view, shot, duration, index);
  }
}

function* runSequence(view: View2D) {
  for (let index = 0; index < story.shots.length; index += 1) {
    yield* runShot(view, story.shots[index], index);
  }
}

const scene = makeScene2D('ai-agent-harness-complete', function* (view) {
  const grid = createRef<Grid>();
  const scan = createRef<Line>();
  const chapterPulse = createRef<Circle>();
  view.fill(C.bg);
  view.add(
    <>
      <Grid ref={grid} size={[2100, 1260]} spacing={64} stroke={'#D8CCBD'} lineWidth={1} opacity={0.68} />
      <Circle x={-820} y={-470} width={520} height={520} fill={'#D8556210'} shadowColor={'#D8556222'} shadowBlur={100} />
      <Circle x={860} y={420} width={620} height={620} fill={'#765D910A'} shadowColor={'#765D9120'} shadowBlur={120} />
      <Line ref={scan} points={[[-960, 0], [960, 0]]} stroke={'#2C8E9222'} lineWidth={2} y={-540} />
      <Layout y={-504}>
        <Line points={[[-360, 0], [360, 0]]} stroke={'#B8AA994F'} lineWidth={2} />
        {story.chapters.map((_, index) => (
          <Circle x={-360 + index * (720 / Math.max(1, story.chapters.length - 1))} width={7} height={7} fill={'#B8AA99'} />
        ))}
        <Circle ref={chapterPulse} x={-360} width={13} height={13} fill={C.red} shadowColor={C.red} shadowBlur={20} />
      </Layout>
      <Layout position={[735, -448]} layout direction={'row'} gap={12} alignItems={'center'}>
        <Circle width={15} height={15} fill={C.red} shadowColor={C.red} shadowBlur={18} />
        <Txt fontFamily={FONT} fontSize={22} fontWeight={750} letterSpacing={2} fill={C.primary} text={'小行星 AI 观测站'} />
      </Layout>
      <Audio src={'/complete/complete-audio.mp3'} play={true} />
    </>,
  );
  yield* all(
    runSequence(view),
    tween(timeline.duration, value => {
      scan().y(-540 + 1080 * value);
      grid().rotation(linear(value, 0, 1));
      chapterPulse().x(-360 + 720 * value);
      chapterPulse().scale(0.88 + Math.sin(value * Math.PI * story.shots.length * 2) * 0.15);
    }),
  );
});

export default makeProject({
  scenes: [scene],
  settings: {shared: {size: {x: 1920, y: 1080}}, rendering: {fps: 30}, preview: {fps: 30}},
});
