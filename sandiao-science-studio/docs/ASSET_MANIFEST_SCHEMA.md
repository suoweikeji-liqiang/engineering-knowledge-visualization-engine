# 设计资产 Manifest v1

## 目的

`design/manifests/design-assets.json` 是视觉设计资产与确定性渲染引擎之间的稳定契约。它记录资产的身份、路径、坐标系、锚点、变体、能力和可寻址图层；不保存对白、镜头内容或渲染器私有参数。

当前 schema 版本为 `1.0`。新增或改变字段语义时必须升级版本并提供迁移说明，不能静默改变 v1。

## 完整示例

```json
{
  "schemaVersion": "1.0",
  "assets": [
    {
      "id": "brand.character.xiaoming.pose.point",
      "type": "character-pose",
      "source": "characters/xiaoming/poses/point.svg",
      "viewBox": [0, 0, 512, 768],
      "anchors": {
        "feet": [256, 744],
        "mouth": [256, 180],
        "leftHand": [120, 410],
        "rightHand": [392, 410]
      },
      "variants": ["default"],
      "capabilities": ["lipSync", "lookAt", "propAttach"],
      "layers": [
        "root",
        "head",
        "mouth",
        "arm_left",
        "arm_right",
        "hand_left",
        "hand_right"
      ]
    }
  ]
}
```

每个资产包把 `manifest.json` 放在包根目录，`source` 相对该包解析。例如品牌包中的
上述文件位于 `design/assets/brand/characters/xiaoming/poses/point.svg`。顶层
`design/manifests/design-assets.json` 是 catalog，只组合品牌、共享和领域 manifest。
完整边界见 `docs/ASSET_DOMAIN_STRUCTURE.md`。

catalog 格式：

```json
{
  "schemaVersion": "1.0",
  "manifests": [
    {"namespace": "brand", "source": "assets/brand/manifest.json"},
    {"namespace": "shared", "source": "assets/shared/manifest.json"},
    {"namespace": "domain.hvac", "source": "assets/domains/hvac/manifest.json"},
    {"namespace": "domain.ai-models", "source": "assets/domains/ai-models/manifest.json"}
  ]
}
```

catalog 会强制每个资产 ID 以对应 namespace 开头。

## 字段

根对象只允许以下字段：

| 字段 | 必填 | 语义 |
| --- | --- | --- |
| `schemaVersion` | 是 | 必须严格等于字符串 `"1.0"` |
| `assets` | 是 | 资产对象数组，可以为空 |

每个资产对象支持：

| 字段 | 必填 | 语义 |
| --- | --- | --- |
| `id` | 是 | 全局唯一稳定 ID；必须带包 namespace，如 `domain.hvac.prop.valve` |
| `type` | 是 | 小写 kebab-case 类型，如 `character-pose`、`background`、`diagram-node`、`prop` |
| `source` | 是 | 资产根目录内以 `/` 分隔的规范化相对路径 |
| `viewBox` | 是 | `[minX, minY, width, height]`，四项均为有限数，宽高必须为正数 |
| `anchors` | 否 | 名称到 `[x, y]` 的映射；坐标使用 `viewBox` 坐标系且必须落在范围内，默认为 `{}` |
| `variants` | 否 | 该资产可选择的视觉变体名，默认为 `[]` |
| `capabilities` | 否 | 引擎可以依赖的功能声明，默认为 `[]` |
| `layers` | 否 | SVG 内可被程序寻址的元素 ID，默认为 `[]` |

`variants`、`capabilities` 和 `layers` 内名称不得重复。它们使用字母开头，可包含字母、数字、`_`、`-`。字段未知或拼错会直接报错，避免设计交付被引擎静默忽略。

### 推荐锚点

- 角色：`feet`、`center`、`head`、`mouth`、`leftHand`、`rightHand`、`lookAt`、`propAnchor`。
- 道具：`center`、`label`、`inlet`、`outlet`、`attach`。
- 图解节点：`center`、`label`、`input`、`output`。

锚点名字是契约。相同语义应跨角色和资产复用同一名字；不要用 `point1`、`temp` 等仅对单个文件有意义的名字。

### 推荐能力

- `lipSync`：允许替换或切换嘴型。
- `lookAt`：支持视线目标。
- `propAttach`：支持在手部或指定锚点挂载道具。
- `tintable`：允许通过主题色着色。
- `stateful`：具有正常、警告、成功等状态。
- `tileable`：可重复铺设。

能力声明不是自由描述文字。引擎尚不认识的能力可以保留在 manifest 中，但在接入前应先写清行为定义。

## 严格校验规则

包加载器 `load_asset_manifest` 和 catalog 入口 `load_asset_source` 会检查：

1. JSON 可解析、对象键不重复、根和资产没有未知字段。
2. `schemaVersion`、字段类型、命名、资产 ID 唯一性。
3. `source` 不是绝对路径、不含 `..` 或反斜杠，解析后没有通过软链接逃出资产根目录，并且文件真实存在。
4. `viewBox` 合法，所有锚点均落在其范围内。非零或负的 `minX/minY` 同样受支持。
5. SVG 是有效 XML，有 `viewBox`，且其数值与 manifest 完全一致。
6. SVG 没有 `DOCTYPE`/`ENTITY`，不引用远程、相对文件、`file:` 或 `data:` 资源；`href="#local-id"` 和 `url(#local-id)` 形式的内部引用允许使用。
7. SVG 元素 ID 不重复，`layers` 声明的每个 ID 确实存在。非 SVG 资产不能声明 `layers`。

加载失败抛出 `AssetManifestError`，消息会指出资产索引、字段或具体文件。构建与 CI 应把该错误视为设计资产不可交付，而不是跳过坏资产继续渲染。

## Python 使用

```python
from sandiao_studio.assets import load_asset_source

manifest = load_asset_source("design/manifests/design-assets.json")
pose = manifest.get("brand.character.xiaoming.pose.point")

print(pose.path)                 # 已校验、解析后的绝对 Path
print(pose.view_box)             # (0.0, 0.0, 512.0, 768.0)
print(pose.anchors["rightHand"]) # (392.0, 410.0)
```

设计资产尚未交付时，可用独立 fixture 测试契约；不要为了让测试通过而提交占位资产到 `design/`。
