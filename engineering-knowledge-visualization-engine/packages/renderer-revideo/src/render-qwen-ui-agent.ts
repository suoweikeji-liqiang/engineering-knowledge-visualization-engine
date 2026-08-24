import {existsSync} from 'node:fs';
import {renderVideo} from '@revideo/renderer';

const executablePath = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium']
  .filter((value): value is string => Boolean(value))
  .find(existsSync);
if (!executablePath) throw new Error('Chrome/Chromium not found.');

const range = process.env.RENDER_RANGE?.split(':').map(Number) as [number, number] | undefined;
if (range && (range.length !== 2 || range.some(value => !Number.isFinite(value)) || range[1] <= range[0])) throw new Error('RENDER_RANGE must use start:end seconds.');

const file = await renderVideo({
  projectFile: './src/qwen-ui-agent-project.tsx',
  settings: {
    outFile: (process.env.RENDER_OUT || (range ? 'qwen-ui-agent-hosted-proof.mp4' : 'qwen-ui-agent-hosted.mp4')) as `${string}.mp4`,
    outDir: '../../examples/qwen-ui-agent-hosted/final',
    workers: 1,
    logProgress: true,
    projectSettings: range ? {range} : undefined,
    ffmpeg: {ffmpegPath: process.env.FFMPEG_PATH || 'ffmpeg', ffprobePath: process.env.FFPROBE_PATH || 'ffprobe', ffmpegLogLevel: 'error'},
    puppeteer: {executablePath},
  },
});
console.log(`Rendered Qwen UI Agent hosted film to ${file}`);
