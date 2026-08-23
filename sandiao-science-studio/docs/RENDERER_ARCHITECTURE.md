# 渲染器组件架构

## 目标

渲染层把 Story 解析后的语义描述交给可替换组件，而不让 Story 契约依赖
Pillow、SVG、Motion Canvas 或其他具体实现。接口骨架现已接入 `DesignStudio`；
未传 `--assets` 时仍使用旧 `Studio`，因此旧 Story 保持兼容。

组件分为四类：

- `CharacterRenderer`：人物姿态、表情与动作；
- `BackgroundRenderer`：环境、布景与氛围；
- `DiagramRenderer`：流程、关系、数据等通用图解；
- `SubtitleRenderer`：字幕排版与呈现。

四类组件采用同一调用形状：

```python
result = renderer.render(context, layer, semantic_spec)
```

`semantic_spec` 是只读约定下的通用映射。具体 spec schema 应由后续 Story v2 或
资产契约定义；接口层不包含 HVAC 名称、角色名称或单条样片逻辑。

## 核心对象

| 对象 | 职责 |
| --- | --- |
| `RenderContext` | 一帧共享的尺寸、时间、帧号、随机种子、语言和后端 surface |
| `Bounds` | 图层在当前坐标系中的矩形范围 |
| `Anchors` | 用于人物、道具、标注互相吸附的命名坐标 |
| `Layer` | bounds、层级、透明度、锚点和少量编排元数据 |
| `RenderResult` | 组件实际覆盖范围、锚点、后端 payload、警告和诊断元数据 |

这些对象使用不可变 dataclass；传入的映射会做浅复制并转为只读映射，避免一个
组件意外修改另一个组件的上下文。

## 后端边界

接口没有导入 Pillow。`RenderContext.surface` 与 `RenderResult.payload` 均是后端
不透明对象：

- Pillow 实现可以把 `Image.Image` 或 `ImageDraw.ImageDraw` 作为 surface；
- SVG 实现可以传入文档构建器并返回节点；
- 命令式视频后端可以返回可延迟执行的 command buffer；
- 测试实现可以只返回确定性的值对象，不创建图片。

因此替换后端不要求修改 Story JSON，也不要求让语义 schema 携带绘图库参数。

## 注册与解析

每一类组件应拥有独立的 `RendererRegistry`，避免不同类别碰巧使用相同 id 时互相
覆盖。组件 id 建议使用稳定的命名空间，例如 `brand.character.vector-v1`。

```python
characters = RendererRegistry[CharacterRenderer]()
characters.register_component(character_renderer)
renderer = characters.resolve("brand.character.vector-v1")
```

重复注册抛出 `DuplicateRendererError`；解析未知 id 抛出
`UnknownRendererError`，错误文本同时列出当前已注册 id。注册表不做静默覆盖或
默认回退，避免错误配置悄悄改变视频视觉。

## 确定性要求

相同的 context、layer、spec 与资产版本必须生成相同结果。需要随机效果时，只能
使用 `RenderContext.seed` 派生本地随机数，不能读取全局随机状态或当前系统时间。
`testing.ProceduralTestRenderer` 展示了不依赖图形库的最小确定性实现；
`NoopRenderer` 可用于尚未交付资产时保持管线可运行。

## 当前 SVG 实现

`SvgAssetRenderer` 读取已经过 `load_asset_source` 严格校验和 catalog 组合的资产，用统一
`RenderContext + Layer + spec` 调用完成等比缩放、cover/contain/stretch、水平镜像、
透明度合成和锚点坐标换算。生产环境使用 CairoSVG；macOS 开发环境在尚未安装依赖
时可回退到系统 `sips`，但 CI 与部署必须安装项目依赖。

`DesignStudio` 使用同一个 SVG renderer 组合背景、角色和工程道具，并由
`LayoutEngine` 分配不重叠区域。CLI 通过 `--assets` 显式启用，不做静默切换：

```bash
sandiao render stories/ac-16c.json \
  --assets design/manifests/design-assets.json \
  --duration 10 \
  --output output/ac-16c-observatory-voice-v2-10s.mp4
```

## 后续接入顺序

1. 把当前 AC-16C 的图解编排进一步拆成通用 `DiagramRenderer` spec。
2. 让 Story v2 的显式 `assetRef` 覆盖当前兼容映射。
3. 增加 16:9 与 9:16 单帧 golden 和视频节奏回归。
4. 接入新的命令式视频后端时复用相同 `RenderContext` 与 manifest。

不要从具体后端反向修改 Story schema；Story 迁移必须继续版本化并保留旧样例兼容。
