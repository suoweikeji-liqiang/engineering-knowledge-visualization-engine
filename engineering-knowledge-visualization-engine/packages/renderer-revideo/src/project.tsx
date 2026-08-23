import {
  Audio,
  Circle,
  Grid,
  Img,
  Layout,
  Line,
  Rect,
  Txt,
  View2D,
  makeScene2D,
} from '@revideo/2d';
import {
  all,
  chain,
  createRef,
  delay,
  easeInOutCubic,
  linear,
  makeProject,
  tween,
  waitFor,
} from '@revideo/core';
import story from '../../../examples/ai-agent-harness-benchmark/storyboard/story.json';
import timeline from '../../../examples/ai-agent-harness-benchmark/audio/ai-agent-harness-benchmark.timeline.json';
import {ASTEROID_WARM_THEME as C} from './theme';
import {
  CINEMATIC_FONT as FONT,
  CINEMATIC_MONO as MONO,
  cinematicCharacterFrame as characterFrame,
  cinematicConnector as connector,
  cinematicHandNote as handNote,
  cinematicNodeCard as nodeCard,
  enterCinematicStage as enter,
  exitCinematicStage as exit,
  makeCinematicStage as makeStage,
} from './cinematic-sketch';

const shots = Object.fromEntries(timeline.shots.map(shot => [shot.id, shot.duration]));
const copy = Object.fromEntries(story.shots.map(shot => [shot.id, shot]));

function* hook(view: View2D) {
  const stage = makeStage(view, '01', copy.hook.headline, copy.hook.dialogue);
  const orb = createRef<Circle>();
  const mark = createRef<Txt>();
  const left = createRef<Rect>();
  const right = createRef<Rect>();
  const host = createRef<Layout>();
  const question = createRef<Rect>();
  stage.body().add(
    <>
      <Layout ref={host} opacity={0} scale={0.92}>
        {characterFrame('/characters/xiaolan-desk.jpg', '小兰的观测手账  //  先别急着叫它 Agent', 610, -490, 15)}
      </Layout>
      <Rect
        ref={question}
        x={405}
        y={10}
        width={650}
        height={430}
        radius={34}
        fill={'#FFF9F0F2'}
        stroke={C.line}
        lineWidth={2}
        opacity={0}
      >
        <Txt
          y={-165}
          width={540}
          textAlign={'left'}
          fontFamily={FONT}
          fontSize={27}
          fontWeight={700}
          fill={C.yellow}
          text={'一个会聊天的大模型'}
        />
        <Txt
          y={-112}
          width={540}
          textAlign={'left'}
          fontFamily={FONT}
          fontSize={25}
          fill={C.soft}
          text={'为什么还不能直接变成 Agent？'}
        />
      </Rect>
      <Circle
        ref={orb}
        x={405}
        y={-18}
        width={160}
        height={160}
        fill={'#E1F0EF'}
        stroke={C.cyan}
        lineWidth={6}
        shadowColor={'#2C8E9266'}
        shadowBlur={55}
        scale={0.45}
      >
        <Txt fontFamily={MONO} fontSize={40} fontWeight={800} fill={C.cyan} text={'LLM'} />
      </Circle>
      <Txt ref={mark} x={405} y={92} fontFamily={FONT} fontSize={62} fill={C.red} text={'≠'} opacity={0} />
      <Rect ref={left} x={245} y={160} opacity={0} scale={0.8}>
        {nodeCard('CHAT', '回答一条消息', C.purple, 0, 0, 270)}
      </Rect>
      <Rect ref={right} x={565} y={160} opacity={0} scale={0.8}>
        {nodeCard('AGENT', '完成一个目标', C.red, 0, 0, 270)}
      </Rect>
    </>,
  );
  yield* enter(stage.root, -1);
  yield* all(
    chain(
      all(host().opacity(1, 0.45), host().scale(1, 0.55)),
      question().opacity(1, 0.3),
      orb().scale(1.08, 0.6, easeInOutCubic),
      orb().scale(1, 0.25),
      all(left().opacity(1, 0.4), left().scale(1, 0.5)),
      all(right().opacity(1, 0.4), right().scale(1, 0.5)),
      mark().opacity(1, 0.25),
    ),
    host().position.x(12, shots.hook - 0.8, easeInOutCubic),
    host().rotation(0.35, shots.hook - 0.8, easeInOutCubic),
    waitFor(shots.hook - 0.8),
  );
  yield* exit(stage.root, 1);
}

function* singleCall(view: View2D) {
  const stage = makeStage(view, '02', copy['single-call'].headline, copy['single-call'].dialogue, C.yellow);
  const evidence = createRef<Layout>();
  const pipeline = createRef<Layout>();
  const input = createRef<Rect>();
  const model = createRef<Rect>();
  const output = createRef<Rect>();
  const line1 = createRef<Line>();
  const line2 = createRef<Line>();
  const blocked = createRef<Layout>();
  stage.body().add(
    <>
      <Layout ref={evidence} opacity={0} scale={0.96}>
        <Layout x={-525} y={5} rotation={-2}>
          <Rect x={8} y={10} width={390} height={520} radius={18} fill={'#DCCFC0'} />
          <Rect width={390} height={520} radius={18} fill={C.paper} stroke={C.line} lineWidth={2} shadowColor={'#6D594033'} shadowBlur={28}>
            <Img src={'/evidence/openai-agent-guide-page-04.png'} width={354} height={458} radius={8} />
          </Rect>
          <Rect y={-266} width={104} height={24} radius={4} fill={`${C.tape}B8`} rotation={3} />
        </Layout>
        <Rect x={260} y={5} width={830} height={500} radius={[28, 22, 30, 24]} fill={C.panel} stroke={C.line} lineWidth={2} shadowColor={'#6D594022'} shadowBlur={24}>
          <Txt x={-345} y={-205} width={90} textAlign={'left'} fontFamily={MONO} fontSize={20} fontWeight={800} fill={C.red} text={'SOURCE 01'} />
          <Txt x={40} y={-142} width={690} textAlign={'left'} fontFamily={FONT} fontSize={44} fontWeight={800} fill={C.primary} text={'单轮 LLM，并不等于 Agent'} />
          <Rect x={-50} y={-98} width={500} height={18} radius={8} fill={`${C.yellow}33`} rotation={-1} />
          <Txt x={40} y={-20} width={690} textAlign={'left'} fontFamily={FONT} fontSize={27} lineHeight={48} fill={C.soft} text={'官方定义强调三个差别：\n• 模型需要管理工作流\n• 动态选择外部工具\n• 识别完成、失败与退出条件'} />
          <Txt x={40} y={202} width={690} textAlign={'left'} fontFamily={MONO} fontSize={18} fill={C.purple} text={'OPENAI · A PRACTICAL GUIDE TO BUILDING AGENTS · P.4'} />
        </Rect>
      </Layout>
      <Layout ref={pipeline} opacity={0}>
        <Rect ref={input} opacity={0}>{nodeCard('INPUT', '用户指令', C.primary, -520, -30)}</Rect>
        <Rect ref={model} opacity={0}>{nodeCard('MODEL', '生成判断', C.cyan, 0, -30)}</Rect>
        <Rect ref={output} opacity={0}>{nodeCard('OUTPUT', '文本答案', C.purple, 520, -30)}</Rect>
        <Line ref={line1} points={[[-380, -30], [-145, -30]]} stroke={C.cyan} lineWidth={5} endArrow arrowSize={14} end={0} />
        <Line ref={line2} points={[[145, -30], [380, -30]]} stroke={C.purple} lineWidth={5} endArrow arrowSize={14} end={0} />
        <Layout ref={blocked} y={175} opacity={0}>
          <Line points={[[-620, 0], [500, 0]]} stroke={C.line} lineWidth={3} lineDash={[16, 12]} />
          <Rect x={610} width={210} height={74} radius={18} fill={'#F8E5E5'} stroke={C.red} lineWidth={2}>
            <Txt fontFamily={MONO} fontSize={24} fontWeight={700} fill={C.red} text={'TASK OPEN'} />
          </Rect>
        </Layout>
        {handNote('一次回答，还不是任务完成', C.red, -260, 255, -1.2)}
      </Layout>
    </>,
  );
  yield* enter(stage.root, 1);
  yield* all(
    chain(
      all(evidence().opacity(1, 0.35), evidence().scale(1, 0.45)),
      waitFor(1.45),
      all(evidence().opacity(0, 0.35), evidence().position.x(-80, 0.35)),
      pipeline().opacity(1, 0.25),
      input().opacity(1, 0.25),
      line1().end(1, 0.55),
      model().opacity(1, 0.25),
      line2().end(1, 0.55),
      output().opacity(1, 0.25),
      blocked().opacity(1, 0.4),
    ),
    waitFor(shots['single-call'] - 0.8),
  );
  yield* exit(stage.root, -1);
}

function* loopShot(view: View2D) {
  const stage = makeStage(view, '03', copy.loop.headline, copy.loop.dialogue, C.cyan);
  const metaphor = createRef<Layout>();
  const diagram = createRef<Layout>();
  const loopLine = createRef<Line>();
  const pulse = createRef<Circle>();
  const goal = createRef<Rect>();
  stage.body().add(
    <>
      <Layout ref={metaphor} opacity={0} scale={0.97}>
        <Rect x={9} y={10} width={1138} height={640} radius={[28, 22, 30, 24]} fill={'#DCCFC0'} rotation={0.8} />
        <Rect width={1140} height={640} radius={[28, 22, 30, 24]} fill={C.paper} stroke={C.line} lineWidth={2} shadowColor={'#6D594044'} shadowBlur={32}>
          <Img src={'/metaphors/xiaolan-agent-loop.png'} width={1100} height={619} radius={[20, 16, 22, 18]} />
          <Rect y={245} width={760} height={64} radius={18} fill={'#FFF9F0E8'} stroke={C.line} lineWidth={2}>
            <Txt fontFamily={'Kaiti SC, STKaiti, KaiTi, serif'} fontSize={30} fontWeight={800} fill={C.primary} text={'行动，是一步一步跨过去的'} />
          </Rect>
        </Rect>
        <Rect x={-420} y={-326} width={116} height={26} radius={4} fill={`${C.tape}C0`} rotation={-3} />
        <Rect x={420} y={-326} width={116} height={26} radius={4} fill={`${C.purple}45`} rotation={3} />
      </Layout>
      <Layout ref={diagram} opacity={0}>
        <Line
          ref={loopLine}
          points={[
            [-520, 80],
            [-260, -125],
            [80, -125],
            [350, 80],
            [80, 250],
            [-260, 250],
            [-520, 80],
          ]}
          stroke={C.cyan}
          lineWidth={5}
          radius={38}
          endArrow
          arrowSize={14}
          end={0}
        />
        {nodeCard('GOAL', '明确目标', C.primary, -520, 80, 240)}
        {nodeCard('PLAN', '决定下一步', C.purple, -260, -125, 240)}
        {nodeCard('ACT', '调用工具', C.yellow, 80, -125, 240)}
        {nodeCard('OBSERVE', '读取结果', C.cyan, 350, 80, 260)}
        {nodeCard('UPDATE', '更新状态', C.green, 80, 250, 240)}
        <Circle ref={pulse} position={[-520, 80]} width={30} height={30} fill={C.primary} shadowColor={C.cyan} shadowBlur={24} />
        <Rect ref={goal} x={580} y={220} width={260} height={86} radius={22} fill={'#E4F0E8'} stroke={C.green} lineWidth={3} opacity={0}>
          <Txt fontFamily={MONO} fontSize={25} fontWeight={700} fill={C.green} text={'✓ DONE'} />
        </Rect>
      </Layout>
    </>,
  );
  yield* enter(stage.root, -1);
  yield* all(
    chain(
      metaphor().opacity(1, 0.3),
      waitFor(1.4),
      metaphor().opacity(0, 0.35),
      diagram().opacity(1, 0.25),
      loopLine().end(1, 2, easeInOutCubic),
    ),
    chain(
      waitFor(2.3),
      pulse().position([-260, -125], 0.4, linear),
      pulse().position([80, -125], 0.4, linear),
      pulse().position([350, 80], 0.4, linear),
      pulse().position([80, 250], 0.4, linear),
      pulse().position([-260, 250], 0.4, linear),
      pulse().position([-520, 80], 0.4, linear),
      goal().opacity(1, 0.3),
    ),
    metaphor().scale(1.02, 2.05, easeInOutCubic),
    metaphor().position.x(-18, 2.05, easeInOutCubic),
    waitFor(shots.loop - 0.8),
  );
  yield* exit(stage.root, 1);
}

function toolPanel(
  title: string,
  command: string,
  result: string,
  color: string,
  x: number,
) {
  return (
    <Layout x={x} rotation={x < 0 ? -0.5 : x > 0 ? 0.45 : -0.15}>
      <Rect x={7} y={8} width={470} height={330} radius={[22, 28, 24, 20]} fill={'#E2D5C5'} rotation={0.8} />
      <Rect width={470} height={330} radius={[26, 21, 27, 23]} fill={C.panel} stroke={C.line} lineWidth={2} shadowColor={'#6D594026'} shadowBlur={18}>
        <Rect y={-132} width={470} height={66} radius={[26, 21, 0, 0]} fill={C.panel2}>
          <Circle x={-190} width={12} height={12} fill={color} />
          <Txt x={-15} width={350} textAlign={'left'} fontFamily={MONO} fontSize={23} fontWeight={700} fill={C.primary} text={title} />
        </Rect>
        <Txt y={-50} width={390} textAlign={'left'} fontFamily={MONO} fontSize={22} fill={C.cyan} text={`$ ${command}`} />
        <Line y={8} points={[[-195, 0], [195, 0]]} stroke={C.line} lineWidth={2} />
        <Txt y={70} width={390} textAlign={'left'} fontFamily={MONO} fontSize={21} lineHeight={34} fill={C.soft} text={result} />
      </Rect>
      <Rect y={-170} width={88} height={22} radius={4} fill={`${color}44`} rotation={-3} />
    </Layout>
  );
}

function* toolsShot(view: View2D) {
  const stage = makeStage(view, '04', copy.tools.headline, copy.tools.dialogue, C.yellow);
  const search = createRef<Rect>();
  const file = createRef<Rect>();
  const code = createRef<Rect>();
  const router = createRef<Rect>();
  stage.body().add(
    <>
      <Rect ref={search} x={-500} y={50} opacity={0} scale={0.9}>{toolPanel('WEB SEARCH', 'search(query)', '12 sources\nranked by relevance', C.cyan, 0)}</Rect>
      <Rect ref={file} x={0} y={50} opacity={0} scale={0.9}>{toolPanel('FILE SYSTEM', 'read(report.md)', '8.4 KB loaded\nencoding: utf-8', C.purple, 0)}</Rect>
      <Rect ref={code} x={500} y={50} opacity={0} scale={0.9}>{toolPanel('TERMINAL', 'pnpm test', '87 passed\nexit code: 0', C.green, 0)}</Rect>
      <Rect ref={router} y={-210} width={360} height={80} radius={40} fill={'#E1F0EF'} stroke={C.cyan} lineWidth={3} opacity={0}>
        <Txt fontFamily={MONO} fontSize={26} fontWeight={700} fill={C.cyan} text={'TOOL ROUTER'} />
      </Rect>
      {connector([[0, -168], [-500, -115]], C.cyan)}
      {connector([[0, -168], [0, -115]], C.purple)}
      {connector([[0, -168], [500, -115]], C.green)}
      {handNote('工具是行动接口', C.yellow, -610, -215, -2)}
    </>,
  );
  yield* enter(stage.root, 1);
  yield* all(
    chain(
      router().opacity(1, 0.35),
      all(search().opacity(1, 0.4), search().scale(1, 0.45)),
      all(file().opacity(1, 0.4), file().scale(1, 0.45)),
      all(code().opacity(1, 0.4), code().scale(1, 0.45)),
    ),
    waitFor(shots.tools - 0.8),
  );
  yield* exit(stage.root, -1);
}

function traceRow(
  step: string,
  label: string,
  status: string,
  color: string,
  y: number,
) {
  return (
    <Layout y={y}>
      <Rect x={3} y={4} width={1156} height={84} radius={[13, 18, 15, 17]} fill={'#E0D4C5'} rotation={0.15} />
      <Rect width={1160} height={86} radius={[16, 13, 18, 14]} fill={C.panel2}>
        <Rect x={-574} width={8} height={62} radius={4} fill={color} opacity={0.75} />
        <Txt x={-520} width={90} textAlign={'left'} fontFamily={MONO} fontSize={21} fill={C.soft} text={step} />
        <Txt x={-115} width={690} textAlign={'left'} fontFamily={MONO} fontSize={24} fill={C.primary} text={label} />
        <Rect x={470} width={150} height={48} radius={24} fill={`${color}22`} stroke={color} lineWidth={2}>
          <Txt fontFamily={MONO} fontSize={19} fontWeight={700} fill={color} text={status} />
        </Rect>
      </Rect>
    </Layout>
  );
}

function* failureShot(view: View2D) {
  const stage = makeStage(view, '05', copy.failure.headline, copy.failure.dialogue, C.red);
  const row1 = createRef<Rect>();
  const row2 = createRef<Rect>();
  const row3 = createRef<Rect>();
  const retry = createRef<Rect>();
  const focus = createRef<Rect>();
  const host = createRef<Layout>();
  const note = createRef<Rect>();
  stage.body().add(
    <>
    <Layout ref={host} opacity={0} scale={0.86}>
      {characterFrame('/characters/xiaolan-surprised.jpg', '等等，真实环境怎么可能永远成功？', 350, -635, 30, -3)}
    </Layout>
    <Rect ref={note} x={-630} y={242} width={380} height={88} radius={18} fill={'#4A2931'} stroke={C.red} lineWidth={2} opacity={0} rotation={-1}>
      <Txt width={330} fontFamily={FONT} fontSize={24} fontWeight={700} fill={C.onDark} text={'超时 · 拒绝 · 参数错误'} />
    </Rect>
    <Rect x={190} width={1240} height={480} radius={30} fill={C.panel} stroke={C.line} lineWidth={2} shadowColor={'#6D594022'} shadowBlur={28}>
      <Rect y={-205} width={1240} height={70} radius={[30, 30, 0, 0]} fill={C.night}>
        <Txt x={-480} width={220} textAlign={'left'} fontFamily={MONO} fontSize={22} fontWeight={700} fill={C.onDark} text={'AGENT TRACE'} />
        <Circle x={520} width={13} height={13} fill={C.green} />
        <Txt x={410} width={180} textAlign={'right'} fontFamily={MONO} fontSize={18} fill={C.mutedOnDark} text={'RUNNING'} />
      </Rect>
      <Rect ref={row1} y={-105} opacity={0} scale={0.96}>{traceRow('01', 'plan  ·  locate quarterly report', 'DONE', C.green, 0)}</Rect>
      <Rect ref={row2} y={0} opacity={0} scale={0.96}>{traceRow('02', 'tool  ·  fetch remote document', 'TIMEOUT', C.red, 0)}</Rect>
      <Rect ref={row3} y={105} opacity={0} scale={0.96}>{traceRow('03', 'policy  ·  write /finance', 'DENIED', C.yellow, 0)}</Rect>
      <Rect ref={retry} y={198} width={420} height={58} radius={29} fill={'#E1F0EF'} stroke={C.cyan} lineWidth={2} opacity={0}>
        <Txt fontFamily={MONO} fontSize={20} fontWeight={700} fill={C.cyan} text={'↻ RETRY 2/3 · BACKOFF 4s'} />
      </Rect>
      <Rect ref={focus} y={0} width={1130} height={98} radius={19} stroke={C.red} lineWidth={4} opacity={0} shadowColor={C.red} shadowBlur={26} />
    </Rect>,
    </>,
  );
  yield* enter(stage.root, -1);
  yield* all(
    chain(
      all(host().opacity(1, 0.4), host().scale(1, 0.5)),
      note().opacity(1, 0.3),
      row1().opacity(1, 0.35),
      row2().opacity(1, 0.35),
      all(focus().opacity(1, 0.25), focus().scale(1.02, 0.25)),
      row3().opacity(1, 0.35),
      retry().opacity(1, 0.35),
      focus().opacity(0, 0.35),
    ),
    host().position.y(-8, shots.failure - 0.8, easeInOutCubic),
    host().rotation(0.45, shots.failure - 0.8, easeInOutCubic),
    waitFor(shots.failure - 0.8),
  );
  yield* exit(stage.root, 1);
}

function* harnessShot(view: View2D) {
  const stage = makeStage(view, '06', copy.harness.headline, copy.harness.dialogue, C.purple);
  const shell = createRef<Rect>();
  const model = createRef<Circle>();
  const memory = createRef<Rect>();
  const policy = createRef<Rect>();
  const tools = createRef<Rect>();
  const context = createRef<Rect>();
  const dataPulse = createRef<Circle>();
  stage.body().add(
    <>
      <Rect ref={shell} width={1320} height={510} radius={42} fill={'#FFF9F0EE'} stroke={C.purple} lineWidth={4} opacity={0} scale={0.94} shadowColor={'#765D9144'} shadowBlur={35}>
        <Txt x={-530} y={-215} width={220} textAlign={'left'} fontFamily={MONO} fontSize={23} fontWeight={700} fill={C.purple} text={'HARNESS'} />
      </Rect>
      <Circle ref={model} width={230} height={230} fill={'#E1F0EF'} stroke={C.cyan} lineWidth={6} scale={0} shadowColor={'#2C8E9255'} shadowBlur={40}>
        <Txt fontFamily={MONO} fontSize={44} fontWeight={800} fill={C.cyan} text={'MODEL'} />
      </Circle>
      <Rect ref={context} x={-420} y={-120} opacity={0}>{nodeCard('CONTEXT', '上下文窗口', C.primary, 0, 0, 290)}</Rect>
      <Rect ref={memory} x={420} y={-120} opacity={0}>{nodeCard('MEMORY', '长期状态', C.purple, 0, 0, 290)}</Rect>
      <Rect ref={policy} x={-420} y={150} opacity={0}>{nodeCard('POLICY', '权限与边界', C.yellow, 0, 0, 290)}</Rect>
      <Rect ref={tools} x={420} y={150} opacity={0}>{nodeCard('TOOLS', '调用与恢复', C.green, 0, 0, 290)}</Rect>
      {connector([[-305, -120], [-125, -40]], C.primary)}
      {connector([[305, -120], [125, -40]], C.purple)}
      {connector([[-305, 150], [-125, 40]], C.yellow)}
      {connector([[305, 150], [125, 40]], C.green)}
      <Circle ref={dataPulse} x={-305} y={-120} width={18} height={18} fill={C.cyan} opacity={0} shadowColor={C.cyan} shadowBlur={20} />
      {handNote('模型之外，才是运行系统', C.purple, 485, -225, 1.5)}
    </>,
  );
  yield* enter(stage.root, 1);
  yield* all(
    chain(
      all(shell().opacity(1, 0.5), shell().scale(1, 0.65)),
      model().scale(1, 0.55, easeInOutCubic),
      all(context().opacity(1, 0.35), memory().opacity(1, 0.35)),
      all(policy().opacity(1, 0.35), tools().opacity(1, 0.35)),
      model().rotation(360, 1.1, easeInOutCubic),
      dataPulse().opacity(1, 0.2),
      dataPulse().position([-125, -40], 0.45, linear),
      dataPulse().position([125, 40], 0.45, linear),
      dataPulse().position([305, 150], 0.45, linear),
      dataPulse().opacity(0, 0.2),
    ),
    waitFor(shots.harness - 0.8),
  );
  yield* exit(stage.root, -1);
}

function* landingShot(view: View2D) {
  const stage = makeStage(view, '07', copy.landing.headline, copy.landing.dialogue, C.green);
  const run = createRef<Rect>();
  const line1 = createRef<Txt>();
  const line2 = createRef<Txt>();
  const line3 = createRef<Txt>();
  const result = createRef<Rect>();
  const progress = createRef<Rect>();
  const terminalScan = createRef<Rect>();
  stage.body().add(
    <Layout>
    <Rect x={-42} y={-18} width={1280} height={458} radius={30} fill={`${C.purple}28`} stroke={`${C.purple}55`} lineWidth={2} rotation={-2.2} />
    <Rect x={44} y={-14} width={1280} height={458} radius={30} fill={`${C.cyan}20`} stroke={`${C.cyan}55`} lineWidth={2} rotation={2} />
    <Rect width={1360} height={500} radius={30} fill={C.night} stroke={C.line} lineWidth={2} shadowColor={'#6D594033'} shadowBlur={30}>
      <Rect y={-215} width={1360} height={70} radius={[30, 30, 0, 0]} fill={C.night2}>
        <Circle x={-620} width={14} height={14} fill={C.red} />
        <Circle x={-590} width={14} height={14} fill={C.yellow} />
        <Circle x={-560} width={14} height={14} fill={C.green} />
        <Txt x={0} fontFamily={MONO} fontSize={20} fill={C.mutedOnDark} text={'agent-run / trace-8F21'} />
      </Rect>
      <Rect ref={run} y={-132} width={1200} height={60} radius={14} fill={'#403947'} opacity={0}>
        <Txt x={0} width={1080} textAlign={'left'} fontFamily={MONO} fontSize={22} fill={'#73C5C5'} text={'$ agent run "summarize the latest AI report"'} />
      </Rect>
      <Txt ref={line1} x={0} y={-48} width={1040} textAlign={'left'} fontFamily={MONO} fontSize={22} fill={C.mutedOnDark} text={'○ planning execution graph'} opacity={0} />
      <Txt ref={line2} x={0} y={18} width={1040} textAlign={'left'} fontFamily={MONO} fontSize={22} fill={C.mutedOnDark} text={'○ reading 12 verified sources'} opacity={0} />
      <Txt ref={line3} x={0} y={84} width={1040} textAlign={'left'} fontFamily={MONO} fontSize={22} fill={C.mutedOnDark} text={'○ validating citations and output'} opacity={0} />
      <Rect y={155} width={1200} height={10} radius={5} fill={'#5B5362'}>
        <Rect ref={progress} x={-600} width={0} height={10} radius={5} fill={C.cyan} offset={[-1, 0]} />
      </Rect>
      <Rect ref={result} y={205} width={460} height={62} radius={31} fill={'#E4F0E8'} stroke={C.green} lineWidth={2} opacity={0}>
        <Txt fontFamily={MONO} fontSize={21} fontWeight={700} fill={C.green} text={'✓ COMPLETED · 7.42s'} />
      </Rect>
      <Rect ref={terminalScan} y={-180} width={1260} height={3} fill={'#73C5C5'} opacity={0.14} shadowColor={'#73C5C5'} shadowBlur={10} />
    </Rect>,
    </Layout>,
  );
  yield* enter(stage.root, -1);
  yield* all(
    chain(
      run().opacity(1, 0.3),
      line1().opacity(1, 0.3),
      line1().text('✓ planning execution graph', 0.35),
      line2().opacity(1, 0.3),
      line2().text('✓ reading 12 verified sources', 0.35),
      line3().opacity(1, 0.3),
      line3().text('✓ validating citations and output', 0.35),
      result().opacity(1, 0.35),
    ),
    progress().width(1200, 3.2, easeInOutCubic),
    terminalScan().position.y(180, shots.landing - 0.8, linear),
    waitFor(shots.landing - 0.8),
  );
  yield* exit(stage.root, 1);
}

function* summaryShot(view: View2D) {
  const stage = makeStage(view, '08', copy.summary.headline, copy.summary.dialogue, C.red);
  const model = createRef<Rect>();
  const times = createRef<Txt>();
  const runtime = createRef<Rect>();
  const result = createRef<Layout>();
  const host = createRef<Layout>();
  const equation = createRef<Rect>();
  stage.body().add(
    <>
      <Layout ref={host} opacity={0} scale={0.9}>
        {characterFrame('/characters/xiaolan-pointing.jpg', '小兰结论  //  模型负责判断，系统负责行动', 560, -520, 10, -2)}
      </Layout>
      <Rect ref={equation} x={360} y={10} width={830} height={440} radius={34} fill={'#FFF9F0F2'} stroke={C.line} lineWidth={2} opacity={0} shadowColor={'#6D594022'} shadowBlur={28}>
        <Rect ref={model} opacity={0} scale={0.8}>{nodeCard('MODEL', '判断', C.cyan, -235, -75, 270)}</Rect>
        <Txt ref={times} x={0} y={-75} fontFamily={MONO} fontSize={72} fontWeight={500} fill={C.soft} text={'×'} opacity={0} />
        <Rect ref={runtime} opacity={0} scale={0.8}>{nodeCard('RUNTIME', '持续行动', C.purple, 235, -75, 270)}</Rect>
        <Layout ref={result} y={130} opacity={0}>
          <Rect width={610} height={110} radius={55} fill={'#F8E5E5'} stroke={C.red} lineWidth={4} shadowColor={'#D8556244'} shadowBlur={34}>
            <Txt fontFamily={MONO} fontSize={44} fontWeight={900} letterSpacing={5} fill={C.primary} text={'=  AGENT'} />
          </Rect>
        </Layout>
      </Rect>
    </>,
  );
  yield* enter(stage.root, 1);
  yield* all(
    chain(
      all(host().opacity(1, 0.4), host().scale(1, 0.5)),
      equation().opacity(1, 0.35),
      all(model().opacity(1, 0.4), model().scale(1, 0.5)),
      times().opacity(1, 0.3),
      all(runtime().opacity(1, 0.4), runtime().scale(1, 0.5)),
      all(result().opacity(1, 0.4), result().position.y(115, 0.5)),
    ),
    host().position.x(10, shots.summary - 0.8, easeInOutCubic),
    host().rotation(0.35, shots.summary - 0.8, easeInOutCubic),
    waitFor(shots.summary - 0.8),
  );
  yield* exit(stage.root, -1);
}

function* runSequence(view: View2D) {
  yield* hook(view);
  yield* singleCall(view);
  yield* loopShot(view);
  yield* toolsShot(view);
  yield* failureShot(view);
  yield* harnessShot(view);
  yield* landingShot(view);
  yield* summaryShot(view);
}

const scene = makeScene2D('agent-harness-benchmark', function* (view) {
  const grid = createRef<Grid>();
  const scan = createRef<Line>();
  const totalDuration = timeline.duration;
  view.fill(C.bg);
  view.add(
    <>
      <Grid
        ref={grid}
        size={[2100, 1260]}
        spacing={64}
        stroke={'#D8CCBD'}
        lineWidth={1}
        opacity={0.7}
      />
      <Circle x={-820} y={-470} width={520} height={520} fill={'#D8556210'} shadowColor={'#D8556222'} shadowBlur={100} />
      <Circle x={860} y={420} width={620} height={620} fill={'#765D910A'} shadowColor={'#765D9120'} shadowBlur={120} />
      <Line ref={scan} points={[[-960, 0], [960, 0]]} stroke={'#2C8E9222'} lineWidth={2} y={-540} />
      <Layout position={[735, -440]} layout direction={'row'} gap={12} alignItems={'center'}>
        <Circle width={16} height={16} fill={C.red} shadowColor={C.red} shadowBlur={18} />
        <Txt fontFamily={FONT} fontSize={24} fontWeight={700} letterSpacing={2} fill={C.primary} text={'小行星 AI 观测站'} />
      </Layout>
      <Audio src={'/benchmark-audio.mp3'} play={true} />
    </>,
  );

  yield* all(
    runSequence(view),
    tween(totalDuration, value => {
      scan().y(-540 + 1080 * value);
      grid().rotation(linear(value, 0, 1.2));
    }),
  );
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: 1920, y: 1080},
    },
    rendering: {
      fps: 30,
    },
    preview: {
      fps: 30,
    },
  },
});
