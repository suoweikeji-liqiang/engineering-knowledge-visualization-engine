import {Audio, Circle, Grid, Layout, Line, Rect, Txt, View2D, makeScene2D} from '@revideo/2d';
import {createRef, easeInOutCubic, makeProject, tween} from '@revideo/core';
import {ASTEROID_WARM_THEME as C} from './theme';
import {CINEMATIC_FONT as FONT, CINEMATIC_MONO as MONO} from './cinematic-sketch';
import {addXiaolanRigV2} from './xiaolan-rig-v2';

const scene = makeScene2D('xiaolan-rig-v2-proof', function* (view: View2D) {
  const actorStage = createRef<Layout>();
  const cards = ['收到通知', '理解影响', '准备方案', '等待确认'].map(() => createRef<Rect>());
  const links = cards.slice(1).map(() => createRef<Line>());
  view.fill(C.bg);
  view.add(
    <>
      <Grid size={[2100, 1260]} spacing={64} stroke={'#D8CCBD'} lineWidth={1} opacity={0.62} />
      <Circle x={-850} y={-450} width={560} height={560} fill={'#D8556210'} />
      <Line points={[[-820, -490], [820, -490]]} stroke={C.red} lineWidth={4} />
      <Txt x={-610} y={-400} width={560} fontFamily={FONT} fontSize={54} fontWeight={880} textAlign={'left'} fill={C.primary} text={'小兰角色动画 V2'} />
      <Txt x={-600} y={-342} width={590} fontFamily={MONO} fontSize={18} fontWeight={820} textAlign={'left'} letterSpacing={1.6} fill={C.purple} text={'REAL JOINTS · FACE SPRITES · ACTION STATE'} />
      <Layout ref={actorStage} />
      {links.map((link, index) => <Line ref={link} points={[[-120 + index * 270, 42], [10 + index * 270, 42]]} stroke={index === 2 ? C.red : C.cyan} lineWidth={5} endArrow arrowSize={16} end={0} />)}
      {cards.map((card, index) => (
        <Rect ref={card} x={-190 + index * 270} y={42} width={220} height={150} radius={28} fill={index === 3 ? '#FFF0F1' : '#FFF9F0'} stroke={index === 3 ? C.red : C.line} lineWidth={index === 3 ? 4 : 2} opacity={0}>
          <Txt y={-38} fontFamily={MONO} fontSize={16} fontWeight={900} fill={[C.red, C.cyan, C.purple, C.yellow][index]} text={String(index + 1).padStart(2, '0')} />
          <Txt y={14} width={180} fontFamily={FONT} fontSize={28} fontWeight={820} fill={C.primary} text={['收到通知', '理解影响', '准备方案', '等待确认'][index]} />
        </Rect>
      ))}
      <Rect x={360} y={262} width={850} height={70} radius={35} fill={C.night}>
        <Txt fontFamily={FONT} fontSize={26} fontWeight={760} fill={C.onDark} text={'转头 → 抬臂 → 屈肘 → 手指落到确认节点'} />
      </Rect>
      <Audio src={'/qwen-ui-agent/qwen-ui-agent-hosted.mp3'} play volume={0.001} />
    </>,
  );

  const rig = addXiaolanRigV2(actorStage(), {action: 'point-emphasis', width: 620, x: -570, y: 70, accent: C.purple, label: '小兰 · 真关节指向动作'});
  yield* tween(12, value => {
    const entrance = easeInOutCubic(Math.min(1, value / 0.12));
    rig.root().opacity(entrance);
    rig.root().scale(0.92 + entrance * 0.08);
    const seconds = value * 12;
    const syllable = Math.max(0, Math.sin(seconds * 8.4) * 0.58 + Math.sin(seconds * 13.7) * 0.32);
    const pause = seconds % 3.1 > 2.48 ? 0 : 1;
    rig.update(value, seconds, syllable * pause);
    cards.forEach((card, index) => {
      const reveal = easeInOutCubic(Math.max(0, Math.min(1, (value - 0.12 - index * 0.11) / 0.1)));
      card().opacity(reveal);
      card().scale(0.84 + reveal * 0.16);
      if (index > 0) links[index - 1]().end(easeInOutCubic(Math.max(0, Math.min(1, (value - 0.18 - index * 0.11) / 0.09))));
    });
  });
});

export default makeProject({
  scenes: [scene],
  settings: {shared: {size: {x: 1920, y: 1080}}, rendering: {fps: 30}, preview: {fps: 30}},
});
