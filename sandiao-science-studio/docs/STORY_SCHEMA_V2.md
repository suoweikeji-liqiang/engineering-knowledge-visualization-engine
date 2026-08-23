# Story Schema v2

Story v2 是内容策划、视觉资产和渲染器之间的语义契约。它描述“镜头想表达什么、如何组织画面”，不保存 SVG 路径、PNG 文件名或 Pillow 坐标等渲染器实现细节。

## 版本规则

- 新文档必须在根节点声明 `"schemaVersion": "2.0"`。
- 未声明版本的文档视为旧版 `1.0`，加载时确定性迁移到 `2.0`。
- 当前只接受 `1.0` 和 `2.0`；未知版本会在渲染前失败，避免静默误读。
- `migrate_story_data(document)` 接收内存对象，返回深拷贝，不修改输入。
- `parse_story(document)` 提供不依赖 CLI 或文件系统的迁移加校验 API；`load_story(path)` 是文件入口。

旧版 `stories/ac-16c.json` 可继续直接加载。迁移只发生在内存中，不会覆盖作者文件。

## 最小结构

```json
{
  "schemaVersion": "2.0",
  "meta": {
    "title": "空调设定温度",
    "slug": "hvac-setpoint",
    "resolution": [1920, 1080],
    "fps": 24
  },
  "characters": [],
  "shots": []
}
```

`meta`、角色的基础字段以及镜头的 `id`、`duration` 延续 v1。镜头不得短于或等于 0.5 秒；坐标仍使用 0..1 的归一化画布。

## 角色与 renderer

角色的 `renderer` 是可选渲染提示。未提供时使用 `procedural`。

```json
{
  "id": "xiaoming",
  "name": "小明",
  "palette": {"accent": "#38D8E8"},
  "voice": {},
  "renderer": {
    "type": "svg-sprite",
    "variant": "default",
    "assetRef": {"id": "brand.character.xiaoming.pose.idle", "variant": "default"}
  }
}
```

支持的 renderer 类型是 `procedural`、`svg-sprite`、`png-pose-pack`。后两者必须提供 `assetRef`。Story 只引用稳定资产 ID，真实文件由 `design-assets.json` 解析。

## 动作和表情 cue

v2 将字符串改为对象，以便增加强度和参数，同时解析后的 `State.action` 与 `State.expression` 仍是字符串，兼容旧渲染器。

```json
{
  "character": "xiaoming",
  "x": 0.22,
  "y": 0.68,
  "scale": 1,
  "facing": 1,
  "action": {"id": "point", "intensity": 0.7, "parameters": {"hand": "right"}},
  "expression": {"id": "serious", "intensity": 0.8}
}
```

内置动作：`idle`、`talk`、`point`、`shock`、`think`、`nod`、`shake`、`celebrate`、`walk`、`run`、`angry`、`laugh`、`cry`、`sweat`、`whisper`。

内置表情：`neutral`、`happy`、`confident`、`serious`、`puzzled`、`shocked`、`angry`、`tired`、`laugh`、`cry`、`embarrassed`、`determined`、`smile`。

`intensity` 必须在 0..1。省略 action/expression 时分别使用 `idle`/`neutral`。未知 ID 会立即报错；新增 ID 应先进入版本化 registry，再供 Story 使用。

## Scene 契约

每个镜头可选 `scene`，下分背景、布局、镜头和资产引用：

```json
{
  "scene": {
    "id": "scene.living-room",
    "background": {
      "id": "background.living-room",
      "variant": "day",
      "mood": "playful",
      "assetRef": {"id": "shared.background.daily-living.scene16x9", "variant": "landscape"}
    },
    "layout": {
      "preset": "dialogue-diagram",
      "focus": "diagram",
      "safeArea": [0.05, 0.05, 0.15, 0.05],
      "zones": {
        "character-left": [0.05, 0.10, 0.30, 0.70],
        "diagram": [0.40, 0.10, 0.55, 0.65]
      }
    },
    "camera": {
      "framing": "medium-wide",
      "movement": "push-in",
      "target": "diagram",
      "intensity": 0.25
    },
    "assetRefs": [
      {"id": "prop.thermometer", "role": "prop", "variant": "cold"}
    ]
  }
}
```

### Background

`background.id` 表达场景语义，`variant` 和 `mood` 用于选择色彩或氛围。`assetRef` 可选；没有资产引用时 renderer 可以程序化生成或按 ID 选择默认实现。

### Layout

`preset` 是稳定布局 ID。`safeArea` 顺序为 `[top, right, bottom, left]`，`zones` 的矩形为 `[x, y, width, height]`；所有值均归一化到 0..1，矩形不得越界。横竖屏 renderer 可以按同一个 preset 重排，不能把这些值当成像素坐标。

### Camera

景别支持 `extreme-wide`、`wide`、`medium-wide`、`medium`、`medium-close`、`close-up`、`extreme-close-up`。运动支持 `static`、`push-in`、`pull-out`、`pan`、`follow`、`cut`。`target` 是语义目标，`intensity` 为 0..1。

### AssetRef

资产引用包含稳定 `id`，并可带 `variant`、`role` 和 renderer-neutral 的 `parameters`。同一 scene 中不允许重复资产 ID。路径、锚点、层级和能力由资产 manifest 管理，不进入 Story。

## v1 → v2 迁移

迁移器执行以下固定转换：

1. 写入 `schemaVersion: "2.0"`。
2. 未声明 renderer 的角色获得 `{"type": "procedural"}`。
3. 每个旧镜头获得 `scene.default`、`background.default`、`legacy-normalized` 布局和静止 wide camera。
4. `action: "talk"` 转为 `action: {"id": "talk"}`。
5. `expression: "neutral"` 转为 `expression: {"id": "neutral"}`；缺省值同样被显式写入。

迁移不会推测具体设计资产或把旧 `diagram` 字符串伪装成文件引用。`diagram`、`headline`、`effect` 等 v1 字段在兼容期保留，后续应由有版本的图解 registry 单独演进。

## 校验边界

Story 层验证结构、语义 ID、引用关系、坐标、布局边界、cue、camera 与 renderer 能力前置条件。资产是否存在、锚点是否齐全以及某角色是否实现某动作，应由设计资产 manifest lint 在下一层验证。
