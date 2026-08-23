from __future__ import annotations

import importlib
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, Mapping

from .settings import load_dotenv, project_root
from .story import load_story


Severity = Literal["ok", "warning", "critical"]


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DoctorReport:
    diagnostics: tuple[Diagnostic, ...]

    @property
    def has_critical(self) -> bool:
        return any(item.severity == "critical" for item in self.diagnostics)

    @property
    def exit_code(self) -> int:
        return 1 if self.has_critical else 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": not self.has_critical,
            "exitCode": self.exit_code,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }

    def render_text(self) -> str:
        labels = {"ok": "OK", "warning": "WARN", "critical": "CRITICAL"}
        lines = ["Sandiao Science Studio doctor"]
        for item in self.diagnostics:
            lines.append(f"[{labels[item.severity]}] {item.code}: {item.message}")
        summary = "ready" if not self.has_critical else "blocked by critical diagnostics"
        warning_count = sum(item.severity == "warning" for item in self.diagnostics)
        lines.append(f"Result: {summary}; {warning_count} warning(s)")
        return "\n".join(lines)


def _python_diagnostic() -> Diagnostic:
    current = sys.version_info[:3]
    supported = current >= (3, 11)
    return Diagnostic(
        code="python",
        severity="ok" if supported else "critical",
        message=(
            f"Python {platform.python_version()} is supported"
            if supported
            else f"Python {platform.python_version()} is too old; Python 3.11+ is required"
        ),
        details={"version": platform.python_version(), "minimum": "3.11"},
    )


def _executable_diagnostic(name: str) -> Diagnostic:
    executable = shutil.which(name)
    if not executable:
        return Diagnostic(
            code=name,
            severity="critical",
            message=f"{name} was not found on PATH",
            details={"path": None},
        )
    try:
        completed = subprocess.run(
            [executable, "-version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = completed.stdout or completed.stderr
        version = output.splitlines()[0].strip() if output else "version unavailable"
        if completed.returncode != 0:
            raise RuntimeError(f"version command exited {completed.returncode}")
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        return Diagnostic(
            code=name,
            severity="critical",
            message=f"{name} exists but could not be executed: {exc}",
            details={"path": str(Path(executable))},
        )
    return Diagnostic(
        code=name,
        severity="ok",
        message=version,
        details={"path": str(Path(executable)), "version": version},
    )


def _font_candidates(environ: Mapping[str, str]) -> tuple[list[Path], list[Path]]:
    regular = [
        Path(environ["SANDIAO_FONT_REGULAR"]).expanduser()
        if environ.get("SANDIAO_FONT_REGULAR")
        else None,
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
    ]
    bold = [
        Path(environ["SANDIAO_FONT_BOLD"]).expanduser()
        if environ.get("SANDIAO_FONT_BOLD")
        else None,
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Bold.otf"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    ]

    windows_dir = Path(environ.get("WINDIR", "C:/Windows")) / "Fonts"
    regular.extend([windows_dir / "msyh.ttc", windows_dir / "simhei.ttf"])
    bold.extend([windows_dir / "msyhbd.ttc", windows_dir / "simhei.ttf"])

    # User-installed font locations vary by OS. Only inspect direct children so
    # doctor remains fast even when a home directory contains many files.
    user_dirs = [Path.home() / "Library/Fonts", Path.home() / ".local/share/fonts"]
    cjk_markers = ("noto", "sourcehan", "source han", "pingfang", "heiti", "yahei", "wqy")
    for directory in user_dirs:
        if not directory.is_dir():
            continue
        try:
            candidates = tuple(directory.iterdir())
        except OSError:
            continue
        for candidate in candidates:
            if candidate.is_file() and any(marker in candidate.name.lower() for marker in cjk_markers):
                regular.append(candidate)
                bold.append(candidate)
    return [item for item in regular if item is not None], [item for item in bold if item is not None]


def discover_chinese_fonts(environ: Mapping[str, str] | None = None) -> tuple[Path | None, Path | None]:
    env = os.environ if environ is None else environ
    regular_candidates, bold_candidates = _font_candidates(env)
    regular = next((path.resolve() for path in regular_candidates if path.is_file()), None)
    bold = next((path.resolve() for path in bold_candidates if path.is_file()), regular)
    return regular, bold


def _font_diagnostic(environ: Mapping[str, str]) -> Diagnostic:
    regular, bold = discover_chinese_fonts(environ)
    if regular is None:
        return Diagnostic(
            code="fonts",
            severity="critical",
            message="no known Chinese font was found; configure SANDIAO_FONT_REGULAR and SANDIAO_FONT_BOLD",
            details={"regular": None, "bold": None},
        )
    return Diagnostic(
        code="fonts",
        severity="ok",
        message=f"Chinese font found: {regular.name}",
        details={"regular": str(regular), "bold": str(bold) if bold else None},
    )


def _tts_diagnostic(environ: Mapping[str, str]) -> Diagnostic:
    selected = environ.get("SANDIAO_TTS_PROVIDER", "auto").strip().lower() or "auto"
    mimo_configured = bool(environ.get("MIMO_API_KEY", "").strip())
    espeak_path = shutil.which("espeak-ng") or shutil.which("espeak")
    available = mimo_configured or espeak_path is not None

    if selected == "mimo":
        usable = mimo_configured
        reason = "MiMo API key is configured" if usable else "MiMo is selected but MIMO_API_KEY is not configured"
    elif selected == "espeak":
        usable = espeak_path is not None
        reason = "espeak is available" if usable else "espeak is selected but was not found on PATH"
    elif selected in {"none", "silent"}:
        usable = True
        reason = "silent speech mode is selected"
    elif selected == "auto":
        usable = available
        if mimo_configured:
            reason = "auto will use MiMo"
        elif espeak_path:
            reason = "auto will use espeak"
        else:
            reason = "auto found no usable speech provider"
    else:
        usable = False
        reason = f"unknown TTS provider: {selected}"

    # Deliberately report only the presence of the MiMo credential. Never put
    # the credential itself in a diagnostic, even in structured details.
    return Diagnostic(
        code="tts",
        severity="ok" if usable else "warning",
        message=reason,
        details={
            "selected": selected,
            "mimoKeyConfigured": mimo_configured,
            "espeakPath": str(Path(espeak_path)) if espeak_path else None,
        },
    )


def _story_diagnostic(path: Path) -> Diagnostic:
    try:
        story = load_story(path)
    except Exception as exc:
        return Diagnostic(
            code="story",
            severity="critical",
            message=f"Story could not be loaded: {exc}",
            details={"path": str(path.resolve())},
        )
    return Diagnostic(
        code="story",
        severity="ok",
        message=f"loaded {story.slug} ({len(story.shots)} shots, {story.duration:.2f}s)",
        details={
            "path": str(story.source),
            "slug": story.slug,
            "shots": len(story.shots),
            "durationSeconds": story.duration,
        },
    )


def _asset_manifest_diagnostic(path: Path) -> Diagnostic:
    if not path.is_file():
        return Diagnostic(
            code="assets",
            severity="critical",
            message=f"asset manifest or catalog was not found: {path}",
            details={"path": str(path.resolve())},
        )
    try:
        assets = importlib.import_module("sandiao_studio.assets")
    except (ImportError, OSError) as exc:
        return Diagnostic(
            code="assets",
            severity="warning",
            message=f"asset source exists, but the optional assets module is unavailable: {exc}",
            details={"path": str(path.resolve())},
        )

    loader = (
        getattr(assets, "load_asset_source", None)
        or getattr(assets, "load_asset_manifest", None)
        or getattr(assets, "load_manifest", None)
    )
    validator = getattr(assets, "validate_asset_manifest", None) or getattr(assets, "validate_manifest", None)
    try:
        if loader is not None:
            loader(path)
        elif validator is not None:
            result = validator(path)
            if result is False:
                raise ValueError("validator returned false")
            if isinstance(result, (list, tuple)) and result:
                raise ValueError("; ".join(str(item) for item in result))
        else:
            return Diagnostic(
                code="assets",
                severity="warning",
                message="assets module has no supported manifest or catalog validation function",
                details={"path": str(path.resolve())},
            )
    except Exception as exc:
        return Diagnostic(
            code="assets",
            severity="critical",
            message=f"asset manifest or catalog is invalid: {exc}",
            details={"path": str(path.resolve())},
        )
    return Diagnostic(
        code="assets",
        severity="ok",
        message="asset manifest or catalog is valid",
        details={"path": str(path.resolve())},
    )


def run_doctor(
    story_path: str | Path | None = None,
    asset_manifest_path: str | Path | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> DoctorReport:
    if environ is None:
        load_dotenv()
        env: Mapping[str, str] = os.environ
    else:
        env = environ

    story = Path(story_path) if story_path is not None else project_root() / "stories" / "ac-16c.json"
    diagnostics = [
        _python_diagnostic(),
        _executable_diagnostic("ffmpeg"),
        _executable_diagnostic("ffprobe"),
        _font_diagnostic(env),
        _tts_diagnostic(env),
        _story_diagnostic(story),
    ]
    if asset_manifest_path is not None:
        diagnostics.append(_asset_manifest_diagnostic(Path(asset_manifest_path)))
    return DoctorReport(tuple(diagnostics))
