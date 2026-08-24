import {Circle, Img, Layout, Line, Rect, Txt} from '@revideo/2d';
import {Reference, createRef} from '@revideo/core';
import {ASTEROID_WARM_THEME as C} from './theme';
import {CINEMATIC_MONO as MONO} from './cinematic-sketch';

export type XiaolanRigPose = 'pointing' | 'thinking' | 'presenting';
export type XiaolanRigAction = 'idle-talk' | 'react-surprise' | 'point-emphasis' | 'think-focus' | 'explain-open' | 'resolve-wave';

type Anchor = {normalizedX: number; normalizedY: number};
type PoseSpec = {
  filename: string;
  intrinsic: {width: number; height: number};
  cut: number;
  eyes: [Anchor, Anchor];
  mouth: Anchor;
  gesture: Anchor;
};

const POSES: Record<XiaolanRigPose, PoseSpec> = {
  pointing: {
    filename: 'xiaolan-pointing.png', intrinsic: {width: 1367, height: 1151}, cut: 0.54,
    eyes: [{normalizedX: 0.446, normalizedY: 0.278}, {normalizedX: 0.556, normalizedY: 0.278}],
    mouth: {normalizedX: 0.498, normalizedY: 0.362}, gesture: {normalizedX: 0.864, normalizedY: 0.372},
  },
  thinking: {
    filename: 'xiaolan-thinking.png', intrinsic: {width: 1369, height: 1149}, cut: 0.55,
    eyes: [{normalizedX: 0.417, normalizedY: 0.24}, {normalizedX: 0.519, normalizedY: 0.24}],
    mouth: {normalizedX: 0.452, normalizedY: 0.379}, gesture: {normalizedX: 0.43, normalizedY: 0.3},
  },
  presenting: {
    filename: 'xiaolan-presenting.png', intrinsic: {width: 1448, height: 1086}, cut: 0.56,
    eyes: [{normalizedX: 0.479, normalizedY: 0.267}, {normalizedX: 0.573, normalizedY: 0.267}],
    mouth: {normalizedX: 0.528, normalizedY: 0.325}, gesture: {normalizedX: 0.18, normalizedY: 0.5},
  },
};

export type XiaolanRigRuntime = {
  root: Reference<Layout>;
  update: (progress: number, localSeconds: number, mouthOpen: number) => void;
};

export function addXiaolanRig(parent: Layout, options: {
  pose: XiaolanRigPose;
  action: XiaolanRigAction;
  width: number;
  x: number;
  y: number;
  accent: string;
  label?: string;
}): XiaolanRigRuntime {
  const spec = POSES[options.pose];
  const height = options.width * spec.intrinsic.height / spec.intrinsic.width;
  const upperHeight = height * spec.cut;
  const lowerHeight = height - upperHeight;
  const seamY = -height / 2 + upperHeight;
  const lowerCenterY = seamY + lowerHeight / 2;
  const root = createRef<Layout>();
  const torso = createRef<Layout>();
  const upper = createRef<Layout>();
  const mouth = createRef<Circle>();
  const eyelids = [createRef<Line>(), createRef<Line>()];
  const gaze = [createRef<Circle>(), createRef<Circle>()];
  const gesture = createRef<Circle>();
  const asset = `/qwen-ui-agent/characters/${spec.filename}`;
  const point = (anchor: Anchor): [number, number] => [(anchor.normalizedX - 0.5) * options.width, (anchor.normalizedY - 0.5) * height];
  const eyePoints = spec.eyes.map(point) as [[number, number], [number, number]];
  const mouthPoint = point(spec.mouth);
  const gesturePoint = point(spec.gesture);

  parent.add(
    <Layout ref={root} x={options.x} y={options.y} opacity={0} scale={0.92}>
      <Circle y={18} width={options.width * 0.78} height={options.width * 0.78} fill={`${options.accent}0D`} shadowColor={`${options.accent}22`} shadowBlur={46} />
      <Layout ref={torso}>
        <Rect y={lowerCenterY} width={options.width} height={lowerHeight + 2} clip>
          <Img src={asset} width={options.width} height={height} y={-lowerCenterY} />
        </Rect>
        <Layout ref={upper} y={seamY}>
          <Rect y={-upperHeight / 2} width={options.width} height={upperHeight + 2} clip>
            <Img src={asset} width={options.width} height={height} y={lowerHeight / 2} />
          </Rect>
          {eyePoints.map((eye, index) => {
            const localY = eye[1] - seamY;
            return <>
              <Line ref={eyelids[index]} x={eye[0]} y={localY} points={[[-11, 0], [11, 0]]} stroke={'#4B2934'} lineWidth={3.5} radius={8} opacity={0} />
              <Circle ref={gaze[index]} x={eye[0]} y={localY - 1} width={3.6} height={3.6} fill={'#FFF8EE'} opacity={0.72} />
            </>;
          })}
          <Circle ref={mouth} x={mouthPoint[0]} y={mouthPoint[1] - seamY + 1} width={23} height={2} fill={'#B85E73'} stroke={'#784052'} lineWidth={0.8} opacity={0.42} />
        </Layout>
      </Layout>
      <Circle ref={gesture} x={gesturePoint[0]} y={gesturePoint[1]} width={18} height={18} fill={`${options.accent}18`} stroke={options.accent} lineWidth={3} opacity={0} shadowColor={options.accent} shadowBlur={18} />
      <Rect y={height / 2 + 18} width={318} height={40} radius={20} fill={C.night} stroke={`${options.accent}88`} lineWidth={2}>
        <Txt fontFamily={MONO} fontSize={16} fontWeight={850} letterSpacing={1.2} fill={C.onDark} text={options.label ?? '小兰 · 主持人'} />
      </Rect>
    </Layout>,
  );

  return {
    root,
    update: (progress, localSeconds, mouthOpen) => {
      const breath = Math.sin(localSeconds * Math.PI * 0.72);
      const sway = Math.sin(localSeconds * Math.PI * 0.42);
      torso().scale.y(1 + breath * 0.008);
      torso().position.y(-breath * 1.8);
      let headRotation = sway * 0.65;
      let headY = -Math.abs(breath) * 1.2;
      if (options.action === 'react-surprise') {
        const recoil = Math.exp(-progress * 6) * Math.sin(progress * Math.PI * 4);
        headRotation += recoil * 2.6;
        headY -= Math.abs(recoil) * 5;
      } else if (options.action === 'point-emphasis') {
        headRotation += Math.sin(progress * Math.PI * 3) * 0.9;
      } else if (options.action === 'think-focus') {
        headRotation += 1.8 + sway * 0.45;
      } else if (options.action === 'explain-open') {
        headRotation -= 0.8 + sway * 0.65;
      } else if (options.action === 'resolve-wave') {
        headRotation += Math.sin(progress * Math.PI * 2) * 1.1;
      }
      upper().rotation(headRotation);
      upper().position.y(seamY + headY);

      const blinkCycle = localSeconds % 3.7;
      const blink = blinkCycle > 3.48 ? Math.sin(((blinkCycle - 3.48) / 0.22) * Math.PI) : 0;
      eyelids.forEach(line => line().opacity(blink * 0.92));
      const gazeX = options.action === 'think-focus' ? -2.2 : options.action === 'point-emphasis' ? 2.4 : sway * 1.2;
      gaze.forEach((dot, index) => {
        dot().position.x(eyePoints[index][0] + gazeX);
        dot().opacity(0.55 + mouthOpen * 0.25);
      });
      mouth().height(1.5 + mouthOpen * 6.5);
      mouth().width(22 + mouthOpen * 3);
      mouth().opacity((0.28 + mouthOpen * 0.48) * (options.pose === 'thinking' ? 0.45 : 1));

      const gestureStrength = options.action === 'point-emphasis' || options.action === 'explain-open' || options.action === 'resolve-wave'
        ? 0.5 + Math.sin(localSeconds * Math.PI * 1.8) * 0.5
        : 0;
      gesture().opacity(gestureStrength * 0.78);
      gesture().scale(0.72 + gestureStrength * 0.72);
      root().position.y(options.y + Math.sin(localSeconds * Math.PI * 0.32) * 2.4);
    },
  };
}
