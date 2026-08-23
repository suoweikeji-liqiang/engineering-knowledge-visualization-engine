import {existsSync} from 'node:fs';
import {renderVideo} from '@revideo/renderer';

async function renderBenchmark() {
  const chromeCandidates = [
    process.env.CHROME_PATH,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
  ].filter((value): value is string => Boolean(value));
  const executablePath = chromeCandidates.find(existsSync);
  if (!executablePath) {
    throw new Error('Chrome/Chromium not found. Set CHROME_PATH to its executable.');
  }
  const ffmpegPath = process.env.FFMPEG_PATH || 'ffmpeg';
  const ffprobePath = process.env.FFPROBE_PATH || 'ffprobe';

  console.log('Rendering AI Agent Harness benchmark...');
  const file = await renderVideo({
    projectFile: './src/project.tsx',
    settings: {
      outFile: 'ai-agent-harness-benchmark.mp4',
      outDir: '../../examples/ai-agent-harness-benchmark/final',
      workers: 1,
      logProgress: true,
      ffmpeg: {
        ffmpegPath,
        ffprobePath,
        ffmpegLogLevel: 'error',
      },
      puppeteer: {
        executablePath,
      },
    },
  });
  console.log(`Rendered benchmark to ${file}`);
}

renderBenchmark().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
