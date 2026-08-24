# 资产领域结构

资产采用“领域边界优先、媒介类型其次”的目录与 ID 结构。不要在 `design/assets/`
下重新创建全局 `characters/`、`backgrounds/`、`props/` 或 `diagrams/`。

```text
design/
  assets/
    brand/                         # 小行星 AI 观测站品牌资产
      manifest.json                # namespace: brand.*
      characters/                  # 老王、小明及后续常驻角色
      backgrounds/                 # 观测站、抽象舞台、总结舞台
    shared/                        # 跨领域可复用资产
      manifest.json                # namespace: shared.*
      backgrounds/                 # 日常生活等中性场景
      diagrams/                    # 对比卡、流程节点、折线图、提示卡
      symbols/                     # 水、气流、电、警告、时钟等科学符号
    domains/
      hvac/                        # HVAC 领域包
        manifest.json              # namespace: domain.hvac.*
        backgrounds/               # 机房等 HVAC 场景
        props/                     # 压缩机、换热器、风机、阀门、传感器
      ai-models/                   # AI 大模型领域包
        manifest.json              # namespace: domain.ai-models.*
        backgrounds/               # 模型观测舱
        components/                # token、Transformer、GPU、向量库等
        diagrams/                  # 训练、推理、RAG、Agent、安全与评测
  manifests/
    design-assets.json             # 只组合上述包，不直接声明资产
```

## 边界规则

- `brand` 只保存栏目身份和常驻角色。它不能依赖 HVAC 名称或设备。
- `shared` 只保存跨领域成立的表达组件。通用图解不得硬编码某一期文案。
- `domains/<domain>` 保存领域设备、领域场景和领域视觉惯例。新增电气、控制等领域时，
  创建新的包与命名空间，例如 `domain.electrical.*`，不能塞进 HVAC。
- 故事与分镜是资产消费者，不属于运行时资产包；示例仍保存在 `design/storyboards/`。

## ID 示例

```text
brand.character.xiaoming.pose.point
brand.background.science-lab.scene-night16x9
shared.diagram.line-chart
shared.symbol.electricity
domain.hvac.prop.compressor
domain.hvac.background.plant-room.scene-night16x9
domain.ai-models.component.transformer-block
domain.ai-models.diagram.rag-pipeline
```

catalog 会检查每个包内的 ID 必须属于声明的 namespace，并拒绝跨包 ID、重复 ID、
越界路径和无效 SVG。各包也可以单独校验：

```bash
sandiao validate-assets design/assets/brand/manifest.json
sandiao validate-assets design/assets/shared/manifest.json
sandiao validate-assets design/assets/domains/hvac/manifest.json
sandiao validate-assets design/assets/domains/ai-models/manifest.json
sandiao validate-assets design/manifests/design-assets.json
```

生成或移动资产后运行 `python scripts/generate_asset_manifest.py`，它会重建所有包的
manifest 和顶层 catalog。
