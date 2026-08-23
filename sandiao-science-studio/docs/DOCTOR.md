# 生产环境诊断模块

`sandiao_studio.doctor` 在开始生成音频或视频前检查本机是否具备完整运行条件。当前模块不接入 CLI，可由调用方直接使用：

```python
from sandiao_studio.doctor import run_doctor

report = run_doctor("stories/ac-16c.json")
print(report.render_text())
raise SystemExit(report.exit_code)
```

## 检查项目

- Python 3.11 或更高版本
- `ffmpeg` 与 `ffprobe` 是否在 `PATH`，以及版本命令能否运行
- macOS、Windows、Linux 上的已知中文字体；可用 `SANDIAO_FONT_REGULAR` 和 `SANDIAO_FONT_BOLD` 显式配置
- 当前 TTS 选择、MiMo 凭证是否已配置、`espeak-ng`/`espeak` 是否可用
- Story JSON 能否通过现有 `load_story` 契约加载
- 可选的资产 manifest；只有传入 `asset_manifest_path` 时才延迟导入 `sandiao_studio.assets`

MiMo 检查只返回 `mimoKeyConfigured: true/false`，不会把 API key 放入文本报告或结构化结果，也不会发起网络请求。

## 结果和严重级别

`run_doctor()` 返回不可变的 `DoctorReport`。`to_dict()` 适合交给 UI、CI 或日志系统，`render_text()` 适合终端显示。

- `ok`：检查通过。
- `warning`：降级能力或可选能力不可用，例如没有 TTS provider。不会让 `exit_code` 失败。
- `critical`：渲染的必要条件不成立，或 Story/指定的 manifest 无效。此时 `exit_code` 为 `1`。

默认检查 `stories/ac-16c.json`。若资产模块尚未安装或仍在开发中，指定 manifest 会得到 warning；manifest 文件缺失或资产模块报告校验失败则为 critical。

结构化结果示例：

```json
{
  "ok": true,
  "exitCode": 0,
  "diagnostics": [
    {
      "code": "python",
      "severity": "ok",
      "message": "Python 3.12.0 is supported",
      "details": {"version": "3.12.0", "minimum": "3.11"}
    }
  ]
}
```
