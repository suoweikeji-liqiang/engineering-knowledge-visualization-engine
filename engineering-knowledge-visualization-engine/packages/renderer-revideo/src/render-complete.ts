import {existsSync} from 'node:fs';
import {renderVideo} from '@revideo/renderer';

async function renderComplete() {
  const chromeCandidates = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium'].filter((value): value is string => Boolean(value));
  const executablePath = chromeCandidates.find(existsSync);
  if (!executablePath) throw new Error('Chrome/Chromium not found. Set CHROME_PATH to its executable.');
  const range = process.env.RENDER_RANGE
    ?.split(':')
    .map(value => Number(value.trim())) as [number, number] | undefined;
  if (range && (range.length !== 2 || range.some(value => !Number.isFinite(value)) || range[1] <= range[0])) {
    throw new Error('RENDER_RANGE must use start:end seconds, for example 0:30.');
  }
  const outFile = process.env.RENDER_OUT || (range ? 'ai-agent-harness-complete-proof.mp4' : 'ai-agent-harness-complete.mp4');
  console.log(`Rendering AI Agent Harness ${range ? `proof ${range[0]}s–${range[1]}s` : 'complete film'}...`);
  const file = await renderVideo({
    projectFile: './src/complete-project.tsx',
    settings: {
      outFile: outFile as `${string}.mp4`,
      outDir: '../../examples/ai-agent-harness-complete/final',
      workers: 1,
      logProgress: true,
      projectSettings: range ? {range} : undefined,
      ffmpeg: {ffmpegPath: process.env.FFMPEG_PATH || 'ffmpeg', ffprobePath: process.env.FFPROBE_PATH || 'ffprobe', ffmpegLogLevel: 'error'},
      puppeteer: {executablePath},
    },
  });
  console.log(`Rendered complete benchmark to ${file}`);
}

renderComplete().catch(error => {console.error(error); process.exitCode = 1;});
