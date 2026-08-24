import {Audio, Circle, Grid, Img, Layout, Line, Rect, Txt, Video, View2D, makeScene2D} from '@revideo/2d';
import {Reference, all, createRef, easeInOutCubic, makeProject, tween} from '@revideo/core';
import storyDocument from '../../../examples/qwen-ui-agent-hosted/storyboard/story.json';
import timelineDocument from '../../../examples/qwen-ui-agent-hosted/audio/video.timeline.json';
import captionDocument from '../../../examples/qwen-ui-agent-hosted/audio/captions.timeline.json';
import {ASTEROID_WARM_THEME as C} from './theme';
import {CINEMATIC_FONT as FONT, CINEMATIC_MONO as MONO} from './cinematic-sketch';
import {fitText} from './layout-contracts';

type Bar = {label: string; value: number};
type HostedVisual = {
  kind: string;
  accent?: string;
  notification?: string;
  demoStart?: number;
  demoEnd?: number;
  callouts?: string[];
  channels?: string[];
  nodes?: string[];
  emphasis?: number;
  center?: string;
  steps?: number;
  environments?: number;
  labels?: string[];
  asset?: string;
  sourceLabel?: string;
  bars?: Bar[];
  note?: string;
  result?: string;
};
type HostedShot = {
  id: string;
  headline: string;
  dialogue: string;
  hostNarrative: {role: string; mode: string; hostOnScreen: boolean; asset?: string; action?: string};
  visual: HostedVisual;
};
type CaptionCue = {shotId: string; localStart: number; localEnd: number; text: string};

const story = storyDocument as unknown as {shots: HostedShot[]; chapters: Array<{id: string; title: string; shotIds: string[]}>};
const timeline = timelineDocument as unknown as {duration: number; shots: Array<{id: string; duration: number}>};
const captions = captionDocument as unknown as {cues: CaptionCue[]};
const durations = Object.fromEntries(timeline.shots.map(shot => [shot.id, shot.duration]));
const captionsByShot = captions.cues.reduce<Record<string, CaptionCue[]>>((result, cue) => {
  (result[cue.shotId] ??= []).push(cue);
  return result;
}, {});
const ACCENTS = [C.red, C.cyan, C.purple, C.yellow, C.green] as const;

type Stage = {root: Reference<Layout>; body: Reference<Layout>; caption: Reference<Txt>; index: number; accent: string};
type Runtime = {update: (value: number) => void};

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function phase(value: number, start: number, end: number): number {
  return easeInOutCubic(clamp01((value - start) / Math.max(0.001, end - start)));
}

function chapterFor(shotId: string): string {
  return story.chapters.find(chapter => chapter.shotIds.includes(shotId))?.title ?? '观察记录';
}

function makeStage(view: View2D, shot: HostedShot, index: number): Stage {
  const root = createRef<Layout>();
  const body = createRef<Layout>();
  const caption = createRef<Txt>();
  const accent = ACCENTS[index % ACCENTS.length];
  view.add(
    <Layout ref={root} size={[1920, 1080]} opacity={0} scale={0.985}>
      <Layout position={[-700, -436]} layout direction={'row'} gap={14} alignItems={'center'}>
        <Rect width={42} height={7} radius={4} fill={accent} />
        <Txt fontFamily={MONO} fontSize={19} fontWeight={850} letterSpacing={2.2} fill={accent} text={`FIELD NOTE ${String(index + 1).padStart(2, '0')}`} />
        <Txt fontFamily={FONT} fontSize={19} fontWeight={650} fill={C.soft} text={`· ${chapterFor(shot.id)}`} />
      </Layout>
      <Txt position={[0, -356]} width={1520} height={82} textAlign={'left'} fontFamily={FONT} fontSize={fitText(shot.headline, 1520, 82, {maxFontSize: 54, minFontSize: 39, maxLines: 2}).fontSize} lineHeight={64} fontWeight={850} fill={C.primary} text={shot.headline} />
      <Rect position={[-610, -302]} width={300} height={13} radius={7} fill={`${accent}25`} rotation={-0.8} />
      <Layout ref={body} position={[0, 24]} size={[1640, 620]} />
      <Layout position={[0, 444]}>
        <Rect y={7} width={1642} height={98} radius={25} fill={'#DCCDBB'} opacity={0.78} />
        <Rect width={1640} height={100} radius={23} fill={'#FFF9F0F5'} stroke={C.line} lineWidth={2}>
          <Txt ref={caption} width={1500} height={72} textWrap fontFamily={FONT} fontSize={31} lineHeight={42} fontWeight={680} textAlign={'center'} fill={C.primary} text={''} />
        </Rect>
        <Rect x={-714} y={-50} width={112} height={21} radius={4} fill={`${C.tape}B5`} rotation={-2.3} />
        <Rect x={714} y={-50} width={112} height={21} radius={4} fill={`${accent}40`} rotation={2.3} />
      </Layout>
    </Layout>,
  );
  return {root, body, caption, index, accent};
}

function addHostImage(stage: Stage, filename: string, label: string): Runtime {
  const image = createRef<Img>();
  const notice = createRef<Rect>();
  const line = createRef<Line>();
  stage.body().add(
    <>
      <Rect x={-220} width={1160} height={620} radius={32} clip stroke={`${stage.accent}88`} lineWidth={3} fill={C.night}>
        <Img ref={image} src={`/qwen-ui-agent/characters/${filename}`} width={1110} height={620} opacity={0.92} />
        <Rect x={350} width={460} height={620} fill={'#201C25B8'} />
      </Rect>
      <Line ref={line} points={[[300, -212], [420, -212], [500, -130]]} stroke={stage.accent} lineWidth={4} endArrow arrowSize={16} end={0} />
      <Rect ref={notice} x={510} y={-76} width={520} height={238} radius={28} fill={'#FFF9F0F5'} stroke={stage.accent} lineWidth={3} opacity={0} shadowColor={'#2B253033'} shadowBlur={30}>
        <Layout y={-72} layout direction={'row'} gap={13} alignItems={'center'}>
          <Circle width={14} height={14} fill={stage.accent} shadowColor={stage.accent} shadowBlur={18} />
          <Txt fontFamily={MONO} fontSize={18} fontWeight={850} letterSpacing={1.8} fill={stage.accent} text={'REAL-WORLD SIGNAL'} />
        </Layout>
        <Txt y={-6} width={440} textWrap fontFamily={FONT} fontSize={31} lineHeight={43} fontWeight={800} fill={C.primary} text={label} />
        <Rect y={79} width={438} height={42} radius={21} fill={`${stage.accent}16`}>
          <Txt fontFamily={FONT} fontSize={19} fontWeight={750} fill={C.primary} text={'先理解影响 · 再准备行动'} />
        </Rect>
      </Rect>
    </>,
  );
  return {update: value => {
    image().scale(1 + value * 0.025);
    notice().opacity(phase(value, 0.12, 0.3));
    notice().position.x(550 - 40 * phase(value, 0.12, 0.3));
    line().end(phase(value, 0.28, 0.46));
  }};
}

function addPhone(stage: Stage, shot: HostedShot, channels = false): Runtime {
  const phone = createRef<Layout>();
  const callouts = (channels ? shot.visual.channels : shot.visual.callouts) ?? [];
  const tags = callouts.map(() => createRef<Rect>());
  const phoneX = channels ? 440 : -500;
  stage.body().add(
    <>
      <Layout ref={phone} x={phoneX} opacity={0} scale={0.94}>
        <Rect width={382} height={684} radius={52} fill={'#17141D'} shadowColor={'#17141D55'} shadowBlur={38} />
        <Rect width={354} height={630} radius={35} clip fill={'#050408'}>
          <Video src={'/qwen-ui-agent/proactive-flight-recovery-hd.mp4'} width={354} height={630} time={shot.visual.demoStart ?? 0} play volume={0} decoder={'web'} />
        </Rect>
        <Rect y={-320} width={82} height={8} radius={4} fill={'#4B4552'} />
      </Layout>
      <Layout x={channels ? -340 : 310} y={-26} layout direction={'column'} gap={22}>
        {callouts.map((label, index) => (
          <Rect ref={tags[index]} width={channels ? 760 : 660} height={92} radius={24} fill={index === 0 ? `${stage.accent}18` : '#FFF9F0E8'} stroke={index === 0 ? stage.accent : C.line} lineWidth={2} opacity={0}>
            <Layout x={-((channels ? 760 : 660) / 2) + 54} layout direction={'row'} gap={18} alignItems={'center'}>
              <Circle width={34} height={34} fill={ACCENTS[index % ACCENTS.length]}>
                <Txt fontFamily={MONO} fontSize={15} fontWeight={900} fill={C.onDark} text={String(index + 1).padStart(2, '0')} />
              </Circle>
              <Txt width={channels ? 620 : 520} textAlign={'left'} fontFamily={channels ? MONO : FONT} fontSize={channels ? 28 : 30} fontWeight={820} fill={C.primary} text={label} />
            </Layout>
          </Rect>
        ))}
        {channels ? <Txt y={230} width={760} textAlign={'left'} fontFamily={FONT} fontSize={22} lineHeight={32} fill={C.soft} text={'界面操作、结构化查询与文件处理\n在同一条任务轨迹里交替出现'} /> : null}
      </Layout>
    </>,
  );
  return {update: value => {
    phone().opacity(phase(value, 0, 0.12));
    phone().scale(0.94 + 0.06 * phase(value, 0, 0.16));
    phone().position.y(Math.sin(value * Math.PI * 2) * 5);
    tags.forEach((tag, index) => {
      const start = 0.18 + index * 0.15;
      tag().opacity(phase(value, start, start + 0.1));
      tag().position.x(-28 + 28 * phase(value, start, start + 0.12));
    });
  }};
}

function addStageActor(stage: Stage, filename: string, side: 'left' | 'right'): Reference<Layout> {
  const actor = createRef<Layout>();
  const x = side === 'left' ? -630 : 630;
  const size = filename.includes('presenting') ? {width: 500, height: 375} : filename.includes('thinking') ? {width: 470, height: 395} : {width: 470, height: 396};
  stage.body().add(
    <Layout ref={actor} x={x} y={70} opacity={0} scale={0.92}>
      <Circle y={22} width={410} height={410} fill={`${stage.accent}0D`} shadowColor={`${stage.accent}20`} shadowBlur={42} />
      <Img src={`/qwen-ui-agent/characters/${filename}`} width={size.width} height={size.height} />
      <Rect y={211} width={300} height={40} radius={20} fill={C.night} stroke={`${stage.accent}88`} lineWidth={2}>
        <Txt fontFamily={MONO} fontSize={17} fontWeight={850} letterSpacing={1.3} fill={C.onDark} text={'XIAOLAN · FIELD HOST'} />
      </Rect>
    </Layout>,
  );
  return actor;
}

function addFlow(stage: Stage, shot: HostedShot): Runtime {
  const actor = addStageActor(stage, shot.hostNarrative.asset ?? 'xiaolan-pointing.png', 'left');
  const nodes = shot.visual.nodes ?? [];
  const boxes = nodes.map(() => createRef<Rect>());
  const paths = nodes.slice(1).map(() => createRef<Line>());
  const startX = -260;
  const gap = 225;
  stage.body().add(
    <>
      {paths.map((path, index) => <Line ref={path} points={[[startX + index * gap + 92, 20], [startX + (index + 1) * gap - 92, 20]]} stroke={index === 2 ? C.red : C.cyan} lineWidth={5} endArrow arrowSize={15} end={0} />)}
      {nodes.map((node, index) => (
        <Rect ref={boxes[index]} x={startX + index * gap} y={20} width={184} height={150} radius={26} fill={index === shot.visual.emphasis ? '#FFF0F1' : '#FFF9F0E8'} stroke={index === shot.visual.emphasis ? C.red : C.line} lineWidth={index === shot.visual.emphasis ? 4 : 2} opacity={0}>
          <Txt y={-39} fontFamily={MONO} fontSize={16} fontWeight={900} fill={ACCENTS[index % ACCENTS.length]} text={String(index + 1).padStart(2, '0')} />
          <Txt y={14} width={150} textWrap fontFamily={FONT} fontSize={27} lineHeight={36} fontWeight={820} fill={C.primary} text={node} />
          {index === shot.visual.emphasis ? <Txt y={56} fontFamily={MONO} fontSize={14} fontWeight={850} fill={C.red} text={'HUMAN GATE'} /> : null}
        </Rect>
      ))}
    </>,
  );
  return {update: value => {
    actor().opacity(phase(value, 0, 0.12));
    actor().scale(0.92 + 0.08 * phase(value, 0, 0.14));
    boxes.forEach((box, index) => {
      const start = 0.08 + index * 0.12;
      box().opacity(phase(value, start, start + 0.1));
      box().scale(0.86 + 0.14 * phase(value, start, start + 0.12));
      if (index > 0) paths[index - 1]().end(phase(value, start - 0.08, start + 0.02));
    });
  }};
}

function addPlatforms(stage: Stage, shot: HostedShot): Runtime {
  const actor = addStageActor(stage, shot.hostNarrative.asset ?? 'xiaolan-presenting.png', 'right');
  const nodes = shot.visual.nodes ?? [];
  const refs = nodes.map(() => createRef<Rect>());
  const links = nodes.map(() => createRef<Line>());
  const positions: Array<[number, number]> = [[-600, -155], [-250, -155], [-600, 180], [-250, 180]];
  const center: [number, number] = [-425, 12];
  stage.body().add(
    <>
      {positions.map((position, index) => <Line ref={links[index]} points={[center, position]} stroke={`${ACCENTS[index]}AA`} lineWidth={4} endArrow arrowSize={14} end={0} />)}
      <Circle position={center} width={210} height={210} fill={C.night} stroke={C.red} lineWidth={4} shadowColor={'#2B253055'} shadowBlur={34}>
        <Txt width={160} textWrap fontFamily={MONO} fontSize={24} lineHeight={32} fontWeight={900} fill={C.onDark} text={shot.visual.center ?? 'TASK'} />
      </Circle>
      {nodes.map((node, index) => (
        <Rect ref={refs[index]} position={positions[index]} width={260} height={120} radius={26} fill={'#FFF9F0'} stroke={ACCENTS[index]} lineWidth={3} opacity={0}>
          <Txt fontFamily={MONO} fontSize={22} fontWeight={900} fill={C.primary} text={node} />
        </Rect>
      ))}
    </>,
  );
  return {update: value => {
    actor().opacity(phase(value, 0.12, 0.25));
    actor().scale(0.92 + 0.08 * phase(value, 0.12, 0.25));
    refs.forEach((ref, index) => {
      const start = 0.08 + index * 0.12;
      links[index]().end(phase(value, start, start + 0.12));
      ref().opacity(phase(value, start + 0.05, start + 0.16));
      ref().scale(0.9 + 0.1 * phase(value, start + 0.05, start + 0.16));
    });
  }};
}

function addSteps(stage: Stage, shot: HostedShot): Runtime {
  const blocks = Array.from({length: 10}, () => createRef<Rect>());
  const labels = (shot.visual.labels ?? []).map(() => createRef<Rect>());
  const env = createRef<Txt>();
  stage.body().add(
    <>
      <Layout x={-230} y={30}>
        {blocks.map((block, index) => (
          <Rect ref={block} x={-570 + index * 120} y={230 - index * 46} width={102} height={40 + index * 10} radius={[10, 10, 2, 2]} fill={index < 7 ? C.cyan : C.red} opacity={0.14}>
            {index === 9 ? <Txt y={-50} fontFamily={MONO} fontSize={29} fontWeight={950} fill={C.red} text={'100+ STEPS'} /> : null}
          </Rect>
        ))}
      </Layout>
      <Rect x={555} width={420} height={340} radius={34} fill={C.night} stroke={`${C.purple}AA`} lineWidth={3}>
        <Txt y={-100} fontFamily={MONO} fontSize={18} fontWeight={850} letterSpacing={2} fill={C.tape} text={'PARALLEL ENVIRONMENTS'} />
        <Txt ref={env} y={-12} fontFamily={MONO} fontSize={78} fontWeight={950} fill={C.onDark} text={'0'} />
        <Txt y={86} width={330} textWrap fontFamily={FONT} fontSize={23} lineHeight={33} fontWeight={650} fill={C.mutedOnDark} text={'让观察、纠错与继续\n在长轨迹里被反复训练'} />
      </Rect>
      <Layout x={55} y={266} layout direction={'row'} gap={16}>
        {(shot.visual.labels ?? []).map((label, index) => (
          <Rect ref={labels[index]} width={180} height={58} radius={29} fill={`${ACCENTS[index]}18`} stroke={ACCENTS[index]} lineWidth={2} opacity={0}>
            <Txt fontFamily={FONT} fontSize={23} fontWeight={800} fill={C.primary} text={label} />
          </Rect>
        ))}
      </Layout>
    </>,
  );
  return {update: value => {
    blocks.forEach((block, index) => {
      const p = phase(value, 0.04 + index * 0.045, 0.16 + index * 0.045);
      block().opacity(0.14 + p * 0.86);
      block().scale.y(0.25 + p * 0.75);
    });
    env().text(Math.round(10000 * phase(value, 0.22, 0.72)).toLocaleString('en-US'));
    labels.forEach((label, index) => label().opacity(phase(value, 0.5 + index * 0.07, 0.6 + index * 0.07)));
  }};
}

function addEvidence(stage: Stage, shot: HostedShot): Runtime {
  const actor = addStageActor(stage, shot.hostNarrative.asset ?? 'xiaolan-thinking.png', 'right');
  const board = createRef<Rect>();
  const marker = createRef<Line>();
  stage.body().add(
    <>
      <Rect ref={board} x={-300} width={1120} height={610} radius={28} clip fill={'#FFFFFF'} stroke={C.line} lineWidth={3} opacity={0} shadowColor={'#2B253033'} shadowBlur={26}>
        <Img src={`/qwen-ui-agent/evidence/${shot.visual.asset}`} width={1120} height={1584} y={388} />
      </Rect>
      <Line ref={marker} points={[[-755, 100], [-230, 100], [50, 140]]} stroke={C.tape} lineWidth={20} opacity={0.52} end={0} />
      <Rect x={-270} y={270} width={900} height={46} radius={23} fill={C.night}>
        <Txt fontFamily={MONO} fontSize={18} fontWeight={850} letterSpacing={1.4} fill={C.onDark} text={shot.visual.sourceLabel ?? 'PRIMARY SOURCE'} />
      </Rect>
    </>,
  );
  return {update: value => {
    board().opacity(phase(value, 0, 0.12));
    board().scale(0.97 + 0.03 * phase(value, 0, 0.15));
    marker().end(phase(value, 0.32, 0.62));
    actor().opacity(phase(value, 0.18, 0.34));
    actor().scale(0.92 + 0.08 * phase(value, 0.18, 0.34));
  }};
}

function addBars(stage: Stage, shot: HostedShot): Runtime {
  const bars = shot.visual.bars ?? [];
  const columns = bars.map(() => createRef<Rect>());
  const values = bars.map(() => createRef<Txt>());
  const scan = createRef<Line>();
  stage.body().add(
    <>
      <Line points={[[-700, 245], [720, 245]]} stroke={C.line} lineWidth={3} />
      <Line ref={scan} x={-700} points={[[0, -210], [0, 245]]} stroke={`${C.cyan}45`} lineWidth={3} lineDash={[10, 12]} />
      {bars.map((bar, index) => {
        const x = -525 + index * 350;
        return <Layout x={x} y={30}>
          <Rect ref={columns[index]} y={210} width={190} height={1} radius={[18, 18, 2, 2]} fill={ACCENTS[index]} />
          <Txt ref={values[index]} y={-220} fontFamily={MONO} fontSize={45} fontWeight={950} fill={ACCENTS[index]} text={'0.0'} />
          <Txt y={260} width={280} textWrap textAlign={'center'} fontFamily={MONO} fontSize={18} lineHeight={25} fontWeight={850} fill={C.primary} text={bar.label} />
        </Layout>;
      })}
      <Rect y={-285} width={1150} height={50} radius={25} fill={'#FFF4C7'} stroke={`${C.yellow}88`} lineWidth={2}>
        <Txt fontFamily={FONT} fontSize={21} fontWeight={750} fill={C.primary} text={shot.visual.note ?? ''} />
      </Rect>
    </>,
  );
  return {update: value => {
    scan().position.x(-700 + 1420 * value);
    scan().opacity(0.35 + Math.sin(value * Math.PI * 8) * 0.12);
    bars.forEach((bar, index) => {
      const p = phase(value, 0.08 + index * 0.1, 0.38 + index * 0.1);
      const height = 4.4 * bar.value;
      columns[index]().height(Math.max(1, height * p));
      columns[index]().position.y(245 - height * p / 2);
      values[index]().text((bar.value * p).toFixed(1));
      values[index]().position.y(210 - height * p - 48);
    });
  }};
}

function addSynthesis(stage: Stage, shot: HostedShot): Runtime {
  const image = createRef<Img>();
  const phone = createRef<Layout>();
  const result = createRef<Rect>();
  stage.body().add(
    <>
      <Rect x={-210} width={1180} height={620} radius={32} clip stroke={`${stage.accent}88`} lineWidth={3} fill={C.night}>
        <Img ref={image} src={`/qwen-ui-agent/characters/${shot.hostNarrative.asset ?? 'char_outro.jpg'}`} width={1110} height={620} opacity={0.92} />
        <Rect x={390} width={420} height={620} fill={'#201C25D0'} />
      </Rect>
      <Layout ref={phone} x={435} y={-38} opacity={0} scale={0.9}>
        <Rect width={230} height={408} radius={36} fill={'#17141D'} shadowColor={'#17141D66'} shadowBlur={28} />
        <Rect width={208} height={370} radius={25} clip fill={'#050408'}>
          <Video src={'/qwen-ui-agent/proactive-flight-recovery-hd.mp4'} width={208} height={370} time={shot.visual.demoStart ?? 50} play volume={0} decoder={'web'} />
        </Rect>
      </Layout>
      <Rect ref={result} x={435} y={220} width={690} height={72} radius={36} fill={C.night} stroke={C.tape} lineWidth={3} opacity={0}>
        <Txt fontFamily={MONO} fontSize={22} fontWeight={900} letterSpacing={1.2} fill={C.onDark} text={shot.visual.result ?? ''} />
      </Rect>
    </>,
  );
  return {update: value => {
    image().scale(1 + value * 0.025);
    phone().opacity(phase(value, 0.14, 0.3));
    phone().scale(0.9 + 0.1 * phase(value, 0.14, 0.3));
    result().opacity(phase(value, 0.48, 0.66));
    result().scale(0.9 + 0.1 * phase(value, 0.48, 0.66));
  }};
}

function buildVisual(stage: Stage, shot: HostedShot): Runtime {
  switch (shot.visual.kind) {
    case 'host': return addHostImage(stage, shot.hostNarrative.asset ?? 'char_surprised.jpg', shot.visual.notification ?? 'REAL-WORLD SIGNAL');
    case 'demo': return addPhone(stage, shot, false);
    case 'demo-channels': return addPhone(stage, shot, true);
    case 'flow': return addFlow(stage, shot);
    case 'platforms': return addPlatforms(stage, shot);
    case 'steps': return addSteps(stage, shot);
    case 'evidence': return addEvidence(stage, shot);
    case 'bars': return addBars(stage, shot);
    case 'host-result': return addSynthesis(stage, shot);
    default: return {update: () => undefined};
  }
}

function* runShot(view: View2D, shot: HostedShot, index: number) {
  const duration = durations[shot.id];
  if (!duration) throw new Error(`Missing duration for ${shot.id}`);
  const stage = makeStage(view, shot, index);
  const runtime = buildVisual(stage, shot);
  const cues = captionsByShot[shot.id] ?? [];
  yield* tween(0.42, value => {
    stage.root().opacity(easeInOutCubic(value));
    stage.root().scale(0.985 + 0.015 * easeInOutCubic(value));
  });
  const active = Math.max(0.2, duration - 0.78);
  yield* tween(active, value => {
    runtime.update(value);
    stage.body().position.y(24 + Math.sin(value * Math.PI * 2) * 3);
    const localTime = 0.42 + value * active;
    const cue = cues.find(item => localTime >= item.localStart && localTime < item.localEnd) ?? cues.at(-1);
    if (cue) stage.caption().text(cue.text);
  });
  yield* tween(0.36, value => {
    stage.root().opacity(1 - easeInOutCubic(value));
    stage.root().scale(1 - 0.012 * easeInOutCubic(value));
  });
  stage.root().remove();
}

function* runSequence(view: View2D) {
  for (let index = 0; index < story.shots.length; index += 1) yield* runShot(view, story.shots[index], index);
}

const scene = makeScene2D('qwen-ui-agent-hosted', function* (view) {
  const grid = createRef<Grid>();
  const scan = createRef<Line>();
  const progress = createRef<Line>();
  view.fill(C.bg);
  view.add(
    <>
      <Grid ref={grid} size={[2100, 1260]} spacing={64} stroke={'#D8CCBD'} lineWidth={1} opacity={0.62} />
      <Circle x={-850} y={-460} width={540} height={540} fill={'#D8556210'} shadowColor={'#D8556222'} shadowBlur={110} />
      <Circle x={840} y={430} width={620} height={620} fill={'#765D910A'} shadowColor={'#765D9120'} shadowBlur={120} />
      <Line ref={scan} points={[[-960, 0], [960, 0]]} stroke={'#2C8E9224'} lineWidth={2} y={-540} />
      <Line points={[[-820, -492], [820, -492]]} stroke={'#B8AA9955'} lineWidth={3} />
      <Line ref={progress} points={[[-820, -492], [820, -492]]} stroke={C.red} lineWidth={4} end={0} />
      <Layout position={[738, -446]} layout direction={'row'} gap={12} alignItems={'center'}>
        <Circle width={15} height={15} fill={C.red} shadowColor={C.red} shadowBlur={18} />
        <Txt fontFamily={FONT} fontSize={22} fontWeight={780} letterSpacing={2} fill={C.primary} text={'小行星 AI 观测站'} />
      </Layout>
      <Audio src={'/qwen-ui-agent/qwen-ui-agent-hosted.mp3'} play />
    </>,
  );
  yield* all(
    runSequence(view),
    tween(timeline.duration, value => {
      scan().position.y(-540 + 1080 * value);
      grid().rotation(value * 0.8);
      progress().end(value);
    }),
  );
});

export default makeProject({
  scenes: [scene],
  settings: {shared: {size: {x: 1920, y: 1080}}, rendering: {fps: 30}, preview: {fps: 30}},
});
