import {readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';

const root = resolve(import.meta.dirname, '..');
const example = resolve(root, 'examples/ai-agent-harness-complete');
const story = JSON.parse(await readFile(resolve(example, 'storyboard/story.json'), 'utf8'));
const timeline = JSON.parse(await readFile(resolve(example, 'audio/video.timeline.json'), 'utf8'));
const captions = JSON.parse(await readFile(resolve(example, 'audio/captions.timeline.json'), 'utf8'));

let cursor = 0;
const events = timeline.shots.map((timing, index) => {
  const shot = story.shots.find(item => item.id === timing.id);
  if (!shot) throw new Error(`Unknown timed shot: ${timing.id}`);
  const start = cursor;
  cursor += timing.duration;
  return {
    sequence: index + 1,
    id: shot.id,
    headline: shot.headline,
    visualKind: shot.visual.kind,
    start: Number(start.toFixed(3)),
    end: Number(cursor.toFixed(3)),
    duration: timing.duration,
    citations: shot.citations,
    semanticEvents: shot.visual.events ?? shot.visual.status ?? shot.visual.nodes ?? shot.visual.layers ?? [],
    captionCueIds: captions.cues.map((cue, cueIndex) => cue.shotId === shot.id ? cueIndex + 1 : null).filter(Boolean),
  };
});

const trace = {
  schemaVersion: '1.0',
  traceKind: 'production-narrative',
  runId: `production-narrative-${timeline.storyFingerprint.slice(0, 12)}`,
  objective: 'Produce a sourced, narrated, animated explanation of AI Agent and Harness.',
  status: 'complete',
  stopReason: 'frozen-story-artifacts-generated',
  evidenceBoundary: 'Generated from the frozen storyboard and media timeline. This is not raw model/tool telemetry.',
  productionTelemetryStillRequired: ['model request/response ids', 'tool call ids and arguments', 'tool results', 'state diffs', 'approval records', 'retry records', 'checkpoint and artifact hashes'],
  duration: timeline.duration,
  artifacts: [
    'ai-agent-harness-complete.mp4', 'subtitles.srt', 'chapters.json',
    '../sources/citations.json', '../evaluation/asr-report.json',
    '../evaluation/technical-qa.json', 'trace.json', 'trace-viewer.html'
  ],
  events,
};

const encoded = JSON.stringify(trace).replaceAll('<', '\\u003c');
const html = `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Production Narrative Trace</title>
<style>body{margin:0;background:#f4ecdf;color:#292333;font:16px system-ui;padding:32px}h1{margin:0 0 8px}.meta{color:#766b64;margin-bottom:24px}.grid{display:grid;gap:10px}.event{background:#fffaf2;border:1px solid #d8ccbd;border-left:5px solid #2c8e92;border-radius:12px;padding:14px 18px;cursor:pointer}.event.open{border-left-color:#d85562}.head{display:flex;gap:16px;align-items:center}.time{font:13px ui-monospace;color:#765d91}.detail{display:none;margin-top:12px;white-space:pre-wrap;font:13px ui-monospace}.open .detail{display:block}</style>
<h1>AI Agent 与 Harness · Production Narrative Trace</h1><div class="meta">由冻结分镜与媒体时间线生成；不是原始模型/工具遥测。</div><div class="meta" id="meta"></div><div class="grid" id="grid"></div>
<script>const trace=${encoded};const f=s=>{const m=Math.floor(s/60),x=(s%60).toFixed(1);return String(m).padStart(2,'0')+':'+String(x).padStart(4,'0')};document.querySelector('#meta').textContent=trace.status.toUpperCase()+' · '+trace.events.length+' events · '+f(trace.duration);document.querySelector('#grid').innerHTML=trace.events.map(e=>'<article class="event"><div class="head"><b>'+String(e.sequence).padStart(2,'0')+' · '+e.headline+'</b><span class="time">'+f(e.start)+' → '+f(e.end)+'</span></div><div class="detail">'+JSON.stringify(e,null,2)+'</div></article>').join('');document.querySelectorAll('.event').forEach(x=>x.onclick=()=>x.classList.toggle('open'));</script></html>`;

await writeFile(resolve(example, 'final/trace.json'), `${JSON.stringify(trace, null, 2)}\n`, 'utf8');
await writeFile(resolve(example, 'final/trace-viewer.html'), `${html}\n`, 'utf8');
console.log(JSON.stringify({runId: trace.runId, events: events.length, status: trace.status}, null, 2));
