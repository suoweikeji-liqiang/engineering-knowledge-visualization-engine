import {Circle, Img, Layout, Line, Rect, Txt, View2D} from '@revideo/2d';
import {Reference, all, createRef, easeInOutCubic} from '@revideo/core';
import {ASTEROID_WARM_THEME as C} from './theme';

export const CINEMATIC_FONT = 'PingFang SC, Noto Sans CJK SC, Microsoft YaHei, sans-serif';
export const CINEMATIC_MONO = 'JetBrains Mono, SFMono-Regular, Menlo, monospace';

export type CinematicStage = {
  root: Reference<Layout>;
  body: Reference<Layout>;
};

export function makeCinematicStage(
  view: View2D,
  number: string,
  headline: string,
  caption: string,
  accent: string = C.red,
): CinematicStage {
  const root = createRef<Layout>();
  const body = createRef<Layout>();
  const markerWidth = Math.min(1100, Math.max(280, headline.length * 54));
  view.add(
    <Layout ref={root} size={[1920, 1080]} opacity={0} scale={0.985}>
      <Layout position={[-760, -430]} layout direction={'row'} gap={20} alignItems={'center'}>
        <Rect width={50} height={8} radius={4} fill={accent} />
        <Txt fontFamily={CINEMATIC_MONO} fontSize={24} fontWeight={700} letterSpacing={3} fill={accent} text={`OBSERVATION ${number}`} />
      </Layout>
      <Rect position={[-760 + markerWidth / 2, -326]} width={markerWidth} height={20} radius={8} fill={`${accent}22`} rotation={-0.45} />
      <Txt position={[0, -365]} width={1520} textAlign={'left'} fontFamily={CINEMATIC_FONT} fontSize={56} fontWeight={700} fill={C.primary} text={headline} />
      <Layout ref={body} position={[0, 35]} size={[1640, 650]} />
      <Layout position={[0, 430]}>
        <Rect x={7} y={7} width={1638} height={110} radius={[21, 27, 23, 25]} fill={'#E7DACA'} rotation={0.25} />
        <Rect width={1640} height={112} radius={[24, 20, 26, 22]} fill={'#FFF9F0F2'} stroke={C.line} lineWidth={2} shadowColor={'#6D594022'} shadowBlur={24}>
          <Txt width={1500} fontFamily={CINEMATIC_FONT} fontSize={36} fontWeight={600} lineHeight={52} textAlign={'center'} fill={C.primary} text={caption} />
        </Rect>
        <Rect x={-710} y={-57} width={112} height={24} radius={4} fill={`${C.tape}A8`} rotation={-2.5} />
        <Rect x={710} y={-57} width={112} height={24} radius={4} fill={`${accent}42`} rotation={2.5} />
      </Layout>
    </Layout>,
  );
  return {root, body};
}

export function* enterCinematicStage(stage: Reference<Layout>, direction = 1) {
  stage().position.x(38 * direction);
  stage().rotation(0.35 * direction);
  yield* all(
    stage().opacity(1, 0.35),
    stage().scale(1, 0.5, easeInOutCubic),
    stage().position.x(0, 0.5, easeInOutCubic),
    stage().rotation(0, 0.5, easeInOutCubic),
  );
}

export function* exitCinematicStage(stage: Reference<Layout>, direction = 1) {
  yield* all(
    stage().opacity(0, 0.3),
    stage().scale(1.01, 0.3),
    stage().position.x(-26 * direction, 0.3, easeInOutCubic),
    stage().rotation(-0.2 * direction, 0.3),
  );
  stage().remove();
}

export function cinematicNodeCard(label: string, detail: string, color: string, x: number, y: number, width = 270) {
  const rotation = x === 0 ? -0.35 : x < 0 ? -0.7 : 0.65;
  return (
    <Layout position={[x, y]} rotation={rotation}>
      <Rect x={6} y={7} width={width} height={146} radius={[20, 26, 18, 25]} fill={'#E5D8C8'} rotation={0.8} />
      <Rect width={width} height={146} radius={[24, 19, 26, 21]} fill={C.panel} stroke={color} lineWidth={3} shadowColor={`${color}38`} shadowBlur={18}>
        <Circle position={[-width / 2 + 34, -38]} width={12} height={12} fill={color} />
        <Txt position={[8, -30]} width={width - 64} textAlign={'left'} fontFamily={CINEMATIC_MONO} fontSize={28} fontWeight={700} fill={C.primary} text={label} />
        <Txt position={[0, 30]} width={width - 44} textAlign={'center'} fontFamily={CINEMATIC_FONT} fontSize={23} fill={C.soft} text={detail} />
      </Rect>
      <Rect x={width / 2 - 42} y={-73} width={66} height={18} radius={3} fill={`${color}36`} rotation={4} />
    </Layout>
  );
}

export function cinematicConnector(points: [number, number][], color: string = C.line) {
  return (
    <Layout>
      <Line points={points.map(([x, y]) => [x + 2, y + 3] as [number, number])} stroke={`${color}28`} lineWidth={9} radius={18} />
      <Line points={points} stroke={color} lineWidth={4} endArrow arrowSize={14} radius={18} />
    </Layout>
  );
}

export function cinematicHandNote(text: string, color: string, x: number, y: number, rotation = -2) {
  const width = Math.max(220, text.length * 30);
  return (
    <Layout position={[x, y]} rotation={rotation}>
      <Rect width={width} height={44} radius={12} fill={`${color}28`} />
      <Line points={[[-width / 2 + 8, 17], [width / 2 - 6, 13]]} stroke={`${color}88`} lineWidth={8} radius={8} />
      <Txt y={-4} width={width - 20} fontFamily={'Kaiti SC, STKaiti, KaiTi, serif'} fontSize={25} fontWeight={700} fill={C.primary} text={text} />
    </Layout>
  );
}

export function cinematicCharacterFrame(src: string, label: string, width: number, x: number, y: number, rotation = -2) {
  const height = width * 0.558;
  return (
    <Layout position={[x, y]} rotation={rotation}>
      <Rect width={width + 34} height={height + 72} radius={26} fill={C.paper} shadowColor={'#00000088'} shadowBlur={36} shadowOffset={[0, 16]}>
        <Img y={-18} src={src} width={width} height={height} radius={18} />
        <Txt y={height / 2 + 17} width={width - 20} textAlign={'left'} fontFamily={CINEMATIC_FONT} fontSize={22} fontWeight={700} fill={C.ink} text={label} />
      </Rect>
      <Rect y={-height / 2 - 40} width={132} height={34} radius={6} fill={`${C.tape}DD`} rotation={3} />
    </Layout>
  );
}
