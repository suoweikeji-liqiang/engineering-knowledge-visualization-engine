import {Circle, Img, Layout, Rect, Txt} from '@revideo/2d';
import {Reference, createRef, easeInOutCubic} from '@revideo/core';
import {ASTEROID_WARM_THEME as C} from './theme';
import {CINEMATIC_MONO as MONO} from './cinematic-sketch';

export type XiaolanRigV2Action = 'point-emphasis' | 'think-focus' | 'explain-open' | 'resolve-wave';

export type XiaolanRigV2Runtime = {
  root: Reference<Layout>;
  update: (progress: number, localSeconds: number, mouthOpen: number) => void;
};

const ASSET = '/qwen-ui-agent/characters-v2';

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function phase(value: number, start: number, end: number): number {
  return easeInOutCubic(clamp01((value - start) / Math.max(0.001, end - start)));
}

function mix(from: number, to: number, value: number): number {
  return from + (to - from) * value;
}

const TARGETS: Record<XiaolanRigV2Action, {
  leftUpper: number;
  leftForearm: number;
  leftHand: number;
  rightUpper: number;
  rightForearm: number;
  rightHand: number;
  head: number;
}> = {
  'point-emphasis': {leftUpper: 16, leftForearm: -8, leftHand: 176, rightUpper: -64, rightForearm: -48, rightHand: 158, head: -3.2},
  'think-focus': {leftUpper: 22, leftForearm: 12, leftHand: 168, rightUpper: -34, rightForearm: -72, rightHand: 142, head: 4.2},
  'explain-open': {leftUpper: 58, leftForearm: 24, leftHand: 94, rightUpper: -58, rightForearm: -26, rightHand: 148, head: -1.8},
  'resolve-wave': {leftUpper: 52, leftForearm: 34, leftHand: 100, rightUpper: -44, rightForearm: -34, rightHand: 154, head: 1.4},
};

export function addXiaolanRigV2(parent: Layout, options: {
  action: XiaolanRigV2Action;
  width: number;
  x: number;
  y: number;
  accent: string;
  label: string;
}): XiaolanRigV2Runtime {
  const root = createRef<Layout>();
  const model = createRef<Layout>();
  const torso = createRef<Layout>();
  const head = createRef<Layout>();
  const eyesOpen = createRef<Img>();
  const eyesClosed = createRef<Img>();
  const mouthClosed = createRef<Img>();
  const mouthMid = createRef<Img>();
  const mouthWide = createRef<Img>();
  const leftUpper = createRef<Layout>();
  const leftForearm = createRef<Layout>();
  const leftHand = createRef<Layout>();
  const rightUpper = createRef<Layout>();
  const rightForearm = createRef<Layout>();
  const rightHand = createRef<Layout>();
  const baseScale = options.width / 590;

  parent.add(
    <Layout ref={root} x={options.x} y={options.y} opacity={0} scale={0.92}>
      <Layout ref={model} scale={baseScale}>
        <Layout ref={leftUpper} x={-112} y={-4} rotation={10}>
          <Img src={`${ASSET}/left-upper-arm.png`} width={96} height={206} y={91} />
          <Layout ref={leftForearm} y={178}>
            <Img src={`${ASSET}/left-forearm.png`} width={78} height={170} y={76} />
            <Layout ref={leftHand} y={153} rotation={180}>
              <Img src={`${ASSET}/left-open-hand.png`} width={112} height={130} y={-57} />
            </Layout>
            <Circle y={153} width={20} height={26} fill={'#F6D9CA'} />
          </Layout>
          <Circle y={178} width={28} height={34} fill={'#F4DDD2'} />
        </Layout>

        <Layout ref={rightUpper} x={112} y={-4} rotation={-10}>
          <Img src={`${ASSET}/right-upper-arm.png`} width={92} height={222} y={99} />
          <Layout ref={rightForearm} y={193}>
            <Img src={`${ASSET}/right-forearm.png`} width={77} height={168} y={75} />
            <Layout ref={rightHand} y={150} rotation={180}>
              <Img src={`${ASSET}/right-pointing-hand.png`} width={105} height={159} y={-71} />
            </Layout>
            <Circle y={150} width={20} height={26} fill={'#F6D9CA'} />
          </Layout>
          <Circle y={193} width={28} height={34} fill={'#F4DDD2'} />
        </Layout>

        <Layout ref={torso} y={92}>
          <Img src={`${ASSET}/torso.png`} width={260} height={350} />
        </Layout>
        <Circle x={-112} y={-4} width={38} height={50} fill={'#F5DED2'} />
        <Circle x={112} y={-4} width={38} height={50} fill={'#F5DED2'} />

        <Layout ref={head} y={-170}>
          <Img src={`${ASSET}/head-base.png`} width={360} height={464} />
          <Img ref={eyesOpen} src={`${ASSET}/eyes-open.png`} y={-67} width={190} height={99} />
          <Img ref={eyesClosed} src={`${ASSET}/eyes-closed.png`} y={-67} width={186} height={101} opacity={0} />
          <Img ref={mouthClosed} src={`${ASSET}/mouth-closed.png`} y={30} width={62} height={28} />
          <Img ref={mouthMid} src={`${ASSET}/mouth-mid.png`} y={31} width={56} height={34} opacity={0} />
          <Img ref={mouthWide} src={`${ASSET}/mouth-open.png`} y={33} width={55} height={40} opacity={0} />
        </Layout>
      </Layout>

      <Rect y={330 * baseScale} width={330} height={42} radius={21} fill={C.night} stroke={`${options.accent}88`} lineWidth={2}>
        <Txt fontFamily={MONO} fontSize={16} fontWeight={850} letterSpacing={1.1} fill={C.onDark} text={options.label} />
      </Rect>
    </Layout>,
  );

  return {
    root,
    update: (progress, localSeconds, mouthOpen) => {
      const pose = phase(progress, 0.08, 0.42);
      const target = TARGETS[options.action];
      const breath = Math.sin(localSeconds * Math.PI * 0.72);
      const settle = Math.sin(phase(progress, 0.08, 0.58) * Math.PI * 2) * (1 - phase(progress, 0.5, 0.82));

      torso().scale.y(1 + breath * 0.009);
      torso().position.y(92 - breath * 1.6);
      head().rotation(mix(0, target.head, pose) + settle * 1.2);
      head().position.y(-170 - Math.abs(breath) * 1.4);

      leftUpper().rotation(mix(10, target.leftUpper, pose));
      leftForearm().rotation(mix(0, target.leftForearm, pose));
      leftHand().rotation(mix(180, target.leftHand, pose));
      rightUpper().rotation(mix(-10, target.rightUpper, pose));
      rightForearm().rotation(mix(0, target.rightForearm, pose));
      rightHand().rotation(mix(180, target.rightHand, pose));

      const blinkCycle = localSeconds % 3.9;
      const blink = blinkCycle > 3.66 ? Math.sin(((blinkCycle - 3.66) / 0.24) * Math.PI) : 0;
      eyesOpen().opacity(1 - blink);
      eyesClosed().opacity(blink);

      const phoneme = clamp01(mouthOpen);
      mouthClosed().opacity(clamp01(1 - phoneme * 3.8));
      mouthMid().opacity(clamp01(1 - Math.abs(phoneme - 0.45) * 4.1));
      mouthWide().opacity(clamp01((phoneme - 0.55) * 2.8));
      model().position.y(Math.sin(localSeconds * Math.PI * 0.34) * 2.2);
    },
  };
}
