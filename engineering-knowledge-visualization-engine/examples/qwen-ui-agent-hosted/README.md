# Qwen UI Agent · 小兰主持人叙事样片

这是 `xiaolan-hosted-case-study-v1` 的首个验证片。它不替换现有 `ai-agent-harness-complete`，而是验证一条新的长期积累方向：固定主持人、连续现实案例、官方演示、一手证据和动态图解共同推进叙事。

## 对比目标

- 小兰有效出场镜头占比 45%–65%，每次出场承担明确叙事动作。
- 官方真实演示占成片时长至少 25%。
- 每 5 秒内至少发生一次有意义的画面状态变化。
- 至少使用两份可追溯的一手证据。
- 开场的“航班取消”必须在结尾得到结果回收。

## 生成

```bash
pnpm qwen-ui-agent:audio
pnpm qwen-ui-agent:render
pnpm qwen-ui-agent:qa
```

官方演示视频和技术报告在 prepare 阶段按 `sources/citations.json` 下载并校验 SHA-256；大体积源视频与渲染结果不提交 Git。
