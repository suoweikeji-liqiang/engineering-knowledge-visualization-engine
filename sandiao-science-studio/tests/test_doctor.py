from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import sandiao_studio.doctor as doctor


def _write_story(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "meta": {"title": "测试", "slug": "test", "resolution": [640, 360], "fps": 12},
                "characters": [
                    {"id": "a", "name": "甲", "palette": {"body": "#fff"}, "voice": {}}
                ],
                "shots": [
                    {
                        "id": "s1",
                        "duration": 1,
                        "speaker": "a",
                        "dialogue": "你好",
                        "states": [],
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_run_doctor_returns_structured_report_without_leaking_key(tmp_path, monkeypatch) -> None:
    story = tmp_path / "story.json"
    font = tmp_path / "chinese.ttf"
    _write_story(story)
    font.write_bytes(b"font")

    monkeypatch.setattr(doctor.shutil, "which", lambda name: f"/tools/{name}")
    monkeypatch.setattr(
        doctor.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="ffmpeg version 7.0\n", stderr=""),
    )
    monkeypatch.setattr(
        doctor,
        "load_story",
        lambda path: SimpleNamespace(
            source=Path(path).resolve(), slug="test", shots=(object(),), duration=1.0
        ),
    )
    secret = "this-must-never-appear"
    report = doctor.run_doctor(
        story,
        environ={
            "SANDIAO_FONT_REGULAR": str(font),
            "SANDIAO_FONT_BOLD": str(font),
            "SANDIAO_TTS_PROVIDER": "mimo",
            "MIMO_API_KEY": secret,
        },
    )

    payload = report.to_dict()
    assert payload["ok"] is True
    assert payload["exitCode"] == 0
    assert secret not in json.dumps(payload)
    assert secret not in report.render_text()
    assert {item["code"] for item in payload["diagnostics"]} == {
        "python", "ffmpeg", "ffprobe", "fonts", "tts", "story"
    }


def test_missing_runtime_dependencies_are_critical_and_tts_is_warning(tmp_path, monkeypatch) -> None:
    story = tmp_path / "story.json"
    _write_story(story)
    monkeypatch.setattr(doctor.shutil, "which", lambda _name: None)
    monkeypatch.setattr(doctor, "discover_chinese_fonts", lambda _env: (None, None))

    report = doctor.run_doctor(story, environ={})
    by_code = {item.code: item for item in report.diagnostics}

    assert report.has_critical
    assert report.exit_code == 1
    assert by_code["ffmpeg"].severity == "critical"
    assert by_code["ffprobe"].severity == "critical"
    assert by_code["fonts"].severity == "critical"
    assert by_code["tts"].severity == "warning"
    assert "CRITICAL" in report.render_text()


def test_invalid_story_is_critical(tmp_path, monkeypatch) -> None:
    font = tmp_path / "chinese.ttf"
    font.write_bytes(b"font")
    monkeypatch.setattr(doctor.shutil, "which", lambda name: f"/tools/{name}")
    monkeypatch.setattr(
        doctor.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="version 1\n", stderr=""),
    )

    report = doctor.run_doctor(
        tmp_path / "missing.json",
        environ={"SANDIAO_FONT_REGULAR": str(font), "SANDIAO_TTS_PROVIDER": "silent"},
    )
    story_result = next(item for item in report.diagnostics if item.code == "story")
    assert story_result.severity == "critical"
    assert "could not be loaded" in story_result.message


def test_asset_manifest_is_imported_only_when_requested(tmp_path, monkeypatch) -> None:
    manifest = tmp_path / "assets.json"
    manifest.write_text("{}", encoding="utf-8")
    calls: list[Path] = []
    fake_assets = SimpleNamespace(load_asset_manifest=lambda path: calls.append(path))
    monkeypatch.setattr(doctor.importlib, "import_module", lambda _name: fake_assets)

    result = doctor._asset_manifest_diagnostic(manifest)

    assert result.severity == "ok"
    assert calls == [manifest]


def test_missing_asset_manifest_is_critical(tmp_path) -> None:
    result = doctor._asset_manifest_diagnostic(tmp_path / "missing.json")
    assert result.severity == "critical"
