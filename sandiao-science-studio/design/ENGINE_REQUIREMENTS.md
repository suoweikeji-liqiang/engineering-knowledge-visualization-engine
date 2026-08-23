# 《小行星原理剧场》渲染引擎对接与工程实现需求规范
## (Rendering Engine Technical Requirements & Integration Specification)

---

### 一、 概述与设计系统约定 (Executive Summary)

本规范为 Antigravity 设计系统与 Codex 渲染引擎实现团队之间的**技术契约 (Contract Specification)**。
旨在指导渲染引擎如何基于 `design-assets.json` 资产清单，将模块化 SVG 资产合成为具有高度表现力、零碰撞缺陷、支持音画同步与双画幅自适应的工程科普短动画。

- **核心资产根目录**：`sandiao-science-studio/design/`
- **资产索引文件**：`design/manifests/design-assets.json`
- **基础画布基准**：
  - 横屏基准：`1920 × 1080` (16:9, 标准 1080p, 30fps/60fps)
  - 竖屏基准：`1080 × 1920` (9:16, 移动端全屏)
- **字体回退规范**：禁止打包字库，使用跨平台系统字体回退：
  ```css
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  ```

---

### 二、 多图层合成顺序与 Z-Index 栈 (Multi-Layer Composition Order)

渲染管线必须严格遵循以下 6 层合成顺序，禁止图层穿插导致的内容遮挡：

| 层级 (Z-Index) | 图层名称 (Layer Name) | 资产来源 (Asset Source) | 渲染职责 (Responsibility) |
| :--- | :--- | :--- | :--- |
| **Z = 0** | `Background` | `assets/{package}/backgrounds/{type}/background_16x9.svg` | 场景远景、墙体、天空、环境基础底色 |
| **Z = 10** | `Midground` | `assets/{package}/backgrounds/{type}/midground_16x9.svg` | 场景中景、家具、窗户、大型固定管道 |
| **Z = 20** | `Characters &amp; Props` | `assets/brand/characters/{id}/poses/*.svg` + `assets/domains/{domain}/props/*.svg` | 角色（老王、小明）及领域道具 |
| **Z = 30** | `Diagram Stage` | `assets/shared/diagrams/*.svg` / `storyboards/{ep}/*.svg` | 核心工程图解展板、折线图、工况流、公式卡 |
| **Z = 40** | `Subtitles &amp; Callouts` | 引擎动态生成 (依据对白轨道) | 说话人徽标、字幕条、警示气泡、动效高亮光圈 |
| **Z = 50** | `Foreground &amp; Watermark` | `assets/{package}/backgrounds/{type}/foreground_16x9.svg` | 品牌水印 (`EP.01` 顶栏)、前景遮罩、镜头光晕 |

---

### 三、 角色 SVG 结构与动态组装管线 (Dynamic Character Assembly)

每个角色的完整 SVG 均由具有固定命名语义的 `<g id="...">` 层级组成：

```xml
<svg viewBox="0 0 512 768">
  <g id="root">
    <g id="legs"> ... </g>
    <g id="torso"> ... </g>
    <g id="arm_left">
      <g id="hand_left"> ... </g>
      <circle id="anchor_hand_left" cx="136" cy="480" r="0" />
    </g>
    <g id="arm_right">
      <g id="hand_right"> ... </g>
      <circle id="anchor_hand_right" cx="376" cy="480" r="0" />
    </g>
    <g id="head">
      <g id="neck"> ... </g>
      <g id="face"> ... </g>
      <g id="hair"> ... </g>
      <g id="eye_left"> ... </g>
      <g id="eye_right"> ... </g>
      <g id="brow_left"> ... </g>
      <g id="brow_right"> ... </g>
      <!-- 动态嘴型挂载点 (Lip-sync Anchor) -->
      <g id="mouth">
        <!-- 默认使用 rest.svg，播放对白时动态替换为 a_shape / o_shape / e_shape 等 -->
      </g>
    </g>
  </g>
</svg>
```

#### 1. 口型对齐映射算法 (TTS Phoneme to Mouth Mapping)
引擎需解析 TTS 音频输出的音素或能量强度，以 80ms~120ms 为间隔动态切换 `#mouth` 内的路径：

| 嘴型资产 (Mouth Asset) | 对应拼音音素 (Phoneme) | 触发条件 (Trigger Condition) |
| :--- | :--- | :--- |
| `rest.svg` | 无 (静音 / 停顿) | 能量 < 0.05 或音频静音段 |
| `slightly_open.svg` | h, l, n, m, d, t | 轻辅音与短过渡音 |
| `a_shape.svg` | a, ia, ua, an, ang | 开口大元音 (啊、大、开、发) |
| `o_shape.svg` | o, u, ou, ong, uo | 圆唇元音 (喔、多、通、度) |
| `e_shape.svg` | e, i, ie, ei, en | 扁平闭合元音 (一、机、定、气) |
| `bite_lip.svg` | f, v, z, c, s, r | 齿唇摩擦音 (服、反、四、风) |

#### 2. 微动画状态机 (Micro-Animation State Machine)
- **眨眼 (Blink)**：每 3.5s ~ 5.0s 随机触发一次眨眼，将 `#eye_left` 和 `#eye_right` 的 `scaleY` 设为 `0.1`，维持 120ms 后平滑还原。
- **呼吸微浮动 (Breathing Idle)**：待机状态下，角色整体 `translateY` 产生 $\pm 2\text{px}$、周期 $2.4\text{s}$ 的正弦缓动 (`sineInOut`)。

---

### 四、 道具动态挂载系统 (Prop Anchor Attachment System)

当剧本指定角色操作某个工程道具时（例如小明手持激光笔指向压缩机、老王头顶冒出疑问问号），引擎通过绝对坐标偏移实现绑定：

1. **锚点查询**：从 `design-assets.json` 读取角色的锚点位置：
   - 老王手部锚点：`hand_left: (136, 480)`, `hand_right: (376, 480)`
   - 小明手部锚点：`hand_left: (140, 440)`, `hand_right: (372, 440)`
   - 头顶锚点：`head_top: (256, 130)`
2. **挂载变换公式**：
   $$\text{PropMatrix} = \text{CharacterTransform} \times \text{AnchorOffset} \times \text{PropScale}$$
3. **支持挂载的道具清单**：
   - 激光笔 (`laser_pointer`) 挂载于 `hand_right`
   - 温度计 (`hvac-thermometer.svg`) 挂载于 `hand_left`
   - 疑问水滴/感叹号 (`symbol-warning.svg`) 挂载于 `head_top`

---

### 五、 双画幅响应式排版引擎规则 (Responsive Layout System)

引擎必须原生支持 16:9 横屏与 9:16 竖屏，禁止粗暴居中裁剪导致两侧被切。

#### 1. 横屏 16:9 (1920 × 1080) 三栏舞台
- **左侧角色区 (Left Character Zone)**：$x = [40, 360]$，宽度 320px
- **中央推导展板区 (Central Diagram Stage)**：$x = [380, 1540]$，宽度 1160px，高度 690px，居中放置
- **右侧角色区 (Right Character Zone)**：$x = [1560, 1880]$，宽度 320px
- **底部字幕区 (Subtitle Zone)**：$x = [180, 1740]$，$y = [930, 1026]$，保证与中央展板保留至少 40px 安全间距。

#### 2. 竖屏 9:16 (1080 × 1920) 三层垂直堆叠
- **顶栏状态与标题 (Top Brand Bar)**：$y = [80, 160]$
- **角色对话交互台 (Character Stage)**：$y = [200, 580]$，老王（左 $x=100$）与小明（右 $x=620$）按 0.75 缩放双人站位
- **中央核心图解卡片 (Central Diagram Card)**：$y = [620, 1500]$，宽度 920px（左右边距 80px，右侧预留 120px 避让平台点赞评论按钮）
- **底部字幕与安全区 (Bottom Subtitle Safe Area)**：$y = [1560, 1720]$，距离屏幕底端预留 200px 避让手机 Home 条与进度条。

---

### 六、 文本与图解防碰撞算法 (Collision Avoidance Engine)

为彻底解决历史版本中文字重叠（Cover Title 盖住白板）与图解截断（Shot 3 第三框切出屏幕）的问题，引擎必须内置如下排版校验器：

1. **包围盒碰撞检测 (Bounding Box Intersection Check)**：
   ```python
   def check_collision(box_a, box_b, min_padding=24):
       return not (
           box_a.right + min_padding <= box_b.left or
           box_a.left >= box_b.right + min_padding or
           box_a.bottom + min_padding <= box_b.top or
           box_a.top >= box_b.bottom + min_padding
       )
   ```
2. **多节点容器自适应分发 (Flow Container Auto-Fit)**：
   当流程图包含 $N$ 个节点时，单个节点的宽度 $W$ 与水平间距 $S$ 计算公式：
   $$W = \frac{W_{\text{stage}} - (N - 1) \cdot S - 2 \cdot P}{N}$$
   以 16:9 中央舞台 ($W_{\text{stage}} = 1160\text{px}$) 3 个节点为例：
   $$W = \frac{1160 - 2 \times 60 - 2 \times 60}{3} \approx 306\text{px}$$
   引擎生成的流程节点宽度必须严格 $\le 280\text{px}$，严禁固定使用超宽元素导致屏幕边缘溢出。

---

### 七、 动效物理插值与运镜曲线 (Motion Interpolation & Camera Curves)

所有角色位移、卡片弹入均必须采用 **3 段式物理弹簧曲线**：

- **预备动作 (Anticipation)**：前 15%~20% 时间，反向微移 $5\%\sim 10\%$
- **主体动作 (Action)**：中间 40%~50% 时间，高速推进 (`cubic-bezier(0.2, 0.8, 0.2, 1)`)
- **回弹与沉降 (Settle / Overshoot)**：后 30%~40% 时间，过冲 $3\%\sim 5\%$ 后回弹稳定。

---

### 八、 验收测试用例 (Engine Acceptance Verification Checklist)

- [x] **测试项 1（剪影辨识）**：纯黑剪影下，老王与小明轮廓 100% 可区分。
- [x] **测试项 2（移动端清晰度）**：12 种表情在 160px 头像尺寸下均清晰可读。
- [x] **测试项 3（图文无遮挡）**：8 个镜头分镜在 1080p 下无任何文字覆盖、折行重叠或图例遮盖。
- [x] **测试项 4（边缘无截断）**：Shot 03 的 3 个流程框在 16:9 与 9:16 下完整显示于可视安全区内。
- [x] **测试项 5（双画幅适配）**：横屏 16:9 与竖屏 9:16 均拥有专属结构化布局，无拉伸失真。
- [x] **测试项 6（清单与文件完整性）**：`design-assets.json` 中定义的所有文件均已落盘并通过语法解析。
