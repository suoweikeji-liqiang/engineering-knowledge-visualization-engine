import {existsSync} from 'node:fs';
import {renderVideo} from '@revideo/renderer';

const executablePath = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium']
  .filter((value): value is string => Boolean(value))
  .find(existsSync);
if (!executablePath) throw new Error('Chrome/Chromium not found.');

const file = await renderVideo({
  projectFile: './src/xiaolan-v2-proof-project.tsx',
  settings: {
    outFile: 'xiaolan-rig-v2-proof.mp4',
    outDir: '../../examples/qwen-ui-agent-hosted/final',
    workers: 1,
    logProgress: true,
    ffmpeg: {ffmpegPath: process.env.FFMPEG_PATH || 'ffmpeg', ffprobePath: process.env.FFPROBE_PATH || 'ffprobe', ffmpegLogLevel: 'error'},
    puppeteer: {executablePath},
  },
});
console.log(`Rendered Xiaolan V2 proof to ${file}`);
