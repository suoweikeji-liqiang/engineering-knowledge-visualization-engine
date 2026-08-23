# AI 大模型领域资产系统

命名空间：`domain.ai-models.*`

这套资产服务于“小行星 AI 观测站”的大模型科普内容。它使用品牌现有的深蓝观测站语言，
但用一套稳定的语义色区分大模型系统中的不同对象：

| 语义 | 颜色 | 用途 |
|---|---|---|
| 数据与 token 流 | 青色 `#1FD6E2` | 输入、token、数据流、观测结果 |
| 参数与模型内部 | 紫色 `#8B5CF6` | 注意力、Transformer、专家模型 |
| 算力与执行 | 蓝色 `#1F5CFF` | GPU、训练、推理执行 |
| 检索与外部工具 | 绿色 `#22C55E` | 向量库、RAG、工具调用 |
| 代价与待确认状态 | 琥珀色 `#F59E0B` | loss、上下文容量、策略检查 |
| 风险与阻断 | 珊瑚红 `#F04B2F` | 幻觉、越界、安全阻断 |

## 资产层级

```text
design/assets/domains/ai-models/
  backgrounds/model-observatory/   # 白天、夜间模型观测舱
  components/                       # 可组合的模型基本元件
  diagrams/                         # 可直接进入分镜的系统级图解
  manifest.json
```

### 核心元件

- `token`、`embedding-vector`：从语言到向量的表示过程。
- `neural-layer`、`attention-head`、`transformer-block`：模型内部结构。
- `model-core`：不绑定具体厂商或模型的通用模型主体。
- `gpu-cluster`、`dataset-stack`：训练和运行所需的算力、数据。
- `vector-database`、`tool-connector`：RAG 与 Agent 的外部能力。

### 教学图解

- `training-pipeline`：数据、前向计算、loss、反向传播和优化器。
- `inference-pipeline`：提示词、模型、KV cache 与逐 token 生成。
- `attention-map`：多头注意力强弱关系。
- `rag-pipeline`：问题、检索、上下文、可信回答和引用回路。
- `agent-loop`：规划、行动、工具、观察和继续推理。
- `moe-routing`：路由器选择少量专家并合并输出。
- `context-window`：上下文占用、窗口边界、溢出和压缩。
- `safety-gate`：输入检查、安全输出、阻断和审计。
- `evaluation-matrix`：不同能力维度、模型和阈值的对比。

## 运行时约定

SVG 内不写课程标题或厂商名称。可见文字、数值、模型名和讲解标签由渲染器注入。
每个可动画语义部分均有稳定的 SVG `id`，manifest 会把这些 id 暴露为 `layers`。

常用资产 ID：

```text
domain.ai-models.background.model-observatory.scene-night16x9
domain.ai-models.component.transformer-block
domain.ai-models.component.gpu-cluster
domain.ai-models.diagram.training-pipeline
domain.ai-models.diagram.rag-pipeline
domain.ai-models.diagram.agent-loop
domain.ai-models.diagram.safety-gate
```

动画建议：

- 数据流沿路径由左向右扫光，token 使用 80–140ms 的错峰出现。
- 注意力只强调少量高权重连线，避免所有连接同时闪烁。
- 训练循环使用琥珀色回程表现反向传播，与青色前向数据流区分。
- Agent 循环每轮只高亮当前阶段，并显示明确的停止条件。
- 安全图解必须同时保留“放行、阻断、审计”三条信息，不能只画盾牌。

重建与校验：

```bash
python scripts/generate_ai_model_assets.py
python scripts/generate_asset_manifest.py
python scripts/generate_ai_model_contact_sheet.py
sandiao validate-assets design/assets/domains/ai-models/manifest.json
```
