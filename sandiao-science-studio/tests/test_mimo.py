from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

from sandiao_studio.mimo import MimoClient, MimoConfig


class FakeResponse:
    def __init__(self, payload: dict[str, Any]):
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self.payload


def client() -> MimoClient:
    return MimoClient(MimoConfig(api_key="test-key", base_url="https://mimo.invalid/v1", retries=1))


def test_tts_writes_decoded_audio(monkeypatch, tmp_path: Path) -> None:
    raw = b"RIFF-test-wav"
    seen: dict[str, Any] = {}

    def post(url: str, **kwargs: Any) -> FakeResponse:
        seen.update({"url": url, **kwargs})
        return FakeResponse({"choices": [{"message": {"audio": {"data": base64.b64encode(raw).decode()}}}]})

    monkeypatch.setattr("sandiao_studio.mimo.requests.post", post)
    output = client().synthesize("测试", tmp_path / "voice.wav")

    assert output.read_bytes() == raw
    assert seen["url"] == "https://mimo.invalid/v1/chat/completions"
    assert seen["json"]["model"] == "mimo-v2.5-tts"
    assert seen["json"]["audio"] == {"format": "wav", "voice": "mimo_default"}


def test_tts_voicedesign_uses_style_without_preset_voice(monkeypatch, tmp_path: Path) -> None:
    seen: dict[str, Any] = {}

    def post(_url: str, **kwargs: Any) -> FakeResponse:
        seen.update(kwargs)
        data = base64.b64encode(b"voice").decode()
        return FakeResponse({"choices": [{"message": {"audio": {"data": data}}}]})

    monkeypatch.setattr("sandiao_studio.mimo.requests.post", post)
    client().synthesize(
        "测试",
        tmp_path / "voice.wav",
        model="mimo-v2.5-tts-voicedesign",
        style="自然的青年男声",
        optimize_text_preview=True,
    )

    assert seen["json"]["model"] == "mimo-v2.5-tts-voicedesign"
    assert seen["json"]["messages"][0] == {"role": "user", "content": "自然的青年男声"}
    assert seen["json"]["audio"] == {"format": "wav", "optimize_text_preview": True}


def test_asr_sends_audio_data_url(monkeypatch, tmp_path: Path) -> None:
    audio = tmp_path / "probe.wav"
    audio.write_bytes(b"wav")
    seen: dict[str, Any] = {}

    def post(_url: str, **kwargs: Any) -> FakeResponse:
        seen.update(kwargs)
        return FakeResponse({"choices": [{"message": {"content": "测试转写"}}]})

    monkeypatch.setattr("sandiao_studio.mimo.requests.post", post)
    assert client().transcribe(audio) == "测试转写"
    media = seen["json"]["messages"][0]["content"][0]
    assert media["type"] == "input_audio"
    assert media["input_audio"]["data"].startswith("data:audio/x-wav;base64,")


def test_video_understanding_accepts_https_url(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    def post(_url: str, **kwargs: Any) -> FakeResponse:
        seen.update(kwargs)
        return FakeResponse({"choices": [{"message": {"content": "视频描述"}}]})

    monkeypatch.setattr("sandiao_studio.mimo.requests.post", post)
    assert client().understand_video("https://example.com/video.mp4", fps=0.5) == "视频描述"
    media = seen["json"]["messages"][0]["content"][0]
    assert media == {
        "type": "video_url",
        "video_url": {"url": "https://example.com/video.mp4"},
        "fps": 0.5,
        "media_resolution": "default",
    }
