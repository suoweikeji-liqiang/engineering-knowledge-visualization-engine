# 反重力任务：沙雕科普动画视觉系统全面重设计

## 任务目标

为“小行星AI观测站”旗下的工程科普动画栏目建立一套可长期复用、可程序化驱动的原创视觉系统。此次不是给现有画面换皮，而是重新设计栏目识别、人物、场景、背景、动作、表情、道具、技术图解、字幕和动效语言，并交付可直接接入渲染引擎的分层资产。

目标观感：**有角色魅力的中文科技科普短片，而不是低幼动画、PPT 或表情包拼贴**。画面可以幽默，但技术信息必须清楚、可信、易读。

工作目录：

```text
/Users/asteroida/work/engineering-knowledge-visualization-engine/sandiao-science-studio
```

当前参考成片：

```text
output/ac-16c-sample.mp4
output/ac-16c-poster.png
stories/ac-16c.json
```

母品牌来源仓库：

```text
/Users/asteroida/work/ai_daily_brief_factory_v3
```

开始设计前必须完整阅读：

```text
/Users/asteroida/work/ai_daily_brief_factory_v3/profiles/creator_profile.yaml
/Users/asteroida/work/ai_daily_brief_factory_v3/dailybrief/brand.py
/Users/asteroida/work/engineering-knowledge-visualization-engine/sandiao-science-studio/docs/BRAND_INHERITANCE_BRIEF.md
```

## 品牌架构

默认品牌层级为：

```text
母品牌：小行星AI观测站
动画栏目：小行星原理剧场（设计阶段工作名）
内容格式：对话式工程科普
内部风格描述：沙雕/幽默科普
```

“沙雕科普实验室”不再作为默认公开品牌名。反重力可以在三个方向提案中提出更好的栏目名，但必须保留“小行星”母品牌关系，并说明新名称相对“小行星原理剧场”的优势。

需要继承的母品牌 DNA：

- 小行星、轨道、观测站、望远镜、雷达/遥测等符号语义。
- 深海军蓝、轨道蓝、遥测青、信号橙红和暖纸色组成的品牌色谱。
- “冷静、明确、少废话”和证据优先的表达气质。
- 观察、发现、验证、画清复杂关系的叙事动作。
- 频道名与轨道标记形成的稳定片头、角标、片尾识别。

不能直接照搬的内容：

- AI 日报和 Poster Deck 的高密度卡片排版。
- 每屏塞满证据条、来源 chip 和技术术语的新闻结构。
- 全片深色控制室背景或无意义的太空装饰。
- 现有临时 mascot prompt、网页 CSS logo 或某一期海报作为最终角色资产。
- 把“AI”图标硬塞进 HVAC、机械、控制等非 AI 原理镜头。

动画栏目要做的是母品牌的“会表演、会讲原理”的分支：品牌识别主要出现在片头、角标、转场、观察仪器和结论卡；人物对话与工程图解仍是画面主体。

## 协作边界

你负责视觉设计与设计资产，不负责修改 Python 渲染代码、Story JSON 契约、TTS、时间线或 CLI。

Codex 负责：

- Story schema 与资产 manifest 契约。
- CharacterRenderer、SceneRenderer、Action/Motion 系统。
- 自适应布局、镜头、字幕、音频和评测。
- 把本任务交付的资产接入确定性渲染管线。

如当前代码限制了设计表现，不要绕过限制去改代码；把所需能力写入 `design/ENGINE_REQUIREMENTS.md`，说明场景、预期表现、所需参数与优先级。

## 不可破坏的原则

1. 所有核心角色与视觉资产必须原创，不使用受版权保护的动漫、表情包或品牌形象。
2. 不把字体文件提交到仓库；字体只提供推荐清单和替代策略。
3. 资产中不固化对白、标题或技术说明文字，文字由程序渲染。
4. 资产必须可拆分、可复用，不交付只有一张完整合成图的“死素材”。
5. 横屏和竖屏使用同一视觉语言，不分别设计成两套品牌。
6. 设计服务于科普表达：人物不能长期遮挡图解，幽默效果不能破坏事实理解。
7. 最终资产必须有明确命名、锚点、尺寸、层级和使用说明。

## 当前问题基线

先审看完整样片，并至少记录以下问题：

- 人物像程序占位符，轮廓、比例、服装和个性不足。
- 背景固定且信息噪声高，不能支持不同知识场景。
- 动作主要是局部抖动，缺少预备、发力、缓冲和跟随。
- 表情辨识度不足，嘴型与讲话状态弱。
- 技术图解缺少统一网格、图标、连线和信息层级。
- 已存在文字重叠、元素越界、右侧裁切和视觉停留不足。
- 字幕、标题、角色、图解之间没有稳定的构图规则。
- 横屏构图几乎无法直接迁移到 9:16。

在 `design/AUDIT.md` 中补充你实际看到的问题，不要只复制上述列表。

## 设计方向

先提出 3 个明显不同的原创方向，每个方向交付一张 1920×1080 style frame，并说明：

- 关键词与目标受众。
- 人物造型逻辑。
- 背景与技术图解语言。
- 色彩、线条、材质和光影策略。
- 为什么适合高频中文科技科普。
- 量产难度和程序化实现风险。

三个方向至少覆盖：

1. 扁平矢量喜剧感。
2. 轻质感二维动画感。
3. 信息图与角色舞台融合感。

推荐其中一个作为主方向，并给出选择理由。除非用户明确叫停，后续完整资产按推荐方向推进。

## 最终交付一：品牌与视觉规范

创建 `design/system/VISUAL_SYSTEM.md`，至少定义：

- 品牌气质与禁区。
- 主色、辅助色、语义色、背景色和对比度规则。
- 描边粗细、圆角、阴影、纹理和高光规则。
- 8px 或其他明确基础网格。
- 16:9 与 9:16 安全区。
- 标题、字幕、标签、角色名牌、提示卡和结论卡层级。
- 中文字体推荐与 macOS/Windows/Linux 回退顺序，但不提交字体。
- 技术图解的节点、连线、箭头、警告、数据和状态颜色规范。
- 动画节奏原则：入场、停留、强调、退出、转场。
- “允许”和“禁止”示例。

文字在 360p 手机预览下仍应可读。不能靠极细字重、低对比度或大段小字营造“高级感”。

## 最终交付二：角色系统

重设计两位常驻角色，可以保留“老王/小明”的叙事关系，但造型不受现有代码限制。

每个角色交付：

- 正面、3/4、侧面和背面 turnaround。
- 头身比例、身高关系和轮廓说明。
- 默认服装、配色、可替换配件。
- 角色性格、说话节奏和动作习惯。
- 眼睛、眉毛、嘴、手的组件拆分。
- 至少 6 个嘴型：闭口、微张、A、O、E、咬唇/齿音。
- 至少 12 个表情：neutral、happy、confident、serious、puzzled、shocked、angry、tired、laugh、cry、embarrassed、determined。
- 至少 14 个动作/姿态：idle、talk、point、think、nod、shake、celebrate、walk、run、angry、laugh、cry、sweat、whisper。
- 每个动作至少提供关键姿态；walk、run、talk、laugh 至少提供 3 个关键帧。

角色资产优先交付 SVG；如必须使用 PNG，应为透明背景、至少 2× 目标分辨率。角色各部件使用稳定 layer id，并标注：

```text
root
head
face
eye_left / eye_right
brow_left / brow_right
mouth
torso
arm_left / arm_right
hand_left / hand_right
leg_left / leg_right
prop_anchor
```

每个角色提供锚点说明：feet、center、head、mouth、left_hand、right_hand、look_at。

## 最终交付三：场景与背景系统

至少设计 5 类可复用场景：

1. 日常空间：客厅/办公室，用于误区对话。
2. 教学空间：科普实验室，用于机制解释。
3. 工程空间：机房/设备间，用于设备和系统流程。
4. 抽象信息舞台：纯色或模块化空间，用于公式、图表、流程图。
5. 总结空间：结论、建议、CTA 或片尾。

每类场景交付：

- 16:9 横屏构图。
- 9:16 竖屏构图或明确重排说明。
- foreground、midground、background 分层。
- 左人物区、右人物区、图解区、标题区、字幕区安全范围。
- 可替换道具和空白信息位。
- 日/夜或冷/暖至少一种色彩变体。

背景不得把关键装饰画死在人物和图解的常用区域。

## 最终交付四：工程科普道具与图解组件

建立第一批 HVAC/通用工程资产包，但视觉系统必须可扩展到其他工程领域。

至少包括：

- 空调室内机、室外机、压缩机、风机、换热器、管路、阀门、传感器、温度计、电表。
- 水滴、气流、热流、冷流、电能、警告、正确/错误、时间、速度、压力等通用图标。
- 流程节点、连接线、箭头、分支、循环、状态灯和标签容器。
- 对比卡、误区卡、三步建议卡、时间线、折线图、柱状图、仪表盘、公式卡。
- 入口、强调、错误、成功、循环、流动和脉冲状态的视觉示意。

同类组件必须共享尺寸、描边和语义颜色，不能每个图解重新发明一套画法。

## 最终交付五：动作与镜头语言

创建 `design/system/MOTION_SYSTEM.md`，定义：

- 动作的 anticipation、action、settle 三阶段。
- talk、point、shock、think、nod、shake、celebrate 等动作的建议时长和振幅。
- 嘴型切换、眨眼、视线和呼吸的基础频率。
- 人物走入、滑入、弹入、遮挡转场、镜头推拉和平移规则。
- 图解逐步出现、路径流动、数字变化和重点强调规则。
- 哪些动效可循环，哪些必须一次性播放。
- 对白期间的动作密度上限，避免所有元素同时动。
- 低动态场景如何通过构图变化而不是无意义抖动保持节奏。

提供一个覆盖前 10 秒的 motion board，逐秒标注人物、镜头、图解、字幕和声音触发点。

## 最终交付六：样例重设计

用现有《空调开到 16℃真的更省电吗？》作为验收样例，交付：

- 新封面 1 张。
- 8 个镜头的最终 style frame。
- 前 10 秒 motion board 或 animatic。
- 16:9 和 9:16 各至少 3 个代表镜头。
- 一张角色、场景、图解汇总 contact sheet。

样例必须解决当前已知的文字重叠、元素裁切、人物遮挡和信息层级问题。

## 资产目录与命名

所有新增设计文件放在：

```text
design/
  AUDIT.md
  ENGINE_REQUIREMENTS.md
  directions/
  system/
  assets/
    brand/
      manifest.json
      characters/
        laowang/
        xiaoming/
      backgrounds/
    shared/
      manifest.json
      backgrounds/
      symbols/
      diagrams/
    domains/hvac/
      manifest.json
      backgrounds/
      props/
  storyboards/ac-16c/
  previews/
  manifests/design-assets.json
```

源文件、SVG、预览 PNG 分开存放。使用 kebab-case，不使用“最终版2”“新建文件”等名称。

每个资产包的 `manifest.json` 记录本包资产；`design-assets.json` 只负责组合包。例如品牌包：

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
      "variants": ["default"]
    }
  ]
}
```

顶层 catalog：

```json
{
  "schemaVersion": "1.0",
  "manifests": [
    {"namespace": "brand", "source": "assets/brand/manifest.json"},
    {"namespace": "shared", "source": "assets/shared/manifest.json"},
    {"namespace": "domain.hvac", "source": "assets/domains/hvac/manifest.json"}
  ]
}
```

坐标可按实际设计调整，但字段和语义要完整。

## 技术约束

- SVG 必须有 `viewBox`，不得依赖画板外元素。
- 透明背景资产不得残留白底。
- 尽量使用基础 path、group、mask；复杂滤镜必须提供无滤镜降级版本。
- 不在 SVG 中嵌入外链图片、字体或远程资源。
- 不把可变文字转曲后固化在通用组件中。
- PNG 预览使用 sRGB。
- 资产打开后不能缺图、缺字体或引用本机绝对路径。
- 单个通用 SVG 尽量小于 500KB；超出时说明原因。
- 同一动作、表情、背景的命名必须能被程序稳定枚举。

## 验收标准

完成时必须同时满足：

1. 两个角色仅看黑色剪影也能明显区分。
2. 12 个表情在 160px 角色头像尺寸下仍能辨认。
3. 前 10 秒内至少出现一次有效人物动作、一次图解构建和一次镜头变化。
4. 360p 预览中标题和字幕可读，没有文字重叠或越界。
5. 16:9 与 9:16 都不依赖简单裁切，关键元素全部位于安全区。
6. 人物、背景、道具和图解均有可复用分层资产，不是只有 style frame。
7. 资产 manifest 可解析，路径全部存在，id 不重复。
8. 不包含字体文件、版权不明素材、远程依赖和硬编码对白。
9. 所有交付都有 contact sheet，Codex 无需逐个打开源文件才能了解资产。
10. `git diff --check` 通过；不要提交、推送或部署。

## 最终汇报

完成后只汇报：

1. 选择了哪个设计方向，为什么。
2. 交付了多少角色、表情、动作、背景、道具和图解资产。
3. 16:9 与 9:16 如何适配。
4. 前 10 秒重设计解决了哪些当前问题。
5. `ENGINE_REQUIREMENTS.md` 中有哪些引擎需求。
6. 尚未解决的问题及原因。

完成后停在本地，等待用户与 Codex 联合验收。不要提交、推送或部署。
